"""SG Tech Pulse 2026 — respondent salary-position page.

Receives SurveySparrow onSubmissionComplete webhooks, stores base-salary
answers in SQLite, and serves a small Spanish web view that shows the live
salary distribution with the respondent's position marked, plus context
modules: same-level percentile, English-usage ladder, AI skills-confidence
distribution, and AI coding-mode shares.

Salary conventions match docs/GENERAL_FINDINGS_2026.md: base monthly salary
normalized to MXN (USD × FX 18.5), trimmed to $8k–$400k.
"""
import hmac
import json
import os
import re
import sqlite3
import statistics
import time
import unicodedata
from collections import defaultdict, deque
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("PULSE_DB", os.path.join(HERE, "pulse.db"))
FX = float(os.environ.get("PULSE_FX", "18.5"))
TRIM_LO = float(os.environ.get("PULSE_TRIM_LO", "8000"))
TRIM_HI = float(os.environ.get("PULSE_TRIM_HI", "400000"))
WEBHOOK_SECRET = os.environ.get("PULSE_WEBHOOK_SECRET", "")
SID_TTL_HOURS = float(os.environ.get("PULSE_SID_TTL_HOURS", "48"))
SURVEY_URL = os.environ.get("PULSE_SURVEY_URL", "https://salarios.sg.com.mx/")
HOME_URL = os.environ.get("PULSE_HOME_URL", "https://salarios.sg.com.mx/")

BIN_WIDTH = 10_000
BIN_MAX = 200_000  # salaries above this go to the "200k+" overflow bucket
MIN_CELL = 25      # minimum n before a subgroup comparison is shown

# Question-text prefixes (normalized) used to pick fields out of both the
# CSV dump headers and webhook payloads, so a question-id remap in
# SurveySparrow can't silently break ingestion.
QUESTION_PREFIXES = {
    "salary_mxn": "¿cual es tu salario base bruto mensual en pesos",
    "salary_usd": "¿cual es tu salario base bruto mensual en dolares",
    "level": "¿cual es tu nivel dentro de esta organizacion",
    "role": "¿cual es tu funcion o actividad principal",
    "years_tech": "¿cuantos de esos anos corresponden especificamente al sector tecnologico",
    "english_usage": "¿con que frecuencia utilizas el ingles en tu trabajo diario",
    "foreign_employer": "¿la empresa esta ubicada en el mismo pais donde tu resides",
    "ai_confidence": "¿que tan seguro/a estas de que tus habilidades actuales seguiran siendo relevantes",
    "ai_coding": "¿como utilizas la ia para crear codigo",
}
NUMERIC_FIELDS = {"salary_mxn", "salary_usd", "years_tech", "ai_confidence"}
UTM_FIELDS = ("utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term")
TEXT_FIELDS = {"level", "role", "english_usage", "foreign_employer", "ai_coding", *UTM_FIELDS}
ALL_FIELDS = NUMERIC_FIELDS | TEXT_FIELDS

# Canonical buckets for the page modules, matched by normalized prefix.
ENGLISH_ORDER = [
    ("nunca", "Nunca"),
    ("ocasionalmente", "Ocasionalmente (leer docs)"),
    ("con regularidad", "Con regularidad (juntas, emails)"),
    ("la mayoria del tiempo", "La mayoría del tiempo"),
    ("todo el tiempo", "Todo el tiempo"),
]
AI_CODING_ORDER = [
    ("programo manualmente y uso ia como soporte",
     "Programo a mano; IA como soporte"),
    ("programo la funcionalidad manualmente",
     "Programo a mano; IA para testing y docs"),
    ("aunque se programar",
     "Doy instrucciones a agentes y reviso"),
]


def norm_text(s):
    s = unicodedata.normalize("NFD", str(s))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s).strip().lower()


def match_field(question_text):
    q = norm_text(question_text)
    for field, prefix in QUESTION_PREFIXES.items():
        if q.startswith(prefix):
            return field
    return None


def parse_money(value):
    v = parse_number(value)
    return v if v is not None and v > 0 else None


def parse_number(value):
    if value is None:
        return None
    s = re.sub(r"[^\d.]", "", str(value))
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def is_placeholder(value):
    """An unreplaced SurveySparrow placeholder like "{question_100413…}" is
    not data — and it contains digits, so it must be rejected before any
    numeric parsing. SurveySparrow renders unanswered questions as the
    string "null", which is equally not data."""
    if not isinstance(value, str):
        return False
    s = value.strip()
    return s.lower() == "null" or re.fullmatch(r"\{[^}]*\}", s) is not None


def parse_field(field, value):
    if is_placeholder(value):
        return None
    if field == "salary_mxn" or field == "salary_usd":
        return parse_money(value)
    if field in NUMERIC_FIELDS:
        return parse_number(value)
    if value in (None, ""):
        return None
    s = str(value).strip()
    return s or None


def normalize_salary(salary_mxn, salary_usd):
    if salary_mxn is not None:
        return salary_mxn
    if salary_usd is not None:
        return salary_usd * FX
    return None


def bucket_key(value, order):
    if value is None:
        return None
    n = norm_text(value)
    for key, _label in order:
        if n.startswith(key):
            return key
    return None


def foreign_of(value):
    """Answer to '¿La empresa está ubicada en el mismo país donde resides?'
    → True means foreign employer (answered No). SurveySparrow renders this
    yes/no question as Yes/Sí/true vs No/false depending on export path."""
    if value is None:
        return None
    n = norm_text(value)
    if n.startswith(("yes", "si", "true")):
        return False
    if n.startswith(("no", "false")):
        return True
    return None


def extract_qa_pairs(payload):
    """Collect (question, answer) pairs from a webhook payload, tolerating
    both list-shaped and dict-keyed-by-question-id answer structures."""
    pairs = []

    def walk(node):
        if isinstance(node, dict):
            if "question" in node and "answer" in node:
                pairs.append((node["question"], node["answer"]))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(payload)
    return pairs


def extract_submission_id(payload):
    if not isinstance(payload, dict):
        return None
    data = payload.get("data", {})
    candidates = [
        data.get("submission_id") if isinstance(data, dict) else None,
        data.get("id") if isinstance(data, dict) else None,
        payload.get("submission_id"),
        payload.get("contact_uniqueId"),  # fallback correlation key
    ]
    for candidate in candidates:
        # tolerate the {"question": ..., "answer": ...} wrapper shape
        if isinstance(candidate, dict):
            candidate = candidate.get("answer")
        if candidate in (None, "") or is_placeholder(candidate):
            continue
        return str(candidate).strip()
    return None


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


EXTRA_COLUMNS = [
    ("years_tech", "REAL"),
    ("english_usage", "TEXT"),
    ("foreign_employer", "TEXT"),
    ("ai_confidence", "REAL"),
    ("ai_coding", "TEXT"),
    ("utm_source", "TEXT"),
    ("utm_medium", "TEXT"),
    ("utm_campaign", "TEXT"),
    ("utm_content", "TEXT"),
    ("utm_term", "TEXT"),
]


def init_db():
    with db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS submissions (
                id TEXT PRIMARY KEY,
                salary_mxn REAL,
                salary_usd REAL,
                salary_norm REAL,
                level TEXT,
                role TEXT,
                completed INTEGER,
                source TEXT NOT NULL,
                received_at TEXT NOT NULL
            )"""
        )
        have = {r[1] for r in conn.execute("PRAGMA table_info(submissions)")}
        for col, typ in EXTRA_COLUMNS:
            if col not in have:
                conn.execute(f"ALTER TABLE submissions ADD COLUMN {col} {typ}")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS raw_events (
                received_at TEXT NOT NULL,
                submission_id TEXT,
                body TEXT NOT NULL
            )"""
        )


UPSERT_SQL = """INSERT INTO submissions
     (id, salary_mxn, salary_usd, salary_norm, level, role, years_tech,
      english_usage, foreign_employer, ai_confidence, ai_coding,
      utm_source, utm_medium, utm_campaign, utm_content, utm_term,
      completed, source, received_at)
   VALUES (:id, :salary_mxn, :salary_usd, :salary_norm, :level, :role,
           :years_tech, :english_usage, :foreign_employer, :ai_confidence,
           :ai_coding, :utm_source, :utm_medium, :utm_campaign, :utm_content,
           :utm_term, :completed, :source, :received_at)
   ON CONFLICT(id) DO UPDATE SET
     salary_mxn=excluded.salary_mxn, salary_usd=excluded.salary_usd,
     salary_norm=excluded.salary_norm, level=excluded.level,
     role=excluded.role, years_tech=excluded.years_tech,
     english_usage=excluded.english_usage,
     foreign_employer=excluded.foreign_employer,
     ai_confidence=excluded.ai_confidence, ai_coding=excluded.ai_coding,
     utm_source=excluded.utm_source, utm_medium=excluded.utm_medium,
     utm_campaign=excluded.utm_campaign, utm_content=excluded.utm_content,
     utm_term=excluded.utm_term,
     completed=excluded.completed, source=excluded.source,
     received_at=excluded.received_at"""


def trimmed_rows(conn):
    return conn.execute(
        "SELECT salary_norm, level, years_tech, english_usage,"
        " foreign_employer, ai_confidence, ai_coding FROM submissions"
        " WHERE salary_norm IS NOT NULL AND salary_norm BETWEEN ? AND ?",
        (TRIM_LO, TRIM_HI),
    ).fetchall()


def quantile(sorted_values, q):
    if not sorted_values:
        return None
    pos = q * (len(sorted_values) - 1)
    lo, hi = int(pos), min(int(pos) + 1, len(sorted_values) - 1)
    frac = pos - lo
    return sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac


def percentile_below(values, x):
    return round(100 * sum(1 for v in values if v < x) / len(values))


app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
init_db()

# Small per-IP rate limit for the sid lookup, to slow down id enumeration.
RATE_LIMIT, RATE_WINDOW = 30, 60.0
_hits = defaultdict(deque)


def rate_limited(request: Request):
    fwd = request.headers.get("x-forwarded-for", "")
    ip = fwd.split(",")[0].strip() or (request.client.host if request.client else "?")
    now = time.monotonic()
    q = _hits[ip]
    while q and now - q[0] > RATE_WINDOW:
        q.popleft()
    if len(q) >= RATE_LIMIT:
        return True
    q.append(now)
    return False


@app.post("/pulse/webhook")
async def webhook(request: Request):
    try:
        payload = json.loads(await request.body())
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(status_code=400, detail="invalid JSON")

    if WEBHOOK_SECRET:
        provided = (
            request.headers.get("x-secret-token")
            or request.headers.get("authorization", "").removeprefix("Bearer ").strip()
            or (payload.get("secret_token") if isinstance(payload, dict) else "")
            or (payload.get("secret") if isinstance(payload, dict) else "")
            or ""
        )
        if not hmac.compare_digest(str(provided), WEBHOOK_SECRET):
            raise HTTPException(status_code=401, detail="bad token")

    sid = extract_submission_id(payload)
    now = datetime.now(timezone.utc).isoformat()
    fields = {f: None for f in ALL_FIELDS}

    # Preferred shape: flat keys defined in the webhook's Content template
    # ({"salary_mxn": "{placeholder}", ...}), at top level or under "data".
    sources = [payload if isinstance(payload, dict) else {}]
    if isinstance(sources[0].get("data"), dict):
        sources.append(sources[0]["data"])
    for src in sources:
        for field in fields:
            if fields[field] is None and field in src:
                value = src[field]
                if isinstance(value, dict) and "answer" in value:
                    value = value["answer"]
                fields[field] = parse_field(field, value)

    # Fallback: question/answer structures anywhere in the payload.
    for question, answer in extract_qa_pairs(payload):
        field = match_field(question)
        if field and fields[field] is None:
            fields[field] = parse_field(field, answer)

    with db() as conn:
        conn.execute(
            "INSERT INTO raw_events (received_at, submission_id, body) VALUES (?, ?, ?)",
            (now, sid, json.dumps(payload, ensure_ascii=False)),
        )
        if sid is not None:
            conn.execute(
                UPSERT_SQL,
                {
                    "id": sid,
                    **fields,
                    "salary_norm": normalize_salary(fields["salary_mxn"], fields["salary_usd"]),
                    "completed": 1,
                    "source": "webhook",
                    "received_at": now,
                },
            )
    return {"ok": True, "id": sid}


@app.get("/pulse/api/distribution")
def distribution():
    with db() as conn:
        rows = trimmed_rows(conn)
    values = sorted(r[0] for r in rows)
    n = len(values)

    n_bins = BIN_MAX // BIN_WIDTH
    counts = [0] * n_bins
    overflow = 0
    for v in values:
        if v >= BIN_MAX:
            overflow += 1
        else:
            counts[int(v // BIN_WIDTH)] += 1

    def cell(vals):
        return {"count": len(vals),
                "median": round(statistics.median(vals)) if vals else None}

    by_english = defaultdict(list)
    by_coding = defaultdict(list)
    conf_counts = defaultdict(int)
    conf_n = 0
    same, foreign = [], []
    for salary, _level, _yt, eng, femp, conf, coding in rows:
        ek = bucket_key(eng, ENGLISH_ORDER)
        if ek:
            by_english[ek].append(salary)
        ck = bucket_key(coding, AI_CODING_ORDER)
        if ck:
            by_coding[ck].append(salary)
        f = foreign_of(femp)
        if f is True:
            foreign.append(salary)
        elif f is False:
            same.append(salary)
    # confidence counts over ALL respondents who answered, salary or not
    with db() as conn:
        for (c,) in conn.execute(
            "SELECT ai_confidence FROM submissions WHERE ai_confidence IS NOT NULL"
        ):
            c = int(c)
            if 1 <= c <= 5:
                conf_counts[c] += 1
                conf_n += 1

    coding_total = sum(len(v) for v in by_coding.values())
    return {
        "n": n,
        "median": round(statistics.median(values)) if values else None,
        "bin_width": BIN_WIDTH,
        "bins": [
            {"lo": i * BIN_WIDTH, "hi": (i + 1) * BIN_WIDTH, "count": c}
            for i, c in enumerate(counts)
        ],
        "overflow": {"lo": BIN_MAX, "count": overflow},
        "quantiles": [round(quantile(values, q / 100), 2) for q in range(101)] if values else [],
        "english": [
            {"key": k, "label": lbl, **cell(by_english.get(k, []))}
            for k, lbl in ENGLISH_ORDER
        ],
        "ai_confidence": {
            "n": conf_n,
            "counts": [conf_counts.get(i, 0) for i in range(1, 6)],
        },
        "ai_coding": [
            {"key": k, "label": lbl, **cell(by_coding.get(k, [])),
             "share": round(100 * len(by_coding.get(k, [])) / coding_total) if coding_total else 0}
            for k, lbl in AI_CODING_ORDER
        ],
        "foreign": {"same": cell(same), "foreign": cell(foreign)},
    }


@app.get("/pulse/api/me")
def me(request: Request, sid: str = ""):
    if rate_limited(request):
        raise HTTPException(status_code=429, detail="too many requests")
    not_found = {"found": False}
    if not sid:
        return not_found
    with db() as conn:
        row = conn.execute(
            "SELECT salary_norm, level, years_tech, english_usage,"
            " foreign_employer, ai_confidence, ai_coding, source, received_at"
            " FROM submissions WHERE id = ?",
            (sid.strip(),),
        ).fetchone()
        rows = trimmed_rows(conn)
    if row is None:
        return not_found
    (salary, level, years_tech, english_usage, foreign_emp,
     ai_confidence, ai_coding, source, received_at) = row
    # Only submissions that just arrived via webhook are retrievable, so old
    # (sequential) submission ids can't be enumerated for their salaries.
    if source != "webhook":
        return not_found
    try:
        age_h = (
            datetime.now(timezone.utc) - datetime.fromisoformat(received_at)
        ).total_seconds() / 3600
    except ValueError:
        return not_found
    if age_h > SID_TTL_HOURS:
        return not_found

    out = {
        "found": True,
        "salary": round(salary) if salary is not None else None,
        "english_key": bucket_key(english_usage, ENGLISH_ORDER),
        "foreign": foreign_of(foreign_emp),
        "ai_confidence": int(ai_confidence) if ai_confidence and 1 <= ai_confidence <= 5 else None,
        "ai_coding_key": bucket_key(ai_coding, AI_CODING_ORDER),
    }
    values = [r[0] for r in rows]
    if salary is None or not values:
        return out
    out["percentile"] = percentile_below(values, salary)
    out["n"] = len(values)

    if level:
        peers = [r[0] for r in rows if r[1] == level]
        if len(peers) >= MIN_CELL:
            out["level"] = level
            out["level_n"] = len(peers)
            out["level_percentile"] = percentile_below(peers, salary)
    if years_tech is not None:
        peers = [r[0] for r in rows if r[2] is not None and abs(r[2] - years_tech) <= 2]
        if len(peers) >= MIN_CELL:
            out["exp_years"] = round(years_tech)
            out["exp_n"] = len(peers)
            out["exp_median"] = round(statistics.median(peers))
    return out


@app.get("/pulse/api/attribution")
def attribution():
    with db() as conn:
        rows = conn.execute(
            "SELECT COALESCE(utm_source, '(sin utm)'),"
            " COALESCE(utm_medium, ''), COALESCE(utm_campaign, ''), COUNT(*)"
            " FROM submissions WHERE source = 'webhook'"
            " GROUP BY 1, 2, 3 ORDER BY COUNT(*) DESC"
        ).fetchall()
        total, since = conn.execute(
            "SELECT COUNT(*), MIN(received_at) FROM submissions WHERE source = 'webhook'"
        ).fetchone()
    return {
        "webhook_submissions": total,
        "since": since,
        "note": "solo respuestas llegadas por webhook; el seed histórico no trae UTM",
        "by_channel": [
            {"utm_source": s, "utm_medium": m, "utm_campaign": c, "count": n}
            for s, m, c, n in rows
        ],
    }


@app.get("/pulse/health")
def health():
    with db() as conn:
        n = conn.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
    return {"ok": True, "submissions": n}


@app.get("/pulse")
@app.get("/pulse/")
def root_redirect():
    return RedirectResponse(url="/pulse/mi-resultado")


@app.get("/pulse/mi-resultado", response_class=HTMLResponse)
def result_page():
    # no-store: the page and its numbers change with every submission, and a
    # heuristically-cached copy would show a respondent a stale version
    return HTMLResponse(
        PAGE_HTML.replace("__SURVEY_URL__", SURVEY_URL).replace("__HOME_URL__", HOME_URL),
        headers={"Cache-Control": "no-store"},
    )


@app.middleware("http")
async def no_store_apis(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/pulse/api/"):
        response.headers["Cache-Control"] = "no-store"
    return response


PAGE_HTML = r"""<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Gracias por participar · SG Tech Pulse</title>
<link rel="icon" href="https://salarios.sg.com.mx/images/brand/isotipo-plasta_hu_95cd1f28bbb616c8.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<script>
  // Apply the shared theme choice before paint (same key as the landing site).
  try {
    var t = localStorage.getItem("tp-theme");
    if (t === "dark" || t === "light") document.documentElement.setAttribute("data-theme", t);
  } catch (e) {}
</script>
<style>
  :root {
    /* SG Tech Pulse 2026 palette (light) */
    --ground: #F6F3EE;
    --ground-rgb: 246,243,238;
    --surface: #FFFFFF;
    --surface-2: #EFEBE4;
    --ink: #171716;
    --ink-2: #5C574E;        /* --tx-soft */
    --muted: #8C867A;        /* --tx-faint */
    --grid: #E0DACF;         /* --rule */
    --baseline: #CFC8BB;
    --border: #E0DACF;
    --violet: #6B3DFA;       /* --accent */
    --violet-rgb: 107,61,250;
    --lime: #C4E833;
    --lime-rgb: 196,232,51;
    --coral: #FD655C;
    --bar: #6B3DFA;          /* chart bar, validated on #FFFFFF */
    --you: #FD655C;          /* respondent marker, validated on #FFFFFF */
    --on-accent: #FFFFFF;
    color-scheme: light;
  }
  :root:not([data-theme="light"]) { }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --ground: #171716;
      --ground-rgb: 23,23,22;
      --surface: #201F1C;
      --surface-2: #2A2825;
      --ink: #F6F3EE;
      --ink-2: #ADA79B;
      --muted: #7D776C;
      --grid: #35322D;
      --baseline: #4A463F;
      --border: #35322D;
      --violet: #8A63FF;
      --violet-rgb: 138,99,255;
      --bar: #8A63FF;        /* validated on #201F1C */
      --you: #F5504A;        /* validated on #201F1C */
      color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --ground: #171716;
    --ground-rgb: 23,23,22;
    --surface: #201F1C;
    --surface-2: #2A2825;
    --ink: #F6F3EE;
    --ink-2: #ADA79B;
    --muted: #7D776C;
    --grid: #35322D;
    --baseline: #4A463F;
    --border: #35322D;
    --violet: #8A63FF;
    --violet-rgb: 138,99,255;
    --bar: #8A63FF;
    --you: #F5504A;
    color-scheme: dark;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--ground); color: var(--ink);
    font-family: "Instrument Sans", system-ui, -apple-system, sans-serif;
    font-size: 17px; line-height: 1.6; -webkit-font-smoothing: antialiased;
    display: flex; flex-direction: column; min-height: 100vh;
  }
  h1, h2, h3 {
    font-family: "Bricolage Grotesque", system-ui, sans-serif;
    font-weight: 800; letter-spacing: -.03em; line-height: 1.04; margin: 0;
    text-wrap: balance;
  }
  svg text { font-family: "Instrument Sans", system-ui, sans-serif; }
  .eyebrow {
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: 12px; letter-spacing: .2em; text-transform: uppercase;
    color: var(--muted); margin: 0;
  }
  .wrap { width: min(760px, 100% - 40px); margin-inline: auto; }
  /* nav */
  nav {
    position: sticky; top: 0; z-index: 60;
    background: color-mix(in srgb, var(--ground) 88%, transparent);
    backdrop-filter: blur(12px); border-bottom: 1px solid var(--grid);
  }
  .nav-in { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; }
  .nav-controls { display: inline-flex; gap: 8px; }
  .brand img { height: 30px; width: auto; display: block; }
  .brand .lg-dark { display: none; }
  :root[data-theme="dark"] .brand .lg-light { display: none; }
  :root[data-theme="dark"] .brand .lg-dark { display: block; }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) .brand .lg-light { display: none; }
    :root:not([data-theme="light"]) .brand .lg-dark { display: block; }
  }
  .theme-btn {
    display: inline-flex; align-items: center; gap: 7px; background: none;
    border: 1.5px solid var(--grid); color: var(--ink-2); cursor: pointer;
    font-family: "IBM Plex Mono", monospace; font-size: 11.5px;
    letter-spacing: .08em; text-transform: uppercase; padding: 8px 13px;
    border-radius: 999px; min-height: 40px;
  }
  .theme-btn svg { width: 15px; height: 15px; }
  .theme-btn .lbl-dark { display: none; }
  :root[data-theme="dark"] .theme-btn .lbl-light { display: none; }
  :root[data-theme="dark"] .theme-btn .lbl-dark { display: inline; }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) .theme-btn .lbl-light { display: none; }
    :root:not([data-theme="light"]) .theme-btn .lbl-dark { display: inline; }
  }
  /* hero / thank-you */
  .hero-sec {
    position: relative; overflow: hidden; text-align: center;
    padding: 52px 0 44px;
    background:
      radial-gradient(ellipse at 22% 0%, rgba(var(--violet-rgb), .16), transparent 55%),
      radial-gradient(ellipse at 82% 8%, rgba(var(--lime-rgb), .20), transparent 52%);
  }
  .hero-sec h1 { font-size: clamp(30px, 5.2vw, 48px); margin: 14px 0 0; }
  .hero-sec .lead {
    font-size: clamp(17px, 2.1vw, 19px); color: var(--ink-2);
    max-width: 52ch; margin: 18px auto 0; text-wrap: pretty;
  }
  .mol { display: inline-block; }
  /* buttons */
  .btn {
    display: inline-flex; align-items: center; gap: 9px; justify-content: center;
    font-family: "Instrument Sans", sans-serif; font-weight: 600; font-size: 16px;
    padding: 13px 26px; border-radius: 999px; text-decoration: none;
    border: 1.5px solid transparent; cursor: pointer;
    transition: transform .15s ease, box-shadow .15s ease;
  }
  .btn-primary { background: var(--violet); color: var(--on-accent); }
  .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(var(--violet-rgb), .35); }
  .closenote {
    font-family: "IBM Plex Mono", monospace; color: var(--muted);
    font-size: 13px; margin: 16px 0 0;
  }
  /* main */
  main { flex: 1; padding: 40px 0 8px; width: 100%; }
  main .wrap > .sectiontitle { font-size: clamp(24px, 3.6vw, 30px); margin: 0 0 4px; }
  h2.sectiontitle { }
  .card h2 { font-size: 19px; margin: 0 0 2px; }
  .sub { color: var(--ink-2); margin: 0 0 22px; font-size: 15.5px; }
  .modsub { color: var(--ink-2); margin: 0 0 14px; font-size: 14.5px; }
  .card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 20px; padding: 24px; margin-bottom: 18px;
    box-shadow: 0 1px 2px rgba(var(--ground-rgb), .5);
  }
  .hero { font-size: 20px; line-height: 1.4; margin: 0; }
  .hero strong { font-size: 40px; display: block; margin-bottom: 2px;
    font-family: "Bricolage Grotesque", sans-serif; font-weight: 800; letter-spacing: -.03em; }
  .hero .pct { color: var(--you); }
  .meta {
    font-family: "IBM Plex Mono", monospace; color: var(--ink-2);
    font-size: 13.5px; margin: 12px 0 0;
  }
  .peerline { font-size: 15px; color: var(--ink); margin: 14px 0 0; padding-top: 14px; border-top: 1px solid var(--grid); }
  .peerline .n { color: var(--muted); }
  #chartwrap { position: relative; }
  svg { display: block; width: 100%; height: auto; }
  .tooltip {
    position: absolute; pointer-events: none; display: none;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 10px; padding: 6px 10px; font-size: 13px; color: var(--ink);
    box-shadow: 0 4px 16px var(--shadow, rgba(23,23,22,.14)); white-space: nowrap; z-index: 2;
  }
  .askrow { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
  .askrow input {
    flex: 1 1 180px; font: inherit; padding: 12px 14px; border-radius: 999px;
    border: 1.5px solid var(--baseline); background: var(--surface); color: var(--ink);
  }
  .askrow input:focus { outline: none; border-color: var(--violet); }
  .askrow button {
    font: inherit; font-weight: 600; padding: 12px 22px; border-radius: 999px;
    border: none; background: var(--violet); color: var(--on-accent); cursor: pointer;
  }
  .privacy {
    font-family: "IBM Plex Mono", monospace; color: var(--muted);
    font-size: 12.5px; margin: 10px 0 0;
  }
  details { margin-top: 14px; font-size: 14px; color: var(--ink-2); }
  details summary { cursor: pointer; color: var(--violet); }
  details table { border-collapse: collapse; margin-top: 8px; font-variant-numeric: tabular-nums; }
  details th, details td { text-align: right; padding: 3px 12px 3px 0; border-bottom: 1px solid var(--grid); }
  details th { color: var(--muted); font-weight: 500; }
  .foot { color: var(--muted); font-size: 13px; line-height: 1.6; margin-top: 22px; }
  .foot a { color: var(--violet); }
  .backrow { text-align: center; margin: 28px 0 8px; }
  .hidden { display: none; }
  .contextline { font-size: 14px; color: var(--ink-2); margin: 14px 0 0; padding-top: 14px; border-top: 1px solid var(--grid); }
  /* footer */
  footer.sg { border-top: 1px solid var(--grid); padding: 28px 0; margin-top: 12px; }
  footer.sg .foot-in { display: flex; flex-wrap: wrap; gap: 16px; align-items: center; justify-content: space-between; }
  footer.sg img { height: 26px; width: auto; }
  footer.sg .lg-dark { display: none; }
  :root[data-theme="dark"] footer.sg .lg-light { display: none; }
  :root[data-theme="dark"] footer.sg .lg-dark { display: block; }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) footer.sg .lg-light { display: none; }
    :root:not([data-theme="light"]) footer.sg .lg-dark { display: block; }
  }
  footer.sg .foot-note { color: var(--muted); font-size: 13px; margin: 0; max-width: 42ch; }
  footer.sg a.foot-link { color: var(--ink-2); text-decoration: none; font-size: 14px; }
  footer.sg a.foot-link:hover { color: var(--violet); }
</style>
</head>
<body>
<nav><div class="wrap nav-in">
  <a class="brand" href="__HOME_URL__" aria-label="SG Tech Pulse 2026 · Encuesta de Salarios">
    <img class="lg-light" src="https://salarios.sg.com.mx/images/brand/logo-negro_hu_4935ae413724ddf0.webp" width="440" height="102" alt="SG Tech Pulse 2026 · Encuesta de Salarios">
    <img class="lg-dark" src="https://salarios.sg.com.mx/images/brand/logo-blanco_hu_d2b6415631d4722c.webp" width="440" height="102" alt="">
  </a>
  <span class="nav-controls">
  <button class="theme-btn" id="lang-toggle" type="button" aria-label="Cambiar idioma / Change language">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.9 3.8 9S14.5 21.3 12 21c-2.5-.3-3.8-5.9-3.8-9S9.5 5.7 12 3z"/></svg>
    <span id="lang-code">EN</span>
  </button>
  <button class="theme-btn" id="theme-toggle" type="button" data-i18n-aria="theme_aria" aria-label="Cambiar entre tema claro y oscuro">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
    <span class="lbl-light" data-i18n="lbl_light">Claro</span><span class="lbl-dark" data-i18n="lbl_dark">Oscuro</span>
  </button>
  </span>
</div></nav>

<section class="hero-sec">
  <div class="wrap">
    <svg class="mol" width="60" height="34" viewBox="0 0 60 34" aria-hidden="true">
      <line x1="16" y1="17" x2="34" y2="11" stroke="var(--lime)" stroke-width="1.5"/>
      <line x1="34" y1="11" x2="46" y2="22" stroke="var(--violet)" stroke-width="1.5"/>
      <circle cx="14" cy="17" r="7" fill="var(--violet)"/>
      <circle cx="34" cy="10" r="5" fill="var(--lime)"/>
      <circle cx="47" cy="23" r="6" fill="var(--coral)"/>
    </svg>
    <p class="eyebrow" data-i18n="eyebrow">SG Tech Pulse 2026 · Encuesta de Salarios</p>
    <h1 data-i18n="thanks_h1">¡Gracias por participar!</h1>
    <p class="lead" data-i18n="thanks_lead">Tu respuesta quedó registrada de forma anónima y ya forma parte del estudio de
    salarios, IA, diversidad y carreras tech en Latinoamérica. Esto es lo que tu respuesta permite ver.</p>
  </div>
</section>

<main>
  <div class="wrap">
  <h2 class="sectiontitle" data-i18n="sectiontitle">¿Dónde está tu sueldo?</h2>
  <p class="sub" data-i18n="sub">Tu sueldo base mensual comparado con quienes ya respondieron la encuesta.</p>

  <div class="card" id="herocard">
    <p class="hero" id="hero" data-i18n="loading">Cargando la distribución…</p>
    <p class="meta" id="herometa"></p>
    <p class="peerline hidden" id="levelline"></p>
    <p class="peerline hidden" id="expline"></p>
    <div class="askrow hidden" id="askrow">
      <input id="salaryinput" type="text" inputmode="numeric"
             data-i18n-ph="ph_salary" data-i18n-aria="aria_salary"
             placeholder="Tu sueldo base mensual en MXN, p. ej. 65000"
             aria-label="Tu sueldo base mensual en pesos mexicanos">
      <button id="askbtn" data-i18n="btn_seeposition">Ver mi posición</button>
    </div>
    <p class="privacy hidden" id="privacynote" data-i18n="privacy">El monto se compara aquí en tu navegador; no se envía a ningún servidor.</p>
  </div>

  <div class="card">
    <div id="chartwrap">
      <div class="tooltip" id="tooltip"></div>
      <svg id="chart" role="img" data-i18n-aria="hist_aria" aria-label="Histograma de sueldos base mensuales en pesos mexicanos"></svg>
    </div>
    <p class="contextline" id="foreignline"></p>
    <details id="tabledetails">
      <summary data-i18n="table_toggle">Ver los datos en tabla</summary>
      <table id="datatable"></table>
    </details>
  </div>

  <div class="card" id="englishcard">
    <h2 data-i18n="english_h2">¿Cuánto vale tu inglés?</h2>
    <p class="modsub" data-i18n="english_sub">Mediana de sueldo base según la frecuencia de uso del inglés en el trabajo.</p>
    <svg id="englishchart" role="img" data-i18n-aria="english_aria" aria-label="Mediana de sueldo por frecuencia de uso del inglés"></svg>
  </div>

  <div class="card" id="aicard">
    <h2 data-i18n="ai_h2">La ventana de la IA</h2>
    <p class="modsub" id="codingsub" data-i18n="coding_sub">Cómo se escribe código ahora, entre quienes programan.</p>
    <svg id="codingchart" role="img" data-i18n-aria="coding_aria" aria-label="Formas de usar IA para crear código"></svg>
    <p class="modsub" style="margin-top:18px" data-i18n="conf_q">«¿Qué tan seguro/a estás de que tus habilidades seguirán siendo relevantes dentro de 3 años?»</p>
    <svg id="confchart" role="img" data-i18n-aria="conf_aria" aria-label="Distribución de confianza en la relevancia futura de habilidades"></svg>
    <p class="contextline hidden" id="confline"></p>
  </div>

  <p class="foot">
    <span id="foottext" data-i18n="foot">Muestra autoseleccionada de la comunidad tech; resultados preliminares que cambian conforme llegan respuestas.
    Sueldos en dólares convertidos a MXN. Las medianas por grupo describen la muestra, no efectos causales.
    La encuesta sigue abierta</span><span id="sharespan"></span>.
  </p>

  <div class="backrow"><a class="btn btn-primary" href="__HOME_URL__" data-i18n="back_btn">Volver a SG Tech Pulse</a>
    <p class="closenote" data-i18n="closenote">Puedes cerrar esta pestaña sin problema: no hay nada pendiente de guardar.</p>
  </div>
  </div>
</main>

<footer class="sg"><div class="wrap foot-in">
  <a class="brand" href="__HOME_URL__" aria-label="SG Software Guru">
    <img class="lg-light" src="https://salarios.sg.com.mx/images/brand/logo-negro_hu_4935ae413724ddf0.webp" width="440" height="102" alt="SG Software Guru">
    <img class="lg-dark" src="https://salarios.sg.com.mx/images/brand/logo-blanco_hu_d2b6415631d4722c.webp" width="440" height="102" alt="">
  </a>
  <p class="foot-note" data-i18n="footnote">Una iniciativa de SG Software Guru, agencia de Developer Relations y bureau de inteligencia del mercado tech.</p>
  <a class="foot-link" href="https://sg.com.mx">sg.com.mx</a>
</div></footer>
<script>
// Theme toggle — shares the "tp-theme" key with the landing site.
(function () {
  var btn = document.getElementById("theme-toggle");
  if (!btn) return;
  function current() {
    var set = document.documentElement.getAttribute("data-theme");
    if (set) return set;
    return matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  btn.addEventListener("click", function () {
    var next = current() === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem("tp-theme", next); } catch (e) {}
  });
})();
// ---- i18n ----------------------------------------------------------
const I18N = {
  es: {
    title: "Gracias por participar · SG Tech Pulse",
    eyebrow: "SG Tech Pulse 2026 · Encuesta de Salarios",
    thanks_h1: "¡Gracias por participar!",
    thanks_lead: "Tu respuesta quedó registrada de forma anónima y ya forma parte del estudio de salarios, IA, diversidad y carreras tech en Latinoamérica. Esto es lo que tu respuesta permite ver.",
    sectiontitle: "¿Dónde está tu sueldo?",
    sub: "Tu sueldo base mensual comparado con quienes ya respondieron la encuesta.",
    loading: "Cargando la distribución…",
    ph_salary: "Tu sueldo base mensual en MXN, p. ej. 65000",
    aria_salary: "Tu sueldo base mensual en pesos mexicanos",
    btn_seeposition: "Ver mi posición",
    privacy: "El monto se compara aquí en tu navegador; no se envía a ningún servidor.",
    table_toggle: "Ver los datos en tabla",
    english_h2: "¿Cuánto vale tu inglés?",
    english_sub: "Mediana de sueldo base según la frecuencia de uso del inglés en el trabajo.",
    ai_h2: "La ventana de la IA",
    coding_sub: "Cómo se escribe código ahora, entre quienes programan.",
    conf_q: "«¿Qué tan seguro/a estás de que tus habilidades seguirán siendo relevantes dentro de 3 años?»",
    foot: "Muestra autoseleccionada de la comunidad tech; resultados preliminares que cambian conforme llegan respuestas. Sueldos en dólares convertidos a MXN. Las medianas por grupo describen la muestra, no efectos causales. La encuesta sigue abierta",
    back_btn: "Volver a SG Tech Pulse",
    closenote: "Puedes cerrar esta pestaña sin problema: no hay nada pendiente de guardar.",
    footnote: "Una iniciativa de SG Software Guru, agencia de Developer Relations y bureau de inteligencia del mercado tech.",
    theme_aria: "Cambiar entre tema claro y oscuro",
    lbl_light: "Claro", lbl_dark: "Oscuro",
    share: "compártela con tu equipo",
    hist_aria: "Histograma de sueldos base mensuales en pesos mexicanos",
    english_aria: "Mediana de sueldo por frecuencia de uso del inglés",
    coding_aria: "Formas de usar IA para crear código",
    conf_aria: "Distribución de confianza en la relevancia futura de habilidades",
    hero_pct: 'Tu sueldo base está por encima del <strong><span class="pct">{pct}&hairsp;%</span></strong> de las {n} personas que han respondido.',
    meta_you: "Tú: {salary} al mes · mediana general: {median}",
    ask_hero: "Escribe tu sueldo base mensual y te decimos dónde estás.",
    ask_meta: "{n} personas han respondido · mediana general: {median}",
    level_line: 'Entre nivel <b>{level}</b> estás por encima del <b>{pct}%</b> <span class="n">({n} personas)</span>.',
    exp_line: 'Para tu experiencia (~{y} años en tech), la mediana es <b>{m}</b> <span class="n">({n} personas con ±2 años)</span>.',
    foreign_line: "Quienes trabajan para una empresa en el extranjero ({nf} personas): mediana {mf} · empresa local ({ns}): {ms}.",
    tt_range: "{lo} – {hi} · {people}",
    tt_over: "Más de {lo} · {people}",
    person_one: "1 persona", person_other: "{n} personas",
    you_label: "Tú · {salary}", you_tag: "Tú",
    tbl_range: "Rango (MXN/mes)", tbl_people: "Personas", tbl_over: "Más de {lo}",
    coding_value: "{share}% · mediana {m}",
    conf_worried: "Compartes esta inquietud con {w} de {n} personas. No estás solo/a.",
    conf_answer: "Tu respuesta: {label} · {n} personas han respondido.",
  },
  en: {
    title: "Thank you for taking part · SG Tech Pulse",
    eyebrow: "SG Tech Pulse 2026 · Salary Survey",
    thanks_h1: "Thank you for taking part!",
    thanks_lead: "Your response was recorded anonymously and is now part of the study on salaries, AI, diversity and tech careers across Latin America. Here's what your response makes visible.",
    sectiontitle: "Where does your salary land?",
    sub: "Your monthly base salary compared with everyone who has already answered the survey.",
    loading: "Loading the distribution…",
    ph_salary: "Your monthly base salary in MXN, e.g. 65000",
    aria_salary: "Your monthly base salary in Mexican pesos",
    btn_seeposition: "See where I land",
    privacy: "The amount is compared here in your browser; nothing is sent to any server.",
    table_toggle: "View the data as a table",
    english_h2: "What is your English worth?",
    english_sub: "Median base salary by how often English is used at work.",
    ai_h2: "The AI window",
    coding_sub: "How code gets written now, among those who program.",
    conf_q: "“How confident are you that your current skills will remain relevant in 3 years?”",
    foot: "Self-selected sample of the tech community; preliminary results that change as responses arrive. USD salaries converted to MXN. Group medians describe the sample, not causal effects. The survey is still open",
    back_btn: "Back to SG Tech Pulse",
    closenote: "You can safely close this tab: nothing is left to save.",
    footnote: "An initiative by SG Software Guru, a Developer Relations agency and tech-market intelligence bureau.",
    theme_aria: "Toggle between light and dark theme",
    lbl_light: "Light", lbl_dark: "Dark",
    share: "share it with your team",
    hist_aria: "Histogram of monthly base salaries in Mexican pesos",
    english_aria: "Median salary by frequency of English use",
    coding_aria: "Ways of using AI to write code",
    conf_aria: "Distribution of confidence in future skill relevance",
    hero_pct: 'Your base salary is higher than <strong><span class="pct">{pct}&hairsp;%</span></strong> of the {n} people who have answered.',
    meta_you: "You: {salary}/mo MXN · overall median: {median}",
    ask_hero: "Enter your monthly base salary and we'll tell you where you land.",
    ask_meta: "{n} people have answered · overall median: {median}",
    level_line: 'At <b>{level}</b> level you\'re higher than <b>{pct}%</b> <span class="n">({n} people)</span>.',
    exp_line: 'For your experience (~{y} years in tech), the median is <b>{m}</b> <span class="n">({n} people within ±2 years)</span>.',
    foreign_line: "People working for a foreign employer ({nf} people): median {mf} · local employer ({ns}): {ms}.",
    tt_range: "{lo} – {hi} · {people}",
    tt_over: "Over {lo} · {people}",
    person_one: "1 person", person_other: "{n} people",
    you_label: "You · {salary}", you_tag: "You",
    tbl_range: "Range (MXN/month)", tbl_people: "People", tbl_over: "Over {lo}",
    coding_value: "{share}% · median {m}",
    conf_worried: "You share this concern with {w} of {n} people. You're not alone.",
    conf_answer: "Your answer: {label} · {n} people have answered.",
  },
};
const LABELS = {
  english: {
    es: { "nunca": "Nunca", "ocasionalmente": "Ocasionalmente (leer docs)", "con regularidad": "Con regularidad (juntas, emails)", "la mayoria del tiempo": "La mayoría del tiempo", "todo el tiempo": "Todo el tiempo" },
    en: { "nunca": "Never", "ocasionalmente": "Occasionally (reading docs)", "con regularidad": "Regularly (meetings, emails)", "la mayoria del tiempo": "Most of the time", "todo el tiempo": "All the time" },
  },
  coding: {
    es: { "programo manualmente y uso ia como soporte": "Programo a mano; IA como soporte", "programo la funcionalidad manualmente": "Programo a mano; IA para testing y docs", "aunque se programar": "Doy instrucciones a agentes y reviso" },
    en: { "programo manualmente y uso ia como soporte": "I code by hand; AI as support", "programo la funcionalidad manualmente": "I code by hand; AI for testing & docs", "aunque se programar": "I instruct agents and review" },
  },
  conf: {
    es: ["Nada", "Poco", "Algo", "Bastante", "Mucho"],
    en: ["Not at all", "A little", "Somewhat", "Quite", "Very"],
  },
};
function normLang(s) {
  s = (s || "").toString().toLowerCase();
  if (!s) return null;
  if (s.indexOf("en") === 0 || s.indexOf("english") >= 0) return "en";
  if (s.indexOf("es") === 0 || s.indexOf("span") >= 0) return "es";
  return null;
}
function detectLang() {
  const p = new URLSearchParams(location.search).get("lang");
  let stored = null; try { stored = localStorage.getItem("tp-lang"); } catch (e) {}
  return normLang(p) || normLang(stored) || normLang(navigator.language) || "es";
}
const LANG = detectLang();
function t(k) { const d = I18N[LANG] || I18N.es; return d[k] != null ? d[k] : (I18N.es[k] != null ? I18N.es[k] : k); }
function tt(k, v) { return t(k).replace(/\{(\w+)\}/g, (_, n) => (v && v[n] != null) ? v[n] : ""); }
document.documentElement.setAttribute("lang", LANG === "en" ? "en" : "es-MX");
document.title = t("title");
(function () {
  document.querySelectorAll("[data-i18n]").forEach(el => { el.textContent = t(el.getAttribute("data-i18n")); });
  document.querySelectorAll("[data-i18n-ph]").forEach(el => { el.setAttribute("placeholder", t(el.getAttribute("data-i18n-ph"))); });
  document.querySelectorAll("[data-i18n-aria]").forEach(el => { el.setAttribute("aria-label", t(el.getAttribute("data-i18n-aria"))); });
  const lc = document.getElementById("lang-code"); if (lc) lc.textContent = LANG === "en" ? "ES" : "EN";
})();
(function () {
  const btn = document.getElementById("lang-toggle"); if (!btn) return;
  btn.addEventListener("click", function () {
    const next = LANG === "en" ? "es" : "en";
    try { localStorage.setItem("tp-lang", next); } catch (e) {}
    const u = new URL(location.href); u.searchParams.set("lang", next); location.href = u.toString();
  });
})();

(async function () {
  const nf = new Intl.NumberFormat(LANG === "en" ? "en-US" : "es-MX", { maximumFractionDigits: 0 });
  const fmt = { format: v => "$" + nf.format(Math.round(v)) };
  const fmtK = v => v >= 1000 ? "$" + Math.round(v / 1000) + "k" : "$" + v;
  const $ = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  const people = n => n === 1 ? t("person_one") : tt("person_other", { n: n });
  const engLabel = k => (LABELS.english[LANG] || LABELS.english.es)[k] || k;
  const codLabel = k => (LABELS.coding[LANG] || LABELS.coding.es)[k] || k;
  const confLabels = LABELS.conf[LANG] || LABELS.conf.es;

  const surveyUrl = "__SURVEY_URL__";
  if (surveyUrl) $("sharespan").innerHTML =
    ' — <a href="' + esc(surveyUrl) + '">' + t("share") + '</a>';

  const sid = new URLSearchParams(location.search).get("sid") || "";
  const dist = await (await fetch("api/distribution")).json();

  let me = { found: false };
  if (sid) {
    try { me = await (await fetch("api/me?sid=" + encodeURIComponent(sid))).json(); }
    catch (e) { me = { found: false }; }
  }

  function percentileOf(salary) {
    const q = dist.quantiles;
    if (!q.length) return null;
    if (salary <= q[0]) return 0;
    if (salary >= q[q.length - 1]) return 100;
    let i = 0;
    while (i < q.length - 1 && q[i + 1] < salary) i++;
    return Math.round(i + (salary - q[i]) / Math.max(q[i + 1] - q[i], 1e-9));
  }

  function setHero(salary, pct) {
    $("hero").innerHTML = tt("hero_pct", { pct: pct, n: dist.n });
    $("herometa").textContent = tt("meta_you", { salary: fmt.format(salary), median: fmt.format(dist.median) });
  }

  function showAskRow() {
    $("hero").textContent = t("ask_hero");
    $("herometa").textContent = tt("ask_meta", { n: dist.n, median: fmt.format(dist.median) });
    $("askrow").classList.remove("hidden");
    $("privacynote").classList.remove("hidden");
  }

  // ---- salary histogram ----------------------------------------------
  const W = 680, H = 300, M = { top: 46, right: 14, bottom: 34, left: 40 };
  const bins = dist.bins.concat([{ lo: dist.overflow.lo, hi: null, count: dist.overflow.count, overflow: true }]);
  const iw = W - M.left - M.right, ih = H - M.top - M.bottom;
  const slot = iw / bins.length;
  const maxC = Math.max(1, ...bins.map(b => b.count));
  const yMax = Math.ceil(maxC / 10) * 10;
  const x = i => M.left + i * slot;
  const y = c => M.top + ih * (1 - c / yMax);
  const xOfSalary = s => {
    if (s >= dist.overflow.lo) return x(bins.length - 1) + slot / 2;
    return M.left + (s / dist.overflow.lo) * (iw - slot);
  };

  const svg = $("chart");
  svg.setAttribute("viewBox", "0 0 " + W + " " + H);
  let g = "";
  const yTicks = 5;
  for (let t = 0; t <= yTicks; t++) {
    const val = Math.round(yMax * t / yTicks), yy = y(val);
    g += '<line x1="' + M.left + '" x2="' + (W - M.right) + '" y1="' + yy + '" y2="' + yy +
         '" stroke="var(--grid)" stroke-width="1"/>' +
         '<text x="' + (M.left - 8) + '" y="' + (yy + 4) + '" text-anchor="end" font-size="11" fill="var(--muted)">' + val + "</text>";
  }
  const barW = Math.min(24, slot - 2);
  bins.forEach((b, i) => {
    const bx = x(i) + (slot - barW) / 2, by = y(b.count), bh = M.top + ih - by;
    if (b.count > 0) {
      const r = Math.min(4, bh);
      g += '<path fill="var(--bar)" d="M' + bx + " " + (by + r) +
           " q0 " + -r + " " + r + " " + -r + " h" + (barW - 2 * r) +
           " q" + r + " 0 " + r + " " + r + " v" + (bh - r) + " h" + -barW + ' z"/>';
    }
    g += '<rect class="hit" data-i="' + i + '" x="' + x(i) + '" y="' + M.top + '" width="' + slot +
         '" height="' + ih + '" fill="transparent"/>';
  });
  g += '<line x1="' + M.left + '" x2="' + (W - M.right) + '" y1="' + (M.top + ih) + '" y2="' + (M.top + ih) +
       '" stroke="var(--baseline)" stroke-width="1"/>';
  [0, 50000, 100000, 150000].forEach(v => {
    g += '<text x="' + xOfSalary(v) + '" y="' + (H - 12) + '" text-anchor="middle" font-size="11" fill="var(--muted)">' + fmtK(v) + "</text>";
  });
  g += '<text x="' + (x(bins.length - 1) + slot / 2) + '" y="' + (H - 12) + '" text-anchor="middle" font-size="11" fill="var(--muted)">$200k+</text>';
  svg.innerHTML = g;

  function drawYou(salary) {
    svg.querySelectorAll(".you").forEach(el => el.remove());
    const xx = xOfSalary(salary), yTop = M.top - 6, label = tt("you_label", { salary: fmt.format(salary) });
    const anchor = xx > W - 140 ? "end" : (xx < M.left + 100 ? "start" : "middle");
    svg.insertAdjacentHTML("beforeend", '<g class="you">' +
      '<line x1="' + xx + '" x2="' + xx + '" y1="' + yTop + '" y2="' + (M.top + ih) + '" stroke="var(--you)" stroke-width="2"/>' +
      '<path d="M' + (xx - 6) + " " + (yTop - 8) + " h12 l-6 9 z" + '" fill="var(--you)"/>' +
      '<text x="' + xx + '" y="' + (yTop - 14) + '" text-anchor="' + anchor + '" font-size="13" font-weight="600" fill="var(--ink)">' + esc(label) + "</text></g>");
  }

  const tip = $("tooltip"), wrap = $("chartwrap");
  svg.addEventListener("mousemove", e => {
    const t = e.target.closest(".hit");
    if (!t) { tip.style.display = "none"; return; }
    const b = bins[+t.dataset.i];
    tip.textContent = b.overflow
      ? tt("tt_over", { lo: fmt.format(b.lo), people: people(b.count) })
      : tt("tt_range", { lo: fmt.format(b.lo), hi: fmt.format(b.hi), people: people(b.count) });
    const r = wrap.getBoundingClientRect();
    tip.style.display = "block";
    tip.style.left = Math.min(e.clientX - r.left + 12, r.width - tip.offsetWidth - 4) + "px";
    tip.style.top = (e.clientY - r.top - 34) + "px";
  });
  svg.addEventListener("mouseleave", () => { tip.style.display = "none"; });

  $("datatable").innerHTML =
    "<tr><th>" + t("tbl_range") + "</th><th>" + t("tbl_people") + "</th></tr>" +
    bins.map(b => "<tr><td>" + (b.overflow ? tt("tbl_over", { lo: fmt.format(b.lo) }) : fmt.format(b.lo) + " – " + fmt.format(b.hi)) +
                  "</td><td>" + b.count + "</td></tr>").join("");

  // foreign-employer context line
  const fr = dist.foreign;
  if (fr.foreign.count >= 20 && fr.same.count >= 20) {
    $("foreignline").textContent = tt("foreign_line", {
      nf: fr.foreign.count, mf: fmt.format(fr.foreign.median),
      ns: fr.same.count, ms: fmt.format(fr.same.median),
    });
  } else {
    $("foreignline").classList.add("hidden");
  }

  // ---- horizontal bar module -----------------------------------------
  function hbars(svgId, rows, maxValue) {
    const rowH = 46, padL = 8, padR = 90, w = 680;
    const h = rows.length * rowH + 6;
    const s = $(svgId);
    s.setAttribute("viewBox", "0 0 " + w + " " + h);
    const scale = v => Math.max(4, (w - padL - padR) * v / maxValue);
    let out = "";
    rows.forEach((r, i) => {
      const top = i * rowH, barY = top + 24, barH = 16;
      const bw = scale(r.value);
      out += '<text x="' + padL + '" y="' + (top + 16) + '" font-size="13" fill="var(--ink-2)">' + esc(r.label) +
             (r.sub ? ' <tspan fill="var(--muted)" font-size="12">' + esc(r.sub) + "</tspan>" : "") + "</text>";
      out += '<path fill="var(--bar)" d="M' + padL + " " + barY + " h" + (bw - 4) +
             " q4 0 4 4 v" + (barH - 8) + " q0 4 -4 4 h" + -(bw - 4) + ' z"/>';
      out += '<text x="' + (padL + bw + 8) + '" y="' + (barY + 13) + '" font-size="13" font-weight="600" fill="var(--ink)">' + esc(r.valueLabel) + "</text>";
      if (r.you) {
        out += '<path d="M' + (padL - 1) + " " + (barY + 2) + " l7 6 l-7 6 z" + '" fill="var(--you)"/>' +
               '<text x="' + (padL + 10) + '" y="' + (barY + 13) + '" font-size="12" font-weight="700" fill="#fff">' + t("you_tag") + '</text>';
      }
    });
    s.innerHTML = out;
  }

  // English ladder: median salary per usage band
  const engRows = dist.english.filter(e => e.count >= 20);
  hbars("englishchart", engRows.map(e => ({
    label: engLabel(e.key), sub: "(" + e.count + ")",
    value: e.median, valueLabel: fmt.format(e.median),
    you: me.found && me.english_key === e.key,
  })), Math.max(...engRows.map(e => e.median)));

  // AI coding modes: share bars with median annotation
  const codRows = dist.ai_coding.filter(c => c.count >= 15);
  if (codRows.length) {
    hbars("codingchart", codRows.map(c => ({
      label: codLabel(c.key), sub: "(" + c.count + ")",
      value: c.share, valueLabel: tt("coding_value", { share: c.share, m: fmtK(c.median) }),
      you: me.found && me.ai_coding_key === c.key,
    })), Math.max(...codRows.map(c => c.share)));
  } else {
    $("codingchart").classList.add("hidden");
    $("codingsub").classList.add("hidden");
  }

  // Confidence distribution: 5 vertical bars, no salary attached
  (function () {
    const cc = dist.ai_confidence;
    const w = 680, h = 190, mm = { top: 54, right: 14, bottom: 26, left: 14 };
    const s = $("confchart");
    s.setAttribute("viewBox", "0 0 " + w + " " + h);
    const innerW = w - mm.left - mm.right, innerH = h - mm.top - mm.bottom;
    const slotW = innerW / 5, maxV = Math.max(1, ...cc.counts);
    let out = "";
    cc.counts.forEach((c, i) => {
      const bw = 24, bx = mm.left + i * slotW + (slotW - bw) / 2;
      const bh = Math.max(2, innerH * c / maxV), by = mm.top + innerH - bh;
      const r = Math.min(4, bh);
      out += '<path fill="var(--bar)" d="M' + bx + " " + (by + r) + " q0 " + -r + " " + r + " " + -r +
             " h" + (bw - 2 * r) + " q" + r + " 0 " + r + " " + r + " v" + (bh - r) + " h" + -bw + ' z"/>';
      out += '<text x="' + (bx + bw / 2) + '" y="' + (by - 6) + '" text-anchor="middle" font-size="12" fill="var(--ink-2)">' + c + "</text>";
      out += '<text x="' + (bx + bw / 2) + '" y="' + (h - 8) + '" text-anchor="middle" font-size="12" fill="var(--muted)">' + confLabels[i] + "</text>";
      if (me.found && me.ai_confidence === i + 1) {
        const cx = bx + bw / 2;
        out += '<text x="' + cx + '" y="' + (by - 36) + '" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">' + t("you_tag") + '</text>' +
               '<path class="you" d="M' + (cx - 7) + " " + (by - 30) + " h14 l-7 10 z" + '" fill="var(--you)"/>';
      }
    });
    out += '<line x1="' + mm.left + '" x2="' + (w - mm.right) + '" y1="' + (mm.top + innerH) + '" y2="' + (mm.top + innerH) +
           '" stroke="var(--baseline)" stroke-width="1"/>';
    s.innerHTML = out;
    if (me.found && me.ai_confidence) {
      const worried = cc.counts[0] + cc.counts[1];
      $("confline").classList.remove("hidden");
      $("confline").textContent = me.ai_confidence <= 2
        ? tt("conf_worried", { w: worried, n: cc.n })
        : tt("conf_answer", { label: confLabels[me.ai_confidence - 1].toLowerCase(), n: cc.n });
    }
  })();

  // ---- wire up the hero ----------------------------------------------
  if (me.found && me.salary) {
    setHero(me.salary, me.percentile);
    drawYou(me.salary);
    if (me.level_percentile !== undefined) {
      $("levelline").classList.remove("hidden");
      $("levelline").innerHTML = tt("level_line", { level: esc(me.level), pct: me.level_percentile, n: me.level_n });
    }
    if (me.exp_median !== undefined) {
      $("expline").classList.remove("hidden");
      $("expline").innerHTML = tt("exp_line", { y: me.exp_years, m: fmt.format(me.exp_median), n: me.exp_n });
    }
  } else {
    showAskRow();
    $("askbtn").addEventListener("click", () => {
      const v = parseFloat(($("salaryinput").value || "").replace(/[^\d.]/g, ""));
      if (!v || v <= 0) return;
      setHero(v, percentileOf(v));
      drawYou(v);
    });
    $("salaryinput").addEventListener("keydown", e => { if (e.key === "Enter") $("askbtn").click(); });
    // SurveySparrow's webhook can lag the redirect by a few minutes: poll
    // quietly and upgrade to the personalized view when the data lands,
    // unless the visitor already started typing their own number.
    if (sid) {
      let tries = 0;
      const poll = setInterval(async () => {
        if (++tries > 30) return clearInterval(poll);
        if ($("salaryinput").value) return;
        try {
          const again = await (await fetch("api/me?sid=" + encodeURIComponent(sid))).json();
          if (again.found && again.salary) { clearInterval(poll); location.reload(); }
        } catch (e) { /* transient; keep polling */ }
      }, 10000);
    }
  }
})();
</script>
<!-- LinkedIn Insight Tag (SG marketing) -->
<script type="text/javascript">
_linkedin_partner_id = "9920940";
window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
window._linkedin_data_partner_ids.push(_linkedin_partner_id);
</script><script type="text/javascript">
(function(l) {
if (!l){window.lintrk = function(a,b){window.lintrk.q.push([a,b])};
window.lintrk.q=[]}
var s = document.getElementsByTagName("script")[0];
var b = document.createElement("script");
b.type = "text/javascript";b.async = true;
b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js";
s.parentNode.insertBefore(b, s);})(window.lintrk);
</script>
<noscript>
<img height="1" width="1" style="display:none;" alt="" src="https://px.ads.linkedin.com/collect/?pid=9920940&fmt=gif" />
</noscript>
<!-- Meta Pixel Code (SG marketing) -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '233146077047917');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=233146077047917&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
</body>
</html>
"""

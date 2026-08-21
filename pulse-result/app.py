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
TEXT_FIELDS = {"level", "role", "english_usage", "foreign_employer", "ai_coding"}
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
    → True means foreign employer (answered No)."""
    if value is None:
        return None
    n = norm_text(value)
    if n.startswith(("yes", "si")):
        return False
    if n.startswith("no"):
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
      completed, source, received_at)
   VALUES (:id, :salary_mxn, :salary_usd, :salary_norm, :level, :role,
           :years_tech, :english_usage, :foreign_employer, :ai_confidence,
           :ai_coding, :completed, :source, :received_at)
   ON CONFLICT(id) DO UPDATE SET
     salary_mxn=excluded.salary_mxn, salary_usd=excluded.salary_usd,
     salary_norm=excluded.salary_norm, level=excluded.level,
     role=excluded.role, years_tech=excluded.years_tech,
     english_usage=excluded.english_usage,
     foreign_employer=excluded.foreign_employer,
     ai_confidence=excluded.ai_confidence, ai_coding=excluded.ai_coding,
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
                fields[field] = parse_field(field, src[field])

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
<style>
  :root {
    color-scheme: light;
    --page: #ffffff;
    --page-rgb: 255,255,255;
    --surface: #ffffff;
    --ink: #212529;
    --ink-2: #495057;
    --muted: #6c757d;
    --grid: #e9ecef;
    --baseline: #ced4da;
    --border: #dee2e6;
    --bar: #712cf9;       /* SG violet, validated on white */
    --you: #dc3545;       /* Bootstrap danger, validated on white */
    --violet: #712cf9;
    --violet-hover: #6528e0;
    --violet-rgb: 112,44,249;
    --accent-rgb: 255,228,132;
    --primary-rgb: 13,110,253;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      color-scheme: dark;
      --page: #212529;
      --page-rgb: 33,37,41;
      --surface: #2b3035;
      --ink: #dee2e6;
      --ink-2: #adb5bd;
      --muted: #868e96;
      --grid: #343a40;
      --baseline: #495057;
      --border: #495057;
      --bar: #8e5cfb;     /* violet stepped for dark, validated on #212529 */
      --you: #e35d6a;     /* danger stepped for dark, validated on #212529 */
    }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--page); color: var(--ink);
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", "Liberation Sans", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    display: flex; flex-direction: column; min-height: 100vh;
  }
  .navbar { padding: 12px 0; }
  .navbar .container { max-width: 960px; margin: 0 auto; padding: 0 16px; }
  .navbar a { color: var(--ink); text-decoration: none; font-size: 20px; font-weight: 500; }
  .masthead {
    padding: 40px 16px 48px; text-align: center;
    background-image:
      linear-gradient(180deg, rgba(var(--page-rgb), 0.01), rgba(var(--page-rgb), 1) 85%),
      radial-gradient(ellipse at top left, rgba(var(--primary-rgb), 0.5), transparent 50%),
      radial-gradient(ellipse at top right, rgba(var(--accent-rgb), 0.5), transparent 50%);
  }
  .masthead .inner { max-width: 720px; margin: 0 auto; }
  .masthead h1 { font-size: clamp(28px, 5vw, 44px); font-weight: 600; margin: 16px 0 12px; }
  .masthead .lead { font-size: 18px; color: var(--ink-2); margin: 0 0 20px; line-height: 1.5; }
  .btn-sg {
    display: inline-block; background: var(--violet); color: #fff;
    font-weight: 600; font-size: 17px; text-decoration: none;
    padding: 12px 28px; border-radius: .5rem; border: 1px solid var(--violet);
  }
  .btn-sg:hover { background: var(--violet-hover); border-color: var(--violet-hover); }
  .closenote { color: var(--muted); font-size: 14px; margin: 14px 0 0; }
  main { max-width: 720px; margin: 0 auto; padding: 8px 16px 48px; width: 100%; flex: 1; }
  h2.sectiontitle { font-size: 24px; margin: 8px 0 4px; }
  h2 { font-size: 17px; margin: 0 0 2px; }
  .sub { color: var(--ink-2); margin: 0 0 20px; font-size: 15px; }
  .modsub { color: var(--ink-2); margin: 0 0 12px; font-size: 14px; }
  .card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: .5rem; padding: 20px; margin-bottom: 16px;
  }
  .hero { font-size: 20px; line-height: 1.35; margin: 0; }
  .hero strong { font-size: 34px; display: block; margin-bottom: 2px; }
  .hero .pct { color: var(--you); }
  .meta { color: var(--ink-2); font-size: 14px; margin: 10px 0 0; }
  .peerline { font-size: 15px; color: var(--ink); margin: 12px 0 0; padding-top: 12px; border-top: 1px solid var(--grid); }
  .peerline .n { color: var(--muted); }
  #chartwrap { position: relative; }
  svg { display: block; width: 100%; height: auto; }
  .tooltip {
    position: absolute; pointer-events: none; display: none;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 6px 10px; font-size: 13px; color: var(--ink);
    box-shadow: 0 2px 8px rgba(0,0,0,.12); white-space: nowrap; z-index: 2;
  }
  .askrow { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 6px; }
  .askrow input {
    flex: 1 1 180px; font: inherit; padding: 10px 12px; border-radius: .5rem;
    border: 1px solid var(--baseline); background: var(--surface); color: var(--ink);
  }
  .askrow button {
    font: inherit; font-weight: 600; padding: 10px 18px; border-radius: .5rem;
    border: none; background: var(--violet); color: #fff; cursor: pointer;
  }
  .askrow button:hover { background: var(--violet-hover); }
  .privacy { color: var(--muted); font-size: 13px; margin: 8px 0 0; }
  details { margin-top: 12px; font-size: 14px; color: var(--ink-2); }
  details table { border-collapse: collapse; margin-top: 8px; font-variant-numeric: tabular-nums; }
  details th, details td { text-align: right; padding: 3px 12px 3px 0; border-bottom: 1px solid var(--grid); }
  details th { color: var(--muted); font-weight: 500; }
  .foot { color: var(--muted); font-size: 13px; line-height: 1.5; }
  .foot a { color: var(--violet); }
  .backrow { text-align: center; margin: 24px 0 8px; }
  .hidden { display: none; }
  .contextline { font-size: 14px; color: var(--ink-2); margin: 12px 0 0; padding-top: 12px; border-top: 1px solid var(--grid); }
  footer.sg {
    padding: 14px 0; text-align: center; color: #fff; font-size: 14px;
    background-image: linear-gradient(to bottom, rgba(var(--violet-rgb), 1), rgba(var(--violet-rgb), 0.95));
  }
  footer.sg a { color: #fff; font-weight: 600; }
</style>
</head>
<body>
<header class="navbar"><div class="container"><a href="__HOME_URL__">SG Tech Pulse</a></div></header>

<section class="masthead">
  <div class="inner">
    <h1>¡Gracias por participar! 🫶</h1>
    <p class="lead">Tu respuesta quedó registrada de forma anónima y ya forma parte del estudio de salarios,
    IA, diversidad y carreras tecnológicas en LATAM. Esto es lo que tu respuesta nos permite ver.</p>
  </div>
</section>

<main>
  <h2 class="sectiontitle">¿Dónde está tu sueldo?</h2>
  <p class="sub">Tu sueldo base mensual comparado con quienes ya respondieron la encuesta.</p>

  <div class="card" id="herocard">
    <p class="hero" id="hero">Cargando la distribución…</p>
    <p class="meta" id="herometa"></p>
    <p class="peerline hidden" id="levelline"></p>
    <p class="peerline hidden" id="expline"></p>
    <div class="askrow hidden" id="askrow">
      <input id="salaryinput" type="text" inputmode="numeric"
             placeholder="Tu sueldo base mensual en MXN, p. ej. 65000"
             aria-label="Tu sueldo base mensual en pesos mexicanos">
      <button id="askbtn">Ver mi posición</button>
    </div>
    <p class="privacy hidden" id="privacynote">El monto se compara aquí en tu navegador; no se envía a ningún servidor.</p>
  </div>

  <div class="card">
    <div id="chartwrap">
      <div class="tooltip" id="tooltip"></div>
      <svg id="chart" role="img" aria-label="Histograma de sueldos base mensuales en pesos mexicanos"></svg>
    </div>
    <p class="contextline" id="foreignline"></p>
    <details id="tabledetails">
      <summary>Ver los datos en tabla</summary>
      <table id="datatable"></table>
    </details>
  </div>

  <div class="card" id="englishcard">
    <h2>¿Cuánto vale tu inglés?</h2>
    <p class="modsub">Mediana de sueldo base según la frecuencia de uso del inglés en el trabajo.</p>
    <svg id="englishchart" role="img" aria-label="Mediana de sueldo por frecuencia de uso del inglés"></svg>
  </div>

  <div class="card" id="aicard">
    <h2>La ventana de la IA</h2>
    <p class="modsub" id="codingsub">Cómo se escribe código ahora, entre quienes programan.</p>
    <svg id="codingchart" role="img" aria-label="Formas de usar IA para crear código"></svg>
    <p class="modsub" style="margin-top:18px">«¿Qué tan seguro/a estás de que tus habilidades seguirán siendo relevantes dentro de 3 años?»</p>
    <svg id="confchart" role="img" aria-label="Distribución de confianza en la relevancia futura de habilidades"></svg>
    <p class="contextline hidden" id="confline"></p>
  </div>

  <p class="foot">
    Muestra autoseleccionada de la comunidad tech; resultados preliminares que cambian conforme llegan respuestas.
    Sueldos en dólares convertidos a MXN. Las medianas por grupo describen la muestra, no efectos causales.
    La encuesta sigue abierta<span id="sharespan"></span>.
  </p>

  <div class="backrow"><a class="btn-sg" href="__HOME_URL__">Volver a SG Tech Pulse</a>
    <p class="closenote">Puedes cerrar esta pestaña sin problema: no hay nada pendiente de guardar.</p>
  </div>
</main>

<footer class="sg">Este es un servicio más de <a href="https://sg.com.mx">SG Software Guru</a>, porque "we ♥ devs".</footer>
<script>
(async function () {
  const fmt = new Intl.NumberFormat("es-MX", { style: "currency", currency: "MXN", maximumFractionDigits: 0 });
  const fmtK = v => v >= 1000 ? "$" + Math.round(v / 1000) + "k" : "$" + v;
  const $ = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

  const surveyUrl = "__SURVEY_URL__";
  if (surveyUrl) $("sharespan").innerHTML =
    ' — <a href="' + esc(surveyUrl) + '">compártela con tu equipo</a>';

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
    $("hero").innerHTML =
      'Tu sueldo base está por encima del <strong><span class="pct">' + pct +
      '&hairsp;%</span></strong> de las ' + dist.n + " personas que han respondido.";
    $("herometa").textContent =
      "Tú: " + fmt.format(salary) + " al mes · mediana general: " + fmt.format(dist.median);
  }

  function showAskRow() {
    $("hero").textContent = "Escribe tu sueldo base mensual y te decimos dónde estás.";
    $("herometa").textContent =
      dist.n + " personas han respondido · mediana general: " + fmt.format(dist.median);
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
    const xx = xOfSalary(salary), yTop = M.top - 6, label = "Tú · " + fmt.format(salary);
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
    const persons = b.count === 1 ? "1 persona" : b.count + " personas";
    tip.textContent = (b.overflow ? "Más de " + fmt.format(b.lo) : fmt.format(b.lo) + " – " + fmt.format(b.hi)) + " · " + persons;
    const r = wrap.getBoundingClientRect();
    tip.style.display = "block";
    tip.style.left = Math.min(e.clientX - r.left + 12, r.width - tip.offsetWidth - 4) + "px";
    tip.style.top = (e.clientY - r.top - 34) + "px";
  });
  svg.addEventListener("mouseleave", () => { tip.style.display = "none"; });

  $("datatable").innerHTML =
    "<tr><th>Rango (MXN/mes)</th><th>Personas</th></tr>" +
    bins.map(b => "<tr><td>" + (b.overflow ? "Más de " + fmt.format(b.lo) : fmt.format(b.lo) + " – " + fmt.format(b.hi)) +
                  "</td><td>" + b.count + "</td></tr>").join("");

  // foreign-employer context line
  const fr = dist.foreign;
  if (fr.foreign.count >= 20 && fr.same.count >= 20) {
    $("foreignline").textContent =
      "Quienes trabajan para una empresa en el extranjero (" + fr.foreign.count + " personas): mediana " +
      fmt.format(fr.foreign.median) + " · empresa local (" + fr.same.count + "): " + fmt.format(fr.same.median) + ".";
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
               '<text x="' + (padL + 10) + '" y="' + (barY + 13) + '" font-size="12" font-weight="700" fill="#fff">Tú</text>';
      }
    });
    s.innerHTML = out;
  }

  // English ladder: median salary per usage band
  const engRows = dist.english.filter(e => e.count >= 20);
  hbars("englishchart", engRows.map(e => ({
    label: e.label, sub: "(" + e.count + ")",
    value: e.median, valueLabel: fmt.format(e.median),
    you: me.found && me.english_key === e.key,
  })), Math.max(...engRows.map(e => e.median)));

  // AI coding modes: share bars with median annotation
  const codRows = dist.ai_coding.filter(c => c.count >= 15);
  if (codRows.length) {
    hbars("codingchart", codRows.map(c => ({
      label: c.label, sub: "(" + c.count + ")",
      value: c.share, valueLabel: c.share + "% · mediana " + fmtK(c.median),
      you: me.found && me.ai_coding_key === c.key,
    })), Math.max(...codRows.map(c => c.share)));
  } else {
    $("codingchart").classList.add("hidden");
    $("codingsub").classList.add("hidden");
  }

  // Confidence distribution: 5 vertical bars, no salary attached
  (function () {
    const cc = dist.ai_confidence;
    const confLabels = ["Nada", "Poco", "Algo", "Bastante", "Mucho"];
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
        out += '<text x="' + cx + '" y="' + (by - 36) + '" text-anchor="middle" font-size="13" font-weight="600" fill="var(--ink)">Tú</text>' +
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
        ? "Compartes esta inquietud con " + worried + " de " + cc.n + " personas. No estás solo/a."
        : "Tu respuesta: " + confLabels[me.ai_confidence - 1].toLowerCase() + " · " + cc.n + " personas han respondido.";
    }
  })();

  // ---- wire up the hero ----------------------------------------------
  if (me.found && me.salary) {
    setHero(me.salary, me.percentile);
    drawYou(me.salary);
    if (me.level_percentile !== undefined) {
      $("levelline").classList.remove("hidden");
      $("levelline").innerHTML = "Entre nivel <b>" + esc(me.level) + "</b> estás por encima del <b>" +
        me.level_percentile + "%</b> <span class=\"n\">(" + me.level_n + " personas)</span>.";
    }
    if (me.exp_median !== undefined) {
      $("expline").classList.remove("hidden");
      $("expline").innerHTML = "Para tu experiencia (~" + me.exp_years + " años en tech), la mediana es <b>" +
        fmt.format(me.exp_median) + "</b> <span class=\"n\">(" + me.exp_n + " personas con ±2 años)</span>.";
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
  }
})();
</script>
</body>
</html>
"""

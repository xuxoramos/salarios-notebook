"""Compute every figure for the findings scrollytelling site + report.

Numbers are COMPUTED FROM THE CURRENT DUMP at runtime (Mexico residents only),
so the site and the report never go stale. Re-run after any dump refresh.
Matches docs/GENDER_FINDINGS_2026.md (Mexico) and the media-stories universe
(Mexico residents). Do not hardcode findings here or in the HTML.

Writes:
  data.js   -> window.SG_DATA = {...}   (consumed by index.html and report.html)
  prints a human-readable summary to stdout for eyeballing.
"""
import os, glob, json, unicodedata
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

np.random.seed(2026)
HERE = os.path.dirname(os.path.abspath(__file__))
FX = 18.5


def find_dump():
    cands = sorted(glob.glob(os.path.join(HERE, "..", "..", "data", "Responses*Encuesta*Salarios*.csv")))
    if not cands:
        raise SystemExit("dump not found under data/")
    return cands[-1]


DUMP = find_dump()
df = pd.read_csv(DUMP)
c = list(df.columns)

def S(i):
    # Force all missing (NaN / pd.NA under the string dtype) to the literal
    # "nan" so every `== "nan"` / `!= "nan"` guard works regardless of dtype.
    col = df[c[i]]
    return col.astype(str).str.strip().mask(col.isna(), "nan")

def num(i):
    return pd.to_numeric(S(i).str.replace(",", "").str.replace("$", ""), errors="coerce")

norm = num(23).fillna(num(24) * FX).where(lambda s: (s >= 8000) & (s <= 400000))
mx = (S(4) == "México")
g = S(3)
W = (g == "Femenino") & mx
M = (g == "Masculino") & mx
lvl = S(22)


def med(mask):
    v = norm[mask].dropna()
    return (int(np.median(v)) if len(v) else None, int(len(v)))


def strip_accents(s):
    s = str(s)
    return "".join(ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch)).lower().strip()


def by_cat(col_idx, mapping=None, min_n=6, mask=None, order=None):
    """Median MXN by category value. mapping: raw->label. Returns list of {label,median,n}."""
    base = mx if mask is None else mask
    vals = S(col_idx)
    out = {}
    for raw in vals[base].unique():
        if raw == "nan":
            continue
        label = raw if mapping is None else mapping.get(raw, raw)
        sub = base & (vals == raw)
        m, n = med(sub)
        if m is None or n < min_n:
            continue
        if label in out:
            # merge (rare: two raws map to same label) -> recompute jointly below
            out[label]["_raws"].append(raw)
        else:
            out[label] = {"label": label, "median": m, "n": n, "_raws": [raw]}
    # recompute merged labels jointly
    res = []
    for label, d in out.items():
        if len(d["_raws"]) > 1:
            sub = base & vals.isin(d["_raws"])
            m, n = med(sub)
            d["median"], d["n"] = m, n
        d.pop("_raws")
        res.append(d)
    if order:
        res.sort(key=lambda r: order.index(r["label"]) if r["label"] in order else 999)
    else:
        res.sort(key=lambda r: -r["median"])
    return res


data = {}

# ── meta ────────────────────────────────────────────────────────────
# Human-readable dump date, parsed from the filename ("... - 12 October 2026.csv")
# so every page can bind it and it never has to be hardcoded in the HTML.
_MESES = {"january":"enero","february":"febrero","march":"marzo","april":"abril",
          "may":"mayo","june":"junio","july":"julio","august":"agosto",
          "september":"septiembre","october":"octubre","november":"noviembre","december":"diciembre"}
import re as _re
_m = _re.search(r"-\s*(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\.csv$", os.path.basename(DUMP))
if _m:
    _date_es = _m.group(1) + " de " + _MESES.get(_m.group(2).lower(), _m.group(2).lower()) + " de " + _m.group(3)
else:
    _date_es = ""

data["meta"] = {
    "dump": os.path.basename(DUMP),
    "date_es": _date_es,
    "total_n": int(len(df)),
    "mx_n": int(mx.sum()),
    "sal_n": int((mx & norm.notna()).sum()),
    "women": int(W.sum()),
    "men": int(M.sum()),
    "women_sal": int((W & norm.notna()).sum()),
    "men_sal": int((M & norm.notna()).sum()),
    "fx": FX,
}
m_all, n_all = med(mx)
data["overall"] = {"median": m_all, "n": n_all}

# ── ACT 1: levers ───────────────────────────────────────────────────
levers = {}

# English use (col 53)
eng_order = ["Nunca", "Ocasionalmente (leer documentación y mensajes)",
             "Con regularidad (juntas y redactar emails)", "La mayoría del tiempo", "Todo el tiempo"]
eng_label = {"Nunca": "Nunca", "Ocasionalmente (leer documentación y mensajes)": "Ocasional",
             "Con regularidad (juntas y redactar emails)": "Con regularidad",
             "La mayoría del tiempo": "La mayoría", "Todo el tiempo": "Todo el tiempo"}
levers["english"] = by_cat(53, eng_label, min_n=6, order=["Nunca", "Ocasional", "Con regularidad", "La mayoría", "Todo el tiempo"])

# Foreign employer (col 10: No = foreign)
fore = (S(10) == "No")
local = (S(10) == "Yes")
fm, fn = med(mx & fore)
lm, ln = med(mx & local)
levers["foreign"] = {
    "foreign_median": fm, "foreign_n": fn, "local_median": lm, "local_n": ln,
    "premium_pct": round(100 * (fm / lm - 1)) if (fm and lm) else None,
    "share_pct": round(100 * (mx & fore).sum() / (mx & (fore | local)).sum()),
}

# Role premiums (col 31), n>=6
levers["role"] = by_cat(31, min_n=6)

# Stack / language (col 41), n>=6
levers["stack"] = by_cat(41, min_n=6)

# Cloud (col 42), n>=6
levers["cloud"] = by_cat(42, min_n=6)

# City (col 5) canonicalized
city_map = {}
for raw in S(5)[mx].unique():
    if raw == "nan":
        continue
    a = strip_accents(raw)
    if any(k in a for k in ["ciudad de mexico", "cdmx", "mexico city", "distrito federal"]) or a in ("df", "mexico"):
        city_map[raw] = "CDMX"
    elif "guadalajara" in a or "zapopan" in a or "tlaquepaque" in a or a == "gdl":
        city_map[raw] = "Guadalajara"
    elif "monterrey" in a or "san pedro" in a or a == "mty" or "garcia" in a:
        city_map[raw] = "Monterrey"
    elif "aguascalientes" in a:
        city_map[raw] = "Aguascalientes"
    elif "queretaro" in a:
        city_map[raw] = "Querétaro"
    elif "puebla" in a:
        city_map[raw] = "Puebla"
    elif "merida" in a:
        city_map[raw] = "Mérida"
    elif "san luis" in a:
        city_map[raw] = "San Luis Potosí"
    elif "tijuana" in a:
        city_map[raw] = "Tijuana"
    elif "leon" in a:
        city_map[raw] = "León"
    else:
        city_map[raw] = None  # drop long tail
cities = {}
cvals = S(5)
for raw, label in city_map.items():
    if not label:
        continue
    cities.setdefault(label, []).append(raw)
city_rows = []
for label, raws in cities.items():
    sub = mx & cvals.isin(raws)
    m, n = med(sub)
    if m and n >= 10:
        city_rows.append({"label": label, "median": m, "n": n})
city_rows.sort(key=lambda r: -r["median"])
levers["city"] = city_rows

# Modality (col 14): remote vs onsite
rvals = S(14)
remote = rvals.str.startswith("Totalmente remoto")
onsite = rvals.str.startswith("Totalmente presencial")
rm, rn = med(mx & remote)
om, on = med(mx & onsite)
levers["modality"] = {"remote_median": rm, "remote_n": rn, "onsite_median": om, "onsite_n": on,
                      "modalities": by_cat(14, min_n=10)}

# Equity (col 27): Yes vs No
eq = S(27)
em, en = med(mx & (eq == "Yes"))
nem, nen = med(mx & (eq == "No"))
levers["equity"] = {"with_median": em, "with_n": en, "without_median": nem, "without_n": nen,
                    "share_pct": round(100 * (mx & (eq == "Yes")).sum() / (mx & eq.isin(["Yes", "No"])).sum())}

# Education / learning path (col 7)
levers["learning"] = by_cat(7, min_n=6)

# Highest degree (col 6)
levers["degree"] = by_cat(6, min_n=6)

# Certifications (cols 44-50): any active cert vs none
cert_cols = range(44, 51)
has_cert = pd.Series(False, index=df.index)
for i in cert_cols:
    col = S(i)
    has_cert = has_cert | ((col != "nan") & (col != "") & (col.str.len() > 0))
cm, cn = med(mx & has_cert)
ncm, ncn = med(mx & ~has_cert)
levers["certs"] = {"with_median": cm, "with_n": cn, "without_median": ncm, "without_n": ncn,
                   "pct_delta": round(100 * (cm / ncm - 1)) if (cm and ncm) else None}

# Company size (col 20)
size_order = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5000+", "Más de 5000"]
levers["company_size"] = by_cat(20, min_n=6)

# Experience brackets (col 9, tech years)
texp = num(9)
exp_rows = []
for lo, hi, lab in [(0, 2, "0-2"), (3, 5, "3-5"), (6, 10, "6-10"), (11, 20, "11-20"), (21, 99, "20+")]:
    sub = mx & (texp >= lo) & (texp <= hi)
    m, n = med(sub)
    if m:
        exp_rows.append({"label": lab, "median": m, "n": n})
levers["experience"] = exp_rows

data["levers"] = levers

# ── ACT 2: gender ───────────────────────────────────────────────────
gender = {}
rm_, rmn = med(M)
rw_, rwn = med(W)
raw_gap = round(100 * (1 - rw_ / rm_))
wv = norm[W].dropna().values
mv = norm[M].dropna().values
boot = [1 - np.median(np.random.choice(wv, len(wv))) / np.median(np.random.choice(mv, len(mv))) for _ in range(3000)]
gender["raw"] = {"men_median": rm_, "women_median": rw_, "gap_pct": raw_gap,
                 "ci_low": round(100 * np.percentile(boot, 2.5)), "ci_high": round(100 * np.percentile(boot, 97.5)),
                 "women_n": rwn, "men_n": rmn}

# by tier
tier_rows = []
for t in ["Medio", "Senior", "Gerente"]:
    a, an = med(M & (lvl == t))
    b, bn = med(W & (lvl == t))
    if a and b:
        tier_rows.append({"tier": t, "men_median": a, "women_median": b, "gap_pct": round(100 * (1 - b / a)),
                          "men_n": an, "women_n": bn})
gender["by_tier"] = tier_rows
# Jr/Mid vs Sr+
jm = lvl.isin(["Junior", "Medio"])
sap = lvl.isin(["Senior", "Staff-Principal", "Gerente", "Director", "C-Level", "Fundador"])
band = []
for lab, msk in [("Junior / Medio", jm), ("Senior+", sap)]:
    a, an = med(M & msk)
    b, bn = med(W & msk)
    band.append({"label": lab, "men_median": a, "women_median": b, "gap_pct": round(100 * (1 - b / a)),
                 "men_n": an, "women_n": bn})
gender["band"] = band

# vanishing
van = []
for t in ["Junior", "Medio", "Senior", "Staff-Principal", "Gerente", "Director"]:
    nf = int((W & (lvl == t)).sum())
    nm = int((M & (lvl == t)).sum())
    if nf + nm >= 8:
        van.append({"tier": t, "women_share": round(100 * nf / (nf + nm)), "n": nf + nm})
nf = int((W & sap).sum()); nm = int((M & sap).sum())
gender["vanishing"] = van
gender["senior_plus_share"] = round(100 * nf / (nf + nm))
gender["participation"] = round(100 * int(W.sum()) / (int(W.sum()) + int(M.sum())))

# Oaxaca-Blinder
d = df[(g.isin(["Femenino", "Masculino"])) & mx & norm.notna()].copy()
d["_e"] = num(9).reindex(d.index)
d = d[d._e.notna()]
gg = S(3).reindex(d.index)
fem = (gg == "Femenino").values
yl = np.log(norm.reindex(d.index).values)
Xo = pd.DataFrame({"exp": d._e.values})
for i, nm_ in [(22, "l"), (53, "e"), (31, "r")]:
    du = pd.get_dummies(S(i).reindex(d.index), prefix=nm_).astype(float)
    Xo = pd.concat([Xo.reset_index(drop=True), du.reset_index(drop=True)], axis=1)
Xo = Xo.astype(float)
tot = yl[~fem].mean() - yl[fem].mean()
beta = LinearRegression().fit(Xo, yl).coef_
expl = (Xo[~fem].mean().values - Xo[fem].mean().values) @ beta
Xf = Xo.copy(); Xf.insert(0, "f", fem.astype(float))
adj = LinearRegression().fit(Xf.astype(float), yl).coef_[0]
resid = 1 - np.exp(adj)
sr_w, _ = med(W & (lvl == "Senior"))
pen_mo = sr_w * resid / (1 - resid)
gender["oaxaca"] = {"explained_pct": round(100 * expl / tot), "unexplained_pct": round(100 * (1 - expl / tot)),
                    "residual_pct": round(100 * resid), "log_gap": round(tot, 2),
                    "senior_woman_median": sr_w, "penalty_mo": int(round(pen_mo, -2)),
                    "penalty_yr": int(round(pen_mo * 12, -3))}

# foreign gap
a, an = med(M & fore)
b, bn = med(W & fore)
accM = round(100 * (fore & M).sum() / M.sum())
accW = round(100 * (fore & W).sum() / W.sum())
gender["foreign_gap"] = {"men_median": a, "women_median": b, "gap_pct": round(100 * (1 - b / a)),
                         "women_n": bn, "men_n": an, "access_m": accM, "access_w": accW}

# pause. Denominator = the full gender group (not only those who answered col 69),
# matching docs/GENDER_FINDINGS_2026.md (16% women / 7% men, "over the total sample").
# The 2.3x ratio is identical either way.
def pause_rate(mask):
    yes = int((S(69)[mask] == "Yes").sum())
    n = int(mask.sum())
    return round(100 * yes / n), n
pw_, pwn = pause_rate(W)
pm_, pmn = pause_rate(M)
gender["pause"] = {"women_pct": pw_, "men_pct": pm_, "women_n": pwn, "men_n": pmn,
                   "ratio": round(pw_ / pm_, 1) if pm_ else None}

# lived experience
h = S(72)[W]
hb = h[h.isin(["No", "Rara vez, pero sí", "Sí, frecuentemente"])]
unsafe = int(((hb == "Rara vez, pero sí") | (hb == "Sí, frecuentemente")).sum())
freq = int((hb == "Sí, frecuentemente").sum())
lp = S(74)[W]; lpa = lp[lp.isin(["Yes", "No"])]
pw_peers = num(70)[W].dropna()
gender["lived"] = {
    "harassment_pct": round(100 * unsafe / len(hb)), "harassment_freq_n": freq, "harassment_n": int(len(hb)),
    "noprogram_pct": round(100 * (lpa == "No").mean()), "noprogram_n": int(len(lpa)),
    "isolation_pct": round(100 * (pw_peers <= 20).mean()), "isolation_median": int(pw_peers.median()),
    "isolation_n": int(len(pw_peers)),
}

# origin (closed)
fp = num(63); comp = S(62)
gender["origin"] = {"first_program_w": int(fp[W].median()), "first_program_m": int(fp[M].median()),
                    "computer_w": round(100 * (comp[W] == "Yes").mean()), "computer_m": round(100 * (comp[M] == "Yes").mean())}
# access parity
def acc(mask_val, col, val):
    x = S(col); return round(100 * (mask_val & (x == val)).sum() / mask_val.sum())
gender["access"] = {
    "equity_m": acc(M, 27, "Yes"), "equity_w": acc(W, 27, "Yes"),
    "foreign_m": accM, "foreign_w": accW,
    "remote_m": acc(M, 14, "Totalmente remoto"), "remote_w": acc(W, 14, "Totalmente remoto"),
    "airole_m": int(S(61)[M].ne("nan").sum()), "airole_w": int(S(61)[W].ne("nan").sum()),
}
data["gender"] = gender

# ── ACT 3: AI ───────────────────────────────────────────────────────
ai = {}
aivals = S(59)
def ai_cat(x):
    x = str(x)
    if x.startswith("Aunque sé programar"):
        return "agentic"
    if x.startswith("Programo manualmente y uso IA como soporte"):
        return "support"
    if x.startswith("Programo la funcionalidad manualmente"):
        return "complementary"
    return None
prog = aivals[mx]
prog = prog[prog != "nan"]
cats = prog.map(ai_cat).dropna()
total_ai = len(cats)
ai["coding_split"] = {
    "agentic_pct": round(100 * (cats == "agentic").mean()),
    "support_pct": round(100 * (cats == "support").mean()),
    "complementary_pct": round(100 * (cats == "complementary").mean()),
    "agentic_n": int((cats == "agentic").sum()), "n": int(total_ai),
}
# agentic pay
agent = aivals.str.startswith("Aunque sé programar")
answered = mx & (aivals != "nan")
am_, _ = med(answered & agent)
rm2, _ = med(answered & ~agent)
ai["agentic_pay"] = {"agent_median": am_, "rest_median": rm2, "pct": round(100 * (am_ / rm2 - 1))}
# adoption by gender (devs)
dev = S(31).str.startswith("Desarrollo de software")
def adopt(mask):
    ans = mask & dev & mx & (aivals != "nan")
    return (round(100 * (agent & ans).sum() / ans.sum()) if ans.sum() else None), int(ans.sum())
aw_, awn = adopt(W); am2, amn = adopt(M)
ai["adoption_by_gender"] = {"women_pct": aw_, "women_n": awn, "men_pct": am2, "men_n": amn}
# adoption by experience
adopt_exp = []
for lo, hi, lab in [(0, 3, "0-3"), (4, 6, "4-6"), (7, 10, "7-10"), (11, 15, "11-15"), (16, 99, "16+")]:
    ans = mx & (texp >= lo) & (texp <= hi) & (aivals != "nan")
    if ans.sum() >= 8:
        adopt_exp.append({"bracket": lab, "pct": round(100 * (agent & ans).sum() / ans.sum()), "n": int(ans.sum())})
ai["adoption_by_exp"] = adopt_exp
# roles
airole = S(61)
ai["roles"] = {"count": int((mx & (airole != "nan")).sum()),
               "men": int(S(61)[M].ne("nan").sum()), "women": int(S(61)[W].ne("nan").sum()),
               "top": {k: int(v) for k, v in airole[mx & (airole != "nan")].value_counts().head(4).items()}}
# confidence
conf = num(60)
ai["confidence"] = {"mean": round(float(conf[mx].mean()), 1), "worried_pct": round(100 * (conf[mx] <= 2).mean()),
                    "n": int(conf[mx].notna().sum())}
data["ai"] = ai

# ── ACT 4: human ledger ─────────────────────────────────────────────
human = {}
sav = num(38)
sav = sav.where(~((sav > 0) & (sav <= 1)), sav * 100)
sav = sav.where((sav >= 0) & (sav <= 100))
savmx = sav[mx].dropna()
ss = S(36)
human["finances"] = {
    "no_savings_pct": round(100 * (savmx == 0).mean()), "savings_median": int(savmx.median()),
    "save10plus_pct": round(100 * (savmx >= 10).mean()),
    "no_retirement_pct": round(100 * (S(39)[mx] == "No").mean()),
    "no_ss_pct": round(100 * ss[mx].str.startswith("No").mean()),
    "edu_debt_pct": round(100 * (S(40)[mx] == "Yes").mean()),
    "second_job_pct": round(100 * (S(33)[mx] == "Yes").mean()),
    "n": int(len(savmx)),
}
vac = num(30)[mx].dropna()
human["vacations"] = {"median": int(vac.median()), "le12_pct": round(100 * (vac <= 12).mean()), "n": int(len(vac))}
# neurodivergence + support
nd = S(66); ndmx = nd[mx & nd.isin(["Yes", "No"])]
nd_yes = mx & (nd == "Yes")
sup = S(67)[nd_yes]; supa = sup[sup != "nan"]
no_support = supa[supa == "No"]
human["neurodiv"] = {"pct": round(100 * (ndmx == "Yes").mean()), "n": int((nd_yes).sum()),
                     "no_support_pct": round(100 * len(no_support) / len(supa)) if len(supa) else None,
                     "no_support_n": int(len(no_support)), "support_answered": int(len(supa))}
# disability + support
dis = S(64); dismx = dis[mx & dis.isin(["Yes", "No"])]
human["disability"] = {"pct": round(100 * (dismx == "Yes").mean()), "n": int((mx & (dis == "Yes")).sum())}
data["human"] = human

# ── Tier-1 rigor: uncertainty + gender sensitivity ──────────────────
# Bootstrap CIs on the headline estimates (self-selected sample, so these are
# sampling-uncertainty bands, not population guarantees), and a control-set
# sensitivity ladder + FX robustness + bootstrap CI for the adjusted gender gap.
def _rint(x):
    return int(round(x))

def median_ci(vec, n=2000):
    vec = np.asarray(vec, float); L = len(vec)
    if L == 0:
        return None
    meds = [np.median(vec[np.random.randint(0, L, L)]) for _ in range(n)]
    return [_rint(np.percentile(meds, 2.5)), _rint(np.percentile(meds, 97.5))]

def ratio_samples(a, b, n=2000):
    a = np.asarray(a, float); b = np.asarray(b, float); la = len(a); lb = len(b)
    return np.array([np.median(a[np.random.randint(0, la, la)]) / np.median(b[np.random.randint(0, lb, lb)]) for _ in range(n)])

def premium_ci(a, b, n=2000):  # % premium of a over b
    r = ratio_samples(a, b, n)
    return [_rint(100 * (np.percentile(r, 2.5) - 1)), _rint(100 * (np.percentile(r, 97.5) - 1))]

def mult_ci(a, b, n=2000):  # multiplier of a over b
    r = ratio_samples(a, b, n)
    return [round(float(np.percentile(r, 2.5)), 1), round(float(np.percentile(r, 97.5)), 1)]

# headline CIs
data["overall"]["median_ci"] = median_ci(norm[mx].dropna().values)
_eng_todo = norm[mx & (S(53) == "Todo el tiempo")].dropna().values
_eng_nunca = norm[mx & (S(53) == "Nunca")].dropna().values
levers["english_mult"] = {"mult": round(float(np.median(_eng_todo) / np.median(_eng_nunca)), 1),
                          "ci": mult_ci(_eng_todo, _eng_nunca)}
levers["foreign"]["premium_ci"] = premium_ci(norm[mx & fore].dropna().values, norm[mx & local].dropna().values)
ai["agentic_pay"]["ci"] = premium_ci(norm[answered & agent].dropna().values, norm[answered & ~agent].dropna().values)

# gender: control-set ladder, FX robustness, bootstrap CI on the adjusted gap
def _gender_design(fx, blocks):
    nf = num(23).fillna(num(24) * fx).where(lambda s: (s >= 8000) & (s <= 400000))
    dd = df[(g.isin(["Femenino", "Masculino"])) & mx & nf.notna()].copy()
    ee = num(9).reindex(dd.index)
    dd = dd[ee.notna()]; ee = ee[ee.notna()]
    femv = (S(3).reindex(dd.index) == "Femenino").values
    yv = np.log(nf.reindex(dd.index).values)
    X = pd.DataFrame({"female": femv.astype(float)})
    if "exp" in blocks:
        X["exp"] = ee.values
    for key, ci in [("eng", 53), ("lvl", 22), ("role", 31)]:
        if key in blocks:
            du = pd.get_dummies(S(ci).reindex(dd.index), prefix=key).astype(float)
            X = pd.concat([X.reset_index(drop=True), du.reset_index(drop=True)], axis=1)
    return X.astype(float).values, yv

def _penalty(fx, blocks):
    X, yv = _gender_design(fx, blocks)
    coef = LinearRegression().fit(X, yv).coef_[0]
    return _rint(100 * (1 - np.exp(coef)))

_LADDER = [("Sin ajuste", []), ("+ experiencia", ["exp"]), ("+ inglés", ["exp", "eng"]),
           ("+ nivel", ["exp", "eng", "lvl"]), ("+ rol", ["exp", "eng", "lvl", "role"])]
_sensitivity = [{"spec": lab, "penalty": _penalty(FX, bl)} for lab, bl in _LADDER]
_fx_rob = [{"fx": fx, "penalty": _penalty(fx, ["exp", "eng", "lvl", "role"])} for fx in [17, 18.5, 20]]

_Xf, _yf = _gender_design(FX, ["exp", "eng", "lvl", "role"])
_idx = np.arange(len(_yf)); _pens = []
for _ in range(1000):
    _s = np.random.randint(0, len(_idx), len(_idx))
    _c = LinearRegression().fit(_Xf[_s], _yf[_s]).coef_[0]
    _pens.append(100 * (1 - np.exp(_c)))
gender["rigor"] = {
    "sensitivity": _sensitivity,
    "fx": _fx_rob,
    "adjusted_ci": [_rint(np.percentile(_pens, 2.5)), _rint(np.percentile(_pens, 97.5))],
    "bounds_lower": _sensitivity[-1]["penalty"],
    "bounds_upper": gender["raw"]["gap_pct"],
}

# ── write ───────────────────────────────────────────────────────────
js = "// AUTO-GENERATED by build_data.py from the current dump. Do not edit by hand.\n"
js += "window.SG_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open(os.path.join(HERE, "data.js"), "w") as f:
    f.write(js)
with open(os.path.join(HERE, "data.json"), "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("dump:", os.path.basename(DUMP))
print(json.dumps(data, ensure_ascii=False, indent=2))
print("\nwrote data.js + data.json ->", HERE)

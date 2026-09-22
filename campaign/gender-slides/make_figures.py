"""Generate gender-gap slide figures (SG Tech Pulse 2026).

Numbers are COMPUTED FROM THE CURRENT DUMP at runtime (Mexico residents only),
so the figures never go stale: re-run this after any dump refresh and the PNGs
follow the data. Do not hardcode findings here. Matches docs/GENDER_FINDINGS_2026.md.
Outputs PNGs to figures/.
"""
import os, glob
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "figures")
os.makedirs(OUT, exist_ok=True)

# ── data ────────────────────────────────────────────────────────────
def find_dump():
    cands = sorted(glob.glob(os.path.join(HERE, "..", "..", "data", "Responses*Encuesta*Salarios*.csv")))
    if not cands:
        raise SystemExit("dump not found under data/")
    return cands[-1]

df = pd.read_csv(find_dump())
c = list(df.columns)
def S(i): return df[c[i]].astype(str).str.strip()
def num(i): return pd.to_numeric(S(i).str.replace(",", "").str.replace("$", ""), errors="coerce")

mx = (S(4) == "México")
sal = num(23); usd = num(24)
norm = sal.fillna(usd * 18.5).where(lambda s: (s >= 8000) & (s <= 400000))
g = S(3); W = (g == "Femenino") & mx; M = (g == "Masculino") & mx
lvl = S(22)

def med(mask):
    v = norm[mask].dropna()
    return float(np.median(v)) if len(v) else np.nan
def gap(mask_m, mask_w):
    mm, mw = med(mask_m), med(mask_w)
    return mm, mw, (1 - mw / mm)
def share_w(mask):
    nf = (W & mask).sum(); nm = (M & mask).sum()
    return 100 * nf / (nf + nm) if (nf + nm) else np.nan
def gpct(v): return f"−{round(100*v)}%"

# ── Oaxaca-Blinder (pooled reference) → explained / unexplained ──────
def oaxaca():
    d = df[(g.isin(["Femenino", "Masculino"])) & mx & norm.notna()].copy()
    d["_exp"] = num(9).reindex(d.index)
    d = d[d._exp.notna()]
    gg = S(3).reindex(d.index); fem = (gg == "Femenino").values
    y = np.log(norm.reindex(d.index).values)
    X = pd.DataFrame({"exp": d._exp.values})
    for i, nm in [(22, "lvl"), (53, "eng"), (31, "role")]:
        du = pd.get_dummies(S(i).reindex(d.index), prefix=nm).astype(float)
        X = pd.concat([X.reset_index(drop=True), du.reset_index(drop=True)], axis=1)
    X = X.astype(float)
    total = y[~fem].mean() - y[fem].mean()
    beta = LinearRegression().fit(X, y).coef_
    explained = (X[~fem].mean().values - X[fem].mean().values) @ beta
    unexplained = total - explained
    Xf = X.copy(); Xf.insert(0, "female", fem.astype(float))
    adj = LinearRegression().fit(Xf.astype(float), y).coef_[0]  # log points
    return dict(total=total, exp_share=explained/total, unexp_share=unexplained/total,
                resid=1 - np.exp(adj))
OX = oaxaca()

MEN = "#94a3b8"; WOMEN = "#e11d48"; INK = "#0f172a"; MUTED = "#64748b"; GRID = "#e2e8f0"
plt.rcParams.update({
    "figure.dpi": 160, "savefig.dpi": 160, "savefig.bbox": "tight",
    "figure.facecolor": "white", "axes.facecolor": "white",
    "font.size": 15, "axes.edgecolor": GRID, "axes.linewidth": 1,
    "axes.grid": True, "grid.color": GRID, "axes.axisbelow": True,
    "xtick.color": INK, "ytick.color": MUTED, "text.color": INK,
})
def peso(ax): ax.yaxis.set_major_formatter(lambda x, _: f"${x/1000:.0f}k")
def save(fig, name):
    fig.savefig(os.path.join(OUT, name)); plt.close(fig); print("wrote", name)

# ── Fig 1: the compounding cost (3 stages) ──────────────────────────
jm = lvl.isin(["Junior", "Medio"])
stages_def = [("Junior / Medio", jm), ("Senior", lvl == "Senior"), ("Gerente", lvl == "Gerente")]
men = [med(M & msk) for _, msk in stages_def]
women = [med(W & msk) for _, msk in stages_def]
gaps = [gpct(1 - w / m) for m, w in zip(men, women)]
stages = [s for s, _ in stages_def]
fig, ax = plt.subplots(figsize=(9.5, 5.4)); x = range(len(stages)); w = 0.36
ax.bar([i-w/2 for i in x], men, w, label="Hombres", color=MEN)
ax.bar([i+w/2 for i in x], women, w, label="Mujeres", color=WOMEN)
for i, (m, f, gg) in enumerate(zip(men, women, gaps)):
    ax.text(i-w/2, m+1800, f"${m/1000:.0f}k", ha="center", fontsize=12, color=INK)
    ax.text(i+w/2, f+1800, f"${f/1000:.0f}k", ha="center", fontsize=12, color=WOMEN, fontweight="bold")
    ax.annotate(gg, (i, max(m, f)+9000), ha="center", color=WOMEN, fontsize=17, fontweight="bold")
ax.set_xticks(list(x)); ax.set_xticklabels(stages); peso(ax)
ax.set_title("El costo se acumula: la brecha crece con cada nivel", fontsize=17, fontweight="bold", loc="left", pad=12)
ax.set_ylabel("Salario base mensual (mediana)"); ax.legend(frameon=False, loc="upper left")
ax.set_ylim(0, max(men)*1.25); ax.spines[["top", "right"]].set_visible(False)
save(fig, "fig1_toll.png")

# ── Fig 2: scissors by tier ─────────────────────────────────────────
tiers = ["Medio", "Senior", "Gerente"]
men = [med(M & (lvl == t)) for t in tiers]; women = [med(W & (lvl == t)) for t in tiers]
fig, ax = plt.subplots(figsize=(9.5, 5.4))
ax.plot(tiers, men, "-o", color=MEN, lw=3, ms=9, label="Hombres")
ax.plot(tiers, women, "-o", color=WOMEN, lw=3, ms=9, label="Mujeres")
for t, m, f in zip(tiers, men, women):
    ax.annotate(gpct(1-f/m), (t, (m+f)/2), ha="center", va="center", color=WOMEN, fontsize=13, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=WOMEN, lw=1))
ax.fill_between(tiers, men, women, color=WOMEN, alpha=0.08); peso(ax)
ax.set_ylabel("Salario base mensual (mediana)")
ax.set_title("Cada ascenso encarece ser mujer", fontsize=18, fontweight="bold", loc="left", pad=12)
ax.legend(frameon=False, loc="upper left"); ax.set_ylim(min(women)*0.8, max(men)*1.1)
ax.spines[["top", "right"]].set_visible(False)
save(fig, "fig2_scissors.png")

# ── Fig 3: the vanishing (female share by tier) ─────────────────────
tiers = ["Junior", "Medio", "Senior", "Staff-Principal", "Gerente", "Director"]
share = [round(share_w(lvl == t)) for t in tiers]
overall = round(share_w(lvl != "__none__"))
fig, ax = plt.subplots(figsize=(9.5, 5.4))
bars = ax.bar(tiers, share, color=[WOMEN if s >= 50 else MEN for s in share])
ax.axhline(50, color=MUTED, ls="--", lw=1); ax.text(5.4, 51, "paridad 50%", color=MUTED, fontsize=11, ha="right")
for b, s in zip(bars, share): ax.text(b.get_x()+b.get_width()/2, s+1.5, f"{s}%", ha="center", fontsize=12, color=INK)
ax.set_ylabel("% de mujeres en el nivel"); ax.set_ylim(0, max(share)+12)
ax.set_title("La desaparición: mayoría en medio, ~1 de 3 arriba", fontsize=18, fontweight="bold", loc="left", pad=12)
ax.tick_params(axis="x", labelrotation=20); ax.spines[["top", "right"]].set_visible(False)
save(fig, "fig3_vanishing.png")

# ── Fig 4: Oaxaca explained vs unexplained ──────────────────────────
exp_pct = round(100*OX["exp_share"]); unexp_pct = 100-exp_pct
sr_woman = med(W & (lvl == "Senior")); resid = OX["resid"]
pen_mo = sr_woman*resid/(1-resid); pen_yr = pen_mo*12
fig, ax = plt.subplots(figsize=(9.5, 3.4))
ax.barh([0], [exp_pct], color="#cbd5e1", label="Explicado por composición")
ax.barh([0], [unexp_pct], left=[exp_pct], color=WOMEN, label="Castigo no explicado")
ax.text(exp_pct/2, 0, f"{exp_pct}%\nexplicado", ha="center", va="center", color=INK, fontsize=14, fontweight="bold")
ax.text(exp_pct+unexp_pct/2, 0, f"{unexp_pct}%\nsin explicación", ha="center", va="center", color="white", fontsize=13, fontweight="bold")
ax.set_xlim(0, 100); ax.set_yticks([]); ax.grid(False); ax.set_xlabel("Proporción de la brecha cruda (%)", labelpad=8)
ax.set_title("La mayor parte es composición; un residuo no lo explica nada", fontsize=16, fontweight="bold", loc="left", pad=10)
ax.spines[["top", "right", "left"]].set_visible(False)
fig.text(0.5, -0.16, rf"$\approx$ \${pen_mo/1000:.1f}k al mes  ·  ~\${pen_yr/1000:.0f}k al año  que una mujer senior pierde sin explicación",
         ha="center", color=WOMEN, fontsize=14, fontweight="bold")
save(fig, "fig4_oaxaca.png")

# ── Fig 4b: peel-away waterfall (same-résumé intuition) ─────────────
raw_m, raw_w = med(M), med(W)
fig, ax = plt.subplots(figsize=(9.5, 5.2)); EXPLAINED = "#cbd5e1"
ax.bar(0, 100, 0.62, color=MEN)
ax.bar(1, exp_pct, 0.62, bottom=unexp_pct, color=EXPLAINED)
ax.bar(2, unexp_pct, 0.62, color=WOMEN)
ax.plot([0.31, 1.31], [100, 100], ls="--", lw=1.4, color=MUTED)
ax.plot([1.31, 1.69], [unexp_pct, unexp_pct], ls="--", lw=1.4, color=MUTED)
ax.text(0, 104, "100%", ha="center", va="bottom", color=INK, fontsize=14, fontweight="bold")
ax.text(1, unexp_pct+exp_pct/2, f"−{exp_pct}%", ha="center", va="center", color=INK, fontsize=15, fontweight="bold")
ax.text(2, unexp_pct/2, f"{unexp_pct}%", ha="center", va="center", color="white", fontsize=17, fontweight="bold")
ax.set_xticks([0, 1, 2])
ax.set_xticklabels([f"Brecha cruda\n\\${raw_m/1000:.0f}k vs \\${raw_w/1000:.0f}k",
                    "− Diferencias reales en el CV\n(experiencia, nivel, rol, inglés)",
                    "Castigo no explicado\nmismo CV, distinto sueldo"], fontsize=11)
ax.set_ylim(0, 116); ax.set_yticks([]); ax.grid(False)
ax.set_title("Con el mismo currículum en papel, un residuo se queda", fontsize=16, fontweight="bold", loc="left", pad=10)
ax.spines[["top", "right", "left"]].set_visible(False)
save(fig, "fig4_waterfall.png")

# ── Fig 5: the cross-border premium repeats the gap ─────────────────
same = (S(10) == "Yes"); fore = (S(10) == "No")
segs = ["Empleador\nnacional", "Empleador\nextranjero"]
men = [med(M & same), med(M & fore)]; women = [med(W & same), med(W & fore)]
acc_m = 100*(fore & M).sum()/M.sum(); acc_w = 100*(fore & W).sum()/W.sum()
fig, ax = plt.subplots(figsize=(9.5, 5.4)); x = range(2); w = 0.36
ax.bar([i-w/2 for i in x], men, w, label="Hombres", color=MEN)
ax.bar([i+w/2 for i in x], women, w, label="Mujeres", color=WOMEN)
for i, (m, f) in enumerate(zip(men, women)):
    ax.text(i-w/2, m+2500, f"${m/1000:.0f}k", ha="center", fontsize=12)
    ax.text(i+w/2, f+2500, f"${f/1000:.0f}k", ha="center", fontsize=12, color=WOMEN, fontweight="bold")
    ax.annotate(gpct(1-f/m), (i, max(m, f)+12000), ha="center", color=WOMEN, fontsize=16, fontweight="bold")
ax.set_xticks(list(x)); ax.set_xticklabels(segs); peso(ax)
ax.set_ylabel("Salario base mensual (mediana)")
ax.set_title("La prima transfronteriza no rescata: repite la brecha", fontsize=17, fontweight="bold", loc="left", pad=12)
ax.legend(frameon=False, loc="upper left"); ax.set_ylim(0, max(men)*1.3)
ax.spines[["top", "right"]].set_visible(False)
fig.text(0.5, -0.03, f"Acceso a empleador extranjero, ya parejo: hombres {acc_m:.0f}% · mujeres {acc_w:.0f}%",
         ha="center", color=MUTED, fontsize=12)
save(fig, "fig5_exit.png")

# ── Fig 6: isolation waffle (women who are ≤20% of their team) ──────
pw = num(70)[W].dropna(); iso = 100*(pw <= 20).mean(); med_peers = int(np.median(pw))
N_ROSE = round(iso); GREY = "#cbd5e1"
fig, ax = plt.subplots(figsize=(9.5, 5.8)); cell, gp = 1.0, 0.14
for idx in range(100):
    r, cc = idx // 10, idx % 10
    ax.add_patch(plt.Rectangle((cc, r), cell-gp, cell-gp, color=(WOMEN if idx < N_ROSE else GREY)))
ax.set_xlim(-0.2, 10.0); ax.set_ylim(-0.2, 10.2); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Dos de cada cinco mujeres son minoría clara en su propio equipo",
             fontsize=17, fontweight="bold", loc="left", pad=14, color=INK)
fig.text(0.5, 0.02, f"{iso:.0f}% son ≤20% de su equipo  ·  mediana: {med_peers}% de pares mujeres  ·  n={len(pw)} mujeres",
         ha="center", color=WOMEN, fontsize=13, fontweight="bold")
save(fig, "fig6_isolation.png")

# ── Fig 7: AI coding-style shift (developers, Mexico) ──────────────
AI_ACCENT = "#d97706"
dev = S(31).str.startswith("Desarrollo de software"); ai = S(59)
prog = ai[mx & dev]; prog = prog[prog != "nan"]
def cat(x):
    x = str(x)
    if x.startswith("Aunque sé programar"): return 0
    if x.startswith("Programo manualmente y uso IA como soporte"): return 1
    if x.startswith("Programo la funcionalidad manualmente"): return 2
    return 3
counts = prog.map(cat).value_counts(normalize=True).mul(100)
vals = [round(counts.get(k, 0)) for k in (0, 1, 2)]
cats = ["Instruyo a los agentes\n(ya casi no programo a mano)",
        "Programo a mano\n+ IA de apoyo", "Programo a mano\n+ IA complementaria"]
fig, ax = plt.subplots(figsize=(9.5, 5.0)); ypos = [2, 1, 0]
ax.barh(ypos, vals, color=[AI_ACCENT, MEN, MEN], height=0.62)
for y, v in zip(ypos, vals):
    ax.text(v+1, y, f"{v}%", va="center", fontsize=14, fontweight="bold", color=(AI_ACCENT if y == 2 else INK))
ax.set_yticks(ypos); ax.set_yticklabels(cats, fontsize=12)
ax.set_xlim(0, max(vals)+12); ax.set_xticks([]); ax.set_xlabel("% de quienes desarrollan software", labelpad=8)
ax.set_title("Casi la mitad ya no programa a mano: instruye a los agentes", fontsize=16, fontweight="bold", loc="left", pad=12)
ax.grid(False); ax.spines[["top", "right", "bottom"]].set_visible(False)
fig.text(0.5, -0.02, f"Entre quienes desarrollan software · n={len(prog)} (México)", ha="center", color=MUTED, fontsize=12)
save(fig, "fig7_ai.png")

print("done ->", OUT)

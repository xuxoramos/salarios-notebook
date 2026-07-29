"""Generate gender-gap slide figures (SG Tech Pulse 2026).
Numbers are the locked findings from GENDER_FINDINGS_2026.md. Outputs PNGs to figures/.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)

MEN = "#94a3b8"      # muted slate
WOMEN = "#e11d48"    # bold rose (draws the eye to the penalty)
INK = "#0f172a"
MUTED = "#64748b"
GRID = "#e2e8f0"

plt.rcParams.update({
    "figure.dpi": 160, "savefig.dpi": 160, "savefig.bbox": "tight",
    "figure.facecolor": "white", "axes.facecolor": "white",
    "font.size": 15, "axes.edgecolor": GRID, "axes.linewidth": 1,
    "axes.grid": True, "grid.color": GRID, "axes.axisbelow": True,
    "xtick.color": INK, "ytick.color": MUTED, "text.color": INK,
})

def peso(ax):
    ax.yaxis.set_major_formatter(lambda x, _: f"${x/1000:.0f}k")

def save(fig, name):
    fig.savefig(os.path.join(OUT, name)); plt.close(fig)
    print("wrote", name)

# ---------- Fig 1: the compounding cost (3 stages) ----------
fig, ax = plt.subplots(figsize=(9.5, 5.4))
stages = ["Junior / Medio", "Senior", "Gerente"]
men = [34500, 78000, 95000]; women = [30000, 56000, 55000]
gaps = ["−13%", "−28%", "−42%"]
x = range(len(stages)); w = 0.36
ax.bar([i-w/2 for i in x], men, w, label="Hombres", color=MEN)
ax.bar([i+w/2 for i in x], women, w, label="Mujeres", color=WOMEN)
for i,(m,f,g) in enumerate(zip(men,women,gaps)):
    ax.text(i-w/2, m+1800, f"${m/1000:.0f}k", ha="center", fontsize=12, color=INK)
    ax.text(i+w/2, f+1800, f"${f/1000:.0f}k", ha="center", fontsize=12, color=WOMEN, fontweight="bold")
    ax.annotate(g, (i, max(m,f)+9000), ha="center", color=WOMEN, fontsize=17, fontweight="bold")
ax.set_xticks(list(x)); ax.set_xticklabels(stages); peso(ax)
ax.set_title("El costo se acumula: la brecha crece con cada nivel", fontsize=17, fontweight="bold", loc="left", pad=12)
ax.set_ylabel("Salario base mensual (mediana)"); ax.legend(frameon=False, loc="upper left")
ax.set_ylim(0, 118000); ax.spines[["top","right"]].set_visible(False)
save(fig, "fig1_toll.png")

# ---------- Fig 2: scissors by tier ----------
fig, ax = plt.subplots(figsize=(9.5, 5.4))
tiers = ["Medio", "Senior", "Gerente"]
men = [50500, 78000, 95000]; women = [38500, 56000, 55000]
ax.plot(tiers, men, "-o", color=MEN, lw=3, ms=9, label="Hombres")
ax.plot(tiers, women, "-o", color=WOMEN, lw=3, ms=9, label="Mujeres")
for t,m,f,g in zip(tiers, men, women, ["−24%","−28%","−42%"]):
    ax.annotate(g, (t, (m+f)/2), ha="center", va="center", color=WOMEN, fontsize=13, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=WOMEN, lw=1))
ax.fill_between(tiers, men, women, color=WOMEN, alpha=0.08)
peso(ax); ax.set_ylabel("Salario base mensual (mediana)")
ax.set_title("Cada ascenso encarece ser mujer", fontsize=18, fontweight="bold", loc="left", pad=12)
ax.legend(frameon=False, loc="upper left"); ax.set_ylim(30000, 105000)
ax.spines[["top","right"]].set_visible(False)
save(fig, "fig2_scissors.png")

# ---------- Fig 3: the vanishing (female share by tier) ----------
fig, ax = plt.subplots(figsize=(9.5, 5.4))
tiers = ["Junior","Medio","Senior","Staff-Principal","Gerente","Director"]
share = [39, 62, 33, 24, 27, 39]
colors = [WOMEN if s>=50 else MEN for s in share]
bars = ax.bar(tiers, share, color=colors)
ax.axhline(50, color=MUTED, ls="--", lw=1)
ax.text(5.4, 51, "paridad 50%", color=MUTED, fontsize=11, ha="right")
for b,s in zip(bars,share): ax.text(b.get_x()+b.get_width()/2, s+1.5, f"{s}%", ha="center", fontsize=12, color=INK)
ax.set_ylabel("% de mujeres en el nivel"); ax.set_ylim(0, 70)
ax.set_title("La desaparición: mayoría en medio, ~1 de 3 arriba", fontsize=18, fontweight="bold", loc="left", pad=12)
ax.tick_params(axis="x", labelrotation=20)
ax.spines[["top","right"]].set_visible(False)
save(fig, "fig3_vanishing.png")

# ---------- Fig 4: Oaxaca explained vs unexplained ----------
fig, ax = plt.subplots(figsize=(9.5, 3.4))
ax.barh([0], [48], color="#cbd5e1", label="Explicado por cualificaciones")
ax.barh([0], [52], left=[48], color=WOMEN, label="Castigo no explicado")
ax.text(24, 0, "48%\nexplicado", ha="center", va="center", color=INK, fontsize=14, fontweight="bold")
ax.text(74, 0, "52%\nsin explicación", ha="center", va="center", color="white", fontsize=14, fontweight="bold")
ax.set_xlim(0,100); ax.set_yticks([]); ax.grid(False); ax.set_xlabel("Proporción de la brecha cruda (%)", labelpad=8)
ax.set_title("La mitad de la brecha no la explica nada del trabajo", fontsize=17, fontweight="bold", loc="left", pad=10)
ax.spines[["top","right","left"]].set_visible(False)
fig.text(0.5, -0.16, r"$\approx$ \$15,000 al mes  ·  ~\$176,000 al año  que una mujer senior pierde sin explicación",
         ha="center", color=WOMEN, fontsize=14, fontweight="bold")
save(fig, "fig4_oaxaca.png")

# ---------- Fig 4b: peel-away waterfall (same-résumé intuition) ----------
fig, ax = plt.subplots(figsize=(9.5, 5.2))
EXPLAINED = "#cbd5e1"
# Waterfall: start at raw gap (100), peel off the explained part (48), land on residual (52).
ax.bar(0, 100, 0.62, bottom=0, color=MEN)
ax.bar(1, 48, 0.62, bottom=52, color=EXPLAINED)
ax.bar(2, 52, 0.62, bottom=0, color=WOMEN)
# dashed connectors that trace the peel-away
ax.plot([0.31, 1.31], [100, 100], ls="--", lw=1.4, color=MUTED)
ax.plot([1.31, 1.69], [52, 52], ls="--", lw=1.4, color=MUTED)
# value labels
ax.text(0, 104, "100%", ha="center", va="bottom", color=INK, fontsize=14, fontweight="bold")
ax.text(1, 76, "−48%", ha="center", va="center", color=INK, fontsize=15, fontweight="bold")
ax.text(2, 26, "52%", ha="center", va="center", color="white", fontsize=17, fontweight="bold")
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(["Brecha cruda\n\\$79,500 vs \\$48,000",
                    "− Diferencias reales en el CV\n(experiencia, nivel, rol, inglés)",
                    "Castigo no explicado\nmismo CV, distinto sueldo"],
                   fontsize=11)
ax.set_ylim(0, 116); ax.set_yticks([]); ax.grid(False)
ax.set_title("Con el mismo currículum en papel, la mitad de la brecha se queda",
             fontsize=16, fontweight="bold", loc="left", pad=10)
ax.spines[["top", "right", "left"]].set_visible(False)
save(fig, "fig4_waterfall.png")

# ---------- Fig 5: the male-only exit ----------
fig, ax = plt.subplots(figsize=(9.5, 5.4))
segs = ["Empleador\nnacional", "Empleador\nextranjero"]
men = [75000, 115000]; women = [48000, 48500]
x = range(len(segs)); w = 0.36
ax.bar([i-w/2 for i in x], men, w, label="Hombres", color=MEN)
ax.bar([i+w/2 for i in x], women, w, label="Mujeres", color=WOMEN)
for i,(m,f,g) in enumerate(zip(men,women,["−36%","−58%"])):
    ax.text(i-w/2, m+2500, f"${m/1000:.0f}k", ha="center", fontsize=12)
    ax.text(i+w/2, f+2500, f"${f/1000:.0f}k", ha="center", fontsize=12, color=WOMEN, fontweight="bold")
    ax.annotate(g, (i, max(m,f)+12000), ha="center", color=WOMEN, fontsize=16, fontweight="bold")
ax.set_xticks(list(x)); ax.set_xticklabels(segs); peso(ax)
ax.set_ylabel("Salario base mensual (mediana)")
ax.set_title("La salida solo para ellos (direccional, n=12 mujeres)", fontsize=17, fontweight="bold", loc="left", pad=12)
ax.legend(frameon=False, loc="upper left"); ax.set_ylim(0, 150000)
ax.spines[["top","right"]].set_visible(False)
save(fig, "fig5_exit.png")

print("done ->", OUT)

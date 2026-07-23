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

# ---------- Fig 1: the toll (bands) ----------
fig, ax = plt.subplots(figsize=(9.5, 5.4))
stages = ["Junior / Medio", "Senior en adelante"]
men = [32000, 95000]; women = [37623, 60000]
x = range(len(stages)); w = 0.36
ax.bar([i-w/2 for i in x], men, w, label="Hombres", color=MEN)
ax.bar([i+w/2 for i in x], women, w, label="Mujeres", color=WOMEN)
for i,(m,f) in enumerate(zip(men,women)):
    ax.text(i-w/2, m+2000, f"${m/1000:.0f}k", ha="center", fontsize=13, color=INK)
    ax.text(i+w/2, f+2000, f"${f/1000:.0f}k", ha="center", fontsize=13, color=WOMEN, fontweight="bold")
ax.annotate("mujeres +18%", (0, 52000), ha="center", color=MUTED, fontsize=12)
ax.annotate("−37%", (1, 78000), ha="center", color=WOMEN, fontsize=20, fontweight="bold")
ax.set_xticks(list(x)); ax.set_xticklabels(stages); peso(ax)
ax.set_title("El peaje: iguales abajo, castigadas arriba", fontsize=18, fontweight="bold", loc="left", pad=12)
ax.set_ylabel("Salario base mensual (mediana)"); ax.legend(frameon=False, loc="upper left")
ax.set_ylim(0, 108000); ax.spines[["top","right"]].set_visible(False)
save(fig, "fig1_toll.png")

# ---------- Fig 2: the toll by tier (scissors) ----------
fig, ax = plt.subplots(figsize=(9.5, 5.4))
tiers = ["Medio", "Senior", "Gerente"]
men = [46500, 79500, 96500]; women = [45500, 56795, 60000]
ax.plot(tiers, men, "-o", color=MEN, lw=3, ms=9, label="Hombres")
ax.plot(tiers, women, "-o", color=WOMEN, lw=3, ms=9, label="Mujeres")
for t,m,f,g in zip(tiers, men, women, ["−2%","−29%","−38%"]):
    ax.annotate(g, (t, (m+f)/2), ha="center", va="center", color=WOMEN, fontsize=13, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=WOMEN, lw=1))
ax.fill_between(tiers, men, women, color=WOMEN, alpha=0.07)
peso(ax); ax.set_ylabel("Salario base mensual (mediana)")
ax.set_title("La brecha se ensancha con el nivel", fontsize=18, fontweight="bold", loc="left", pad=12)
ax.legend(frameon=False, loc="upper left"); ax.set_ylim(30000, 108000)
ax.spines[["top","right"]].set_visible(False)
save(fig, "fig2_scissors.png")

# ---------- Fig 3: the vanishing (female share by tier) ----------
fig, ax = plt.subplots(figsize=(9.5, 5.4))
tiers = ["Junior","Medio","Senior","Staff-Principal","Gerente","Director"]
share = [19, 62, 28, 19, 21, 20]
colors = [WOMEN if s>=50 else MEN for s in share]
bars = ax.bar(tiers, share, color=colors)
ax.axhline(50, color=MUTED, ls="--", lw=1)
ax.text(5.4, 51, "paridad 50%", color=MUTED, fontsize=11, ha="right")
for b,s in zip(bars,share): ax.text(b.get_x()+b.get_width()/2, s+1.5, f"{s}%", ha="center", fontsize=12, color=INK)
ax.set_ylabel("% de mujeres en el nivel"); ax.set_ylim(0, 70)
ax.set_title("La desaparición: mayoría en medio, ~1 de 4 arriba", fontsize=18, fontweight="bold", loc="left", pad=12)
ax.tick_params(axis="x", labelrotation=20)
ax.spines[["top","right"]].set_visible(False)
save(fig, "fig3_vanishing.png")

# ---------- Fig 4: Oaxaca explained vs unexplained ----------
fig, ax = plt.subplots(figsize=(9.5, 3.4))
ax.barh([0], [50], color="#cbd5e1", label="Explicado por cualificaciones")
ax.barh([0], [50], left=[50], color=WOMEN, label="Castigo no explicado")
ax.text(25, 0, "50%\nexplicado", ha="center", va="center", color=INK, fontsize=14, fontweight="bold")
ax.text(75, 0, "50%\nsin explicación", ha="center", va="center", color="white", fontsize=14, fontweight="bold")
ax.set_xlim(0,100); ax.set_yticks([]); ax.grid(False); ax.set_xlabel("Proporción de la brecha cruda (%)", labelpad=8)
ax.set_title("La mitad de la brecha no la explica nada del trabajo", fontsize=17, fontweight="bold", loc="left", pad=10)
ax.spines[["top","right","left"]].set_visible(False)
fig.text(0.5, -0.16, r"$\approx$ \$15,000 al mes  ·  ~\$176,000 al año  que una mujer senior pierde sin explicación",
         ha="center", color=WOMEN, fontsize=14, fontweight="bold")
save(fig, "fig4_oaxaca.png")

# ---------- Fig 5: the male-only exit ----------
fig, ax = plt.subplots(figsize=(9.5, 5.4))
segs = ["Empleador\nnacional", "Empleador\nextranjero"]
men = [78500, 120000]; women = [55000, 44400]
x = range(len(segs)); w = 0.36
ax.bar([i-w/2 for i in x], men, w, label="Hombres", color=MEN)
ax.bar([i+w/2 for i in x], women, w, label="Mujeres", color=WOMEN)
for i,(m,f,g) in enumerate(zip(men,women,["−30%","−63%"])):
    ax.text(i-w/2, m+2500, f"${m/1000:.0f}k", ha="center", fontsize=12)
    ax.text(i+w/2, f+2500, f"${f/1000:.0f}k", ha="center", fontsize=12, color=WOMEN, fontweight="bold")
    ax.annotate(g, (i, max(m,f)+12000), ha="center", color=WOMEN, fontsize=16, fontweight="bold")
ax.set_xticks(list(x)); ax.set_xticklabels(segs); peso(ax)
ax.set_ylabel("Salario base mensual (mediana)")
ax.set_title("La salida solo para ellos (direccional, n=11 mujeres)", fontsize=17, fontweight="bold", loc="left", pad=12)
ax.legend(frameon=False, loc="upper left"); ax.set_ylim(0, 150000)
ax.spines[["top","right"]].set_visible(False)
save(fig, "fig5_exit.png")

print("done ->", OUT)

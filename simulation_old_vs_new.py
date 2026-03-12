"""
Simulated comparison: Old Survey (2020–2022) vs Redesigned Survey (2026)

Generates synthetic data matching known distributions from the real analysis,
fits OLS salary models for both designs, and compares:
  1. R² and adjusted R²
  2. Multicollinearity (VIF)
  3. Coefficient stability (bootstrap SE)
  4. Sparsity in tech blocks
  5. Information efficiency (R² per predictor)
  6. Effective sample size for subgroup analyses
  7. Completion-rate impact on usable N

Results are saved to simulation_results/ directory.
"""

import os
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings("ignore")

np.random.seed(2026)

OUT_DIR = "simulation_results"
os.makedirs(OUT_DIR, exist_ok=True)

N = 6000  # matches real ~5,798

# ────────────────────────────────────────────────────────────────
# PART 0: Shared latent structure
# ────────────────────────────────────────────────────────────────
# The "true" salary DGP has known effect sizes from the real analysis.
# We simulate latent factors and then project them into old vs new designs.

# Demographics / professional
age = np.random.normal(32, 7, N).clip(18, 65).astype(int)
gender = np.random.choice(["hombre", "mujer", "nb"], N, p=[0.93, 0.05, 0.02])
is_female = (gender == "mujer").astype(float)

experience_tech = np.random.exponential(6, N).clip(0, 40).round(1)
experience_total = (experience_tech + np.random.exponential(3, N).clip(0, 20)).round(1)
tenure_current = np.minimum(experience_tech, np.random.exponential(3, N).clip(0, 20)).round(1)

seniority_levels = ["Junior", "Mid", "Senior", "Staff-Principal", "Lead-Manager", "Director+", "Founder-C-Level"]
seniority_probs = [0.15, 0.30, 0.30, 0.08, 0.10, 0.05, 0.02]
seniority_level = np.random.choice(seniority_levels, N, p=seniority_probs)
seniority_premium = {"Junior": 0, "Mid": 8000, "Senior": 18000, "Staff-Principal": 28000,
                     "Lead-Manager": 22000, "Director+": 35000, "Founder-C-Level": 40000}

english = np.random.choice(range(6), N, p=[0.05, 0.10, 0.20, 0.30, 0.25, 0.10])
english_use_levels = ["Nunca", "Ocasionalmente", "Regularmente", "La mayor parte", "Todo en inglés"]
english_use_probs = np.array([0.08, 0.20, 0.30, 0.25, 0.17])
english_use = np.random.choice(english_use_levels, N, p=english_use_probs)
english_use_score = np.array([english_use_levels.index(e) for e in english_use])

cities = ["CDMX", "Guadalajara", "Monterrey", "Hermosillo", "Querétaro", "Mérida",
          "Aguascalientes", "León", "SLP", "Puebla", "Otra"]
city_probs = [0.30, 0.15, 0.15, 0.05, 0.07, 0.04, 0.03, 0.03, 0.02, 0.04, 0.12]
city = np.random.choice(cities, N, p=city_probs)
city_premium = {"CDMX": 5000, "Guadalajara": 2000, "Monterrey": 4000, "Hermosillo": 11000,
                "Querétaro": 1000, "Mérida": -2000, "Aguascalientes": -3000, "León": -6000,
                "SLP": -4000, "Puebla": -2000, "Otra": -1000}

is_remote = np.random.binomial(1, 0.45, N)
work_arrangements = ["Fully remote", "Hybrid", "Fully on-site", "Nomadic"]
work_arr = np.where(is_remote, np.random.choice(["Fully remote", "Hybrid", "Nomadic"], N, p=[0.55, 0.35, 0.10]),
                    "Fully on-site")

company_sizes = ["1-10", "11-50", "51-200", "201-1000", "1001-5000", "5000+"]
company_size = np.random.choice(company_sizes, N, p=[0.08, 0.15, 0.22, 0.25, 0.18, 0.12])
company_size_premium = {"1-10": -5000, "11-50": -2000, "51-200": 0, "201-1000": 3000,
                        "1001-5000": 7000, "5000+": 10000}

industries = ["Tech/Software", "Finance/Fintech", "Health", "E-commerce", "Education",
              "Manufacturing", "Government", "Consulting", "Telecom", "Entertainment", "Other"]
industry = np.random.choice(industries, N, p=[0.30, 0.15, 0.05, 0.10, 0.04, 0.06, 0.05, 0.10, 0.05, 0.03, 0.07])
industry_premium = {"Tech/Software": 3000, "Finance/Fintech": 8000, "Health": 0, "E-commerce": 2000,
                    "Education": -5000, "Manufacturing": -2000, "Government": -4000, "Consulting": 1000,
                    "Telecom": 2000, "Entertainment": 1000, "Other": -1000}

# Roles (old: 26 binary checkboxes; new: single primary_role)
roles = ["Backend", "Frontend", "Fullstack", "Mobile", "DataScience", "DataEng",
         "DevOps", "InfoSec", "Architecture", "PM", "QA", "UXD", "Direction",
         "AI-ML", "Support", "Other"]
role_probs = [0.18, 0.12, 0.15, 0.05, 0.07, 0.05, 0.08, 0.03, 0.05, 0.06, 0.04, 0.03, 0.03, 0.03, 0.02, 0.01]
primary_role = np.random.choice(roles, N, p=role_probs)
role_premium = {"Backend": 4000, "Frontend": 2000, "Fullstack": 3000, "Mobile": 3000,
                "DataScience": 6000, "DataEng": 5000, "DevOps": 5000, "InfoSec": 4000,
                "Architecture": 9000, "PM": 3000, "QA": -2000, "UXD": -3000,
                "Direction": 16000, "AI-ML": 8000, "Support": -11000, "Other": 0}

# Languages (old: 20 binary checkboxes; new: single primary_language)
languages = ["JavaScript-TS", "Python", "Java", "C#", "Go", "Rust", "PHP", "Ruby",
             "Kotlin", "Swift", "C-C++", "Scala", "Elixir", "Other"]
lang_probs = [0.25, 0.20, 0.12, 0.10, 0.05, 0.02, 0.08, 0.03, 0.03, 0.02, 0.04, 0.01, 0.01, 0.04]
primary_language = np.random.choice(languages, N, p=lang_probs)
lang_premium = {"JavaScript-TS": 0, "Python": 2000, "Java": 1000, "C#": -3000,
                "Go": 6000, "Rust": 5000, "PHP": -4000, "Ruby": 6500,
                "Kotlin": 3000, "Swift": 3000, "C-C++": 1000, "Scala": 4000,
                "Elixir": 12000, "Other": 0}

# Certifications
has_certs = np.random.binomial(1, 0.35, N)
cert_count = np.where(has_certs, np.random.poisson(2, N).clip(1, 10), 0)

primary_lang_years = np.minimum(experience_tech, np.random.exponential(4, N).clip(0.5, 25)).round(1)
tech_breadth = np.random.choice(range(1, 8), N, p=[0.15, 0.25, 0.25, 0.15, 0.10, 0.05, 0.05])

# ────────────────────────────────────────────────────────────────
# PART 1: True salary DGP
# ────────────────────────────────────────────────────────────────
base = 25000  # base intercept
salary = (
    base
    + 1267 * experience_tech                                    # +$1,267/yr (multivariate)
    + 500 * (experience_total - experience_tech)                # career-switcher small premium
    + 7305 * english                                            # +$7,305/level (multivariate)
    + 3000 * english_use_score                                  # behavioral anchor adds signal
    + is_remote * 12213                                         # +$12,213 remote (multivariate)
    + is_female * -12442                                        # -$12,442 gender gap
    + np.array([city_premium[c] for c in city])
    + np.array([seniority_premium[s] for s in seniority_level])
    + np.array([company_size_premium[s] for s in company_size])
    + np.array([industry_premium[i] for i in industry])
    + np.array([role_premium[r] for r in primary_role])
    + np.array([lang_premium[l] for l in primary_language])
    + has_certs * 3000
    + cert_count * 800
    + primary_lang_years * 400
    + tech_breadth * 500
    + np.random.normal(0, 20000, N)  # irreducible noise
)
salary = salary.clip(8000, 250000)

print(f"Synthetic salary: mean={salary.mean():,.0f}, median={np.median(salary):,.0f}, "
      f"sd={salary.std():,.0f}")
print(f"Real survey:      mean=47,415,  median=40,000,  sd≈35,000")
print()

# ────────────────────────────────────────────────────────────────
# PART 2: Old survey design (checkbox matrices)
# ────────────────────────────────────────────────────────────────
print("=" * 70)
print("CONSTRUCTING OLD SURVEY DESIGN")
print("=" * 70)

# Old: experience (ambiguous — we average tech + total with noise)
old_experience = (experience_tech * 0.6 + experience_total * 0.4 + np.random.normal(0, 1, N)).clip(0, 40)

# Old: seniority (role tenure, not company tenure — noisier proxy)
old_seniority = (tenure_current * 0.7 + np.random.normal(0, 2, N)).clip(0, 30)

# Old: english (ILR only, no behavioral anchor)
old_english = english

# Old: remote (binary)
old_remote = is_remote

# Old binary role checkboxes (26 columns, each person checks 1-5)
old_role_cols = ["act_backend", "act_frontend", "act_fullstack", "act_mobile", "act_datasci",
                 "act_dataeng", "act_devops", "act_infosec", "act_arq", "act_pm",
                 "act_qa", "act_uxd", "act_dir", "act_aiml", "act_support", "act_other",
                 "act_dba", "act_erp", "act_techsales", "act_techwrite", "act_training",
                 "act_consulting", "act_bi", "act_iot", "act_devrel", "act_docencia"]
role_to_primary_col = {
    "Backend": "act_backend", "Frontend": "act_frontend", "Fullstack": "act_fullstack",
    "Mobile": "act_mobile", "DataScience": "act_datasci", "DataEng": "act_dataeng",
    "DevOps": "act_devops", "InfoSec": "act_infosec", "Architecture": "act_arq",
    "PM": "act_pm", "QA": "act_qa", "UXD": "act_uxd", "Direction": "act_dir",
    "AI-ML": "act_aiml", "Support": "act_support", "Other": "act_other"
}

old_roles_df = pd.DataFrame(0, index=range(N), columns=old_role_cols)
for i in range(N):
    pcol = role_to_primary_col[primary_role[i]]
    old_roles_df.loc[i, pcol] = 1
    # Add 1-4 random secondary roles (noise)
    extra = np.random.randint(0, 5)
    if extra > 0:
        extras = np.random.choice(old_role_cols, extra, replace=False)
        old_roles_df.loc[i, extras] = 1

# Old binary language checkboxes (20 columns)
old_lang_cols = ["lang_js", "lang_python", "lang_java", "lang_csharp", "lang_go",
                 "lang_rust", "lang_php", "lang_ruby", "lang_kotlin", "lang_swift",
                 "lang_c", "lang_scala", "lang_elixir", "lang_bash", "lang_perl",
                 "lang_cobol", "lang_groovy", "lang_plsql", "lang_vbnet", "lang_dart"]
lang_to_primary_col = {
    "JavaScript-TS": "lang_js", "Python": "lang_python", "Java": "lang_java",
    "C#": "lang_csharp", "Go": "lang_go", "Rust": "lang_rust", "PHP": "lang_php",
    "Ruby": "lang_ruby", "Kotlin": "lang_kotlin", "Swift": "lang_swift",
    "C-C++": "lang_c", "Scala": "lang_scala", "Elixir": "lang_elixir", "Other": "lang_dart"
}

old_langs_df = pd.DataFrame(0, index=range(N), columns=old_lang_cols)
for i in range(N):
    pcol = lang_to_primary_col.get(primary_language[i], "lang_js")
    old_langs_df.loc[i, pcol] = 1
    # Random secondary languages (1-3 extras)
    extra = np.random.randint(0, 4)
    if extra > 0:
        extras = np.random.choice(old_lang_cols, extra, replace=False)
        old_langs_df.loc[i, extras] = 1

# Old: 27 cert checkboxes (sparse)
old_cert_cols = [f"cert_{i}" for i in range(27)]
old_certs_df = pd.DataFrame(0, index=range(N), columns=old_cert_cols)
for i in range(N):
    if has_certs[i]:
        n_certs = min(cert_count[i], 27)
        cols = np.random.choice(old_cert_cols, n_certs, replace=False)
        old_certs_df.loc[i, cols] = 1

# Old: city dummies, gender, education (same in both designs)
old_city_dummies = pd.get_dummies(pd.Series(city), prefix="city", drop_first=True)

# Old: no company_size, no industry, no seniority_level
# Old: profile (noisy mapping of seniority_level)
old_profile = pd.Series(seniority_level).map({
    "Junior": "godin", "Mid": "godin", "Senior": "godin",
    "Staff-Principal": "godin", "Lead-Manager": "directivo",
    "Director+": "directivo", "Founder-C-Level": "emprendedor"
})
old_profile_dummies = pd.get_dummies(old_profile, prefix="profile", drop_first=True)

# Build old design matrix
old_X = pd.DataFrame({
    "experience": old_experience,
    "seniority": old_seniority,
    "english": old_english,
    "remote": old_remote,
    "is_female": is_female,
})
old_X = pd.concat([old_X, old_city_dummies, old_profile_dummies,
                    old_roles_df, old_langs_df, old_certs_df], axis=1)

# Simulate 15% survey dropout for old design (fatigue at the checkbox section)
old_completion_mask = np.random.binomial(1, 0.85, N).astype(bool)
old_X_complete = old_X[old_completion_mask].reset_index(drop=True)
old_y_complete = salary[old_completion_mask]

print(f"Old design: {old_X.shape[1]} predictors, {old_X_complete.shape[0]} complete responses "
      f"(of {N}; 85% completion)")

# ────────────────────────────────────────────────────────────────
# PART 3: New survey design (role-first, structured)
# ────────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("CONSTRUCTING NEW SURVEY DESIGN")
print("=" * 70)

new_role_dummies = pd.get_dummies(pd.Series(primary_role), prefix="role", drop_first=True)
new_lang_dummies = pd.get_dummies(pd.Series(primary_language), prefix="lang", drop_first=True)
new_seniority_dummies = pd.get_dummies(pd.Series(seniority_level), prefix="seniority", drop_first=True)
new_company_dummies = pd.get_dummies(pd.Series(company_size), prefix="compsize", drop_first=True)
new_industry_dummies = pd.get_dummies(pd.Series(industry), prefix="industry", drop_first=True)
new_city_dummies = pd.get_dummies(pd.Series(city), prefix="city", drop_first=True)
new_work_dummies = pd.get_dummies(pd.Series(work_arr), prefix="work", drop_first=True)

new_X = pd.DataFrame({
    "experience_tech": experience_tech,
    "experience_total": experience_total,
    "tenure_current": tenure_current,
    "english": english,
    "english_use": english_use_score,
    "is_female": is_female,
    "has_certs": has_certs.astype(float),
    "cert_count": cert_count.astype(float),
    "primary_lang_years": primary_lang_years,
    "tech_breadth": tech_breadth.astype(float),
})
new_X = pd.concat([new_X, new_city_dummies, new_seniority_dummies, new_company_dummies,
                    new_industry_dummies, new_role_dummies, new_lang_dummies,
                    new_work_dummies], axis=1)

# 95% completion rate (shorter survey, no checkbox fatigue)
new_completion_mask = np.random.binomial(1, 0.95, N).astype(bool)
new_X_complete = new_X[new_completion_mask].reset_index(drop=True)
new_y_complete = salary[new_completion_mask]

print(f"New design: {new_X.shape[1]} predictors, {new_X_complete.shape[0]} complete responses "
      f"(of {N}; 95% completion)")

# ────────────────────────────────────────────────────────────────
# PART 4: Fit OLS models and compare
# ────────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

# Old model
from numpy.linalg import lstsq, matrix_rank
old_Xm = old_X_complete.values.astype(float)
old_Xm_int = np.column_stack([np.ones(old_Xm.shape[0]), old_Xm])
old_coef, _, _, _ = lstsq(old_Xm_int, old_y_complete, rcond=None)
old_pred = old_Xm_int @ old_coef
old_ss_res = np.sum((old_y_complete - old_pred) ** 2)
old_ss_tot = np.sum((old_y_complete - old_y_complete.mean()) ** 2)
old_r2 = 1 - old_ss_res / old_ss_tot
old_n = old_Xm.shape[0]
old_k = old_Xm.shape[1]
old_adj_r2 = 1 - (1 - old_r2) * (old_n - 1) / (old_n - old_k - 1)
old_esr = np.sqrt(old_ss_res / (old_n - old_k - 1))

# New model
new_Xm = new_X_complete.values.astype(float)
new_Xm_int = np.column_stack([np.ones(new_Xm.shape[0]), new_Xm])
new_coef, _, _, _ = lstsq(new_Xm_int, new_y_complete, rcond=None)
new_pred = new_Xm_int @ new_coef
new_ss_res = np.sum((new_y_complete - new_pred) ** 2)
new_ss_tot = np.sum((new_y_complete - new_y_complete.mean()) ** 2)
new_r2 = 1 - new_ss_res / new_ss_tot
new_n = new_Xm.shape[0]
new_k = new_Xm.shape[1]
new_adj_r2 = 1 - (1 - new_r2) * (new_n - 1) / (new_n - new_k - 1)
new_esr = np.sqrt(new_ss_res / (new_n - new_k - 1))

print(f"\n{'Metric':<35} {'Old Design':>15} {'New Design':>15} {'Change':>15}")
print("-" * 80)
print(f"{'Predictors (k)':<35} {old_k:>15} {new_k:>15} {new_k - old_k:>+15}")
print(f"{'Usable N (after completion)':<35} {old_n:>15,} {new_n:>15,} {new_n - old_n:>+15,}")
print(f"{'R²':<35} {old_r2:>15.4f} {new_r2:>15.4f} {new_r2 - old_r2:>+15.4f}")
print(f"{'Adjusted R²':<35} {old_adj_r2:>15.4f} {new_adj_r2:>15.4f} {new_adj_r2 - old_adj_r2:>+15.4f}")
print(f"{'ESR (Standard Error of Estimate)':<35} {old_esr:>15,.0f} {new_esr:>15,.0f} {new_esr - old_esr:>+15,.0f}")
print(f"{'R² per predictor':<35} {old_r2/old_k:>15.5f} {new_r2/new_k:>15.5f} {new_r2/new_k - old_r2/old_k:>+15.5f}")
print(f"{'Adj R² per predictor':<35} {old_adj_r2/old_k:>15.5f} {new_adj_r2/new_k:>15.5f} "
      f"{new_adj_r2/new_k - old_adj_r2/old_k:>+15.5f}")

# ────────────────────────────────────────────────────────────────
# PART 5: Multicollinearity (VIF)
# ────────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("MULTICOLLINEARITY ANALYSIS (VIF)")
print("=" * 70)

def compute_vif(X_df, sample_n=2000):
    """Compute VIF for each column. Uses a sample for speed."""
    X_sample = X_df.sample(min(sample_n, len(X_df)), random_state=42).values.astype(float)
    vifs = {}
    for j in range(X_sample.shape[1]):
        y_j = X_sample[:, j]
        X_j = np.delete(X_sample, j, axis=1)
        X_j_int = np.column_stack([np.ones(X_j.shape[0]), X_j])
        coef, _, _, _ = lstsq(X_j_int, y_j, rcond=None)
        pred_j = X_j_int @ coef
        ss_res = np.sum((y_j - pred_j) ** 2)
        ss_tot = np.sum((y_j - y_j.mean()) ** 2)
        r2_j = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        vif = 1 / (1 - r2_j) if r2_j < 1 else np.inf
        vifs[X_df.columns[j]] = vif
    return vifs

# Old VIF (sample for speed)
old_vif = compute_vif(old_X_complete)
old_vif_series = pd.Series(old_vif).sort_values(ascending=False)

# New VIF
new_vif = compute_vif(new_X_complete)
new_vif_series = pd.Series(new_vif).sort_values(ascending=False)

print(f"\n{'':=<52}")
print(f"OLD DESIGN — Top 15 VIF values")
print(f"{'':=<52}")
for name, v in old_vif_series.head(15).items():
    flag = " ⚠️  SEVERE" if v > 10 else (" ⚡ HIGH" if v > 5 else "")
    print(f"  {name:<30} VIF = {v:>8.2f}{flag}")

print(f"\n{'':=<52}")
print(f"NEW DESIGN — Top 15 VIF values")
print(f"{'':=<52}")
for name, v in new_vif_series.head(15).items():
    flag = " ⚠️  SEVERE" if v > 10 else (" ⚡ HIGH" if v > 5 else "")
    print(f"  {name:<30} VIF = {v:>8.2f}{flag}")

old_vif_gt5 = (old_vif_series > 5).sum()
old_vif_gt10 = (old_vif_series > 10).sum()
new_vif_gt5 = (new_vif_series > 5).sum()
new_vif_gt10 = (new_vif_series > 10).sum()

print(f"\nVIF Summary:")
print(f"  Old design: {old_vif_gt5} vars with VIF>5, {old_vif_gt10} vars with VIF>10")
print(f"  New design: {new_vif_gt5} vars with VIF>5, {new_vif_gt10} vars with VIF>10")
print(f"  Old mean VIF: {old_vif_series.mean():.2f}")
print(f"  New mean VIF: {new_vif_series.mean():.2f}")

# ────────────────────────────────────────────────────────────────
# PART 6: Coefficient stability (Bootstrap)
# ────────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("COEFFICIENT STABILITY (200 Bootstrap iterations)")
print("=" * 70)

B = 200

def bootstrap_coefs(X_df, y, n_boot=B):
    """Return (n_boot × k) array of coefficient estimates."""
    X_np = X_df.values.astype(float)
    n = X_np.shape[0]
    coefs = np.zeros((n_boot, X_np.shape[1]))
    for b in range(n_boot):
        idx = np.random.choice(n, n, replace=True)
        X_b = np.column_stack([np.ones(n), X_np[idx]])
        y_b = y[idx] if isinstance(y, np.ndarray) else y.values[idx]
        c, _, _, _ = lstsq(X_b, y_b, rcond=None)
        coefs[b] = c[1:]  # exclude intercept
    return coefs

old_boot = bootstrap_coefs(old_X_complete, old_y_complete)
new_boot = bootstrap_coefs(new_X_complete, new_y_complete)

old_cv = np.abs(old_boot.std(0) / (old_boot.mean(0) + 1e-10))
new_cv = np.abs(new_boot.std(0) / (new_boot.mean(0) + 1e-10))

# For comparable predictors: experience, english, remote/remote-like, gender
key_old = {"experience": 0, "english": 2, "remote": 3, "is_female": 4}
key_new = {"experience_tech": 0, "english": 3, "is_female": 5}

print(f"\nBootstrap SE for key predictors:")
print(f"{'Predictor':<25} {'Old SE':>12} {'Old CV':>10} {'New Predictor':<25} {'New SE':>12} {'New CV':>10}")
print("-" * 95)

pairs = [
    ("experience", "experience_tech"),
    ("english", "english"),
    ("remote", None),
    ("is_female", "is_female"),
]

for old_name, new_name in pairs:
    old_idx = list(old_X_complete.columns).index(old_name)
    old_se = old_boot[:, old_idx].std()
    old_cv_val = old_cv[old_idx]
    if new_name:
        new_idx = list(new_X_complete.columns).index(new_name)
        new_se = new_boot[:, new_idx].std()
        new_cv_val = new_cv[new_idx]
        print(f"  {old_name:<25} {old_se:>10,.0f}   {old_cv_val:>8.3f}   "
              f"{new_name:<25} {new_se:>10,.0f}   {new_cv_val:>8.3f}")
    else:
        print(f"  {old_name:<25} {old_se:>10,.0f}   {old_cv_val:>8.3f}   {'(decomposed in new)':>25}")

# Overall coefficient stability
print(f"\n  Old design: mean CV across all predictors = {old_cv.mean():.3f}")
print(f"  New design: mean CV across all predictors = {new_cv.mean():.3f}")
print(f"  Stability improvement: {(1 - new_cv.mean()/old_cv.mean()) * 100:.1f}%")

# ────────────────────────────────────────────────────────────────
# PART 7: Sparsity analysis
# ────────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("SPARSITY ANALYSIS")
print("=" * 70)

# Old tech checkbox sparsity
old_tech_cols = old_lang_cols + old_role_cols + old_cert_cols
old_tech_df = pd.concat([old_langs_df, old_roles_df, old_certs_df], axis=1)
old_sparsity = 1 - old_tech_df.mean()  # fraction of zeros per column
old_mean_sparsity = old_sparsity.mean()
old_cols_gt90 = (old_sparsity > 0.90).sum()
old_cols_gt95 = (old_sparsity > 0.95).sum()

# New tech fields: all are either numeric or one-hot with solid representation
new_tech_cols_num = ["has_certs", "cert_count", "primary_lang_years", "tech_breadth"]
new_tech_cat = pd.concat([new_role_dummies, new_lang_dummies], axis=1)
new_tech_sparsity = 1 - new_tech_cat.mean()
new_mean_sparsity = new_tech_sparsity.mean()
new_cols_gt90 = (new_tech_sparsity > 0.90).sum()
new_cols_gt95 = (new_tech_sparsity > 0.95).sum()

print(f"\nTech block sparsity (fraction of zero cells):")
print(f"  Old design: {len(old_tech_cols)} binary columns, "
      f"mean sparsity = {old_mean_sparsity:.1%}")
print(f"    Columns with >90% zeros: {old_cols_gt90} ({old_cols_gt90/len(old_tech_cols):.0%})")
print(f"    Columns with >95% zeros: {old_cols_gt95} ({old_cols_gt95/len(old_tech_cols):.0%})")
print(f"  New design: {new_tech_cat.shape[1]} one-hot columns + {len(new_tech_cols_num)} numeric, "
      f"mean sparsity = {new_mean_sparsity:.1%}")
print(f"    Columns with >90% zeros: {new_cols_gt90} ({new_cols_gt90/new_tech_cat.shape[1]:.0%})")
print(f"    Columns with >95% zeros: {new_cols_gt95} ({new_cols_gt95/new_tech_cat.shape[1]:.0%})")

# ────────────────────────────────────────────────────────────────
# PART 8: Subgroup effective sample sizes
# ────────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("SUBGROUP EFFECTIVE SAMPLE SIZES")
print("=" * 70)

print(f"\nFor rare categories (old = niche checkbox; new = single-select primary):")
old_elixir_n = old_langs_df["lang_elixir"].sum()
new_elixir_n = (pd.Series(primary_language) == "Elixir").sum()
old_rust_n = old_langs_df["lang_rust"].sum()
new_rust_n = (pd.Series(primary_language) == "Rust").sum()
old_dir_n = old_roles_df["act_dir"].sum()
new_dir_n = (pd.Series(primary_role) == "Direction").sum()

print(f"  {'Category':<20} {'Old (checked)':<18} {'New (primary)':<18} {'Interpretation'}")
print(f"  {'-'*80}")
print(f"  {'Elixir':<20} {int(old_elixir_n):<18} {int(new_elixir_n):<18} "
      f"{'Old = Elixir among others; New = Elixir is their main language'}")
print(f"  {'Rust':<20} {int(old_rust_n):<18} {int(new_rust_n):<18} "
      f"{'Smaller N but cleaner signal'}")
print(f"  {'Direction/Strategy':<20} {int(old_dir_n):<18} {int(new_dir_n):<18} "
      f"{'Old = people who do strategy sometimes'}")

# ────────────────────────────────────────────────────────────────
# PART 9: Information efficiency
# ────────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("INFORMATION EFFICIENCY")
print("=" * 70)

# Survey items (not predictors — respondent-facing questions)
old_items = 130  # ~18 Ben + 5 COVID + ~80 tech checkboxes + 27 certs + ~26 acts + ~14 core
new_items = 62

old_minutes = 30  # estimated
new_minutes = 14  # estimated from REDESIGN_2026.md

print(f"\n{'Metric':<40} {'Old':>12} {'New':>12} {'Improvement':>15}")
print("-" * 80)
print(f"{'Survey items':<40} {old_items:>12} {new_items:>12} {(1-new_items/old_items)*100:>14.0f}%")
print(f"{'Est. completion time (min)':<40} {old_minutes:>12} {new_minutes:>12} {(1-new_minutes/old_minutes)*100:>14.0f}%")
print(f"{'R²':<40} {old_r2:>12.4f} {new_r2:>12.4f} {(new_r2 - old_r2):>+14.4f}")
print(f"{'R² per survey item':<40} {old_r2/old_items:>12.5f} {new_r2/new_items:>12.5f} "
      f"{(new_r2/new_items)/(old_r2/old_items) - 1:>+14.0%}")
print(f"{'R² per minute of respondent time':<40} {old_r2/old_minutes:>12.5f} {new_r2/new_minutes:>12.5f} "
      f"{(new_r2/new_minutes)/(old_r2/old_minutes) - 1:>+14.0%}")
print(f"{'Usable responses (completion effect)':<40} {old_n:>12,} {new_n:>12,} {new_n-old_n:>+14,}")
print(f"{'Effective info (R² × N)':<40} {old_r2*old_n:>12,.0f} {new_r2*new_n:>12,.0f} "
      f"{(new_r2*new_n)/(old_r2*old_n) - 1:>+14.0%}")

# ────────────────────────────────────────────────────────────────
# PART 10: New predictors — added explanatory power
# ────────────────────────────────────────────────────────────────
print()
print("=" * 70)
print("INCREMENTAL R² FROM NEW PREDICTORS")
print("=" * 70)

# Fit baseline model matching old-equivalent predictors on new data
old_equiv_cols = ["experience_tech", "english", "is_female"]
# Add city and work arrangement dummies
old_equiv_X = new_X_complete[old_equiv_cols].copy()
# Add remote-like column from work arrangement
old_equiv_X["remote_approx"] = (new_X_complete.filter(like="work_Fully remote").sum(axis=1) +
                                 new_X_complete.filter(like="work_Hybrid").sum(axis=1) +
                                 new_X_complete.filter(like="work_Nomadic").sum(axis=1)).clip(0, 1)
old_equiv_X = pd.concat([old_equiv_X, new_X_complete.filter(like="city_")], axis=1)

base_Xm = np.column_stack([np.ones(new_n), old_equiv_X.values.astype(float)])
base_c, _, _, _ = lstsq(base_Xm, new_y_complete, rcond=None)
base_pred = base_Xm @ base_c
base_ss_res = np.sum((new_y_complete - base_pred) ** 2)
base_r2 = 1 - base_ss_res / new_ss_tot

# Incrementally add each new block
blocks = {
    "seniority_level": new_X_complete.filter(like="seniority_"),
    "company_size": new_X_complete.filter(like="compsize_"),
    "industry": new_X_complete.filter(like="industry_"),
    "english_use": new_X_complete[["english_use"]],
    "experience_total + tenure": new_X_complete[["experience_total", "tenure_current"]],
    "primary_role": new_X_complete.filter(like="role_"),
    "primary_language": new_X_complete.filter(like="lang_"),
    "work_arrangement (expanded)": new_X_complete.filter(like="work_"),
    "cert_depth (has + count)": new_X_complete[["has_certs", "cert_count"]],
    "tech_depth (lang_yrs + breadth)": new_X_complete[["primary_lang_years", "tech_breadth"]],
}

incremental_results = []
cumulative_X = old_equiv_X.copy()
prev_r2 = base_r2

print(f"\nBaseline (old-equivalent predictors on new data): R² = {base_r2:.4f}")
print(f"\n{'Block':<35} {'Δ R²':>10} {'Cumulative R²':>15} {'Predictors added':>18}")
print("-" * 80)

for block_name, block_df in blocks.items():
    cumulative_X = pd.concat([cumulative_X, block_df.reset_index(drop=True)], axis=1)
    Xm = np.column_stack([np.ones(new_n), cumulative_X.values.astype(float)])
    c, _, _, _ = lstsq(Xm, new_y_complete, rcond=None)
    pred = Xm @ c
    ss_res = np.sum((new_y_complete - pred) ** 2)
    r2 = 1 - ss_res / new_ss_tot
    delta = r2 - prev_r2
    n_added = block_df.shape[1]
    incremental_results.append((block_name, delta, r2, n_added))
    print(f"  + {block_name:<33} {delta:>+9.4f} {r2:>14.4f} {n_added:>17}")
    prev_r2 = r2

print(f"\nTotal R² gained from new predictors: {prev_r2 - base_r2:+.4f} "
      f"({base_r2:.4f} → {prev_r2:.4f})")

# ────────────────────────────────────────────────────────────────
# PART 11: Save results to CSV
# ────────────────────────────────────────────────────────────────
summary = pd.DataFrame({
    "Metric": [
        "Predictors (k)", "Usable N", "R²", "Adjusted R²", "ESR",
        "Survey items", "Est. completion (min)", "R² per item",
        "R² per minute", "Mean VIF", "VIF > 5 count", "VIF > 10 count",
        "Mean bootstrap CV", "Tech block mean sparsity"
    ],
    "Old Design": [
        old_k, old_n, round(old_r2, 4), round(old_adj_r2, 4), round(old_esr, 0),
        old_items, old_minutes, round(old_r2/old_items, 5),
        round(old_r2/old_minutes, 5), round(old_vif_series.mean(), 2),
        old_vif_gt5, old_vif_gt10,
        round(old_cv.mean(), 3), f"{old_mean_sparsity:.1%}"
    ],
    "New Design": [
        new_k, new_n, round(new_r2, 4), round(new_adj_r2, 4), round(new_esr, 0),
        new_items, new_minutes, round(new_r2/new_items, 5),
        round(new_r2/new_minutes, 5), round(new_vif_series.mean(), 2),
        new_vif_gt5, new_vif_gt10,
        round(new_cv.mean(), 3), f"{new_mean_sparsity:.1%}"
    ],
})
summary.to_csv(os.path.join(OUT_DIR, "comparison_summary.csv"), index=False)

incremental_df = pd.DataFrame(incremental_results,
                               columns=["Block", "Delta_R2", "Cumulative_R2", "Predictors_Added"])
incremental_df.to_csv(os.path.join(OUT_DIR, "incremental_r2.csv"), index=False)

old_vif_series.to_frame("VIF").to_csv(os.path.join(OUT_DIR, "old_vif.csv"))
new_vif_series.to_frame("VIF").to_csv(os.path.join(OUT_DIR, "new_vif.csv"))

print()
print("=" * 70)
print(f"Results saved to {OUT_DIR}/")
print("  comparison_summary.csv  — side-by-side metrics")
print("  incremental_r2.csv      — R² gain per new block")
print("  old_vif.csv             — VIF values for old design")
print("  new_vif.csv             — VIF values for new design")
print("=" * 70)

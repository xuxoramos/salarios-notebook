# SG Tech Pulse — "¿Dónde está tu sueldo?" result page

Post-survey page that shows each SurveySparrow respondent where their base
salary lands in the live distribution of responses, with a red marker and
percentile — plus same-level and same-experience percentiles, the
English-usage salary ladder, and two AI modules (skills-relevance confidence
1–5, and how code gets written: by hand vs. instructing agents). Deployed at
**https://thedata.pub/pulse/mi-resultado**.

Subgroup comparisons only render when the cell has enough respondents
(`MIN_CELL = 25` server-side; the page applies similar floors), and the
confidence module deliberately shows no salary linkage.

## How it works

1. **Seed**: `seed.py` loads a SurveySparrow CSV dump into SQLite
   (`submissions` table, keyed by Submission Id).
2. **Webhook**: SurveySparrow POSTs each new submission to
   `https://thedata.pub/pulse/webhook` (secret-token auth). The app extracts
   the base-salary MXN/USD, level, and role answers — matched by
   question-text prefix, so question-id remaps can't break ingestion — and
   upserts them.
3. **Redirect**: the survey's thank-you page redirects to
   `https://thedata.pub/pulse/mi-resultado?sid={submission_id}`. The page
   fetches the binned distribution plus that submission's salary/percentile
   and draws the marker. If `sid` is missing or can't be resolved, the page
   falls back to a local input: the visitor types a salary and the percentile
   is computed client-side from the quantile grid (nothing leaves the browser).

Salary conventions match `docs/GENERAL_FINDINGS_2026.md`: base monthly salary
normalized to MXN (USD × FX 18.5), trimmed to $8k–$400k.

Anti-enumeration: `api/me` only resolves submissions that arrived via webhook
within the last `PULSE_SID_TTL_HOURS` (default 48), and is rate-limited per
IP — historical sequential Submission Ids cannot be walked to read salaries.

## SurveySparrow configuration (done in their UI)

- **Webhook** (Integrations → Webhooks, event *Submission Completed*):
  URL `https://thedata.pub/pulse/webhook`; custom header `X-Secret-Token` =
  the value of `PULSE_WEBHOOK_SECRET` in `/etc/sg-pulse.env` on the server.
  Content template (fill each `{...}` from the $ placeholder picker):

  ```json
  {
    "submission_id": "{submission id}",
    "salary_mxn":    "{answer: salario base mensual en pesos}",
    "salary_usd":    "{answer: salario base mensual en dólares}",
    "level":         "{answer: nivel dentro de la organización}",
    "role":          "{answer: función o actividad principal}",
    "years_tech":    "{answer: años en el sector tecnológico}",
    "english_usage": "{answer: frecuencia de inglés en el trabajo}",
    "foreign_employer": "{answer: empresa en el mismo país (Yes/No)}",
    "ai_confidence": "{answer: habilidades relevantes en 3 años (1-5)}",
    "ai_coding":     "{answer: cómo utilizas la IA para crear código}"
  }
  ```

  The left-hand key names are load-bearing; empty or unreplaced placeholders
  are handled. Categorical answers are matched by text prefix
  (see `ENGLISH_ORDER` / `AI_CODING_ORDER` in `app.py`).
- **Thank-you page redirect**: enable Page Redirect with URL
  `https://thedata.pub/pulse/mi-resultado?sid={submission_id}` (pick the
  submission-id variable from the redirect field's variable picker; if the
  plan doesn't offer one, use the URL without `?sid=…` — the fallback input
  still works).

## Server layout (hetzner-web)

- App: `/opt/sg-pulse` (venv + `app.py` + `pulse.db`), runs as user `sgpulse`.
- Service: `systemd` unit `sg-pulse` → uvicorn on `127.0.0.1:8020`
  (8010 is taken by dssg-calibration). Env in `/etc/sg-pulse.env`
  (`PULSE_DB`, `PULSE_WEBHOOK_SECRET`, `PULSE_FX`, optional
  `PULSE_SURVEY_URL` to show a share link, `PULSE_SID_TTL_HOURS`).
- Apache: `ProxyPass /pulse http://127.0.0.1:8020/pulse` inside the
  `thedata.pub` `*:443` vhost (`deploy/apache-pulse.conf` mirrors it;
  pre-change backup at `/root/thedata.pub-le-ssl.conf.bak-pulse`).

## Operations

```bash
# redeploy after editing app.py
scp pulse-result/app.py hetzner-web:/opt/sg-pulse/ && ssh hetzner-web 'systemctl restart sg-pulse'

# re-seed from a fresh dump (webhook rows are never overwritten)
scp "data/<dump>.csv" hetzner-web:/opt/sg-pulse/data/dump.csv
ssh hetzner-web 'cd /opt/sg-pulse && PULSE_DB=/opt/sg-pulse/pulse.db venv/bin/python seed.py data/dump.csv && chown sgpulse:sgpulse pulse.db*'

# logs / health
ssh hetzner-web 'journalctl -u sg-pulse -n 50 --no-pager'
curl https://thedata.pub/pulse/health
```

Debugging ingestion: every webhook body is stored verbatim in the
`raw_events` table, so a payload-shape surprise can be inspected after the
fact.

## Local development

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
PULSE_DB=/tmp/pulse.db .venv/bin/python seed.py
PULSE_DB=/tmp/pulse.db PULSE_WEBHOOK_SECRET=dev .venv/bin/uvicorn app:app --port 8020
# open http://127.0.0.1:8020/pulse/mi-resultado
```

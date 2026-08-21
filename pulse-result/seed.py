"""Seed the pulse SQLite DB from a SurveySparrow CSV dump.

Usage: python seed.py [path-to-dump.csv]

Idempotent: rows are upserted by Submission Id. Webhook rows are never
overwritten by seed rows (seed data is the same submission, just older).
"""
import csv
import sys
import os
from datetime import datetime, timezone

from app import (
    ALL_FIELDS, DB_PATH, UPSERT_SQL, db, init_db, match_field,
    normalize_salary, parse_field,
)

DEFAULT_DUMP = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "data", "Salarios2026-Dump - Encuesta de Salarios SG 2026.csv",
)


def parse_submitted(value):
    try:
        dt = datetime.strptime(value.strip(), "%b %d, %Y %I:%M %p")
        return dt.replace(tzinfo=timezone.utc).isoformat()
    except (ValueError, AttributeError):
        return datetime.now(timezone.utc).isoformat()


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DUMP
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    col = {}
    for i, h in enumerate(header):
        field = match_field(h)
        if field and field not in col:
            col[field] = i
    meta = {name: header.index(name) for name in ("Submission Id", "CompletionStatus", "Submitted Time")}
    missing = sorted(ALL_FIELDS - col.keys())
    if missing:
        sys.exit(f"could not locate columns for: {missing}")

    init_db()
    seeded = with_salary = 0
    with db() as conn:
        for r in rows:
            sid = r[meta["Submission Id"]].strip()
            if not sid:
                continue
            existing = conn.execute(
                "SELECT source FROM submissions WHERE id = ?", (sid,)
            ).fetchone()
            if existing and existing[0] == "webhook":
                continue
            fields = {f: parse_field(f, r[col[f]]) for f in ALL_FIELDS}
            norm = normalize_salary(fields["salary_mxn"], fields["salary_usd"])
            conn.execute(
                UPSERT_SQL,
                {
                    "id": sid,
                    **fields,
                    "salary_norm": norm,
                    "completed": 1 if r[meta["CompletionStatus"]].strip() == "Completed" else 0,
                    "source": "seed",
                    "received_at": parse_submitted(r[meta["Submitted Time"]]),
                },
            )
            seeded += 1
            if norm is not None:
                with_salary += 1

    print(f"db: {DB_PATH}")
    print(f"seeded {seeded} submissions ({with_salary} with a usable base salary)")


if __name__ == "__main__":
    main()

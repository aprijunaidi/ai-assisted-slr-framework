#!/usr/bin/env bash
# Runs every script on small SYNTHETIC fixtures (not real bibliographic records).
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=$(mktemp -d)
python scripts/dedup_ris.py tests/fixtures/db_a.ris tests/fixtures/db_b.ris --out "$OUT/merged.ris" --log "$OUT/dedup_log.csv"
python scripts/qa_score.py tests/fixtures/qa.csv --threshold 50 --mandatory QA1 QA6 --out "$OUT/qa_results.csv"
python scripts/qa_score.py tests/fixtures/screen.csv --kappa reviewer1_ta reviewer2_ta
python scripts/prisma_flow.py tests/fixtures/prisma.csv --out "$OUT/prisma_flow.png"
python scripts/bibliometrics.py "$OUT/merged.ris" --out "$OUT/bibliometrics"
echo "All scripts ran successfully. Outputs in $OUT"

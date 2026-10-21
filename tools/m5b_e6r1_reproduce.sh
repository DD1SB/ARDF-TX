#!/usr/bin/env bash
# Read review/M5B-E6R1/REPRODUCE.md before execution. No CAD export or hardware IO.
set -euo pipefail
cd "$(dirname "$0")/.."
analysis_python="${ARDF_E6R1_PYTHON:-/tmp/m5b-e6-py312/bin/python}"
analysis_logs=hardware/2m/review/M5B-E6R1/logs
mkdir -p "$analysis_logs"
export MPLCONFIGDIR=/tmp/m5b-e6-matplotlib
for analysis_stage in morse power electrical spice thermal sensor cooling budget regression figures; do
    "$analysis_python" "tools/m5b_e6r1_${analysis_stage}.py" > "$analysis_logs/reproduction-${analysis_stage}.log" 2>&1
    printf '%s PASS (execution only; engineering disposition HOLD)\n' "$analysis_stage"
done
"$analysis_python" tools/test_m5b_e6_analysis.py > "$analysis_logs/reproduction-E6-tests.log" 2>&1
"$analysis_python" tools/test_m5b_e6r1_analysis.py > "$analysis_logs/reproduction-R1-tests.log" 2>&1
"$analysis_python" tools/m5b_e6r1_execution.py
"$analysis_python" tools/m5b_e6r1_inventory.py
printf '25 E6 +37 R1 tests executed; see raw logs and decision. No PCB implementation.\n'

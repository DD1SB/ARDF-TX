# Reproduce M5B-E6R1 analysis

Read this complete document before running commands. These commands write **only new E6R1 analysis evidence** and its inventory. They do not export or alter native CAD/historical reviews, access hardware, publish Git refs or generate fabrication. The engineering outcome is HOLD even when execution/tests pass.

Starting history must contain `85186204619edec32ad1bb2a3044bb55ea399658`. Run from the repository root on the E6 development branch. `preserved-start.json` checks 2,831 starting tracked files; only root README and docs index may differ. It preserves all original E6 scripts, inputs, failure evidence, native boards and historical fabrication archives. Do not execute old E6 model mains: those write the frozen E6 review directory. The old **test** entry point is read-only.

Actual environment: Linux x86_64, glibc 2.39, Python 3.12.3, KiCad CLI/pcbnew 10.0.6, NumPy 2.5.4, SciPy 1.18.1, Matplotlib 3.11.2, ngspice 42. pcbnew loads the actual E5 PCB read-only to check source-via thermal storage. No ERC/DRC was rerun in this analysis-only milestone. Existing E6 native replay evidence is historical and explicitly remains so.

The executed interpreter was `/tmp/m5b-e6-py312/bin/python`, a venv with system-site access to the matching pcbnew Python binding. For another environment, create an equivalent Python 3.12 environment with `--system-site-packages` and install the pinned numerical dependencies in `requirements.txt`. The system must provide matching KiCad/pcbnew and ngspice. Dependency installation is not performed by the runner. Set `ARDF_E6R1_PYTHON` to that interpreter if different. No network is required once dependencies are available.

Executed final procedure:

```bash
git status --short --branch
git rev-parse HEAD
ARDF_E6R1_PYTHON=/tmp/m5b-e6-py312/bin/python bash tools/m5b_e6r1_reproduce.sh
sha256sum -c hardware/2m/review/M5B-E6R1/SHA256SUMS.txt
git diff --check
```

The runner executes these exact commands, each with stdout/stderr recorded in `logs/reproduction-<stage>.log`:

```bash
export MPLCONFIGDIR=/tmp/m5b-e6-matplotlib
/tmp/m5b-e6-py312/bin/python tools/m5b_e6r1_morse.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6r1_power.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6r1_electrical.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6r1_spice.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6r1_thermal.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6r1_sensor.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6r1_cooling.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6r1_budget.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6r1_regression.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6r1_figures.py
/tmp/m5b-e6-py312/bin/python tools/test_m5b_e6_analysis.py
/tmp/m5b-e6-py312/bin/python tools/test_m5b_e6r1_analysis.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6r1_execution.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6r1_inventory.py
```

The fresh run must report 25 old numerical tests and 37 R1 tests with zero failures/errors/skips, ngspice return 0 and energy checks passing. R1 tests independently check Morse arithmetic, energy domains/storage, identical E6-network propagation, matrix exponential observer behavior, native critical nets, complete 64 gate combinations, slot inhibition, transient integration, ideal-spectrum comparison and detection of unsafe local-fault/healthy-threshold cases. They intentionally require the unsafe cases to remain unsafe. A test PASS is not approval of an overtemperature scenario.

Exact command settings and counts are in [execution evidence](EXECUTION.md). Re-running overwrites only generated R1 numerical/figure outputs and `reproduction-*.log`; archived development/failure logs retain their names. JSON/CSV numeric comparisons should be identical in the pinned environment to numerical precision. PDF/PNG bytes may vary with rendering-library/font metadata across hosts; no such output is manufacturing data. The SHA inventory captures actual artifacts in this run and is refreshed by the last command. Original primary PDFs were downloaded outside the repository for reference and are not vendored.

No acceptance tag, fabrication ZIP, stencil, cutouts, native E6R1 3D assembly or PCB is produced. [Review decision](../../../../docs/M5B_E6R1_REVIEW_DECISION.md) is the controlling engineering disposition.

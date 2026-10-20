# Reproduce the M5B-E6 analysis HOLD

Read this document fully. This procedure calculates an **analysis HOLD**, not a fabrication acceptance. Never run old generators against active sources or frozen reports. No E6 CAD/fabrication export is expected. Existing native inputs remain E5.

## Environment actually used

Linux x86-64/glibc 2.39; KiCad/pcbnew 10.0.6; `/usr/bin/python3` 3.12.3. Temporary uv 0.12.18 environment `/tmp/m5b-e6-py312`, with system site packages for matching pcbnew, NumPy 2.5.4, SciPy 1.18.1, Matplotlib 3.11.2 and Pillow 13.0.0. Those analytical dependencies were installed only in `/tmp`; no repository environment or system package was changed. Standard C/C++ fixture work was not needed because no firmware changed. Existing RF2M verification is Python/native KiCad.

Example environment setup using the recorded versions (requires their availability):

```sh
uv --cache-dir /tmp/m5b-e6-uv-cache venv --python /usr/bin/python3 --system-site-packages /tmp/m5b-e6-py312
uv --cache-dir /tmp/m5b-e6-uv-cache pip install --python /tmp/m5b-e6-py312/bin/python numpy==2.5.4 scipy==1.18.1 matplotlib==3.11.2 pillow==13.0.0
```

Run from repository root. Preserve an existing nonempty `/tmp` work directory rather than deleting it. The commands below use the exact paths used in this run; choose a new clone path on another reproduction and pass it to the evidence assembler. `m5b_e6_common.guard()` protects all controller/RF80/historical RF2M review inputs from the starting commit. Native hash checks add protection for the active E5 project.

## Power, source and transient commands executed

```sh
/tmp/m5b-e6-py312/bin/python tools/m5b_e6_power.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6_sources.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6_thermal.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6_stress.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6_faults.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6_closure.py
/usr/bin/python3 tools/m5b_e6_costs.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6_concept.py
/tmp/m5b-e6-py312/bin/python tools/m5b_e6_run_tests.py
```

Each command's stdout/stderr was captured under `/tmp/m5b-e6/logs/` and copied to `logs/`. The run-tests command executes the suite and records actual counts, not historical PASS text. Results: 25 tests, 0 failures/errors. Original development failures remain beside corrected runs. PDF/PNG/SVG export metadata can differ; numeric values/input hashes and plotted data are the reproducibility authorities. An exit-zero calculation means completed computation, not a GO decision. The closure file explicitly records HOLD.

## Fresh native baseline regression, isolated output

The disposable clone was created from the clean starting commit before E6 additions:

```sh
git clone --no-hardlinks /home/stefan/src/ardf-tx /tmp/m5b-e6-baseline-regression
git -C /tmp/m5b-e6-baseline-regression checkout --detach 256c64888b680f5152e92f035e2ea0676a83630a
cp tools/m5b_e6_baseline_replay.py /tmp/m5b-e6-baseline-regression/tools/
```

Then from `/tmp/m5b-e6-baseline-regression`:

```sh
/usr/bin/python3 tools/m5b_e6_baseline_replay.py checks
/usr/bin/python3 tools/m5b_e6_baseline_replay.py verify
/usr/bin/python3 tools/m5b_e6_baseline_replay.py models
/usr/bin/python3 tools/m5b_e6_baseline_replay.py dfm
/usr/bin/python3 tools/m5b_e6_baseline_replay.py thermal
/usr/bin/python3 tools/m5b_e6_baseline_replay.py engineering
/usr/bin/python3 tools/m5b_e6_baseline_replay.py ground
/usr/bin/python3 tools/m5b_e6_baseline_replay.py closure
```

Native writers must finish before another starts. The wrapper redirects to the new `review/M5B-E6/baseline-regression` path, copies only frozen input fixtures/profile, and checks tracked native hashes. It does not modify old electrical/DFM/package thresholds. `engineering` depends on the fresh thermal output: the original failed attempt before that dependency is retained, followed by the successful rerun. Ground/closure are analytical reads; no routing is written. Native checks execute actual KiCad hierarchy ERC, netlist export, refill+DRC/parity and report export; exact CLI arguments/stdout/stderr are in `baseline-regression/check-commands.json`.

Expected unchanged-E5 baseline: ERC zero findings; DRC zero errors, 11 existing missing-courtyard warnings; zero unrouted/parity; 4,096 enable combinations, 39 states, 320 native package checks; 19+18 electrical negatives; 18 compact+16 source geometry+4 thermal negatives; 11 DFM negatives. Existing annulus preferred-margin exceptions remain explicit. This baseline replay is not an E6 zero-warning CAD result.

From the main working repository, collect the evidence only after commands complete:

```sh
/usr/bin/python3 tools/m5b_e6_evidence.py /tmp/m5b-e6-baseline-regression /tmp/m5b-e6/logs
sha256sum --check hardware/2m/review/M5B-E6/SHA256SUMS.txt
git diff -- hardware/2m/RF2M.kicad_pcb hardware/2m/RF2M.kicad_sch hardware/2m/RF2M.kicad_pro hardware/2m/RF2M.electrical.json hardware/controller hardware/80m
```

Hash regeneration binds the locally regenerated data. The committed manifest checks the archived evidence; it should not be compared byte-for-byte after PDF/log/date regeneration. Native/historical source hashes must remain identical. All toolchain/parameter assumptions and the unresolved source/RF-loss bound must be reviewed before changing the engineering disposition.

Copied baseline CSVs use LF line endings; generated concept SVG path-line trailing spaces are trimmed. These are text-format normalizations only, with no numerical/geometry change. Raw test/failure logs are copied unchanged.

#!/usr/bin/env python3
"""Documentation/model consistency; not RF hardware qualification."""
import csv
import json
import math
from pathlib import Path
import re
import m2_rf_analysis
import m2_system_costs

ROOT = Path(__file__).resolve().parents[1]


def main():
    errors = []
    docs = ["M2_PREPARATION.md", "M2_VHF_RF_REVIEW.md", "M2_HF_CIRCUIT_PROPOSALS.md",
            "M2_RF_EVALUATION.md", "M2_SYSTEM_COST.md", "M2_SOURCES.md", "M2_POWER_BUDGET.md", "M2_CHECKS.md"]
    for name in docs:
        path = ROOT / "docs" / name
        if not path.exists() or "2026-10-13" not in path.read_text():
            errors.append("Missing/undated preparation document: " + name)
    plan = (ROOT / "docs/M2_RF_EVALUATION.md").read_text()
    gates = set(re.findall(r"\| (G\d) ", plan))
    if gates != {"G" + str(i) for i in range(10)}:
        errors.append("Evaluation gate matrix incomplete")
    d = m2_rf_analysis.calculations()
    rf_doc = (ROOT / "docs/M2_VHF_RF_REVIEW.md").read_text()
    for row in d["vhf"]["gain_cases"]:
        token = f"{row['headroom_to_typ_p1db_db']:.2f}".replace("-", "−")
        if token not in rf_doc:
            errors.append("Driver headroom table inconsistent: " + token)
    prep = (ROOT / "docs/M2_PREPARATION.md").read_text()
    if len(set(re.findall(r"\| PREP-\d+ \|", prep))) != 8:
        errors.append("Missing preparation trace")
    rows = list(csv.DictReader((ROOT / "analysis/hf_lpf_ideal.csv").open()))
    epsilon2 = 10 ** 0.01 - 1
    max_error = 0.0
    for row in rows:
        f = float(row["frequency_hz"])
        butter = -10 * math.log10(1 + (f / 4.2e6) ** 10)
        x = f / 4.1e6
        tn = math.cos(7 * math.acos(x)) if x <= 1 else math.cosh(7 * math.acosh(x))
        cheby = -10 * math.log10(1 + epsilon2 * tn ** 2)
        max_error = max(max_error, abs(float(row["butterworth_db"]) - butter),
                        abs(float(row["chebyshev_db"]) - cheby))
    if len(rows) != 496 or max_error > 0.005:
        errors.append("Actual ideal-SPICE results differ from independent transfer calculation")
    costs = m2_system_costs.report()
    if len(costs["standalone_boards"]) != 12:
        errors.append("Standalone PCB/batch comparison incomplete")
    if len(d["operating_profiles"]) != 9 or len(d["universal_single_band_sensitivity"]) != 4:
        errors.append("Pack/profile or installed-board standby scope incomplete")
    if any(r["fabricated_count_per_design"] < r["batch"] for r in costs["rows"]):
        errors.append("Fabrication allowance undercounts boards")
    for r in costs["rows"]:
        if not r["material_eur"][0] <= r["material_eur"][1] <= r["material_eur"][2]:
            errors.append("Cost sensitivity ordering invalid")
    decision = (ROOT / "docs/decisions/ADR-0007-cost-optimized-m1.md").read_text()
    proposal = (ROOT / "docs/decisions/ADR-0008-rf-evaluation-gates.md").read_text()
    if "Conditionally accepted" not in decision or "Proposed" not in proposal:
        errors.append("ADR state does not reflect review scope")
    print(json.dumps({"preparation_documents": len(docs), "review_requirements": 8,
                      "go_no_go_gates": len(gates), "actual_ideal_spice_rows": len(rows),
                      "spice_vs_formula_max_error_db": round(max_error, 6),
                      "all_in_baskets": len(costs["rows"]),
                      "standalone_board_baskets": len(costs["standalone_boards"]),
                      "revised_profile_rows": len(d["operating_profiles"]),
                      "universal_idle_sensitivity_rows": len(d["universal_single_band_sensitivity"]),
                      "hardware_tests": "NOT RUN",
                      "errors": errors}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()

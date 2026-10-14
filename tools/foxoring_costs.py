#!/usr/bin/env python3
"""Foxoring material audit only: no procurement, PCB design or firmware."""
import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP
import io
import json
from pathlib import Path
import m1_costs

ROOT = Path(__file__).resolve().parents[1]
D = Decimal
EXTRA = json.loads((ROOT / "docs/FOXORING_COST_PARTS.json").read_text())["parts"]
PARTS = {**m1_costs.PARTS, **EXTRA}
BATCHES = (10, 20)
CORE = m1_costs.population(["controller", "80m", "compact80"], fox_only=True)
ADDITIONS = [
    ("low_guard", "LOWGUARD", 1),
    ("pack", "CELL25R", 2), ("pack", "CELLTABS", 2), ("pack", "PACKPCM", 1),
    ("qualification_reserve", "PCMRESERVE", 1),
    ("pack", "PACKFUSE", 1), ("pack", "PACKPAPER", 1), ("pack", "PACKSHRINK", 1),
    ("pack", "PACKREST", 1), ("pack", "PACKLEADS", 1),
    ("power_connector", "POWERPLUG", 4), ("low_connector", "LOWPORT", 1),
    ("harness", "POWERWIRE", 1), ("harness", "LOGICWIRE", 1),
    ("harness", "RFWIRE", 1), ("harness", "HARNESSREST", 1),
    ("fabrication", "FABCTRL", 1), ("fabrication", "FABRF", 1),
    ("enclosure", "SHELL", 1), ("enclosure", "BOARDMOUNT", 1),
    ("enclosure", "GROMMETS", 1), ("enclosure", "CASESEAL", 1),
    ("assembly_material", "CONSUMABLE", 1), ("assembly_material", "LABEL", 1),
]


def money(value):
    return str(D(value).quantize(D(".01"), rounding=ROUND_HALF_UP))


def quote(part, needed):
    minimum = max(needed, part["moq"])
    ordered = (minimum + part["multiple"] - 1) // part["multiple"] * part["multiple"]
    point = max(int(q) for q in part["price_breaks_eur"] if int(q) <= ordered)
    return ordered, D(str(part["price_breaks_eur"][str(point)])), point


def report():
    old = json.loads((ROOT / "docs/M2_SYSTEM_COST.json").read_text())
    reports = []
    for n in BATCHES:
        core_basket = m1_costs.basket(CORE, n)
        lines = []
        # Allocate pooled M1 purchased material exactly, without duplicating a MPN's basket.
        for row in CORE:
            pid = row["part_id"]
            p = core_basket["purchases"][pid]
            cost = D(p["batch_eur"]) * D(row["qty"] * n) / D(p["needed"])
            lines.append({"group": row["board"], "part_id": pid, "qty_per_unit": row["qty"],
                          "needed": row["qty"] * n, "ordered_allocated": row["qty"] * n,
                          "unit_eur": p["unit_eur"], "batch_eur_exact": str(cost),
                          "per_unit_eur_exact": str(cost / n), "evidence": PARTS[pid]["evidence"]})
        for group, pid, qty in ADDITIONS:
            ordered, price, point = quote(PARTS[pid], n * qty)
            cost = ordered * price
            lines.append({"group": group, "part_id": pid, "qty_per_unit": qty,
                          "needed": n * qty, "ordered_allocated": ordered, "price_break": point,
                          "unit_eur": str(price), "batch_eur_exact": str(cost),
                          "per_unit_eur_exact": str(cost / n), "evidence": PARTS[pid]["evidence"]})
        grouped = {}
        classified = {}
        for r in lines:
            v = D(r["batch_eur_exact"])
            grouped[r["group"]] = grouped.get(r["group"], D(0)) + v
            evidence = "OBSERVED" if r["evidence"].startswith("OBSERVED") else r["evidence"]
            classified[evidence] = classified.get(evidence, D(0)) + v
        unit_budget_batch = sum(grouped.values(), D(0))
        unit_candidate_batch = unit_budget_batch - grouped["qualification_reserve"]
        shared = []
        for pid, qty in (("CHARGER", n // 10), ("CHARGEADAPTER", n // 10), ("PROVISION", 1)):
            ordered, price, point = quote(PARTS[pid], qty)
            shared.append({"part_id": pid, "qty_per_fleet": ordered, "unit_eur": str(price),
                           "batch_eur": money(ordered * price), "evidence": PARTS[pid]["evidence"]})
        shared_batch = sum((D(r["batch_eur"]) for r in shared), D(0))
        # Preserve old EUR60 freight assumption for the recommended budget.
        # A consolidated EUR40 case is shown only as an unquoted optimization sensitivity.
        freight = D("60")
        fleet = unit_budget_batch + shared_batch + freight
        old_row = next(r for r in old["rows"] if r["configuration"].startswith("Fox-only")
                       and r["batch"] == n and r["pack"] == "2S1P")
        historical_baseline = D(core_basket["per_unit_eur"])
        old_additions = {k: str(D(str(v[1]))) for k, v in old_row["items"].items()
                         if not k.startswith("PCB components") and not k.startswith("Complete compact")}
        bridge = {"Additional RF guard provision": str(old_row["M2_increment_eur"]), **old_additions}
        reports.append({"batch": n, "m1_baseline_per_unit_eur": str(historical_baseline),
            "m1_baseline_batch_eur": core_basket["batch_eur"], "old_m2_per_unit_eur": str(old_row["material_eur"][1]),
            "old_scope_additions": bridge,
            "old_minus_m1_eur": money(D(str(old_row["material_eur"][1])) - historical_baseline),
            "unit_candidate_eur": money(unit_candidate_batch / n),
            "unit_budget_incl_bms_reserve_eur": money(unit_budget_batch / n),
            "unit_budget_batch_eur": money(unit_budget_batch),
            "shared_equipment_batch_eur": money(shared_batch), "freight_budget_batch_eur": money(freight),
            "fleet_budget_eur": money(fleet), "fleet_budget_per_unit_eur": money(fleet / n),
            "fleet_with_eur40_freight_per_unit_eur": money((fleet - 20) / n),
            "candidate_fleet_per_unit_eur": money((fleet - grouped["qualification_reserve"]) / n),
            "one_charger_per_unit_per_unit_eur": money((unit_budget_batch + n * D(16) + D(5) + freight) / n),
            "groups_per_unit": {k: str(v / n) for k, v in grouped.items()},
            "evidence_batch_eur": {k: money(v) for k, v in classified.items()},
            "unit_lines": lines, "shared_lines": shared, "core_pooled_purchases": core_basket["purchases"]})
    # A lower-capacity cell changes the endurance inputs explicitly, not RF performance.
    capacity_cases = []
    for capacity in (D("2.50"), D("2.45")):
        usable = D("7.2") * capacity * D("0.8") * D("0.9") * D("0.9")
        capacity_cases.append({"cell_ah": str(capacity), "usable_wh": str(usable),
              "hours_at_035w": str(usable / D(".350")), "hours_with_lora_rx_0395w": str(usable / D(".395")),
              "maximum_mean_w_for_24h": str(usable / 24)})
    return {"date": "2026-10-13", "classification": "CANDIDATE, OBSERVED PRICES + EXPLICIT ALLOWANCES; NOT ORDERED/VALIDATED",
            "tax": "EUR ex VAT planning; labor/instruments/spares excluded and open; baseline estimates retained",
            "unpriced_scopes": {"labor": "OPEN: assembly, pack/tab connections, winding, programming, calibration and field work",
                                "capital": "OPEN: computer, workshop tools, calibrated RF/pack instrumentation or hire",
                                "yield_and_spares": "OPEN: one accepted unit per planned material set is assumed",
                                "bulk_material_minimums": "OPEN: allowance sets are not verified roll/container purchase minima"},
            "batches": reports, "cell_capacity_sensitivity": capacity_cases}


def render(data):
    out = ["# Foxoring-only itemized candidate BOM", "", "Date: **2026-10-13**. **No parts purchased; no ordering release or hardware validation.**", "",
           "Generated by `python3 tools/foxoring_costs.py --write`. Read [the audit](FOXORING_COST_AUDIT.md) for "
           "scope, sources, safety/qualification and TinyFox/Fixle comparison. The original M1/M2 figures remain historical records.", "",
           "ESP32-S3/RTC controller and the **same 80 m PCB with the M1 Fox-only population** are unchanged. "
           "Silicontra LoRa footprint remains unpopulated; optional module and RF/antenna additions cost zero in this population. "
           "The optional-footprint contract is retained; exact Silicontra MPN/land pattern remains OPEN as in M1, with no layout claim. "
           "No fourth transmitter PCB or replacement MCU. The protection circuit to be procured belongs inside the external battery pack.", "",
           "Prices are EUR ex VAT planning. OBSERVED means a supplier observation, not purchased or qualified. ESTIMATE means "
           "unquoted material allowance; RESERVE is unspent provision, not a physical line item. Exact electrical values, footprints "
           "and stock remain open. All quoted discounts use actual aggregated same-MPN quantities.", "",
           "## Totals and cost scopes", "", "| Scope | Ten units: EUR/unit | Twenty units: EUR/unit |", "| --- | ---: | ---: |"]
    fields = [("Preserved M1 controller/RF/compact antenna", "m1_baseline_per_unit_eur"),
              ("Old M2 scope, individual charger + allocations", "old_m2_per_unit_eur"),
              ("Candidate complete unit material, including protected pack", "unit_candidate_eur"),
              ("Recommended unit material budget, including BMS replacement reserve", "unit_budget_incl_bms_reserve_eur"),
              ("Recommended fleet cash budget per unit, shared charging + EUR60 freight", "fleet_budget_per_unit_eur"),
              ("Candidate fleet if EUR1.29 BMS passes qualification", "candidate_fleet_per_unit_eur"),
              ("Unquoted consolidation sensitivity: EUR40 fleet freight", "fleet_with_eur40_freight_per_unit_eur"),
              ("Individual EUR15 chargers + EUR1 adapters, same audited hardware", "one_charger_per_unit_per_unit_eur")]
    for label, field in fields:
        out.append(f"| {label} | " + " | ".join(r[field] for r in data["batches"]) + " |")
    out += ["", "Shared charging uses **one charger per ten packs**: one/two chargers for ten/twenty transmitters. "
            "It changes fleet logistics, not the transmitter's RF/timing/safety. Charger and adapter are fleet equipment to purchase, "
            "reusable across events, itemized separately below. A serial schedule may take roughly 30–40 h per ten fully discharged "
            "packs at 1 A including CV tail; this is a planning example, not a measured charging time. No packs are paralleled.", "",
            "## Exact bridge from M1 to old M2", "", "| Addition beyond M1 baseline | Ten-unit EUR/unit | Twenty-unit EUR/unit |", "| --- | ---: | ---: |"]
    for name in data["batches"][0]["old_scope_additions"]:
        out.append(f"| {name} | " + " | ".join(money(r["old_scope_additions"][name]) for r in data["batches"]) + " |")
    out.append("| Total difference | " + " | ".join(r["old_minus_m1_eur"] for r in data["batches"]) + " |")
    out += ["", "## Itemized unit material and functional provisions", "",
            "Batch purchase allocation, rather than rounded row sums, determines totals. Unit/extended prices below retain "
            "four decimals where useful; the CSV/JSON keep exact decimals and pooled purchases. Group labels are accounting "
            "scopes, not additional boards. Quantities for functional material sets are explicit allowances; supplier minimums "
            "and unused bulk spools remain unquoted rather than being presented as confirmed purchase counts.", "",
            "| Assembly / part | Qty/unit; needed 10 / 20 | Candidate / supplier code | Price evidence / stock | MOQ / multiple | Unit EUR at 10 / 20 fleets | Extended EUR/unit at 10 / 20 |", "| --- | --- | --- | --- | --- | --- | --- |"]
    a, b = data["batches"]
    for ra, rb in zip(a["unit_lines"], b["unit_lines"]):
        p = PARTS[ra["part_id"]]
        name = p.get("mpn", p.get("description"))
        supplier = f"[{p['supplier']}]({p['source_url']})" if p["source_url"] else p["supplier"]
        ordering = f"{p['moq']} / {p['multiple']}"
        if not ra["evidence"].startswith("OBSERVED"):
            ordering += " assumed"
        out.append(f"| {ra['group']} / {ra['part_id']} | {ra['qty_per_unit']}; {ra['needed']} / {rb['needed']} | "
                   f"{name}; {supplier}: {p['supplier_part_number']} | {ra['evidence']}; {p['availability']} | {ordering} | "
                   f"{D(ra['unit_eur']):.4f} / {D(rb['unit_eur']):.4f} | "
                   f"{D(ra['per_unit_eur_exact']):.4f} / {D(rb['per_unit_eur_exact']):.4f} |")
    out += ["", "## Assembly/scope subtotals", "", "| Scope | EUR/unit: 10 | EUR/unit: 20 |", "| --- | ---: | ---: |"]
    for group in a["groups_per_unit"]:
        out.append(f"| {group} | " + " | ".join(money(r["groups_per_unit"][group]) for r in data["batches"]) + " |")
    out += ["", "## Price evidence exposure of unit budget", "",
            "These classify prices, not proof that supplier claims or the hardware are qualified. The RF guard and BMS reserve "
            "are separated from material quotes. Labor, tooling capital and freight are not hidden inside component lines.", "",
            "| Class | Batch EUR: 10 | Batch EUR: 20 |", "| --- | ---: | ---: |"]
    for evidence in dict.fromkeys(k for r in data["batches"] for k in r["evidence_batch_eur"]):
        out.append(f"| {evidence} | " + " | ".join(r["evidence_batch_eur"].get(evidence, "0.00") for r in data["batches"]) + " |")
    out += ["", "## Shared fleet equipment, freight and cash budgets", "",
            "| Equipment / scope | Qty/fleet: 10 / 20 | Unit EUR | Batch EUR: 10 / 20 | Class |", "| --- | --- | ---: | --- | --- |"]
    for i, r in enumerate(a["shared_lines"]):
        other = b["shared_lines"][i]
        p = PARTS[r["part_id"]]
        out.append(f"| {p['description']} / {r['part_id']} | {r['qty_per_fleet']} / {other['qty_per_fleet']} | "
                   f"{money(r['unit_eur'])} | {r['batch_eur']} / {other['batch_eur']} | ESTIMATE; quote/qualification open |")
    out += ["| Consolidated fleet freight | one budget / one budget | — | 60.00 / 60.00 | ESTIMATE; actual routes/baskets open |",
            "", "| Fleet budget | Ten units EUR | Twenty units EUR |", "| --- | ---: | ---: |"]
    for label, field in (("Budgeted unit material", "unit_budget_batch_eur"), ("Shared equipment", "shared_equipment_batch_eur"),
                         ("Freight", "freight_budget_batch_eur"), ("Total, before labor/instruments/spares/VAT", "fleet_budget_eur")):
        out.append(f"| {label} | " + " | ".join(r[field] for r in data["batches"]) + " |")
    out += ["", "A shared EUR5 provisioning cable is not the RF test laboratory. Assembly/pack/tab soldering, winding, "
            "programming, calibration, field work and instrument access are **labor/capital OPEN**, not paid/free services "
            "implicitly supplied with the BOM. Consumables are included. The scope assumes one accepted unit per planned "
            "component set; reject/spare allowance and bulk-material leftovers need separate cash planning.", "",
            "## Protected 2S1P endurance check — calculations only", "",
            "Two 25R cells preserve the 2S domain and use a lower capacity explicitly. Aging80% × discharge-window90% × "
            "temperature90% is still an assumption. The 0.350 W Foxoring load is the M2 full-key-down allowance, not a measured current.", "",
            "| Cell capacity basis | Usable Wh | Runtime at 0.350 W | Runtime with +0.045 W LoRa RX | 24h mean-power ceiling |", "| --- | ---: | ---: | ---: | ---: |"]
    for r in data["cell_capacity_sensitivity"]:
        out.append(f"| {r['cell_ah']} Ah | {D(r['usable_wh']):.3f} | {D(r['hours_at_035w']):.1f} h | "
                   f"{D(r['hours_with_lora_rx_0395w']):.1f} h | {D(r['maximum_mean_w_for_24h']):.3f} W |")
    out += ["", "No LoRa is populated here. Pack compatibility does not mean this smaller capacity meets full-power "
            "Classic/Sprint/VHF endurance. Use the conservative 2.45 Ah ceiling for this Foxoring candidate; actual pack capacity, "
            "cold performance, cell imbalance, RF end-of-run level and peak/trip behavior remain measured gates.", "",
            "[Machine-readable bill](FOXORING_COST_BOM.csv), [totals](FOXORING_COST_TOTALS.json), "
            "[additional part/allowance catalog](FOXORING_COST_PARTS.json) and [source log](FOXORING_COST_SOURCES.md).", ""]
    return "\n".join(out)


def csv_text(data):
    stream = io.StringIO()
    fields = ["batch", "scope", "group", "part_id", "qty_per_unit_or_fleet", "needed", "planned_purchase_count",
              "supplier", "supplier_part_number", "unit_eur", "batch_eur", "evidence", "source_url", "availability", "note"]
    w = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for r in data["batches"]:
        for row in r["unit_lines"]:
            p = PARTS[row["part_id"]]
            w.writerow(dict(batch=r["batch"], scope="unit_material_or_provision", group=row["group"], part_id=row["part_id"],
                qty_per_unit_or_fleet=row["qty_per_unit"], needed=row["needed"],
                planned_purchase_count="" if row["evidence"] == "RESERVE" else row["ordered_allocated"],
                supplier=p["supplier"], supplier_part_number=p["supplier_part_number"], unit_eur=row["unit_eur"],
                batch_eur=row["batch_eur_exact"], evidence=row["evidence"], source_url=p["source_url"], availability=p["availability"], note=p.get("note", "")))
        for row in r["shared_lines"]:
            p = PARTS[row["part_id"]]
            w.writerow(dict(batch=r["batch"], scope="shared_equipment", group="fleet", part_id=row["part_id"],
                qty_per_unit_or_fleet=row["qty_per_fleet"], needed=row["qty_per_fleet"], planned_purchase_count=row["qty_per_fleet"],
                supplier=p["supplier"], supplier_part_number=p["supplier_part_number"], unit_eur=row["unit_eur"],
                batch_eur=row["batch_eur"], evidence=row["evidence"], source_url=p["source_url"], availability=p["availability"], note=p["note"]))
        w.writerow(dict(batch=r["batch"], scope="fleet_freight", group="transport", part_id="FREIGHT",
                        qty_per_unit_or_fleet=1, needed=1, planned_purchase_count="", supplier="Actual routes OPEN",
                        supplier_part_number="OPEN", unit_eur=r["freight_budget_batch_eur"],
                        batch_eur=r["freight_budget_batch_eur"], evidence="ESTIMATE",
                        source_url="https://www.nkon.nl/pt/orderingshipping", availability="No cart quote obtained",
                        note="Fleet-only budget; not a material part or shared capital. EUR40 optimization is sensitivity only."))
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = report()
    outputs = [(ROOT / "docs/FOXORING_COST_TOTALS.json", json.dumps(data, indent=2) + "\n"),
               (ROOT / "docs/FOXORING_COST_BOM.md", render(data)),
               (ROOT / "docs/FOXORING_COST_BOM.csv", csv_text(data))]
    if args.write:
        for path, text in outputs:
            path.write_text(text)
    errors = []
    if args.check:
        errors += [f"Stale {p.name}" for p, text in outputs if not p.exists() or p.read_text() != text]
        for r in data["batches"]:
            total = sum((D(v) for v in r["old_scope_additions"].values()), D(0))
            if money(total) != r["old_minus_m1_eur"]:
                errors.append("M1/M2 bridge does not close")
            if any(x["ordered_allocated"] < x["needed"] for x in r["unit_lines"]):
                errors.append("Planned material purchase undercounts demand")
            if any(x["part_id"] in {"HFPA", "HFDRIVE", "BOOST", "ISOFET", "HFCORE", "SINK", "VPA", "MMIC", "EOLDRIVER"}
                   for x in r["unit_lines"]):
                errors.append("Watt/VHF material entered Fox-only bill")
            if any(x["part_id"] == "CELL25R" and x["price_break"] != 10 for x in r["unit_lines"]):
                errors.append("Unjustified cell quantity discount")
            if not all(pid in r["core_pooled_purchases"] for pid in ("S3", "RTC", "SYNTH", "MONO", "LATCH", "POR", "RFDET", "FOXTUNE", "FOXRAD")):
                errors.append("Locked common hardware/safety/matching removed")
        if any(D(r["hours_at_035w"]) < 24 for r in data["cell_capacity_sensitivity"]):
            errors.append("Candidate 2S1P misses nominal modeled Foxoring endurance")
        # Independent exported-ledger closure checks that freight/shared equipment
        # are counted once and unspent reserves are not fake physical purchases.
        exported = list(csv.DictReader(io.StringIO(csv_text(data))))
        for r in data["batches"]:
            rows = [x for x in exported if int(x["batch"]) == r["batch"]]
            total = sum((D(x["batch_eur"]) for x in rows), D(0))
            if money(total) != r["fleet_budget_eur"]:
                errors.append("CSV fleet ledger does not close")
            if any(x["evidence"] == "RESERVE" and x["planned_purchase_count"] for x in rows):
                errors.append("Reserve falsely labeled as physical purchase")
        audit = (ROOT / "docs/FOXORING_COST_AUDIT.md").read_text()
        for r in data["batches"]:
            for key in ("unit_budget_incl_bms_reserve_eur", "fleet_budget_per_unit_eur", "one_charger_per_unit_per_unit_eur"):
                if r[key] not in audit:
                    errors.append("Audit price summary stale: " + key)
        print(json.dumps({"batches": list(BATCHES), "unit_material_lines_per_batch": len(data["batches"][0]["unit_lines"]),
            "shared_equipment_lines_per_batch": 3, "csv_ledger_lines": len(exported),
            "baseline_bridge_10_eur": data["batches"][0]["old_minus_m1_eur"],
            "hardware_tests": "NOT RUN", "errors": errors}, indent=2))
        raise SystemExit(bool(errors))
    print(json.dumps([{k: r[k] for k in ("batch", "unit_candidate_eur", "unit_budget_incl_bms_reserve_eur", "fleet_budget_eur", "fleet_budget_per_unit_eur")}
                      for r in data["batches"]], indent=2))


if __name__ == "__main__":
    main()

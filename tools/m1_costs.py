#!/usr/bin/env python3
"""Candidate material basket arithmetic only. No circuit, firmware or procurement."""
import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = json.loads((ROOT / "docs/M1_COST_PARTS.json").read_text())["parts"]
ROWS = list(csv.DictReader((ROOT / "docs/M1_COST_BOM.csv").open()))
BATCHES = (6, 10, 20)


def money(value):
    return str(Decimal(value).quantize(Decimal(".01"), rounding=ROUND_HALF_UP))


def population(boards, stock_limited=False, fox_only=False, enhanced=False):
    chosen = []
    for row in ROWS:
        if row["board"] not in boards:
            continue
        if row["population"] == "optional" and not enhanced:
            continue
        if stock_limited and row["board"] == "2m" and row["part_id"] == "LDO5":
            continue  # Discrete driver uses quiet controller 3.3V, below 4V VCEO.
        qty = int(row["quantity_per_board"])
        item = row.copy()
        if fox_only and row["board"] == "80m":
            if row["cost_group"] == "watt":
                continue
            # Explicit M1 count allowances for omitted watt-support functions.
            reduced = {"CMP": 1, "C0G": 4, "RFCOIL": 2, "SMALLBJT": 2,
                       "C100N": 6, "CBULK": 2, "RES": 12, "TRIM": 1}
            qty = reduced.get(row["part_id"], qty)
        if stock_limited and row["board"] == "2m" and row["part_id"] == "MMIC":
            item["part_id"] = "EOLDRIVER"
            qty = 2
        item["qty"] = qty
        chosen.append(item)
    return chosen


def basket(rows, batch):
    aggregate = {}
    for row in rows:
        pid = row["part_id"]
        aggregate[pid] = aggregate.get(pid, 0) + row["qty"] * batch
    prices = {}
    purchases = {}
    for pid, needed in aggregate.items():
        part = PARTS[pid]
        minimum = max(needed, part["moq"])
        count = ((minimum + part["multiple"] - 1) // part["multiple"]) * part["multiple"]
        eligible = [int(q) for q in part["price_breaks_eur"] if int(q) <= count]
        price = Decimal(str(part["price_breaks_eur"][str(max(eligible))]))
        prices[pid] = price
        purchases[pid] = {"needed": needed, "ordered": count, "leftover": count - needed,
                          "unit_eur": str(price), "batch_eur": money(count * price)}
    nominal = sum((Decimal(p["batch_eur"]) for p in purchases.values()), Decimal("0")) / batch
    estimated = sum((Decimal(p["batch_eur"]) for pid, p in purchases.items()
                    if PARTS[pid]["evidence"] == "ESTIMATE"), Decimal("0")) / batch
    lines = []
    for row in rows:
        part = PARTS[row["part_id"]]
        lines.append({**row, "unit_eur": str(prices[row["part_id"]]),
                      "line_eur_per_board": money(row["qty"] * prices[row["part_id"]]),
                      "evidence": part["evidence"]})
    return {"per_unit_eur": money(nominal), "batch_eur": money(nominal * batch),
            "estimated_eur_per_unit": money(estimated),
            "observed_eur_per_unit": money(nominal - estimated),
            "estimate_plus_50_percent_eur": money(nominal + estimated / 2),
            "estimate_minus_25_percent_eur": money(nominal - estimated / 4),
            "purchases": purchases, "lines": lines}


def report():
    variants = {
        "Controller": population(["controller"]),
        "80 m RF full": population(["80m"]),
        "2 m RF with MMIC driver": population(["2m"]),
        "2 m RF stock-limited discrete driver": population(["2m"], stock_limited=True),
        "80 m RF Fox-only population": population(["80m"], fox_only=True),
        "All three PCBs": population(["controller", "80m", "2m"]),
        "All three PCBs enhanced population": population(["controller", "80m", "2m"], enhanced=True),
        "All three PCBs stock-limited driver": population(["controller", "80m", "2m"], stock_limited=True),
        "All three PCBs plus mandatory port wiring": population(["controller", "80m", "2m", "wiring-controller", "wiring-80m", "wiring-2m"]),
        "Controller + full 80 m": population(["controller", "80m"]),
        "Controller + 2 m": population(["controller", "2m"]),
        "Controller + Fox-only RF + compact antenna": population(["controller", "80m", "compact80"], fox_only=True),
        "Long 80 m accessory": population(["long80"]),
        "Compact 80 m accessory": population(["compact80"]),
        "Mandatory port sockets excluding cable": population(["wiring-controller", "wiring-80m", "wiring-2m"]),
    }
    return {"date": "2026-10-13", "classification": "candidate, observed prices plus explicit unquoted estimates",
            "tax": "EUR ex VAT; shipping, PCB manufacture/assembly and labor excluded",
            "assumptions": "ESTIMATE rows assume MOQ1/no price breaks; counts unverified architecture allowances",
            "variants": {name: {str(n): basket(rows, n) for n in BATCHES} for name, rows in variants.items()}}


def render(data):
    out = ["# M1 itemized cost workbook", "", "Date: 2026-10-13. **CANDIDATE; NOT AN ORDERING LIST.**",
           "", "Generated by `python3 tools/m1_costs.py --write` from [candidate counts](M1_COST_BOM.csv) and "
           "[part/source catalog](M1_COST_PARTS.json). See [cost analysis](M1_COST_REWORK.md) for topology and feasibility.",
           "", "Conditional M1 acceptance authorizes [M2 RF preparation](M2_PREPARATION.md), not an ordering BOM. "
           "BFP650 variants below are preserved historical comparisons and are **excluded from current selection**. "
           "The M2 all-in view adds proposed pass-device, driver, filter and thermal material to these baseline costs.",
           "", "EUR ex VAT. OBSERVED prices are cached distributor observations, not reserved live quotes. "
           "ESTIMATE prices/availability and assumed MOQ1 require verification. Counts are functional planning allowances. "
           "RF values and connector footprints stay open. Each board table prices that board's identical batch independently; "
           "configuration totals pool identical MPNs across boards. No discounts pool different resistor/capacitor values. "
           "Unquoted estimates are flat at all quantities. No reel purchase or unjustified 20-piece discount.", "",
           "## Batch and configuration totals", "",
           "| Configuration | EUR/unit: 6 | EUR/unit: 10 | EUR/unit: 20 | Material basket EUR: 6 / 10 / 20 |",
           "| --- | ---: | ---: | ---: | --- |"]
    for name, sizes in data["variants"].items():
        out.append(f"| {name} | " + " | ".join(sizes[str(n)]["per_unit_eur"] for n in BATCHES) + " | "
                   + " / ".join(sizes[str(n)]["batch_eur"] for n in BATCHES) + " |")
    out.extend(["", "## Estimate exposure", "", "Only unquoted ESTIMATE rows are varied below. "
                "This is sensitivity arithmetic, not a statistical confidence interval or a price ceiling. "
                "Quoted parts, circuit changes, VAT, shipping, calibration labor and critical-stock risk can add further cost.", "",
                "| Assembly, ten boards | Observed EUR/unit | Estimated EUR/unit | Nominal | Estimates −25% / +50% |",
                "| --- | ---: | ---: | ---: | --- |"])
    for name in ("Controller", "80 m RF full", "2 m RF with MMIC driver", "All three PCBs"):
        value = data["variants"][name]["10"]
        out.append(f"| {name} | {value['observed_eur_per_unit']} | {value['estimated_eur_per_unit']} | "
                   f"{value['per_unit_eur']} | {value['estimate_minus_25_percent_eur']} / {value['estimate_plus_50_percent_eur']} |")
    for name in ("Controller", "80 m RF full", "2 m RF with MMIC driver", "Long 80 m accessory", "Compact 80 m accessory", "Mandatory port sockets excluding cable"):
        out.extend(["", f"## {name}", "", "Prices below are per component, followed by extended material cost per board. "
                    "Total needed quantities are batch × quantity/board; exact purchased quantities and leftovers are in "
                    "[machine-readable calculations](M1_COST_TOTALS.json).", "",
                    "| Function / part ID | Qty/board; needed 6 / 10 / 20 | Candidate MPN; supplier order code | Package | Evidence; availability | MOQ / order multiple | Unit EUR at batch 6 / 10 / 20 | Extended EUR/board 6 / 10 / 20 |",
                    "| --- | --- | --- | --- | --- | --- | --- | --- |"])
        for i, row in enumerate(data["variants"][name]["6"]["lines"]):
            part = PARTS[row["part_id"]]
            stock = part["availability"]
            qtys = " / ".join(str(row["qty"] * n) for n in BATCHES)
            source = f"[{part['supplier']}]({part['source_url']})" if part["source_url"] else part["supplier"]
            units = " / ".join(data["variants"][name][str(n)]["lines"][i]["unit_eur"] for n in BATCHES)
            extended = " / ".join(data["variants"][name][str(n)]["lines"][i]["line_eur_per_board"] for n in BATCHES)
            ordering = f"{part['moq']} / {part['multiple']}"
            if part["evidence"] == "ESTIMATE":
                ordering += " assumed"
            out.append(f"| {row['cost_group']} / {row['part_id']} | {row['qty']}; {qtys} | {part['mpn']}; "
                       f"{source}: {part['supplier_part_number']} | {part['package']} | {part['evidence']}; {stock} | "
                       f"{ordering} | {units} | {extended} |")
    out.extend(["", "## Optional material details", "",
                "These rows are omitted from the essential population. All are unquoted estimates with assumed MOQ1; "
                "the ten-unit enhanced population adds EUR1.65 per universal unit.", "",
                "| Board / function | Qty/board; needed 6 / 10 / 20 | Candidate MPN; package | Supplier / order code | Unit EUR estimate |",
                "| --- | --- | --- | --- | --- |"])
    for row in ROWS:
        if row["population"] != "optional":
            continue
        part = PARTS[row["part_id"]]
        qty = int(row["quantity_per_board"])
        qtys = " / ".join(str(qty * n) for n in BATCHES)
        out.append(f"| {row['board']} / {row['part_id']} | {qty}; {qtys} | {part['mpn']}; {part['package']} | "
                   f"{part['supplier']}: {part['supplier_part_number']} | {part['price_breaks_eur']['1']} |")
    out.extend(["", "## Population and sourcing limitations", "",
                "Fox-only omits every watt-group row: PA, driver, boost, isolation power FETs, power inductor, "
                "two watt LPF cores, normal socket, heat sink and electrolytics. Its remaining count adjustments "
                "are explicit in the analysis script; source, local hardware lease/latch/POR, own low-power port, "
                "passive identity/manual calibration, pads/filter/shield and compact antenna remain.", "",
                "Stock-limited VHF replaces GVA-84+ with two BFP650H6327XTSA1 devices. "
                "Its driver rail is filtered controller 3.3 V, omitting the 5 V LDO; "
                "never connect BFP650 to raw 2S or 5 V. Its <=4 V VCEO, matching, stability and output "
                "must be qualified. This is an EOL-dependent "
                "comparison with different matching/bias, not a drop-in validated alternative.", "",
                "OPEN supplier part numbers, RF component values, stock conflicts, current ratings and thermal "
                "assumptions prevent an ordering-ready BOM. Custom wound coils have material allowances, "
                "with build/calibration labor separate. The proposed base has soldered RF pigtails to "
                "separate mechanically keyed bulkhead sockets. Those sockets are itemized outside the PCB "
                "target in the mandatory wiring variant, together with both halves of the detachable raw-2S feeds "
                "and the transmitter-side battery plug. The pack-side mate belongs to the external pack. "
                "Cable/crimps/strain relief are additional unquoted costs. Logic board sockets are included.", "",
                "## Optional population rows", "",
                "The controller USB socket/ESD, RTC hold-up capacitor and pack-current shunt, and RF-board "
                "EEPROMs remain in the CSV/catalog as optional. Essential provisioning uses service pads "
                "and a shared external fixture. A cold pack swap invalidates time and requires resynchronization "
                "before arming without backup. RF-local current/thermal hardware cutoffs, fault outputs "
                "and calibration trimmers remain essential.", ""])
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = report()
    rendered = render(data)
    encoded = json.dumps(data, indent=2) + "\n"
    md = ROOT / "docs/M1_COSTED_BOM.md"
    js = ROOT / "docs/M1_COST_TOTALS.json"
    if args.write:
        md.write_text(rendered)
        js.write_text(encoded)
    if args.check:
        errors = []
        for path, expected in ((md, rendered), (js, encoded)):
            if not path.exists() or path.read_text() != expected:
                errors.append(f"Stale generated cost workbook: {path.name}")
        for name, sizes in data["variants"].items():
            for n, value in sizes.items():
                for pid, purchase in value["purchases"].items():
                    if purchase["ordered"] < purchase["needed"]:
                        errors.append(f"Underbuy: {name}/{n}/{pid}")
                    if PARTS[pid]["moq"] >= 1000 or PARTS[pid]["multiple"] >= 1000:
                        errors.append(f"Unexpected bulk/reel assumption: {name}/{n}/{pid}")
        print(json.dumps({"bom_lines": len(ROWS), "catalog_parts": len(PARTS), "batches": BATCHES,
                          "errors": errors}, indent=2))
        raise SystemExit(bool(errors))
    summary = {name: {n: v["per_unit_eur"] for n, v in sizes.items()}
               for name, sizes in data["variants"].items()}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

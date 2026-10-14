#!/usr/bin/env python3
"""All-in candidate MATERIAL cost view. No fabrication quote or procurement."""
import argparse
import json
import math
from pathlib import Path
import m1_costs
from m2_rf_analysis import prose_spacing

ROOT = Path(__file__).resolve().parents[1]
BATCHES = (6, 10, 20)


def proposal_increment(n, full_hf=False, vhf=False, fox=False):
    """Per-unit low/nominal/high deltas; pool only the identical D45H11 MPN."""
    pass_count = int(full_hf) + int(vhf)
    pass_price = 1.08 if pass_count * n >= 10 else 1.71
    q = lambda pid: float(m1_costs.basket([{"part_id": pid, "qty": 1}], n)["purchases"][pid]["unit_eur"])
    values = [0.0, 0.0, 0.0]
    if full_hf:
        quoted = 1.39 - q("HFDRIVE") + pass_price
        for i, support in enumerate((0.8 + 0.15 + 1.0 + 0.2,
                                     0.9 + 0.20 + 1.5 + 0.3,
                                     1.2 + 0.35 + 2.5 + 0.5)):
            values[i] += quoted + support
    if vhf:
        quoted = pass_price - q("MODULATOR")
        for i, support in enumerate((0.15 + 2.0, 0.20 + 3.0, 0.35 + 5.0)):
            values[i] += quoted + support
        # TPS61088 cannot supply the new 13.5 V rail. Pool the SAME TPS611781
        # MPN across installed full HF/VHF boards and subtract original prices.
        new_boost = float(m1_costs.basket([{"part_id": "BOOST", "qty": pass_count}], n)["purchases"]["BOOST"]["unit_eur"])
        boost_delta = pass_count * new_boost - int(full_hf) * q("BOOST") - q("VBOOST")
        values = [v + boost_delta for v in values]
    if full_hf or fox:
        for i, guard in enumerate((0.5, 0.75, 1.0)):
            values[i] += guard
    return values


def report():
    configs = {
        "Full 80 m unit, long + compact antennas": dict(boards=["controller", "80m"], full_hf=True, vhf=False, fox=False),
        "2 m AM + training unit": dict(boards=["controller", "2m"], full_hf=False, vhf=True, fox=False),
        "Universal three-PCB unit, all antennas": dict(boards=["controller", "80m", "2m"], full_hf=True, vhf=True, fox=False),
        "Fox-only unit, complete compact antenna": dict(boards=["controller", "80m"], full_hf=False, vhf=False, fox=True),
    }
    rows = []
    for name, cfg in configs.items():
        for n in BATCHES:
            base = m1_costs.basket(m1_costs.population(cfg["boards"], fox_only=cfg["fox"]), n)
            delta_min, delta_nom, delta_max = proposal_increment(n, cfg["full_hf"], cfg["vhf"], cfg["fox"])
            base_nom = float(base["per_unit_eur"])
            base_min = float(base["estimate_minus_25_percent_eur"])
            base_max = float(base["estimate_plus_50_percent_eur"])
            components = {"PCB components incl M2 proposal increments": (base_min + delta_min, base_nom + delta_nom, base_max + delta_max)}
            modules = len(cfg["boards"]) - 1
            # Both halves of raw-power plugs + normal/low RF sockets, transmitter battery half.
            ports = 0.6 + modules * 1.2 + (0.4 if cfg["fox"] else modules * 1.1)
            components["Mandatory transmitter power/RF connector material"] = (ports, ports, ports)
            components["Wire/coax/crimps/strain relief"] = (1.5 if cfg["fox"] else 2.0, 2.5 if cfg["fox"] else 3.5, 4.0 if cfg["fox"] else 5.0)
            bare_order = math.ceil(n / 5) * 5  # EXPLICIT ASSUMED MOQ5 per design; not a vendor quote.
            boards_per_unit = len(cfg["boards"])
            components["Bare PCB fabrication incl assumed MOQ5 leftovers"] = tuple(x * bare_order / n * boards_per_unit for x in (1.5, 3.0, 4.5))
            components["Outer enclosure/seals/mounting"] = (3, 4.5, 7) if cfg["fox"] else (5, 8, 12)
            if cfg["full_hf"]:
                components["Long-wire match/radiator/symmetric return"] = (10.25 * 0.75, 10.25, 10.25 * 1.5)
                components["HF installation line/lashing/support allocation"] = (2, 3, 5)
            if cfg["full_hf"] or cfg["fox"]:
                components["Complete compact Foxoring cartridge/radiator/return"] = (8.38 * 0.75, 8.38, 8.38 * 1.5)
            if cfg["vhf"]:
                components["VHF normal antenna/feed/balun"] = (10, 15, 20)
                components["VHF 2-3m support"] = (5, 8, 15)
                components["Training antenna"] = (2, 3, 5)
            components["External qualified 2S charger, one per unit"] = (7, 10, 15)
            components["Shared provisioning fixture allocation"] = (3 / n, 5 / n, 6 / n)
            components["Shipping allocation for consolidated fleet baskets"] = (30 / n, 60 / n, 90 / n)
            for pack in range(1, 5):
                # All cells NEW, matched, protected external pack. Cell price is UNQUOTED.
                pack_scope = {
                    "New reference cells, 2 x P": (2 * pack * 3, 2 * pack * 4, 2 * pack * 5),
                    "Qualified balancing/protection BMS": (2, 3, 5),
                    "Pack fuse/tabs/insulation/restraint/assembly material": (3, 4, 7),
                    "Pack-side mating power connector": (0.6, 0.6, 0.6),
                }
                all_items = {**components, **pack_scope}
                totals = [sum(v[i] for v in all_items.values()) for i in range(3)]
                rows.append({"configuration": name, "batch": n, "pack": f"2S{pack}P",
                    "base_M1_PCB_eur": base_nom, "M2_increment_eur": round(delta_nom, 3),
                    "proposed_PCB_components_eur": round(base_nom + delta_nom, 3),
                    "pack_eur": [round(sum(v[i] for v in pack_scope.values()), 2) for i in range(3)],
                    "material_eur": [round(v, 2) for v in totals], "items": all_items,
                    "fabricated_count_per_design": bare_order, "unused_bare_boards_per_design": bare_order - n})
    standalone = []
    for name, board, hf, vhf, fox in (("Controller, no LoRa", "controller", False, False, False),
                                     ("80 m full", "80m", True, False, False),
                                     ("2 m MMIC AM + training", "2m", False, True, False),
                                     ("80 m Fox-only population", "80m", False, False, True)):
        for n in BATCHES:
            b = m1_costs.basket(m1_costs.population([board], fox_only=fox), n)
            delta = proposal_increment(n, hf, vhf, fox)
            standalone.append({"board": name, "batch": n, "base_M1_eur": float(b["per_unit_eur"]),
                               "proposed_nominal_eur": round(float(b["per_unit_eur"]) + delta[1], 3)})
    return {"date": "2026-10-13", "classification": "CANDIDATE MATERIAL COST; OBSERVATIONS PLUS EXPLICIT UNQUOTED ALLOWANCES",
            "scope": "EUR exVAT planning; assembly/test labor and instruments unquoted/excluded; LoRa optional separately",
            "standalone_boards": standalone, "rows": rows}


def render(data):
    lines = ["# All-in system material cost — M2 preparation", "", "Date: **2026-10-13**. **Candidate planning baskets, not quotes or an ordering list.**",
       "", "Generated by `python3 tools/m2_system_costs.py --write`. The [M1 component workbook](M1_COSTED_BOM.md) is preserved. "
       "This view adds the [HF circuit proposal](M2_HF_CIRCUIT_PROPOSALS.md), [VHF review](M2_VHF_RF_REVIEW.md), "
       "and mandatory external system material. [Sources](M2_SOURCES.md) distinguish observations from estimates.",
       "", "**Foxoring audit supersedes the Fox-only fleet recommendation below.** Its [itemized audit](FOXORING_COST_AUDIT.md) "
       "preserves this original EUR77.11/EUR73.82 scope, which allocated a charger to every unit and freight/tooling. "
       "The [audited bill](FOXORING_COST_BOM.md) preserves the same ESP32-S3/RTC and common reduced RF board; "
       "its budgeted complete-unit material is EUR55.24/EUR55.20 at 10/20, with separately shared charging/equipment/freight "
       "giving EUR63.34/EUR60.05 fleet cash allocation before VAT/labor/instruments/spares. Original rows remain historical scope comparisons.",
       "", "The earlier component-only Fox label named the final configuration, but its EUR20.68/EUR20.64 entries "
       "exclude the EUR8.38 compact antenna. The true preserved controller/RF/antenna baseline is EUR29.06/EUR29.02; "
       "the audit makes these boundaries explicit rather than changing historical arithmetic.",
       "", "EUR ex VAT planning basis. Every unquoted accessory, fabrication, battery, enclosure, shipping and proposal-support number is an "
       "**ESTIMATE**, not an observed discount or upper bound. Cell price was not captured; no retail-gross price is silently converted to net. "
       "Shipping is an assumed consolidated fleet allocation. Assembly/winding/calibration labor and laboratory instruments remain **unquoted/excluded**; "
       "this is an all-in MATERIAL view, not a turnkey delivered-product quote. Rejects, spares and extra packs are additional.",
       "", "## Component-only proposals beside the M1 baseline", "",
       "| Configuration | M1 components 6 / 10 / 20 | With nominal M2 increments 6 / 10 / 20 |", "| --- | --- | --- |"]
    names = list(dict.fromkeys(r["configuration"] for r in data["rows"]))
    for name in names:
        subset = [r for r in data["rows"] if r["configuration"] == name and r["pack"] == "2S1P"]
        lines.append(f"| {name} | " + " / ".join(f"{r['base_M1_PCB_eur']:.2f}" for r in subset) + " | " +
                     " / ".join(m1_costs.money(str(r['proposed_PCB_components_eur'])) for r in subset) + " |")
    lines += ["", "Standalone board component estimates (independent board batches, not pooled fleet purchases):", "",
              "| PCB population | Nominal EUR/board: 6 | 10 | 20 |", "| --- | ---: | ---: | ---: |"]
    for name in dict.fromkeys(r["board"] for r in data["standalone_boards"]):
        sub = [r for r in data["standalone_boards"] if r["board"] == name]
        lines.append(f"| {name} | " + " | ".join(m1_costs.money(str(r['proposed_nominal_eur'])) for r in sub) + " |")
    lines += ["", "At ten standalone boards, the controller estimate is within its EUR8–15 target; "
              "full HF is EUR23.33 (EUR3.33 above the EUR20 ceiling) and MMIC VHF EUR36.15 (EUR6.15 above EUR30). "
              "The pooled universal estimate EUR72.13 exceeds the earlier EUR65 combined target by EUR7.13. "
              "These misses are explicit: thermal/SOA, CW shaping, stronger filtering and low-path protection take precedence. "
              "Cost reductions need measured efficiency, verified shared heat sinking and fresh support baskets; EOL substitution "
              "or omitted matching/interlocks is not credited."]
    lines += ["", "M2 increments: HF industrial gate-driver replacement; **additional D45H11 CW shaping pass device**; "
              "helper upgrade, drain-to-50-ohm match, seventh-order filter and thermal allowance; low-branch guard/input-limiting support. "
              "VHF replaces the 12.6 V-limited TPS61088 with the already cataloged 20 V TPS611781 for its 13.5 V rail; "
              "identical boost MPNs pool across HF/VHF. VHF replaces BD140 with "
              "D45H11, upgrades the base helper and increases the existing heat-spreader allowance. Existing shield, safety, "
              "LPF, low-source, connector and matching allocations are not removed. These are circuit-proposal deltas; supporting counts/quotes "
              "are pending. Identical D45H11 devices pool across HF/VHF, reaching the ten-part break at six universal units. "
              "GVA-84+ remains the driver baseline; PHA-1+ adds observed EUR0.25 silicon, plus unmeasured rail/source costs. "
              "ADF4002/VCO fallback adds approximately EUR4–5.5 per VHF board before any further support changes.",
              "", "### Incremental candidate BOM — supplements the itemized M1 baseline", "",
              "These are additions/replacements, not a second complete BOM. Exact support counts/footprints remain proposed. "
              "Supplier prices, customer MOQ1 and indexed stock/access limits are in [dated sources](M2_SOURCES.md). "
              "Quoted replacement values are held flat until their observed break; estimates have no invented quantity discount.", "",
              "| Part / support function | Quantity / disposition | Supplier code / availability | EUR unit or functional allowance, 6 / 10 / 20 |", "| --- | --- | --- | --- |",
              "| ST D45H11 | +1 full HF; replaces 1 BD140 on VHF | Mouser 511-D45H11; indexed stock 3,988, current basket open | 1.71 / 1.08 / 1.08 per device when standalone; universal six-unit batch pools 12 identical devices at 1.08 |",
              "| Industrial TC4427A | Replaces 1 IRS4427 on full HF | Mouser 579-TC4427AEOA; incoming tube / in-stock AEOA713 alternative, exact basket open | 1.39 / 1.39 / 1.39; next observed break is 25 |",
              "| TPS611781RNWR, 20 V boost | Replaces 1 TPS61088 on VHF; existing 1 full HF retained | Mouser 595-TPS611781RNWR; indexed stock 2,288, exact basket open | 2.79 / 2.09 / 2.09 standalone; universal aggregate 12/20/40 devices uses 2.09 / 2.09 / 1.92 |",
              "| BD139-class helper / base-current limit support | One upgraded helper function per pass device; baseline small-BJT allocation retained | Exact supplier suffix and resistor/NPN counts open | Increment 0.20 / 0.20 / 0.20 nominal per full HF or VHF board; ESTIMATE range 0.15–0.35 |",
              "| Additional HF drain-to-50-ohm match | One L/C cell; final values and RF ratings open | Unquoted RF coil/capacitor material | 0.30 / 0.30 / 0.30 nominal; ESTIMATE range 0.20–0.50 |",
              "| Additional seventh-order HF filter material | One extra series-coil/shunt-capacitor group versus baseline; final layout/values open | Unquoted characterized windings / C0G material | 0.90 / 0.90 / 0.90 nominal; ESTIMATE range 0.80–1.20 |",
              "| HF shaping-device thermal material | One thermal provision beyond isolation FETs | Sink/interface hardware unquoted | 1.50 / 1.50 / 1.50 nominal; ESTIMATE range 1.00–2.50 |",
              "| VHF pass/helper thermal material | Additional sink/interface beyond baseline spreaders | Sink/interface hardware unquoted | 3.00 / 3.00 / 3.00 nominal; ESTIMATE range 2.00–5.00 |",
              "| HF bounded-low-source guard and drive-input limits | One local protection function, full HF or Fox-only | Exact detector/limiter/clamp MPNs and counts open | 0.75 / 0.75 / 0.75 nominal; ESTIMATE range 0.50–1.00 |",
              "| PHA-1+ comparator, optional | Replaces GVA only if measured driver gate requires it | Mouser 139-PHA-1; indexed stock 4,662, basket open | 2.82 / 2.82 / 2.82 silicon; omitted from baseline totals |",
              "", "## Pack material scope", "", "| Pack | New cells | Low / nominal / high EUR |", "| --- | ---: | --- |"]
    example = [r for r in data["rows"] if r["configuration"] == names[0] and r["batch"] == 10]
    for r in example:
        count = int(r["pack"][2]) * 2
        lines.append(f"| {r['pack']} | {count} | " + " / ".join(f"{v:.2f}" for v in r["pack_eur"]) + " |")
    lines += ["", "Pack includes new matched reference cells at **EUR3/4/5 each estimated**, qualified balancing/protection BMS "
              "EUR2/3/5, pack fuse/tabs/insulation/restraint EUR3/4/7, and the EUR0.60 pack-side mating connector. "
              "The transmitter-side half is already in its connector row. No reclaimed-cell or unprotected-pack shortcut. "
              "A commercial protected pack quote can replace these allowances; pack assembly labor is not priced. "
              "Qualify at least the single-band 5 A path for the revised high-power stress allowance, or 7 A only for an explicitly supported simultaneous-TX configuration. "
              "For Fox-only use this is a full-family interchangeability gate, not a claim of 5 A Foxoring consumption. "
              "One external 8.4 V charger per unit is allocated; charging current/temperature must meet the selected cell/BMS. "
              "The estimate does not approve a particular charger or home-built pack.",
              "", "## All-in nominal material by pack and batch", "",
              "Includes proposed component changes, **all applicable antennas/matching**, required power/RF connectors/wiring, "
              "bare PCB fabrication, enclosure, one pack/charger, shared provisioning fixture and shipping allocation. "
              "A universal unit carries both HF installations and normal/training VHF antennas. No extra fourth product PCB.",
              "", "| Configuration / pack | EUR/unit: 6 | EUR/unit: 10 | EUR/unit: 20 | Ten-unit basket sensitivity, low–high |",
              "| --- | ---: | ---: | ---: | --- |"]
    for name in names:
        for pack in range(1, 5):
            sub = [r for r in data["rows"] if r["configuration"] == name and r["pack"] == f"2S{pack}P"]
            t = next(r for r in sub if r["batch"] == 10)
            lines.append(f"| {name} / 2S{pack}P | " + " | ".join(f"{r['material_eur'][1]:.2f}" for r in sub) +
                         f" | {t['material_eur'][0]:.2f}–{t['material_eur'][2]:.2f} |")
    lines += ["", "Sensitivity varies M1 estimated support −25%/+50% and the declared new allowance ranges. "
              "It is not a confidence interval or price ceiling. Current quoted silicon is held fixed; RF topology changes, "
              "stock loss, VAT and extra shipping can exceed it. All 48 baskets and line scopes are in "
              "[machine-readable totals](M2_SYSTEM_COST.json).", "", "## Ten universal units with 2S4P: itemized example", "",
              "| Material scope | Low / nominal / high EUR per unit | Evidence |", "| --- | --- | --- |"]
    exemplar = next(r for r in data["rows"] if "Universal" in r["configuration"] and r["batch"] == 10 and r["pack"] == "2S4P")
    for name, values in exemplar["items"].items():
        evidence = "M1 observed prices + estimates; quoted replacement silicon + estimated support" if name.startswith("PCB components") else "ESTIMATE; quote/qualification open"
        lines.append(f"| {name} | " + " / ".join(f"{v:.2f}" for v in values) + f" | {evidence} |")
    lines += ["", "Bare-board fabrication uses **assumed MOQ5 per design**, EUR1.50/3.00/4.50 per fabricated board, "
              "with leftovers: six units order ten of each design; ten/twenty have no modeled leftover. These are allowances, "
              "not a vendor quote. Board dimensions, layers, RF stack-up and surface finish remain open. "
              "Do not use a promotional PCB price to imply delivered fleet fabrication cost.", "",
              "The proposal remains cost-sensitive: an enclosure used as a verified shared heat sink could reduce separate "
              "thermal material, and existing site supports/chargers could reduce a deployment basket. No such credit is taken "
              "before its scope and thermal performance are established. Optional exact Silicontra LoRa remains unquoted; "
              "the earlier EUR10–20 module allowance can be shown separately with supply/antenna material still open. "
              "No-LoRa operation is the complete base configuration.", "",
              "## Endurance and release boundary", "",
              "All pack sizes are electrically compatible candidates; their inclusion in a cost table does not mean they meet "
              "every 24 h profile. Conservative VHF preparation uses **4P (about 27.1 h modeled)**; a low-bias measured chain "
              "might qualify 3P, while poor efficiency fails even4P. HF Classic uses4P, Sprint2P, Foxoring1P in current planning; "
              "Sprint1P requires efficiency/current closure. Continuous full-power beacons and "
              "simultaneous dual-band 24 h still fail within 4P. See [VHF review](M2_VHF_RF_REVIEW.md) and "
              "[revised full profile budget](M2_POWER_BUDGET.md); the M1 profile assumptions are retained as history.", "",
              "**No full-set manufacture or order.** Replace allowances with complete comparable baskets only after circuit "
              "and RF gates close. A decision to use a safer pass device or better filter takes precedence over the old "
              "component targets; its full material, heat and battery consequences remain visible.", ""]
    return prose_spacing("\n".join(lines))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--write", action="store_true")
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    d = report()
    js = json.dumps(d, indent=2) + "\n"
    md = render(d)
    paths = [(ROOT / "docs/M2_SYSTEM_COST.json", js), (ROOT / "docs/M2_SYSTEM_COST.md", md)]
    if args.write:
        for path, content in paths:
            path.write_text(content)
    if args.check:
        errors = [f"Stale {path.name}" for path, content in paths if not path.exists() or path.read_text() != content]
        if len(d["rows"]) != 48:
            errors.append("Missing configuration/pack/batch scope")
        print(json.dumps({"baskets": len(d["rows"]), "errors": errors}, indent=2))
        raise SystemExit(bool(errors))
    print(json.dumps({"universal_4p": [{"batch": r["batch"], "pcb_eur": r["proposed_PCB_components_eur"],
          "material_eur": r["material_eur"]} for r in d["rows"] if "Universal" in r["configuration"] and r["pack"] == "2S4P"]}, indent=2))


if __name__ == "__main__":
    main()

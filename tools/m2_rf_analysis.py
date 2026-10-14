#!/usr/bin/env python3
"""Original M2-preparation calculations. No transistor model or hardware control."""
import argparse
import cmath
import json
import math
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prose_spacing(value):
    chunks = re.split(r"(https?://[^\s)]+)", value)
    prefixes = ("at|about|for|under|with|plus|to|uses|requires|from|on|even|each|the|and|all|"
                "continuous|scheduled|complete|independent|declaring|qualify|guessed|earlier|"
                "modeled|stock|provision|nominal|before|after|reach|between|need|better|aim|clean|"
                "re-evaluate|exceeds|stated|near|through|approximate|gain|require|typically|typical")
    for i in range(0, len(chunks), 2):
        s = chunks[i].replace("P1dB", "COMPRESSIONTOKEN")
        s = re.sub(r"\b(" + prefixes + r")(?=\d)", r"\1 ", s, flags=re.I)
        s = re.sub(r"(?<![A-Za-z0-9_])(\d+(?:\.\d+)?)(µW|mW|µA|mA|Ah|Wh|MHz|kHz|ms|ns|ppm|dBc|dBd|dBm|dB|W|V|A|h)\b", r"\1 \2", s)
        s = re.sub(r"\b(HF|VHF|Sprint|Foxoring|LoRa|ERP)(?=\d)", r"\1 ", s)
        s = re.sub(r"(?<!\d)([,;|])(?=[\d+])", r"\1 ", s)
        s = s.replace("None≤", "None ≤").replace("COMPRESSIONTOKEN", "P1dB")
        chunks[i] = s
    return "".join(chunks)


def dbm(watts):
    return 10 * math.log10(watts * 1000)


def polar(magnitude, degrees):
    return cmath.rect(magnitude, math.radians(degrees))


def envelope(erp=1.0, modulation=0.8, efficiency=0.45, iq=0.15,
             boost=13.5, center=12 / 1.8, capacitance=100e-9, samples=7200):
    # Efficiency applies ONLY to the voltage-dependent RF-conversion component.
    # iq is a separate stress allowance; it is NOT added to a measured total efficiency.
    connector_carrier = erp * 10 ** 0.1
    internal_carrier = connector_carrier * 10 ** 0.05  # illustrative 0.5 dB output loss
    k = internal_carrier / (efficiency * center ** 2)
    rows = []
    for i in range(samples):
        phase = 2 * math.pi * i / samples
        voltage = center * (1 + modulation * math.sin(phase))
        load = k * voltage + iq
        charging = capacitance * center * modulation * 2 * math.pi * 800 * math.cos(phase)
        required = load + charging
        rows.append((voltage, load, required, (boost - voltage) * max(0, required)))
    return {
        "erp_w": erp, "m": modulation, "eta_dynamic": efficiency, "iq_a": iq,
        "boost_v": boost, "center_v": center, "capacitance_f": capacitance,
        "carrier_connector_w": connector_carrier, "carrier_before_filter_w": internal_carrier,
        "v_min": min(r[0] for r in rows), "v_max": max(r[0] for r in rows),
        "current_peak_a": max(r[2] for r in rows),
        "required_current_min_a": min(r[2] for r in rows),
        "sink_required": any(r[2] < 0 for r in rows),
        "pass_mean_w": sum(r[3] for r in rows) / samples,
        "pass_peak_w": max(r[3] for r in rows),
        "peak_dissipation_point": dict(zip(("v_v", "load_a", "required_a", "pass_w"), max(rows, key=lambda r: r[3]))),
        "boost_mean_output_w": boost * (k * center + iq),
        "mean_formula_w": k * center * (boost - center * (1 + modulation ** 2 / 2))
                          + iq * (boost - center),
        "phase_points": [dict(zip(("v_v", "load_a", "required_a", "pass_w"), rows[i]))
                         for i in (0, samples // 4, samples // 2, 3 * samples // 4)],
    }


def calculations():
    carrier = 10 ** 0.1
    pep = carrier * 1.8 ** 2
    clean = pep * 10 ** 0.1
    p1db = 20.73  # lower of published 100/200 MHz typical values; NOT a guarantee
    gain_rows = []
    for gain in (15, 17, 20, 21, 23):
        # gain is intrinsic large-signal gain, with both 0.5 dB loss allowances external.
        drive = clean * 10 ** ((1.0 - gain) / 10)
        gain_rows.append({"gain_db": gain, "driver_w": drive, "driver_dbm": dbm(drive),
                          "headroom_to_typ_p1db_db": p1db - dbm(drive)})
    s11, s21, s12, s22 = (polar(0.803, -162), polar(5.19, 67),
                           polar(0.032, -18), polar(0.704, -157))
    delta = s11 * s22 - s12 * s21
    stability_k = (1 - abs(s11) ** 2 - abs(s22) ** 2 + abs(delta) ** 2) / (2 * abs(s12 * s21))
    zin, zout = 50 * (1 + s11) / (1 - s11), 50 * (1 + s22) / (1 - s22)
    cases = {
        "full_mark_no_bias": envelope(iq=0),
        "full_mark_bias": envelope(),
        "full_carrier_no_tone": envelope(modulation=0),
        "full_carrier_hot_efficiency_stress": envelope(modulation=0, efficiency=0.35),
        "quarter_mark_fixed_boost": envelope(erp=0.25, center=6 / 1.8),
        "quarter_mark_tracking_boost": envelope(erp=0.25, center=6 / 1.8, boost=9),
        "quarter_carrier_fixed_boost": envelope(erp=0.25, center=6 / 1.8, modulation=0),
        "quarter_mark_22uF_no_bias": envelope(erp=0.25, center=6 / 1.8, iq=0, capacitance=22e-6),
    }
    usable = 7.2 * 3.4 * 0.8 * 0.9 * 0.9
    endurance = []
    for name in ("full_mark_no_bias", "full_mark_bias", "full_carrier_hot_efficiency_stress"):
        active = cases[name]["boost_mean_output_w"] / 0.88 + 1.55
        for duty in (0.2, 1):
            total = 0.13 + duty * active
            endurance.append({"case": name, "duty": duty, "battery_w": total,
                              "wh_24h": total * 24,
                              "hours_1p_to_4p": [usable * n / total for n in range(1, 5)]})
    omega = 2 * math.pi * 4.2e6
    # Original fifth-order 50-ohm Butterworth pi ladder; ideal, unrounded values.
    g = [2 * math.sin((2 * i - 1) * math.pi / 10) for i in range(1, 6)]
    lpf = {"c1_f": g[0] / (50 * omega), "l2_h": g[1] * 50 / omega,
           "c3_f": g[2] / (50 * omega), "l4_h": g[3] * 50 / omega,
           "c5_f": g[4] / (50 * omega)}
    beta = math.log(1 / math.tanh(0.1 / 17.37))
    gamma = math.sinh(beta / 14)
    cg = [2 * math.sin(math.pi / 14) / gamma]
    for i in range(2, 8):
        a_prev = math.sin((2 * i - 3) * math.pi / 14)
        a_now = math.sin((2 * i - 1) * math.pi / 14)
        b_prev = gamma ** 2 + math.sin((i - 1) * math.pi / 7) ** 2
        cg.append(4 * a_prev * a_now / (b_prev * cg[-1]))
    cw = 2 * math.pi * 4.1e6
    cheby = {("c" if i % 2 else "l") + str(i) + ("_f" if i % 2 else "_h"):
             value / (50 * cw) if i % 2 else value * 50 / cw for i, value in enumerate(cg, 1)}
    eps2 = 10 ** 0.01 - 1
    def cheby_gain(f):
        x = f / 4.1e6
        tn = math.cos(7 * math.acos(x)) if x <= 1 else math.cosh(7 * math.acosh(x))
        return -10 * math.log10(1 + eps2 * tn ** 2)
    rf_freq = 3.55e6
    w = 2 * math.pi * rf_freq
    lmatch_q = math.sqrt(50 / 20 - 1)
    drain_r = 15.5 ** 2 / (2 * 5 * 10 ** 0.05)
    drain_q = math.sqrt(50 / drain_r - 1)
    hf_active = 5 / 0.60 / 0.85 + 1.00
    sprint_active = 1 / 0.55 / 0.88 + 0.65
    vhf_active = cases["full_mark_bias"]["boost_mean_output_w"] / 0.88 + 1.55
    profile_powers = {
        "HF Classic 5W, 20%": 0.13 + 0.2 * hf_active,
        "Sprint 1W, 20%": 0.13 + 0.2 * sprint_active,
        "Foxoring 10mW continuous": 0.35,
        "VHF Classic 1W carrier ERP, 20%": 0.13 + 0.2 * vhf_active,
        "HF 5W continuous beacon": 0.13 + hf_active,
        "Sprint 1W continuous beacon": 0.13 + sprint_active,
        "VHF 1W ERP continuous beacon": 0.13 + vhf_active,
        "Training 1mW continuous": 0.45,
        "Dual Classic, each20%": 0.14 + 0.2 * (hf_active + vhf_active),
    }
    profiles = [{"profile": name, "battery_w": power, "wh_24h": 24 * power,
                 "runtime_h_1p_to_4p": [usable * n / power for n in range(1, 5)],
                 "minimum_p_for_24h": next((n for n in range(1, 5) if usable * n >= 24 * power), None)}
                for name, power in profile_powers.items()]
    stress_current = carrier * 10 ** 0.05 / (0.35 * (12 / 1.8)) * 1.8 + 0.15
    return {
        "date": "2026-10-13", "classification": "DESIGN CALCULATIONS; NOT MEASURED; NOT A TRANSISTOR SIMULATION",
        "vhf": {"carrier_connector_w": carrier, "mark_mean_connector_w": carrier * 1.32,
                "pep_connector_w": pep, "clean_connector_w": clean,
                "stress_peak_pack_a": ((13.5 * stress_current / 0.88 + 0.95 + 1.0 + 0.13 + 0.44) * 1.25 / 6),
                "intrinsic_gain_needed_db": dbm(clean) + 1 - (p1db - 3), "gain_cases": gain_rows},
        "pd55008_small_signal_150mhz": {"table": "ST Table10, 12.5V/150mA; formed-lead",
                "k": stability_k, "delta_abs": abs(delta), "unmatched_s21_db": 20 * math.log10(abs(s21)),
                "msg_db_if_conditionally_stable": 10 * math.log10(abs(s21 / s12)),
                "zin_ohm": [zin.real, zin.imag], "zout_ohm": [zout.real, zout.imag]},
        "envelope_cases": cases, "vhf_endurance_sensitivity": endurance, "operating_profiles": profiles,
        "universal_single_band_sensitivity": [
            {"profile": r["profile"], "battery_w": r["battery_w"] + 0.01,
             "runtime_h_1p_to_4p": [usable * n / (r["battery_w"] + 0.01) for n in range(1, 5)]}
            for r in profiles[:4]],
        "hf_ideal_lpf": {"values": lpf, "samples_db": {str(f): -10 * math.log10(1 + (f / 4.2e6) ** 10)
                                                        for f in (3.51e6, 3.60e6, 7.02e6, 10.53e6)}},
        "hf_chebyshev_lpf": {"values": cheby, "samples_db": {str(f): cheby_gain(f)
                                                              for f in (3.51e6, 3.60e6, 7.02e6, 10.53e6)}},
        "long_match_example": {"antenna_z": [20, -300], "series_l_h": (300 + 20 * lmatch_q) / w,
                               "source_shunt_c_f": lmatch_q / (50 * w)},
        "hf_drain_match_example": {"drain_r_ohm": drain_r, "series_l_h": drain_q * drain_r / w,
                                   "load_side_shunt_c_f": drain_q / (50 * w)},
        "fox_example": {"c_f": 10e-12, "q_assumed": 50, "series_l_h": 1 / (w ** 2 * 10e-12),
                        "reactance_ohm": 1 / (w * 10e-12), "coil_loss_ohm": 1 / (w * 10e-12 * 50)},
    }


def power_document(data):
    lines = ["# M2 preparation power budget", "", "Date: **2026-10-13**. **Calculated evaluation allowances; no measured currents or runtime.**",
        "", "This supersedes the M1 profile assumptions for the proposed circuits while retaining "
        "[M1 calculations](M1_POWER_BUDGET.md) as history. Generated by `python3 tools/m2_rf_analysis.py --write`; "
        "[JSON](M2_RF_CALCULATIONS.json) contains the inputs/results. Exact PA bias/efficiency and "
        "[circuit choices](M2_PREPARATION.md) remain qualification gates.", "",
        "The [Foxoring cost audit](FOXORING_COST_AUDIT.md) separately evaluates its lower-cost two-25R-cell 2S1P "
        "candidate: 2.45 Ah conservative basis, about32.7 h at0.350 W and a0.476 W 24h ceiling, all modeled. "
        "The3.4 Ah reference table below remains unchanged and must not be used as that smaller pack's runtime claim.", "",
        "Reference packs still use 3.4Ah cells at3.6V nominal, 80% aging ×90% discharge window ×90% temperature = "
        "64.8% usable nominal energy: **15.863 /31.726 /47.589 /63.452 Wh** for1P/2P/3P/4P. "
        "All remain compatible;4P is maximum, not a required universal pack. No cell/pack measurement exists.", "",
        "## Loads explicitly revised", "", "| Load | Evaluation input | Evidence |", "| --- | --- | --- |",
        "| Controller/RTC/buck/monitoring |0.120W common plus0.010W per installed RF board |Retained unmeasured M1 allowance; no invented savings |",
        "| HF active overhead |1.00W Classic;0.65W Sprint |Gate charge/driver, source, shaping helper and control provision; not datasheet total current |",
        "| HF conversion |60% effective RF stage /85% boost Classic;55% /88% Sprint |Assumed RF-stage efficiency includes shaping-pass drop, drain PA and output loss; validate the complete shaped chain |",
        "| Foxoring total |0.350W battery continuous |Increased reserve for independent buffer/pad/current/RF guard; watt stage off |",
        "| VHF voltage-dependent load |45% dynamic conversion,0.5dB filter loss,150mA separate bias allowance |Envelope calculation; do not add bias twice to measured total efficiency |",
        "| VHF active source/driver/control overhead |1.55W battery |Earlier0.95W plus0.60W allowance for pass base-drive/helper/feedback; no unmeasured helper omitted |",
        "| VHF boost |88% |Assumption; linear modulator input derives from13.5V × mean load current, replacing guessed70% modulator efficiency |",
        "| Training total |0.450W battery continuous |Own AM buffer/filter/pad/source; normal PA off; increased provision |",
        "| LoRa absent |0W increment |Fully supported base |",
        "| LoRa 10% RX / continuous RX | +0.006 / +0.045 W | M1 assumptions incl MCU wakes/module extras; exact Silicontra remains open |",
        "| LoRa TX burst |0.44W peak provision |Not measured or permission for a given radiated power/airtime |",
        "", "RF windows use20% with no Morse key-up energy credit; Foxoring/beacons/training use continuous worst-service inputs. "
        "VHF carrier1W ERP corresponds to1.259W connector carrier under−1dBd net antenna/feed gain, 80% AM. "
        "All regulator/standby losses are battery-side; no double application of efficiency.", "",
        "## No-LoRa operating profiles", "",
        "Single-band rows assume a controller plus one RF PCB; dual Classic explicitly includes both. "
        "A universal three-PCB unit with only one active band adds the second board's 0.010 W idle allowance, shown separately below.", "",
        "| Profile | Battery W |24h Wh |Runtime h:1P /2P /3P /4P |Minimum model pack |",
        "| --- | ---: | ---: | --- | --- |"]
    for r in data["operating_profiles"]:
        minimum = f"2S{r['minimum_p_for_24h']}P" if r["minimum_p_for_24h"] else "None≤4P"
        lines.append(f"| {r['profile']} | {r['battery_w']:.3f} | {r['wh_24h']:.2f} | " +
                     " / ".join(f"{h:.1f}" for h in r["runtime_h_1p_to_4p"]) + f" | {minimum} |")
    lines += ["", "### Universal three-PCB unit, one active RF band", "",
              "| Profile | Battery W incl second RF idle | Runtime h: 1P / 2P / 3P / 4P |",
              "| --- | ---: | --- |"]
    for r in data["universal_single_band_sensitivity"]:
        lines.append(f"| {r['profile']} | {r['battery_w']:.3f} | " +
                     " / ".join(f"{h:.1f}" for h in r["runtime_h_1p_to_4p"]) + " |")
    lines += ["", "**Planning normal packs: HF4P, Sprint2P, Foxoring1P, VHF4P.** "
        "Sprint1P is a close **model fail**, not an abandoned electrical compatibility requirement. It requires measured total mean≤0.661W; "
        "with the retained common load/conversion inputs, active overhead must be≤0.591W. Lower gate-drive loss/bias or "
        "measured controller savings may restore it; no such saving is assumed. The all-in table therefore lists every pack rather than declaring1P qualified.",
        "", "## VHF sensitivity", "", "| Bias/efficiency case, scheduled20% |Battery W |Runtime1P /2P /3P /4P |", "| --- | ---: | --- |"]
    for r in data["vhf_endurance_sensitivity"]:
        if r["duty"] != 0.2:
            continue
        lines.append(f"| {r['case']} | {r['battery_w']:.3f} | " + " / ".join(f"{h:.1f}" for h in r["hours_1p_to_4p"]) + " |")
    lines += ["", "The 35% dynamic-efficiency stress case **fails 24 h even on 4P**, before adding LoRa. "
        "A low-bias measured design may qualify3P, but cannot inherit the older M1 result. "
        "With continuous LoRa RX, nominal modeled HF 4P is about 27.2 h, VHF 4P 26.6 h, Sprint 2P 44.2 h and Foxoring 1P 40.2 h. "
        "A rise in MCU mean 20→60 mA adds about 0.147 W; temperature/ESR/bias/driver changes require recalculation. "
        "The mean-power limits are 1P 0.661 / 2P 1.322 / 3P 1.983 / 4P 2.644 W using this usable-energy model.",
        "", "## Peaks and acceptance", "",
        f"The VHF35% efficiency envelope crest plus1W peak base/helper provision, LoRa and25% transient margin gives "
        f"about **{data['vhf']['stress_peak_pack_a']:.1f}A at6V**, a calculation. Provision **≥5A single-band** protected "
        "power/connector/BMS paths. Simultaneous dual-TX needs its own waveform/inrush/current qualification and≥7A "
        "initial path provision; poor-efficiency cases can require more. No fuse/current-limit rating is released. "
        "Measure converter switch current separately from pack/PA currents and test all1P–4P geometries/BMS/ESR/cold cutoff.",
        "", "Continuous full-power HF/VHF and conservatively budgeted1W Sprint beacons **do not reach24h within4P**. "
        "Their event duration or power arrangement is a separate user input; do not apply20% duty or silently reduce required RF settings. "
        "A unit remaining powered after RF droops below specification is a fail. Real discharge and temperature tests "
        "must verify the selected profile, optional-LoRa state and end-of-run RF level.", ""]
    return prose_spacing("\n".join(lines))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--write", action="store_true")
    p.add_argument("--check", action="store_true")
    p.add_argument("--simulate", action="store_true", help="Run ideal passive LPFs in installed ngspice only")
    args = p.parse_args()
    data = calculations()
    if args.simulate:
        Path("/tmp/ardf-m2-prep").mkdir(exist_ok=True)
        # Construct the original deck from calculated values; no transistor/source simulation.
        lines = ["* ARDF-TX original ideal LPF comparison; no measured or transistor model.", "Vsource src 0 AC 1"]
        for prefix, values in (("b", data["hf_ideal_lpf"]["values"]),
                               ("c", data["hf_chebyshev_lpf"]["values"])):
            lines.append(f"R{prefix}source src {prefix}1 50")
            node = 1
            for name, value in values.items():
                if name.startswith("c"):
                    lines.append(f"C{prefix}{name[1]} {prefix}{node} 0 {value:.14g}")
                else:
                    lines.append(f"L{prefix}{name[1]} {prefix}{node} {prefix}{node+1} {value:.14g}")
                    node += 1
            lines.append(f"R{prefix}load {prefix}{node} 0 50")
        lines += [".control", "set wr_singlescale", "set wr_vecnames", "ac dec 200 100k 30Meg",
                  "let butterworth_db = db(2*v(b3))", "let chebyshev_db = db(2*v(c4))",
                  "wrdata /tmp/ardf-m2-prep/hf_lpf_ideal.csv butterworth_db chebyshev_db",
                  "quit", ".endc", ".end", ""]
        deck = ROOT / "analysis/hf_lpf_ideal.cir"
        deck.write_text("\n".join(lines))
        subprocess.run(["ngspice", "-b", str(deck)], check=True, capture_output=True, text=True)
        raw = Path("/tmp/ardf-m2-prep/hf_lpf_ideal.csv").read_text().splitlines()[1:]
        (ROOT / "analysis/hf_lpf_ideal.csv").write_text("frequency_hz,butterworth_db,chebyshev_db\n" +
                  "\n".join(",".join(line.split()) for line in raw) + "\n")
    encoded = json.dumps(data, indent=2) + "\n"
    path = ROOT / "docs/M2_RF_CALCULATIONS.json"
    if args.write:
        path.write_text(encoded)
        (ROOT / "docs/M2_POWER_BUDGET.md").write_text(power_document(data))
    if args.check:
        errors = []
        if not path.exists() or path.read_text() != encoded:
            errors.append("Stale calculation artifact")
        if (ROOT / "docs/M2_POWER_BUDGET.md").read_text() != power_document(data):
            errors.append("Stale preparation power table")
        for name, case in data["envelope_cases"].items():
            if not case["sink_required"] and abs(case["pass_mean_w"] - case["mean_formula_w"]) > 1e-8:
                errors.append("Envelope integration disagrees with closed form: " + name)
        if data["pd55008_small_signal_150mhz"]["k"] >= 1:
            errors.append("Source transcription/stability conclusion changed")
        print(json.dumps({"classification": data["classification"], "envelope_cases": len(data["envelope_cases"]),
                          "errors": errors}, indent=2))
        raise SystemExit(bool(errors))
    print(json.dumps({"vhf": data["vhf"], "pd55008": data["pd55008_small_signal_150mhz"],
                      "thermal": {n: {k: c[k] for k in ("pass_mean_w", "pass_peak_w", "current_peak_a", "sink_required")}
                                  for n, c in data["envelope_cases"].items()},
                      "endurance": data["vhf_endurance_sensitivity"], "lpf": data["hf_ideal_lpf"],
                      "chebyshev": data["hf_chebyshev_lpf"]}, indent=2))


if __name__ == "__main__":
    main()

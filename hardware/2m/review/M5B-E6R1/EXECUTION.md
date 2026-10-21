# Executed E6R1 analysis — 21 October 2026

Starting branch `m5b-e6-unified-heatsink`, HEAD `85186204619edec32ad1bb2a3044bb55ea399658`, initially clean. All changes are new E6R1 analysis/scripts/documentation plus current root/docs indexes. No branch history was rewritten. [Machine execution evidence](execution-results.json) records actual environment and run counts; [reproduction](REPRODUCE.md) lists exact commands. Numerical sources and primary documents were inspected before the keying choice.

The complete reproduction runner executed all ten calculation/figure stages, both test suites and the hash inventory. Actual final raw logs are named `logs/reproduction-*.log`. Before finalization the runner was extended to capture `execution-results.json`; that read-only recording step and inventory were executed separately as well. No historical model main or CAD-export command was run.

| Actual check | Outcome |
| --- | --- |
| E6 numerical regression replay | 25 tests, PASS |
| New E6R1 numerical/default-off/negative tests | 37 tests, 0 failures/errors/skips |
| Original E6 thermal failure, newly calculated | 133.7888364489861°C PA; historical difference 0°C; current 1.736013 A, Q401 NTC 56.4397°C |
| Energy balance | Per-phase and integrated DC = RF + device/other heat + signed storage; both supply populations and transitions checked |
| Native-source preservation | 2,831 starting tracked files unchanged, except two explicitly excluded current indexes; all native boards, E6/E5 sources and historical archives included |
| Numerical breadth | 612 normal thermal rows, 108 local thermal sensitivities, 288 sensor faults, 18 healthy sensor checks, 144 electrical/operating sensitivity rows, 18 CW-ID rows, 24 outdoor cases |
| Additional outputs | 54 energy-integral rows, 486 whole-system overhead sensitivities, exactly 3 cooler structures and 117 cooler cases, 8 PDF/PNG plot pairs |
| Linear AM model | 49/51 stable; two unloaded high-gain cases unstable and retained as OPEN, not discarded |
| Independent ngspice 42 fixture | Exit 0; passive tail 0.4142815 ms to 0.1 V, released 2.60028 µJ; analytic agreement within 1% |
| Ideal spectrum | Soft-edge envelope improvement confirmed; physical spectrum/AM/PEP NOT_RUN |
| ERC / DRC / new DFM | NOT_RERUN / NOT_CREATED: this milestone makes no native PCB change |
| Physical tests | NOT_RUN |

The existing E6 baseline native replay (ERC zero errors/warnings; DRC zero errors, **11 existing courtyard warnings**, zero unrouted/parity; 4,096 hardware enable combinations; standard DFM PASS) is **historical evidence**, not fresh E6R1 execution. It is retained byte-for-byte. No warnings were hidden, exclusions introduced, safety thresholds relaxed or CAD manufacturing success claimed here.

Failures and corrections during this run remain in the original development logs:

- An initial independent Morse test expected MO5 repetition length 44 dits. Manual element/letter/word accounting gave 40; the test expectation was corrected and the failed output retained. Actual waveform arithmetic was not changed to satisfy the error.
- Early C kept the driver powered during SPACE. Its nominal beacon pass-case result exceeded 60°C. That result remains in `thermal-driver-kept-on-in-spaces.log`; selected C instead keys U305's actual small downstream domain, includes preparation energy and retains upstream C409. This is a revised proposal, not a change to native hardware or E6 evidence.
- The solar sensitivity originally mutated a cached electrical point dictionary, triggering the energy-conservation assertion. It was corrected to inject external heat into the thermal plate, separately from electrical consumption. Original failures remain in cooling logs; a regression ensures solar cannot alter the electrical cache or create fictitious battery power.
- Adding healthy sensor checks exposed a NumPy boolean JSON-serialization failure. Explicit scalar conversion corrected output serialization; the test now serializes that evidence. The failure remains in `sensor-headroom-final.log`.
- Periodic MO uses the true word period rather than a clipped 60 s restart. Interior edge FFTs likewise use a middle periodic word. These are documented numerical-method corrections; no historical file was overwritten. Guard tests confirm preservation.
- Early open-drain monitor planning could make a missing IC look healthy. The final proposal uses push-pull healthy outputs with pull-downs, NAND fault logic and a default-fault gate pull-up. This remains an unimplemented proposal; 64 gate truth combinations and absent-monitor defaults are tested.

KiCad's Python import prints a property-enum diagnostic and occasionally duplicate image-handler debug messages in raw logs. The source board loads and the actual 98-via/native-hash checks complete with process exit 0. These are binding diagnostics, not fresh ERC/DRC results. A Matplotlib default-config warning during environment inspection was avoided in reproduction by setting a writable `/tmp` cache.

The final decision remains **HOLD for native PCB implementation**. Source/sensor thermal coupling and a simultaneous healthy-operation/fault-interruption threshold window are not bounded. Separate valid full-beacon loss/cooling cases also exceed the Q401 criterion. These engineering failures were not reclassified as harmless tooling warnings. Minimum next closure is the bounded source-stack/junction-proxy/sensor characterization described in the [PA safety note](../../../../docs/M5B_E6R1_PA_THERMAL_SAFETY.md), followed by review of any independent hardware energy restriction required. No hardware experiment, fabrication, push, tag, order or operational release occurred.

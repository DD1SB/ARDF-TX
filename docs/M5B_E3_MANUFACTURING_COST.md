# M5B-E3 standard manufacturing and cost

Select **5 pieces,2 layers, standardFR4,1.6 mm,1 oz, green mask, white legend, lead-free HASL**, one180 ×140 mm routed rectangle. Use ordinary plated through-vias, standard electrical test and no impedance control, via filling/capping, special laminate, castellations, edge plating or factory assembly. Do not substitute1.6 mm/2 oz: JLC's0.16 mm geometry requirement would conflict with existing0.15 mm signals. The1 oz power/thermal analysis provides no reason to select that alternative. Do not specify the analytical1.50 mm dielectric as a negotiated core tolerance.

The proposal is manually assembled in stages, with one of five boards initially populated. HASL is selected for ordinary cost and hand assembly. Its nonplanarity requires inspection/reflow care on the PHA, PD andRNW hidden contacts; see [JLC's HASL discussion](https://jlcpcb.com/blog/hasl-surface-finish-pcb). Their fine contacts are a solder-process risk, not an established incompatibility requiring ENIG. Do not silently change finish inCAM. If real incoming planarity or joint inspection fails, hold assembly and review ordinary ENIG as a separate quoted correction. A stencil/paste file is an assembly aid, not a required JLC assembly service.

Only `hardware/2m/review/M5B-E3/gerbers/` is proposed fabrication data. It contains nine copper/mask/paste/legend/outline Gerbers, job metadata, separatePTH/NPTH drills and maps. Retain the **physical-netties IPC** as a review reference; standard JLC electrical test derives connectivity from Gerber copper, so no special netlist service is required. the logicalIPC and alias table explain intentional RF net merges. Do not upload `development/` or analysis screenshots. `SHA256SUMS` and `native-inputs.json` bind the files to the final native project. No files have been uploaded.

Purchased parts and prices are unchanged fromE2. Full itemized6/10/20 budgets and source classifications are regenerated, not hand-patched:

| Population | 6 each | 10 each | 20 each | Unquoted at10 |
| --- | --- | --- | --- | --- |
| BOOST2S | €54.33 | €50.27 | €49.94 | €28.09 |
| BUCK4S | €52.76 | €49.03 | €48.71 | €27.95 |
| TRAIN_ONLY | €14.11 | €14.11 | €14.11 | €10.02 |

There are272 fitted purchased parts/25ICs inBOOST2S,268/25 inBUCK4S and 103/13 inTRAIN_ONLY. RF lines, test pads and footprint assignments are not extra purchased parts. The dated pricing observations remain observations, not current reservations. L301 zero-stock/backorder, L634 nonstocked cut-tape lead time and U950 conflicting regional stock remain visible. Unquoted material remains€28.09/€27.95/€10.02 respectively at 10. No new supplier quote is claimed.

`PCB-cost-estimate.csv` gives a deliberately transparent **engineering allowance**, not JLC pricing:€10–20 setup plus€250–500/m² at actual 0.0252 m² area. Five boards:€41.50–83; ten:€73–146; twenty:€136–272 net. Shipping€10–25 and destinationVAT are separate. The historicalE2 five-board allowance was€60–100 before shipping; the ranges overlap, so **no achieved PCB saving is booked**. An actual automated quote is still pending. Published capability, localDFM compatibility, budget estimate, quote and factory CAM acceptance are separate statuses.

The180 ×140 outline is retained because the RF return strip, separate ports, hand-rework access and two insulated thermal assemblies use the geometry. Blank evaluation area is acknowledged, but shrinking/panelizing this first board would add routing/mechanical risk unrelated to the manufacturing correction. No100 ×100 promotional price is assumed. External heatsinks/TIM/mounts remain approximately€12 per initially populated board, harness€3 and antenna/feed€12 estimates; controller, battery, charger, enclosure and labor remain separate. Measure actual commissioning time rather than booking fictitious labor savings.

The package is **GO for independent standard-option quotation-data review**, subject to user authorization before upload. It is not an order or manufacturing release. Normal automated pricing should require only the standard selections above; no exceptional fabrication agreement is part of the design.

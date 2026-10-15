# M5A-R1 — ST reference audit

Date: **2026-10-15**. **M5A-R1 electrical evaluation candidate — NOT RELEASED. All physical tests NOT_RUN.**

**Reference reconstruction is incomplete.** Original document text and tables were retrieved, but the raster circuit/package drawings could not be inspected. Direct binary downloads failed with HTTP/2 errors,403 responses or timeouts, including approved network retries. Browser screenshot calls supplied image markers without usable image pixels. The original Gerber ZIP was located but not downloaded. No connection trace, pad numbering or Gerber inspection is claimed from those unavailable images. This blocks acceptance criteria 1 and 4–5 and the coupon layout.

## Dated primary-source log

| Source | Version/evidence available on 2026-10-15 | Disposition |
| --- | --- | --- |
| [ST board page](https://www.st.com/en/evaluation-tools/steval-tdr003v1.html) | NRND; original PD84001/PD54008L-E board | Historical RF evidence; not production procurement |
| [Full board document](https://www.st.com.cn/resource/en/datasheet/steval-tdr003v1.pdf) | DocID17343 Rev 1, 31-Mar-2010; text/tables retrieved | Figures 12–17 require visual tracing; layout figures 10–11 unavailable as pixels |
| [Original schematic](https://www.st.com/resource/en/schematic_pack/steval-tdr003v1_schematic.pdf) | Raster circuit not recoverable in this environment | OPEN, do not infer nets from BOM |
| [Original BOM](https://www.st.com/resource/en/bill_of_materials/steval-tdr003v1_bom.pdf) | Two-page spreadsheet export, no visible revision/date | Values and discrepancies below; topology not established |
| [Original Gerber ZIP](https://www.st.com/resource/en/board_manufacturing_specification/steval-tdr003v1_gerber.zip) | Manufacturer link found; binary inaccessible | NOT_INSPECTED; no guessed aperture/line endpoints |
| [Final datasheet](https://www.st.com/resource/en/datasheet/pd54008l-e.pdf) | January 2007 Rev 2; text retrieved, package picture unavailable | Functional G/D/S only; numeric landing OPEN |
| [Final product status](https://www.st.com/en/radio-frequency-transistors/pd54008l-e.html) | Active, volume production, PowerFLAT5×5HV | Current device candidate; not the obsolete PD84001 |

The 2010 document reports 5 W,135–175 MHz at 7.2 V with 5–10 dBm input,≤1.5 A and 47–52% PAE under its table conditions. These apply to the complete original two-stage assembly. Its harmonic and mismatch claims cannot transfer to changed matching, driver or AM operation. No RF AM transfer curve or isolated 144 MHz final gain was retrieved.

## Component evidence and contradictions

Standalone BOM positions, values only: C1/C5/C6=1 µF; C16=NC; C2/C3/C4/C7/C8/C9/C10=330 pF; C11=56 pF, C12=27 pF, C13=33 pF, C14=100 pF, C15=39 pF. L1=24 nH, L2=33 nH, L3=35.5 nH, L4/L5=18 nH. R1/R4=62 kΩ, R2=430 kΩ, R3=240 Ω, R5=150 kΩ, R6=11 Ω. Filter C1F..C7F=3.3/18/12/22/27/22/15 pF; L1F/L2F/L3F=39/22/27 nH. This is an inventory, not a netlist.

The standalone BOM labels the final PD54008L but gives part-code PD54003L. The 2010 document title/component table and current board page identify **PD54008L-E**. Therefore choose that exact device; actual characterization-lot markings remain unknown. Never substitute PD54003L.

Other conflicts:330 pF versus Murata 391 code; 2010 C1/C5=NC instead of 1 µF; L1 nominal 24 nH with 33 nH code; L3 nominal 35.5 nH with 22 nH code; L5 differs between 18nH0603 and 18.5 nH minispring. Connector codes differ 801/881. Resolve from actual drawings/layout and supplier data before copying any order list.

## Transmission-line inventory and reuse matrix

The BOM specifies 0.508 mm FR4/70 µm copper,0.92 mm nominal 50 Ω lines, TL1..TL9 lengths 3/7.2/6.23/6.62/5.8/2.2/11/12.4/2 mm. **Endpoints and stage assignment are OPEN.** Numbers alone cannot reconstruct their matching function.

| Original block | Disposition | Exact remaining evidence |
| --- | --- | --- |
| RF input/PD84001 matching | Incompatible with substituted MMIC | Read Figure 15; retain 50 Ω boundary only after verification |
| PD84001 | Not reusable | Obsolete; no old-stock production strategy |
| Interstage | Recalculate/measure | Figure 16 endpoints and final gate impedance; MMIC output differs |
| PD54008L-E final | Preferred evaluation candidate | Physical terminal map, thermal land and 144 MHz gain OPEN |
| Drain supply/decoupling | Modify for AM | Figure 12/13; fixed bias and no bulk capacitor on modulated drain |
| APC/bias | Not copied blindly | Identify gates controlled by APC before deciding removal; no servo-modulation assertion |
| Final matching | Potentially reusable after stack-up validation | Figure 17 and Gerber endpoints OPEN |
| Harmonic LPF | Potentially reusable | Figure 14 topology OPEN; R1 retains explicitly interim R0 ladder |
| Ground/thermal vias | Reuse principles after drawings | Package/land images and actual stack-up mandatory |


R1 deliberately contains OPEN matching positions rather than falsely claiming the original ST network. Close this narrowly: obtain readable Figures 12–20 and original manufacturing archive; trace named nodes and physical G/D/S lands; replace the marked R1 matching harness/LPF with the verified reference derivative. No broader architecture study is required.

The calculation script evaluates microstrip impedance with zero-thickness formulas only. At 1.6 mm,0.92 mm copper is far above 50 Ω; line width and phase must be recalculated. Proposed coupon substrate remains 0.508 mm FR4/70 µm copper, supplier-declared dielectric/mask/tolerances. Copper-thickness and launch/via corrections require EM or VNA confirmation. Original artwork is manufacturer copyright; linked, not relicensed or reproduced as project-owned CAD.

## Calculated substrate sensitivity

Zero-thickness, unmasked microstrip approximation, not a qualified fabrication stack-up. The original70µm copper correction is intentionally not hidden in these numbers. Supplier dielectric and actual launch/via geometry remain required.

| Height mm | Assumedεr | Z at0.92mm Ω | Approximate50Ω width mm | Phase deg/mm at144.7MHz |
| --- | --- | --- | --- | --- |
| 0.508 | 4.2 | 53.0 | 1.014 | 0.310 |
| 0.508 | 4.5 | 51.3 | 0.962 | 0.320 |
| 0.508 | 4.8 | 49.9 | 0.916 | 0.329 |
| 1.6 | 4.2 | 92.3 | 3.192 | 0.299 |
| 1.6 | 4.5 | 89.5 | 3.031 | 0.308 |
| 1.6 | 4.8 | 87.0 | 2.884 | 0.317 |

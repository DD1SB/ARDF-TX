"""Bind executed gates to final native inputs and write the evaluation decision."""
import collections,hashlib,subprocess,zipfile
from m5b_e6r2_common import *
def read(n):return json.loads((OUT/n).read_text())
def main():
 guard();boardhash=sha(HW/'RF2M.kicad_pcb');erc=read('ERC.json');drc=read('DRC.json');v=read('verification.json');dfm=read('JLCPCB-DFM.json');reg=read('DFM-regression.json');src=read('source-assembly-regression.json');ground=read('ground-contact-audit.json');fab=read('fabrication-data-audit.json');rep=read('final-reproduction.json');mech=read('mechanical-solid-checks.json');sim=read('simulation-results.json');mass=read('mechanical-mass.json')
 assert not [x for s in erc['sheets'] for x in s['violations']]
 assert not drc['unconnected_items'] and not drc['schematic_parity'];assert all(x['severity']=='warning' and x['type']=='missing_courtyard' for x in drc['violations'])
 old=json.loads(gitfile('hardware/2m/review/M5B-E5/DRC.json'))
 def warnset(j):return sorted((x['type'],tuple(sorted(i['description'] for i in x['items'])))for x in j['violations'])
 assert warnset(old)==warnset(drc) and len(drc['violations'])==11
 assert sha(HW/'RF2M.kicad_pro')==hashlib.sha256(gitfile('hardware/2m/RF2M.kicad_pro')).hexdigest(),'No new DRC exclusions/rules/ignored checks'
 for name,got in [('verify',v['native_sha256']),('DFM',dfm['native_sha256']),('ground',ground['native_SHA256']),('fabrication',fab['native_SHA256']),('reproduction',rep['native_SHA256'])]:assert got==boardhash,('stale report',name)
 assert not dfm['errors'] and reg['status']=='PASS' and ground['components']==1 and rep['netlist_semantics_equal']
 assert v['logic']['combinations']==4096 and len(v['keying_truth_rows'])==16 and len(sim['cases'])==8 and len(sim['loop_gain'])==2
 assert all(x['ngspice_returncode']==0 for x in sim['cases']) and all(x['positive_margin'] for x in sim['loop_gain'])
 assert len(src['native_tests'])==16 and len(src['thermal_model_negative_cases'])==4 and len(mech['negative_solid_tests'])==2
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));collision=[]
 for f in b.GetFootprints():
  for a in f.Pads():
   if a.GetAttribute()!=p.PAD_ATTRIB_PTH:continue
   x,y=xy(a.GetPosition())
   if 84.5<=x<=99.5 and 28<=y<=72 or any(abs(x-xx)<=2 and abs(y-yy)<=7 for xx in [41,143]for yy in [40,100]):collision.append((f.GetReference(),a.GetNumber(),x,y))
 assert not collision,'PTHlead/bar/support collision'
 for archive in ['RF2M-M5B-E6R2_JLCPCB_5boards.zip','RF2M-M5B-E6R2_FULL_TOP_STENCIL.zip']:
  with zipfile.ZipFile(OUT/'fabrication'/archive)as z:
   assert z.testzip() is None
   for name in z.namelist():assert z.read(name)==(OUT/'gerbers'/name).read_bytes(),('Archive byte mismatch',archive,name)
 costs=read('costs.json');native=boardhash[:16]
 report=dict(date=DATE,starting_commit=START,branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip(),native_SHA256=boardhash,disposition='GO_FOR_FIVE_BARE_RF2M_E6R2_EVALUATION_BOARDS',ERC_errors=0,ERC_warnings=0,DRC_errors=0,DRC_inherited_warnings=len(drc['violations']),unrouted=0,parity=0,new_exclusions=0,enable_combinations=v['logic']['combinations'],safety_scenarios=len(v['logic']['scenarios']),local_keying_rows=len(v['keying_truth_rows']),negative_native_cases=len(v['negative_tests']),critical_maps=v['manufacturer_pin_maps'],source_native_cases=len(src['native_tests']),source_thermal_model_negatives=4,DFM_mutations=len(reg['mutations']),solid_negative_cases=2,ngspice_transients=8,AC_cases=2,numerical_unittests=14,CAM_reproduced=len(rep['CAM_comparisons']),PTH_hits=fab['PTH_hits'],NPTH_hits=fab['NPTH_hits'],PTH_under_bar_support_hits=collision,cooling_material_mass_g=mass['cooling_hardware_g'],hardware_qualification='NOT_RUN',pushed=False,ordered=False,production_release=False)
 save('final-review.json',report)
 text=f'''# M5B-E6R2 review decision

**GO for five bare RF2M E6R2 evaluation boards.** This is an engineering
candidate for independent review, not powered-operation or production acceptance.
No boards/stencils were ordered, hardware energized, Git branch pushed or tag created.

Starting `{START}`, branch `m5b-e6-unified-heatsink`.
Final local commit is recorded by Git history. Native PCB SHA-256:
`{boardhash}`.

| Gate | Disposition | Evidence |
|---|---|---|
|1.Native electrical/mechanical implementation|PASS|Complete native schematic/PCB; one supported cooler; insulation and exact device lead views audited|
|2.Five bare evaluation PCBs|GO|CAD/electrical/DFM/reproduction gates below; no known intrinsic blocker remains|
|3.Initial powered prototype|NOT_RUN|Requires assembled interfaces,verified isolation,inhibit,current-limited supply and dummy-load instrumentation|
|4.Operational transmitter|NOT_RUN|Measured RF/AM,spectrum,thermal,shutdown,continuous beacon and environment qualification required|

Executed: ERC 0 errors/0 warnings; DRC 0 errors, 0 unrouted, 0 parity issues. All 11
missing-courtyard warnings exactly match E5. The project configuration is
byte-identical: no new exclusions or ignored checks. Python enum/image-handler
diagnostics are recorded in raw logs; they are not hidden CAD violations.

Electrical/native checks: {v['parts']} footprints, {v['manufacturer_pin_maps']} critical manufacturer maps,
4,096 enable combinations, {len(v['logic']['scenarios'])} safety scenarios, 16 local-keying rows,
{len(v['negative_tests'])} negative cases. Source process: 16 native/input mutations and 4 adverse
thermal-model cases rejected; these are not physical fault-detection results.
The final source/mask/paste/98-via geometry is independently checked unchanged.
Two actual solid-collision negatives exercise the carrier/tab checks. Ground
contact graph: one component. All 12 main-current copper paths remain connected.

Ngspice: 8 transient cases, 2 AC return-ratio cases, 14 numerical tests. Loaded/
unloaded modeled loop margins are 85.87°/68.92°. The TI model is external;
ST BJTs and PA load are bounded generic/envelope models, not characterized RF
models. Converter switching-loop/RF spectra and hot device corners remain open.
BF20 clips the modeled crest; it is explicitly not full-profile qualification.

Standard-JLCPCB DFM PASS, {len(reg['mutations'])} native mutations detected. Actual minimum track 0.15 mm,
via annulus 0.15 mm, component PTH annulus 0.275 mm. Ordinary 0.6/0.3 mm via margin
exceptions remain individually listed. No special stackup, filled/capped vias
or controlled-impedance service. 150×110 mm, 2 layers, 1.6 mm FR4, 1 oz, green/white, HASL.
Nine Gerbers + separate PTH/NPTH drills ({fab['PTH_hits']}/{fab['NPTH_hits']} hits) reproduce from native.
Fresh 11 CAM files are geometrically identical; only export timestamps differ.
Five source-paste windows still total 6.765 mm². Full top stencil is supplied.

The new flat BD139 footprint initially mirrored the manufacturer front view.
It was corrected to physical 3E–2C–1B left-to-right, while numeric 1B/2C/3E remains.
The rejected draft is preserved and detected by a native negative test. The
shared Q404/Q405 normal-key clamp injection was also corrected by separating
Q405's emergency base network. An isolated C409 reservoir-ground pour found by
the actual contact graph was corrected before final routing. Mechanical review
corrected carrier/foot overlap and foot-screw engagement. These were real
implementation corrections; all final relevant gates pass.

One SK81 100 SA 100×100×15 mm, 15×44×6 mm bar, rated 0.25 mm source TIM, two mica interfaces,
IB6/steel Q401 fastening and PA66 Q402 fastening form one independently supported
assembly. Calculated/indexed hardware mass {mass['cooling_hardware_g']:.1f} g before braid/compound,
approximately 254 g assembled allowance; not weighed. Lower carrier ~113 g and the
preserved upper carrier are separate. Seven-unit cooler material estimate
€{costs['cooler_material_each_estimate'][0]:.2f}–{costs['cooler_material_each_estimate'][1]:.2f}/unit plus €2.59 keying parts;
base, posts, housing, labor and minimum stock costs are stated separately.
No complete €120/€150 transmitter price is demonstrated.

E6R1's modeled 1 W/40°C Classic/Sprint/continuous-MO PA peaks remain
74.31/73.72/87.76°C; Q401 46.43/46.03/59.51°C. The continuous-beacon margin is
only 0.49°C. The 134.72°C degraded-contact scenario remains an assembly/qualification
risk. Preserve 110°C PA target, 125°C ceiling, Q401 60°C and Q402 80°C criteria.
No source-region sensor is claimed to measure Tj; no threshold was raised.
First-article solder/contact/insulation/current/RF/temperature measurements
must precede prolonged full-power use. These uncertainties do not prohibit bare
boards under the requested evaluation gates.

Controller M6-L2, RF80 M4A-V1R1 and every historical review/archive pass the
preserved-start hash guard. Protected RF signal copper, matching/filter geometry,
Q501 position and all 20 controller pins are retained. Current core native sources
are revised only for RF2M. No acceptance tag or production release.

See [manufacturing](M5B_E6R2_MANUFACTURING.md), [first article](M5B_E6R2_FIRST_ARTICLE_TEST.md)
and [review/reproduction](../hardware/2m/review/M5B-E6R2/README.md).
'''
 (ROOT/'docs/M5B_E6R2_REVIEW_DECISION.md').write_text(text)
 (OUT/'README.md').write_text('''# RF2M M5B-E6R2 evaluation review

**GO for five bare evaluation PCBs**, subject to independent review. Powered/
operational qualification remains NOT_RUN. No order,push,tag or release.

- [Decision](../../../../docs/M5B_E6R2_REVIEW_DECISION.md),[implementation](../../../../docs/M5B_E6R2_IMPLEMENTATION.md),[first article](../../../../docs/M5B_E6R2_FIRST_ARTICLE_TEST.md).
- [Native project](../../RF2M.kicad_pro),[native snapshot](RF2M-M5B-E6R2-native.zip),[schematic PDF](RF2M.pdf),[netlist](RF2M.net.xml).
- [Fabrication ZIP](fabrication/RF2M-M5B-E6R2_JLCPCB_5boards.zip),[full top stencil](fabrication/RF2M-M5B-E6R2_FULL_TOP_STENCIL.zip),[manufacturing](../../../../docs/M5B_E6R2_MANUFACTURING.md).
- [ERC](ERC.json),[DRC](DRC.rpt),[DFM](JLCPCB-DFM.json),[electrical/native results](verification.json),[final gate record](final-review.json).
- [Complete native3D](RF2M-3D.png),[top](RF2M-3D-top.png),[bottom](RF2M-3D-bottom.png),[mechanical drawings/STEP](mechanical/).
- Population BOMs: [BUCK4S](BOM_BUCK4S.csv),[BOOST2S](BOM_BOOST2S.csv),[TRAIN_ONLY](BOM_TRAIN_ONLY.csv),[shared cooler](shared-heatsink-BOM.csv),[costs](costs.json).
- [Package audit](COMPONENT_FOOTPRINT_AUDIT.md),[simulation](simulation-results.json),[source regressions](source-assembly-regression.json),[ground graph](ground-contact-audit.json).
- [Executed final report](FINAL_REPRODUCTION.md), [reproduce](REPRODUCE.md), [fresh CAM comparison](final-reproduction.json), [repeat ZIP comparison](archive-repack-comparison.json), [SHA256 inventory](SHA256SUMS).

Historical E5/E6/E6R1 evidence is immutable. `baseline-E5-native.zip` captures
starting native sources. Development drafts/failures are retained for audit;
**development/** is not manufacturing data. In particular,the initial mirrored
BD139 draft is deliberately rejected. Use only the final fabrication directory.

The complete new cooling geometry is dimensioned. Upper controller/carrier
views retain the historical study transform and are identified reference
envelopes,not a newly qualified housing. Package plastic/fin details are
simplifications; mounting planes,formed leads,hardware and cutouts are explicit.
''')
 print('GO five bare evaluation PCBs; physical gates NOT_RUN')
if __name__=='__main__':main()

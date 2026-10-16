#!/usr/bin/python3
"""Reproduce and seal R4 CAD review. Never creates a PCB or manufacturing order."""
import argparse,csv,hashlib,json,math,re,subprocess,sys,xml.etree.ElementTree as ET
from pathlib import Path
from m5a_r4_design import ROOT,DEST,OUT,frozen

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj):(OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
def run(*args):
    result=subprocess.run(args,cwd=ROOT,capture_output=True,text=True)
    if result.returncode:raise RuntimeError(' '.join(args)+'\n'+result.stdout+result.stderr)
    return (result.stdout+result.stderr).strip()

def sources():
    entries=[
      ('ST_VHF','https://www.st.com/resource/en/datasheet/steval-tdr003v1.pdf','DocID17343Rev1March2010;printedpp9-11visuallyinspected;26matching/filter positions transcribed','st-full.pdf','Recovered manufacturer PDF via DatasheetArchive distributors/Datasheets-DGA5/438709.pdf;mirror appends one archive page. Direct ST PDF/schematic binary HTTP2/HTTP1 failures. No original GerberZIP obtained.'),
      ('ST_PD54008','https://www.st.com/resource/en/datasheet/pd54008l-e.pdf','Jan2007Rev2pp1/11/13;pinregions/mechanical/landing visuallyinspected','pd54008.pdf','Manufacturer-authored PDF retrieved from https://media.pneda.com/datasheetfiles/pd54008l-e.pdf ;not sourcing from that broker.'),
      ('ST_status','https://www.st.com/en/radio-frequency-transistors/pd54008l-e.html','Active;volumeproduction;PowerFLAT5x5HV',None,'Manufacturer page read;does not establish stock.'),
      ('PD_price','https://www.mouser.de/de/ProductDetail/STMicroelectronics/PD54008L-E?qs=sGAEpiMZZMsPo2fL1zXfdqEwePZnwSUq%2Fv1gNDbGsv4%3D','EUR7.35@1/5.30@10/4.78@100;CTMOQ1;indexed3430stock',None,'Indexed/cached dated lookup,not reserved quote. Manufacturer tray/reel3000 is not customer MOQ.'),
      ('PHA_datasheet','https://pccomponents.com/datasheets/MINI_-PHA1.pdf','Mini-CircuitsRevDoriginalpin/operatingtable','pha1.pdf','Manufacturer-authored distributor mirror;main Mini-CircuitsPDFreturned403.'),
      ('PHA_extended','https://filur.net/userdata/modules/productFiles/file_v0DXDEJ.pdf','ManufacturerRevD+2011typicaldata+DF782RevG2017drawing;31page distributor bundle inspected','pha1-layout.pdf','5V50/200MHzexamples22.70/22.64dBm;not a guaranteed144MHzminimum. Suggested land transcribed and dimensions asserted;ground stencil/vias/assembly remain OPEN.'),
      ('PHA_price','https://www.digikey.es/es/products/detail/mini-circuits/PHA-1/13928098','EUR2.88@1/2.351@50;CTMOQ1;indexed12794stock',None,'Other regional caches differ,including an anomalousFRMouser1pieceprice. SelectedDigiKeyEURnetbasket,not cross-mixed quantities.'),
      ('RF_L56','https://www.digikey.fr/fr/products/detail/murata-electronics/LQW18AN56NG80D/4422179','EUR.120@1/.102@10/.0839@100;indexed28315;RFwirewound56nH',None,'Exact56nH observation.91/180nH costs remain estimates;no silent application of56n price to allRFinductors.'),
      ('RF_L_specs','https://www.mouser.com/datasheet/2/281/1/JELF243A_0102-3158940.pdf','Murata-authoredQ/SRF/currentfamilytable read via browser',None,'Binaryfailed;91nHspec33Q,1.9GHz,520mA frommanufacturer table.180nHcomplete qualificationOPEN.'),
      ('Coilcraft_LPF','https://www.coilcraft.com/en-us/products/rf/ceramic-core-chip-inductors/1008-%282520%29/1008cs/1008cs-390/','39nH,Q60@350MHz,SRF1500MHz,1Arise-currentbasis',None,'Manufacturer family/current suffix confirmed;EUR0.75prices for LPFvalues remain estimates,not USDconversion claims.'),
      ('Coilcraft_A05T','https://www.coilcraft.com/en-us/products/rf/air-core-inductors/mini-spring/axxt-bxxt/a05t/','5turns18.5nH,Q132@150MHz,SRF2.5GHz,4Arise-currentbasis',None,'OriginalSTcoil family. Exact land to be transcribed;no inventedDIY geometry.'),
      ('Coilcraft_bias_feed','https://www.coilcraft.com/en-us/products/rf/air-core-inductors/midi-spring/1812sms/1812sms-33n/','Current1812SMS-33NJLC/GLC33nH,Qmin100@150MHz,SRF2.5GHz,3Arisebasis',None,'Manufacturer selected configuration not directly purchasable. Exact CT EUR quote/landing still OPEN.0.80EUR remains estimate,not stock-backed.'),
      ('Panasonic_reservoir','https://industrial.panasonic.com/sa/products/pt/os-con/models/25SVPG150M','150uF25V+/-20percent,ESR13mohm@100kHz,4.2Arms@105C,C10diameter6.3mm/height9.9mm',None,'Exact candidate replaces generic OPEN MPN. CT catalog entry exists at DigiKey26003740;EUR price,available stock,temperature ESR and exact land not closed. No500factoryMOQ assumption.1.50EUR estimate unchanged.'),
      ('A05T_price','https://eu.mouser.com/ProductDetail/Coilcraft/A05TJLC?qs=zCSbvcPd3pYJqqPlmZ4EHA%3D%3D','EUR1.51@1/1.28@10/1.18@25;CTMOQ1;stock110EU/331ATcaches',None,'Not factory700MOQ. Dates/caches/stock not reservation.'),
      ('TPS611781_price','https://www.digikey.fr/en/products/detail/texas-instruments/TPS611781RNWR/7056156','EUR2.71@1/2.031@10/1.86@25;CTMOQ1;indexed4371',None,'Replaces carried2.25EURestimate. Manufacturer RNW land now recovered separately.'),
      ('TPS611781_drawing','https://www.ti.com/lit/ds/symlink/tps61178.pdf','SLVSDA7E,August2019;RNW0013A4222804/C11/2019board/stencil drawings visually inspected','tps61178.pdf','13 physical terminals include independent center6PGND7SW8VOUT bars. Local candidate copper/mask/paste land dimensions asserted;no common grounded EP invented.'),
      ('TPS54302_price','https://www.digikey.de/en/products/detail/texas-instruments/TPS54302DDCR/6572466','EUR1.21@1/.879@10/.796@25;CTMOQ1;indexed6904',None,'SameDDCRsilicon/ordercode,not a nonexistent CT assumption. Replaces0.55EURestimate;otherregionalcachesvary.'),
      ('HC21','https://assets.nexperia.com/documents/data-sheet/74HC21.pdf','Rev10Jan17,2024;dual4inputANDphysicalpinmap',None,'CurrentmanufacturerPDFtext inspected;old74HC_HCT21URLfailed. No discontinued652 suffix selected.'),
      ('D45H11','https://www.st.com/resource/en/datasheet/d45h11.pdf','DocID4213Rev5Oct2009;RthJC2.5K/W;hotSOAgraphqualificationOPEN',None,'Manufacturerpinmap inheritedR1assertion;thermal rating is not hot linear SOA proof.'),
      ('RD06HVF1','https://www.rfparts.com/old_site/pdf_docs/RD/rd06hvf1.pdf','Mitsubishi175MHz6W12.5Vactualtestcircuit','rd06.pdf','OriginalmanufacturerPDFdistributormirror. Finite-stock alternative not selected;175MHzperformance not144MHzAMproof.'),
      ('RD06_EOL','https://www.anglia.com/registration/pcn_ptn/docs/ptn/SiRF%20TO-220%20EOL%20announcement_20220511.pdf','MitsubishiMay11,2022TO220discontinuation,Dec2022lastorders','rd06-eol.pdf','Originalmanufacturer notice obtained. SDR-Kits listing alone cannot confirm25+sparesallocation.'),
      ('IARU','https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf','2025Appendix1T2.8andT2.4',None,'Primaryrulesread;not legal transmitter authorization.'),
    ]
    data=[]
    for key,url,version,file,note in entries:
        p=Path('/tmp/ardf-m5ar4')/file if file else None
        data.append(dict(id=key,accessed='2026-10-16',url=url,evidence=version,note=note,retrieved_binary_sha256=sha(p)if p and p.exists()else None,temporary_original_file=str(p)if p and p.exists()else None))
    write('sources.json',dict(date='2026-10-16',entries=data,third_party_files='Not vendored/relicensed. Temporary originals used for inspection;stable publisher URLs and retrieval hashes retained.',failed_originals=['ST standalone schematic binary','ST standalone BOM binary','ST Gerber ZIP main/regional servers','Mini-Circuits directPDF403','several archive/download mirrors;usable manufacturer-authored PDFs recovered as stated']))

def checks():
    erc=json.loads((OUT/'erc.json').read_text());issues=[v for s in erc['sheets']for v in s['violations']]
    assert not any(v['severity']=='error'for v in issues)
    for p in (ROOT/'tools').glob('m5a_r4_*.py'):compile(p.read_text(),str(p),'exec')
    assert frozen()==json.loads((OUT/'preserved-baseline.json').read_text())
    # Check old R3 bytes IN THE TAG, not historical root-relative hashes against new CAD.
    manifest=json.loads(run('git','show','m5a-r3:hardware/2m/review/M5A-R3/file-manifest.json'))
    for name,digest in manifest['files'].items():
        blob=subprocess.check_output(['git','show','m5a-r3:'+name],cwd=ROOT)
        assert hashlib.sha256(blob).hexdigest()==digest,('historicalR3',name)
    # Run the original R1 expectations/pin assertions read-only on its own frozen netlist.
    import m5a_r1_verify as old
    nets={}
    for net in ET.parse(DEST/'review/M5A-R1/RF2M.net.xml').findall('./nets/net'):
      for node in net.findall('node'):
        nets.setdefault(node.get('ref'),{})[node.get('pin')]=None if net.get('name').startswith('unconnected-')else net.get('name')
    parts={p['ref']:p for p in json.loads((DEST/'archive/M5A-R1/RF2M.electrical.json').read_text())['parts']}
    prior=old.tests(nets);priorpins=old.audit(nets,parts)
    write('archived-r1-regression.json',dict(logic=prior,pin_assertions=len(priorpins),status='PASS_READ_ONLY_ARCHIVED_DESIGN',note='OriginalR1expectations,not claimingunchangedR1RFvaluesareR4. No old artifacts overwritten.'))
    # Dated local documentation links, including artifact/native links.
    docs=list((ROOT/'docs').glob('M5A_R4_*.md'))+[DEST/'README.md',OUT/'README.md'];links=[]
    assert len(list((ROOT/'docs').glob('M5A_R4_*.md')))==6
    for doc in docs:
      for target in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
        if target.startswith(('https://','http://','#')):continue
        path=(doc.parent/target.split('#')[0]).resolve();assert path.exists(),(doc,target);links.append(dict(document=str(doc.relative_to(ROOT)),target=target))
    costs=json.loads((OUT/'costs.json').read_text());rows=list(csv.DictReader((OUT/'RF2M_BOM.csv').open()))
    for s in costs['summary']:
        rs=[x for x in rows if x['variant']==s['variant']and int(x['fleet'])==s['fleet']]
        assert len(rs)==s['physical_components']
        assert abs(sum(float(x['allocated_per_board_net_EUR'])for x in rs)-s['component_net_EUR'])<1e-8
        pooled={}
        for r in rs:
            value=float(r['unit_net_EUR']);assert pooled.setdefault(r['MPN'],value)==value,('pooledMPNprice',r['MPN'])
    c=json.loads((OUT/'calculations.json').read_text())
    assert 5.2<c['driver_OV_min_V_under_assumed_1p5percent_reference']<5.4
    assert c['driver_OV_max_V_under_same']<5.55 and c['driver_20us_RC_plus_ESR_upper_calculation_V']<5.9
    for row in csv.DictReader((OUT/'thermal.csv').open()):
        pc=(1 if row['profile']=='full'else .3)*10**.175;m=float(row['depth']);i=float(row['carrier_drain_current_A_ASSUMED']);vc=float(row['PA_center_V']);vin=float(row['upstream_V'])
        assert pc*(1+m*m/2)<vc*i*(1+m*m/2),'RF energy exceeds modeled PA input'
        assert abs(vin*i-vc*i*(1+m*m/2)-float(row['pass_mean_AM_W']))<1e-8
    assert not (DEST/'RF2M.kicad_pcb').exists(),'Do not silently claim a PCB release'
    parsed=run('/usr/bin/python3','-c',"import pcbnew;from pathlib import Path;p=Path('hardware/2m/ARDF_2M.pretty');print([(f.stem,len(pcbnew.FootprintLoad(str(p),f.stem).Pads()))for f in sorted(p.glob('*.kicad_mod'))])")
    write('native-footprint-parse.json',dict(tool='KiCad10.0.6 pcbnew.FootprintLoad',status='ALL_3_CANDIDATE_LAND_FILES_LOAD',output_and_diagnostics=parsed,note='Headless KiCad emits PROPERTY_ENUM No enum choices defined diagnostics while loading;files load and pad counts are asserted separately. This is not PCB DRC or physical footprint qualification.'))
    pdf=run('pdfinfo',str(OUT/'RF2M.pdf'));assert 'Pages:'in pdf
    write('final-checks.json',dict(status='PASS_DOCUMENT_CAD_LEDGER_CHECKS_ONLY',ERC_errors=0,ERC_warnings=sum(v['severity']=='warning'for v in issues),ERC_ignored_checks=erc['ignored_checks'],local_links=len(links),documents=6,historical_R3_files_in_tag=len(manifest['files']),archived_R1_combinations=prior['combinations'],archived_R1_scenarios=len(prior['scenarios']),preserved_files=len(frozen()),population_cost_baskets=len(costs['summary']),driver_model='Conditional RC upper arithmetic<5.9V;not physical qualification',RF_energy_sanity='PASS for stated efficiency assumptions',PCB_DRC='NOT_RUN_NO_PCB',physical_tests='NOT_RUN'))

def seal():
    paths=list(OUT.rglob('*'))+list((ROOT/'docs').glob('M5A_R4_*.md'))+list((ROOT/'tools').glob('m5a_r4_*.py'))
    paths += [p for p in DEST.iterdir()if p.is_file()and p.suffix in ['.kicad_sch','.kicad_pro','.kicad_sym','.json']]
    paths += list((DEST/'ARDF_2M.pretty').glob('*'))+[DEST/'README.md',DEST/'sym-lib-table',DEST/'fp-lib-table']
    files={str(p.relative_to(ROOT)):sha(p)for p in sorted(set(paths))if p.is_file()and p.name not in ['file-manifest.json','SHA256SUMS']}
    write('file-manifest.json',dict(revision='M5A-R4',status='SCHEMATIC_REVIEW_PRE_LAYOUT_HOLD_NO_MANUFACTURING',files=files))
    files[str((OUT/'file-manifest.json').relative_to(ROOT))]=sha(OUT/'file-manifest.json')
    (OUT/'SHA256SUMS').write_text(''.join(h+'  '+p+'\n'for p,h in sorted(files.items())))
    print('Sealed',len(files),'R4 sources/artifacts;review only, no PCB')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');a=parser.parse_args()
    if a.check:
        for p,h in json.loads((OUT/'file-manifest.json').read_text())['files'].items():assert sha(ROOT/p)==h,p
        print(run('sha256sum','-c',str(OUT/'SHA256SUMS')).splitlines()[-1]);print('PASS R4 package hashes');return
    for command in [
      [sys.executable,'tools/m5a_r4_design.py'],
      ['kicad-cli','sch','export','netlist','--format','kicadxml','-o',str(OUT/'RF2M.net.xml'),str(DEST/'RF2M.kicad_sch')],
      ['kicad-cli','sch','erc','--format','json','-o',str(OUT/'erc.json'),str(DEST/'RF2M.kicad_sch')],
      ['kicad-cli','sch','export','pdf','--output',str(OUT/'RF2M.pdf'),str(DEST/'RF2M.kicad_sch')],
      [sys.executable,'tools/m5a_r4_verify.py'],[sys.executable,'tools/m5a_r4_models.py'],[sys.executable,'tools/m5a_r4_docs.py']]:print(run(*command))
    sources()
    (OUT/'README.md').write_text('''# M5A-R4 electrical review — pre-layout hold

One actual integrated-transmitter schematic; **no RF2M PCB/DRC/Gerbers** are claimed. No purchases, manufacture, assembly or RF operation.

Start with the [decision](../../../../docs/M5A_R4_REVIEW_DECISION.md), [modernization/interface](../../../../docs/M5A_R4_MODERNIZATION.md), [traced ST RF stage](../../../../docs/M5A_R4_RF_STAGE.md), [costs](../../../../docs/M5A_R4_COST_RECONCILIATION.md), [AM/power](../../../../docs/M5A_R4_AM_POWER.md) and [one-device acceptance](../../../../docs/M5A_R4_BUILD_AND_TEST.md).

[Editable schematic](../../RF2M.kicad_sch), [PDF](RF2M.pdf), [exported netlist](RF2M.net.xml), [itemized BOM](RF2M_BOM.csv), [population list](positions.csv), [pinout audit](pinout-audit.json). sources.json records obtained manufacturer PDFs, dates, hashes and failed original downloads; whole third-party PDFs/artwork are not redistributed.

verification.json is Boolean/connectivity/physical-landing assertion evidence only; analog/RF/thermal/endurance remain NOT_RUN. ERC footprint warnings and remaining missing landings are explicitly retained. The 50-ohm MMIC-to-ST-interstage adaptation and listed reservoir/coil/connector definitions block a credible integrated PCB release. DF782 and TI RNW candidate lands are manufacturer-derived and dimensionally checked; their thermal/stencil/assembly integration remains unqualified. No coupons or competing boards are proposed.

R3 is preserved at Git tag m5a-r3(daf994c); R1/R0 tags and R1 native archive remain unchanged. R4 checks verify the old R3 hashes IN THAT TAG. Historical root-relative R3 hashes naturally refer to old CAD, not current R4 files. RF80/M4A/accepted ADR files are hash-preserved.

Reproduce from repository root: `python3 tools/m5a_r4_review.py`; then `python3 tools/m5a_r4_review.py --check`. Review status is not manufacturing authorization.
''')
    write('tool-versions.json',dict(KiCad=run('kicad-cli','--version'),Python=run(sys.executable,'--version'),Git=run('git','rev-parse','HEAD'),PDF_export='KiCadCLI native multipagePDF;not screenshot-only schematic',SPICE='NOT_RUN;LPF is Python ABCD analysis,AM/thermal/energy are calculations',PCB_DRC='NOT_RUN_NO_PCB'))
    checks();seal()

if __name__=='__main__':main()

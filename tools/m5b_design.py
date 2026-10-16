#!/usr/bin/python3
"""Evolve R4 into the one M5B integrated schematic. No historical writes."""
import copy,hashlib,json,tempfile
from pathlib import Path
import m5a_r1_design as cad
import m5a_r4_design as r4
from m5b_footprints import write as footprints,width50

ROOT=Path(__file__).resolve().parents[1];HW=ROOT/'hardware/2m';OUT=HW/'review/M5B-E1'


def preserved():
    paths=[]
    for folder in ['hardware/80m','hardware/2m/archive','docs/decisions']:
        paths.extend((ROOT/folder).rglob('*'))
    for rev in ['M5A-R0','M5A-R1','M5A-R2','M5A-R3','M5A-R4']:
        paths.extend((HW/'review'/rev).rglob('*'))
    for pattern in ['M5_2M*','M5A_R*','M4A*']:
        paths.extend((ROOT/'docs').glob(pattern))
    paths.append(ROOT/'README.md')
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(set(paths))if p.is_file()and p.suffix not in ['.pyc','.kicad_prl']}


def build():
    OUT.mkdir(parents=True,exist_ok=True);snapshot=OUT/'preserved-baseline.json'
    if not snapshot.exists():snapshot.write_text(json.dumps(preserved(),indent=2)+'\n')
    assert preserved()==json.loads(snapshot.read_text())
    # Historical source generators execute only in a temporary directory.
    with tempfile.TemporaryDirectory(prefix='m5b-source-')as tmp:
        r4.DEST=Path(tmp);r4.OUT=Path(tmp)/'review/M5A-R4';r4.frozen=lambda:{}
        d=r4.build()
    cad.DEST=HW;cad.DATE='2026-10-16';d.revision='M5B-E1'
    allplacements=[(s,pl)for s in d.sheets for pl in s.placements]
    original=copy.deepcopy(d.parts)
    def change(ref,**kw):d.parts[ref].update(kw)
    change('J301',mpn='B2P-VH(LF)(SN)',value='Protected pack JST VH',footprint='Connector_JST:JST_VH_B2P-VH_1x02_P3.96mm_Vertical',supplier='JST authorized distributor',supplier_part_number='455-1639-ND',source_url='https://www.jst.com/wp-content/uploads/2025/06/eVH.pdf',price_breaks_eur={'1':.35},note='JST VH polarized locking2pin,3.96mm pitch.1PACK+2GND. VHR-2N housing/SVH contacts;strain-relief harness to board support. Different charger interface required. Hardware pack window precedes converter feed;never assume connector identifies cell count.')
    change('J101',mpn='61202021621',supplier='Wurth authorized distributor',supplier_part_number='710-61202021621',source_url='https://www.we-online.com/components/products/datasheet/61202021621.pdf',note='WR-BHD20pin2.54 pitch,33.06mm body9.1mm width8.75mm height;drawing002.00130Aug2026. Local version of IDC pattern has1.1mm drills and manufacturer body envelope.',footprint='ARDF_2M:WR_BHD_61202021621')
    change('J302',mpn='TSW-103-07-G-S',source_url='https://www.samtec.com/products/tsw',note='One3pin2.54mm row with SNT-100-BK-G shunt;factory variant selection only. Never populate both converters or change under power.')
    change('J701',mpn='66012102111404',value='TRAIN MMCX 50ohm',footprint='Connector_Coaxial:WR-MMCX_Wuerth_66012102111404_Vertical',source_url='https://www.we-online.com/components/products/datasheet/66012102111404.pdf',supplier='Wurth authorized distributor',supplier_part_number='710-66012102111404',price_breaks_eur={'1':3.68},note='Exact selected MMCX instead of unspecified MCX. Not compatible with SMA normal port. Wurth001.00013Mar2019 land pattern:1.47signal,2.59groundopening,4.21/4.22overall.5mmheight;strain-relieve pigtail.3.68EUR indexed MOQ1price;not a reserved quote.')
    change('C409',footprint='ARDF_2M:CP_Panasonic_OSCON_C10',supplier='DigiKey Germany',supplier_part_number='10-25SVPG150MCT-ND',price_breaks_eur={'1':1.47,'10':.95,'50':.7336},evidence='OBSERVED_2026_10_16_NET',availability='Indexed752stock;CTMOQ1. Reconfirm at order. Factory500not customer MOQ.',source_url='https://industrial.panasonic.com/cdbs/www-data/pdf/AAB8000/AAB8000COL10.pdf',note='Panasonic C10 land a2.1 b9.1 c1.6mm;150u25V+/-20,13mohm100kHz. Cold/life ESR and LDO response remain qualification gates.')
    for ref in ['L606','L635']:
        change(ref,footprint='ARDF_2M:Coilcraft_1812SMS_Doc184',supplier='Mouser Europe',supplier_part_number='994-1812SMS-33NJLC',price_breaks_eur={'1':1.64,'10':1.40,'25':1.29},evidence='OBSERVED_2026_10_16_NET',availability='Indexed2263stock,CTMOQ1. Reconfirm before procurement.',source_url='https://www.coilcraft.com/getmedia/c6fe1f83-b176-469d-a071-e2edb068fef2/midi.pdf',note='RetainedST33nH feed;M5B exactDoc184-2 staggered land/currentJLCsuffix.3A rise-current basis,Qmin100@150MHz,SRF2.5GHz. Current indexed pricing/stock in M5B BOM;RFbehavior NOT_RUN.')
    change('L634',value='47n',mpn='0603HC-47NXJRW',footprint='ARDF_2M:Coilcraft_0603HC_Doc218',price_breaks_eur={'1':.75},source_url='https://www.coilcraft.com/pdfs/0603hc.pdf',note='M5B50ohm initial match includes retainedL60633n bias-feed shunt:47n withC631/C63322p. Assumed3ohm series80pF intrinsic gate is a sensitivity model,NOT measured144MHzimpedance. Coilcraft0603HC47n Qmin40@250MHz,SRF1.53GHz,Irms.85A rise basis. Doc218landing unchanged. Small bounded same-board C/L alignment required.')
    change('L638',footprint='ARDF_2M:Coilcraft_A05T_Doc107',note='Actual Doc107-1 sizeA staggered lands,not generic axial pads. 18.5nH5turns,Q132@150MHz,SRF2.5GHz,4Arisebasis;3.94x4.45body,H3.15max. Reference output match unchanged.')
    change('L604',value='150n',mpn='1812SMS-R15JLC',footprint='ARDF_2M:Coilcraft_1812SMS_Doc184',price_breaks_eur={'1':1.40},note='M5B corrects actualMMIC DC bias loss:originalMurata180n maxDCR1.65ohm could drop0.30V at180mA. Selected documented Coilcraft150n maxDCR33mohm,SRF750MHz,Qmin100@150MHz,1.2A. Approx136ohm choke reactance at144.7MHz;small RF loading change requires end-to-end driver test.1.40EUR estimate;stock quote required.',source_url='https://www.coilcraft.com/en-us/products/rf/air-core-inductors/midi-spring/1812sms/1812sms-r15/')
    for ref in ['L641','L642','L643']:change(ref,footprint='ARDF_2M:Coilcraft_1008CS_Doc101',note=original[ref]['note']+' M5B actualDoc101-1 land H2.54 I1.02 J1.27mm;body2.92x2.79,H2.03+.152solder. Values unchanged;1A rise-current,not measured RF RMS margin.')
    # Resolve remaining actual purchased-part identities without inventing prices.
    change('R309',value='0.068',mpn='WSL2512R0680FEA',note='M5B confirmed current-protection correction:.068ohm1percent1W2terminal. Original.1ohm+divider required3.75V from3.3V INA180,so could never trip reliably. WithR8285.11k/R8294.02k actual threshold1.796A at amplifieroutput2.443V,below saturation. Kelvin trace takeoff at pad inner edges;measure dynamic fault response.')
    change('R828',value='5.11k',mpn='RT0603BRD075K11L',note='0.1percent current-sense divider upper resistor. With4.02k lower,.068ohmshunt,INA180A1gain20,Vref1.0758V:trip1.796A,required INAoutput2.443V. Original10k demanded3.752V and was ineffective.')
    change('R413',value='4.7',mpn='RC2512FK-074R7L',note='4.7ohm1W feed before two independent regulators. Precharge/current limiting includes both LDOs;old RC20us guarantee is no longer used.')
    change('R506',mpn='RC2512FK-0710RL',footprint='Resistor_SMD:R_2512_6332Metric',note='10ohm1W base-path resistor,selected2512 package;not an unqualified2010power rating.')
    for ref,p in list(d.parts.items()):
        if p['mpn'].startswith('OPEN: 0603 C0G50V'):
            code={'100p':'101','33p':'330','8.2p':'8R2'}[p['value']]
            change(ref,mpn='CC0603'+('C'if p['value']=='8.2p'else'J')+'RNPO9BN'+code,note=p['note']+' Selected Yageo C0G50V;exact stock/price still estimated.')
    change('C635',mpn='GRM188R71E105KA12D',note='Murata1u25V X7R0603 local supply bypass;effective capacitance qualification required.')
    change('TH801',value='10k NTC B3977',mpn='NTCLE100E3103JB0',footprint='ARDF_2M:NTC_Remote_2Wire',note='Vishay10k25C bead B25/853977K,not3950. Insulated wires to pass case;2.54mmwire termination,NOT axial-resistor body. Recalculate thermal trip for actual beta/tolerance;nominal66C shifts <1C. Sensor open/short window retained;detachment requires mounting inspection.')
    change('L301',source_url='https://www.bourns.com/docs/product-datasheets/srp1265a.pdf',mpn='SRP1265A-100M',footprint='ARDF_2M:Bourns_SRP1265A',price_breaks_eur={'1':1.30},note='Bourns SRP1265A10uH shielded family;manufacturer12.5mm square6.5mmheight land. Current/ripple qualification against selected actual curve;not generic SRR1260.')
    change('L302',source_url='https://www.bourns.com/docs/product-datasheets/srp1265a.pdf',mpn='SRP1265A-4R7M',footprint='ARDF_2M:Bourns_SRP1265A',price_breaks_eur={'1':1.30},note='Bourns SRP1265A4.7uH shielded,manufacturer landing;2S boost only. Isat/Irms/ripple must pass at6V minimum pack.')
    # Rated switch removes the TPS22919 5.5V recommended limit problem.
    d.lib.box('TPS22810_DBV',{'1':('VIN','power_in'),'2':('GND','power_in'),'3':('EN','input'),'4':('CT','passive'),'5':('QOD','passive'),'6':('VOUT','power_out')})
    change('U305',source_url='https://www.ti.com/lit/ds/symlink/tps22810.pdf',value='TPS22810DBVR',mpn='TPS22810DBVR',footprint='Package_TO_SOT_SMD:SOT-23-6',pins={'1':'VDRV_FILTER','2':'GND','3':'NORMAL_PERMIT','4':None,'5':'VDRV_RF','6':'VDRV_RF'},price_breaks_eur={'1':.55},note='TI DBV1VIN2GND3EN4CT5QOD6OUT.2.7-18V recommended,20Vabs. CTopen,quick discharge tied output. Replaces6Vabs TPS22919. Output is still5V;never directly feeds MMIC from rawpack.')
    change('U303',pins={'1':'GND','2':'VDRV_FILTER','3':'VDRV_PREREG'},note='Existing TLV76150 fixed5V is second independent regulation barrier after5.456V TLV767. Single failure of either regulator does not directly expose MMIC to9/16.8V. Normal voltage/dropout and startup remain measured gates.')
    change('R815',value='73.2k',mpn='RT0603BRD0773K2L',note='0.1percent driver OV divider;nominal5.269V with originalreference/divider. Threshold tolerance and actual startup tested before MMIC population.')
    # Initial source pad is bounded/calibratable; LVC clock gate normalizes
    # amplitude, so Si5351 drive-strength alone cannot set the MMIC input.
    for ref,val,mpn in [('R602','71.5','RC0603FR-0771R5L'),('R603','96.5','RC0603FR-0796R5L'),('R604','96.5','RC0603FR-0796R5L')]:
        change(ref,value=val,mpn=mpn,note='Initial10dB50ohm pi pad;after one integrated calibration6/8/10dB options allowed. Clock gate outputs full logic amplitude;do not assume Si drive strength controls RF amplitude. Required driver output19dBm remains target.')
    change('C602',pins={'1':'MMIC_RF_DC','2':'MMIC_COUPLED'},note='Existing1nF MMIC output DC block;R650 liftable link now isolates matching input for one-board50ohm driver test.')
    for ref in ['L604','C603','C604']:
        change(ref,pins={k:('VDRV_MMIC'if n=='VDRV_RF'else n)for k,n in d.parts[ref]['pins'].items()})
    change('C631',value='22p',mpn='GRM1885C1H220JA01D',note='M5B22p starting50ohm input match withL63447n/C63322p,includingL60633n gate-bias feed. BoundedDNP/22/33/47/56p tuning. Not a manufacturer-characterized144MHz device input.')
    change('C633',value='22p',mpn='GRM1885C1H220JA01D',note='M5B22p initial50ohm input match,withC63122p/L63447n andretained33nL606biasfeed. Nominal full-feed assumed-gate model is credible,not a measured match. BoundedDNP/22/27/33/39/47p tuning. SToutputmatching/ellipticLPF unchanged.')
    for ref,p in d.parts.items():
        if ref.startswith('TL'):
            length=float(p['value'].split()[1].removesuffix('mm'))
            p['footprint']='ARDF_2M:TL50_'+str(length).replace('.','p')+'mm'
            p['note']='M5B actual copper microstrip,0.8mm finished PCB/core0.64mm nominalDk4.3/Cu70um;W'+str(width50())+'mm;originalSTcenterline length '+str(length)+'mm. End pads1/2 are intentional net-tie ports. Pads/junctions add disclosed discontinuities;VNA qualification NOT_RUN.'
    # Rebuild original symbols from manifest and their actual prior unit positions.
    d.sheets=[];by={}
    for old,pl in allplacements:
        ref=pl['ref'];p=d.parts[ref];name=old.name
        if name not in by:
            by[name]=d.sheet(name,old.title);by[name].text('M5B-E1 / integrated evaluation PCB / NOT RELEASED / hardware tests NOT_RUN',18,26,1.1)
        typ='TPS22810_DBV'if ref=='U305'else pl['type'];u=pl['unit'];numbers={x[0]for x in d.lib.pins(typ,u)}
        by[name].place(ref,typ,p['value'],{n:p['pins'][n]for n in numbers},pl['x'],pl['y'],p['footprint'],p['mpn'],p['group'],p['population'],unit=u,note=p['note'],source=p['source_url'],price=p['price_breaks_eur'],evidence=p['evidence'],supplier=p['supplier'],code=p['supplier_part_number'],availability=p['availability'],moq=p['moq'])
    s=d.sheet('12_m5b_qualification','12 Independent driver regulator and integrated alignment links')
    s.text('Pre-regulation5.456V then existing5V LDO. Rated18V switch. No20us RC assumption is claimed as protection proof.\nFit driver link only after power-only qualification. RF link and optional50ohm load permit alignment on THIS board.',18,27,1.1)
    d.lib.box('TLV767_DRV',{'1':('OUT','power_out'),'2':('FB','input'),'3':('GND','power_in'),'4':('EN','input'),'5':('GND','power_in'),'6':('IN','power_in'),'7':('EP_GND','power_in')})
    def add(ref,typ,value,pins,fp,mpn,group='driver_supply',pop='NORMAL',cost=.04,note='',source=''):
        i=len(s.placements);s.place(ref,typ,value,pins,62+(i%5)*112,70+(i//5)*58,fp,mpn,group,pop,price={'1':cost},note=note,source=source)
    add('U950','TLV767_DRV','TLV76701DRVR',{'1':'VDRV_PREREG','2':'DRV_PRE_FB','3':'GND','4':'CONV_EN','5':'GND','6':'VDRV_LDO_IN','7':'GND'},'Package_SON:WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm','TLV76701DRVR',cost=.664,source='https://www.ti.com/lit/ds/symlink/tlv767.pdf',note='TI SLVSE84D DRV adjustable1OUT2FB3GND4EN5GND6IN7EP.0.8V(1+58.2/10)=5.456V.1percentaccuracy+.1percentdivider bounds about5.39-5.52V. Current stock conflicting regional caches;quote required.')
    for ref,val,a,b,mpn in [('R950','58.2k','VDRV_PREREG','DRV_PRE_FB','RT0603BRD0758K2L'),('R951','10k','DRV_PRE_FB','GND','RT0603BRD0710KL')]:
        add(ref,'R',val,{'1':a,'2':b},cad.FP_R,mpn,cost=.05)
    for ref,a in [('C950','VDRV_LDO_IN'),('C951','VDRV_PREREG')]:
        add(ref,'C','4.7u',{'1':a,'2':'GND'},'Capacitor_SMD:C_0805_2012Metric','GRM21BR71E475KA73L',cost=.15,note='4.7u25V X7R0805;effective capacitance must remain >=1u over actual bias/temp/tolerance for TLV767. Check vendor bias curves and power-only startup before fitting MMIC.')
    add('R952','R','0',{'1':'VDRV_RF','2':'VDRV_MMIC'},'Resistor_SMD:R_1206_3216Metric','RC1206JR-070RL',cost=.025,note='Physical power isolation link;omit until power/fault qualification with external dummy load. Same PCB,not a separate coupon.')
    add('R650','R','0',{'1':'MMIC_COUPLED','2':'MMIC_AC'},cad.FP_R,'RC0603JR-070RL','pa_match',cost=.02,note='Lift to measure PHA into optionalR65150ohm or injectRF into final matching from50ohm generator. Fit in normal operation;pad discontinuity included in RF qualification.')
    add('R651','R','49.9',{'1':'MMIC_COUPLED','2':'GND'},'Resistor_SMD:R_1206_3216Metric','RC1206FR-0749R9L','evaluation','DNP',cost=.025,note='Optional50ohm driver-only test load;never populate withR650/finalRFdrive. At19dBm80mW within.25W rating.')
    # Existing24compact pads remain; only two additional supply contacts.
    add('TP950','TestPoint','DRV pre5.456V',{'1':'VDRV_PREREG'},'TestPoint:TestPoint_Pad_D1.0mm','PCB feature','test',cost=0)
    add('TP951','TestPoint','MMIC isolated5V',{'1':'VDRV_MMIC'},'TestPoint:TestPoint_Pad_D1.0mm','PCB feature','test',cost=0)
    for ref in ['TP601','TP602','TP603','TP604']:d.parts[ref]['footprint']='ARDF_2M:Probe_Pad_0p6'
    for ref,net,pop in [('C960','BOOST2S','BOOST2S'),('C961','BUCK4S','BUCK4S')]:
        add(ref,'C','22u',{'1':'VIN_CONV','2':'GND'},'Capacitor_SMD:C_1210_3225Metric','GRM32ER71V226KE15L','power',pop,cost=.30,note='Added local converter INPUT reservoir22u35V. Shared pre-isolation capacitor is too remote to close the switching input loop;effective capacitance/current measured during supply commissioning.')
    from m5a_r4_readable import reflow
    reflow(d)
    # These selected manufacturer landings were individually reviewed; extend
    # the generic symbol filters to describe them, retaining the generic choices.
    for typ,addition in [('Conn_02x10_Odd_Even','ARDF_2M:WR_BHD_61202021621'),('L','ARDF_2M:Bourns_SRP1265A'),('Thermistor_NTC','ARDF_2M:NTC_Remote_2Wire'),('TestPoint','ARDF_2M:Probe_Pad_0p6')]:
        prop=next(p for p in cad.children(d.lib.defs[typ],'property')if p[1]=='ki_fp_filters');prop[2]+=' '+addition
    d.save()
    for sheet in HW.glob('*.kicad_sch'):
        if sheet.name=='RF2M.kicad_sch':continue
        sx=cad.parse(sheet.read_text())
        for item in cad.children(sx,'symbol'):
            ref=next(p[2]for p in cad.children(item,'property')if p[1]=='Reference')
            if ref.startswith('TL'):cad.child(item,'in_bom')[1]=cad.Atom('no')
        sheet.write_text(cad.dump(sx)+'\n')
    # Fix the inherited index layout/text; electrical UUIDs remain stable.
    root=cad.parse((HW/'RF2M.kicad_sch').read_text())
    for i,sh in enumerate(cad.children(root,'sheet')):
        at=cad.child(sh,'at');oldy=float(at[2]);newy=65+(i//3)*45;at[2]=cad.Atom(str(newy))
        for prop in cad.children(sh,'property'):
            a=cad.child(prop,'at');a[2]=cad.Atom(str(float(a[2])+newy-oldy))
    for t in cad.children(root,'text'):
        t[1]='M5B-E1 / ONE INTEGRATED 144MHz TRUE-AM EVALUATION PCB / NOT RELEASED\nPHA-1+ and PD54008L-E retained; documented ST output match and elliptic LPF.\n2S9Vboost OR4S9V/7.5Vbuck exclusive populations. Separate3.3Vtraining.\nDriver: independent5.456V/5V regulation and18V-rated switch. Power-only qualification beforeR952/MMIC.\nInput match has bounded same-board tuning;RF gain/AM/thermal/endurance tests NOT_RUN.\nReview-only PCB/Gerbers. No ordering,fabrication,assembly or RF operation authorized.'
    (HW/'RF2M.kicad_sch').write_text(cad.dump(root)+'\n')
    (HW/'RF2M.electrical.json').write_text(json.dumps({'date':cad.DATE,'revision':'M5B-E1','status':'INTEGRATED EVALUATION / ALL HARDWARE TESTS NOT_RUN','parts':list(d.parts.values()),'placements':{s.name:s.placements for s in d.sheets}},indent=2)+'\n')
    footprints(HW/'ARDF_2M.pretty')
    # Match the name used by the manifest to the explicit Panasonic C10 landing.
    src=HW/'ARDF_2M.pretty/Panasonic_OSCON_C10.kicad_mod';dst=HW/'ARDF_2M.pretty/CP_Panasonic_OSCON_C10.kicad_mod'
    dst.write_text(src.read_text().replace('"Panasonic_OSCON_C10"','"CP_Panasonic_OSCON_C10"'));src.unlink()
    delta=[]
    for ref in sorted(original.keys()|d.parts.keys()):
        old=original.get(ref);new=d.parts.get(ref)
        if old!=new:delta.append(dict(ref=ref,old=old,new=new))
    (OUT/'schematic-delta.json').write_text(json.dumps(delta,indent=2)+'\n')
    assert preserved()==json.loads(snapshot.read_text())
    print('M5B schematic generated:',len(d.parts),'positions,',len(d.sheets),'sheets; prior revisions preserved')
    return d


if __name__=='__main__':build()

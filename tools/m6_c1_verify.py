#!/usr/bin/python3
"""Independent connector/package/native-pad assertions and meaningful mutations."""
import sys,json,copy,itertools,hashlib,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-C1'
from m6_c1_contracts import GPIO,STATIC
def nets(b):return {f.GetReference():{a.GetNumber():a.GetNetname() for a in f.Pads() if a.GetNumber()} for f in b.GetFootprints()}
def verify(b):
    n=nets(b);errors=[]
    contracts=json.loads((D/'RF-interface-contracts.json').read_text())
    for band,ref in [('RF80','J4'),('RF2M','J5')]:
        for row in contracts[band]['pins']:
            if n[ref].get(str(row['pin']))!=row['controller_net']:errors.append('connector:'+ref+':'+str(row['pin']))
    critical={'U1':{'1':'V3V3','2':'VIN_SYS','3':'VIN_SYS','4':'GND','5':'BUCK_SW','6':'BUCK_BST'},
    'U2':{'1':'USB_VBUS','2':'GND','3':'USB_VBUS','4':'USB_OC_N','5':'USB_ILIM','6':'USB_LIMIT'},
    'U3':{'1':'USB_DP_CONN','2':'GND','3':'USB_DM_CONN','4':'USB_DM_CONN','5':'V3V3','6':'USB_DP_CONN'},'F1':{'1':'PACK_RAW','2':'PACK_FUSED'},'U4':{'1':'GND','2':'MCU_EN','3':'V3V3'},'D1':{'1':'PACK_PROT','2':'PACK_FUSED'},'D4':{'1':'VIN_SYS','2':'PACK_PROT'},'D2':{'1':'PACK_PROT','2':'GND'},
    'D3':{'1':'VIN_SYS','2':'USB_LIMIT'},'D21':{'1':'USB_LIMIT','2':'GND'},'Q2':{'1':'USB_BASE','2':'GND','3':'USB_VBUS_N'},'D20':{'1':'CELL_POS','3':'BACKUP_D'},'Q1':{'1':'BATT_BASE','2':'GND','3':'PACK_ABSENT'},
    'U20':{'1':'RTC_BACKUP','2':'RTC80_SDA','4':'GND','5':'GND','6':'V3V3','8':'RTC80_SCL'},
    'U21':{'1':'V3V3','2':'BAT_DIV','3':'BAT_ADC','4':'V3V3','5':'PACK_ID_RAW','6':'PACK_ID_ADC','7':'GND','8':'MODULE_ID_ADC','9':'RF2M_MODULE_ID','10':'V3V3','11':'PA_RAIL_ADC','12':'RF2M_PA_RAIL_ADC','13':'V3V3','14':'V3V3'},
    'U33':{'1':'INIT_OK','2':'MCU_EN','3':'GND','4':'SAFE_OE_N','5':'V3V3','6':'PACK_PRESENT'},
    'U35':{'1':'SAFE','2':'BAND80','3':'OE80_N','4':'SAFE','5':'BAND2','6':'OE2M_N','7':'GND','14':'V3V3'},
    'U37':{'1':'BUS80','2':'DISARMED','3':'BUS80_EN','4':'BUS2M','5':'DISARMED','6':'BUS2M_EN','7':'GND','14':'V3V3'},
    'U40':{'1':'V3V3','2':'GND','3':'POWER80','5':'V3V3_RF80','6':'V3V3_RF80'},
    'U50':{'1':'V3V3','2':'GND','3':'POWER2M','5':'V3V3_RF2M','6':'V3V3_RF2M'},
    'U43':{'1':'V3V3','2':'RTC80_SCL','3':'RTC80_SDA','4':'GND','5':'BUS80_EN','6':'RF80_SDA','7':'RF80_SCL','8':'V3V3_RF80'},
    'U53':{'1':'V3V3','2':'RF2M_SCL','3':'RF2M_SDA','4':'GND','5':'BUS2M_EN','6':'RF2M_I2C_SDA','7':'RF2M_I2C_SCL','8':'V3V3_RF2M'},
    'U60':{'1':'RF80_FAULT_N','2':'RF2M_FAULT','3':'GND','4':'RF2M_FAULT_N','5':'RF80_FAULT','6':'V3V3'},'J7':{'1':'LORA_ANT','2':'GND'}}
    critical.update({
      'U30':{'15':'PA_REQ','1':'FOX_REQ','2':'PWR0','3':'PWR1','4':'PACK4_SOFT','5':'PATH_TRAIN','6':'PROFILE_FULL','7':'PREPARE','8':'GND','9':'SHIFT_CHAIN','10':'MCU_EN','11':'SPI_SCK','12':'SHIFT_LATCH','13':'SAFE_OE_N','14':'SPI_MOSI','16':'V3V3'},
      'U31':{'15':'PA_PREPARE','1':'POWER80','2':'POWER2M','3':'BUS80','4':'BUS2M','5':'LED_ARM','6':'LED_FAULT','7':'BAND2','8':'GND','10':'MCU_EN','11':'SPI_SCK','12':'SHIFT_LATCH','13':'SAFE_OE_N','14':'SHIFT_CHAIN','16':'V3V3'},
      'U32':{'2':'PACK_ABSENT','3':'GND','4':'PACK_PRESENT','5':'V3V3'},
      'U34':{'1':'SAFE_OE_N','2':'BAND80','3':'GND','4':'BAND2','5':'SAFE','6':'V3V3'},
      'U36':{'2':'ARM','3':'GND','4':'DISARMED','5':'V3V3'},
      'J1':{'1':'PACK_RAW','2':'GND','3':'PACK_ID_RAW'},'J3':{'1':'GND','2':'UART_TX','3':'UART_RX'},
      'BT1':{'1':'CELL_POS','2':'GND'},
      'U70':{'1':'GND','2':'GND','3':'GND','4':'GND','5':'LORA_DIO1','10':'LORA_BUSY','11':'GND','12':'GND','13':'V3V3','14':'SPI_SCK','15':'SPI_MISO','16':'SPI_MOSI','17':'LORA_NSS','18':'LORA_RESET','19':'GND','20':'GND','21':'LORA_ANT','22':'GND'}
    })
    for base,band in [(40,'RF80'),(50,'RF2M')]:
        controls=[('ARM','ARM'),('CW_KEY','KEY'),('LEASE','PROGRESS'),('MUTE_N','MUTE_RELEASE'),('PA_REQ','PA_REQ'),('FOX_REQ','FOX_REQ'),('PWR0','PWR0'),('PWR1','PWR1'),('PACK4_OK','PACK4_SOFT')] if band=='RF80' else [('ARM','ARM'),('SLOT','SLOT'),('KEY','KEY'),('PROGRESS','PROGRESS'),('MUTE_N','MUTE_RELEASE'),('PATH_TRAIN','PATH_TRAIN'),('PROFILE_FULL','PROFILE_FULL'),('AF_PWM','AF_PWM'),('LEVEL_PWM','LEVEL_PWM'),('PREPARE','PREPARE'),('PA_PREPARE','PA_PREPARE')]
        oe='OE80_N' if band=='RF80' else 'OE2M_N';rail='V3V3_'+band
        mp={'1':oe,'10':'GND','19':oe,'20':rail}
        for (sig,host),(ip,op) in zip(controls,[(2,18),(4,16),(6,14),(8,12),(11,9),(13,7),(15,5),(17,3)]):mp[str(ip)]=host;mp[str(op)]=band+'_'+sig+'_BUF'
        critical['U'+str(base+1)]=mp
        mp={'7':'GND','14':rail}
        for i,(en,ip,op) in enumerate([(1,2,3),(4,5,6),(10,9,8),(13,12,11)]):
            if i<len(controls)-8:
                sig,host=controls[i+8];mp[str(en)]=oe;mp[str(ip)]=host;mp[str(op)]=band+'_'+sig+'_BUF'
            else:mp[str(en)]=rail;mp[str(ip)]='GND'
        critical['U'+str(base+2)]=mp
    for ref in ['U40','U50']:
        fp=next(f for f in b.GetFootprints() if f.GetReference()==ref)
        if fp.GetValue()!='TPS22918DBVR':errors.append('switch_hot_rating:'+ref)
        if fp.GetFPIDAsString()!='ARDF_CTL:SOT-23-6_CTL':errors.append('switch_DBV_package:'+ref)
        for pad in fp.Pads():
            if abs(p.ToMM(pad.GetSize().x)-1.325)>.001 or abs(p.ToMM(pad.GetSize().y)-.6)>.001:errors.append('switch_DBV_land:'+ref)
    for ref,pins in critical.items():
        for pin,net in pins.items():
            if n[ref].get(pin)!=net:errors.append('physical:'+ref+':'+pin)
    esp={1:'GND',2:'V3V3',3:'MCU_EN',4:'MODULE_ID_ADC',5:'PA_RAIL_ADC',6:'AF_PWM',7:'LEVEL_PWM',8:'LORA_BUSY',9:'LORA_DIO1',10:'RF2M_SDA',11:'RF2M_SCL',12:'RTC80_SDA',13:'USB_DM',14:'USB_DP',17:'RTC80_SCL',18:'LORA_NSS',19:'SPI_MOSI',20:'SPI_SCK',21:'SPI_MISO',22:'INIT_OK',23:'RF2M_FAULT',24:'KEY',25:'SLOT',27:'BOOT',28:'RF80_FAULT',29:'START_N',30:'USB_VBUS_N',31:'SHIFT_LATCH',32:'PROGRESS',33:'LORA_RESET',34:'ARM',35:'MUTE_RELEASE',36:'UART_RX',37:'UART_TX',38:'PACK_ID_ADC',39:'BAT_ADC',40:'GND',41:'GND'}
    for pin,net in esp.items():
        if n['U10'].get(str(pin))!=net:errors.append('ESP32:'+str(pin))
    for pin in ['15','16','26']:
        if not n['U10'][pin].startswith('unconnected-'):errors.append('strap:'+pin)
    f={f.GetReference():f for f in b.GetFootprints()}
    if f['U10'].GetValue()!='ESP32-S3-WROOM-1-N4':errors.append('non_PSRAM_module')
    # Verify every physical pad, including repeated ground/shield contacts.
    xml=ET.parse(D/'CTRL.net.xml');expected={}
    for net in xml.findall('./nets/net'):
        for node in net.findall('node'):expected[(node.get('ref'),node.get('pin'))]=net.get('name')
    count=0
    for ref,fp in f.items():
        if ref.startswith('H'):continue
        for pad in fp.Pads():
            num=pad.GetNumber()
            if not num:continue
            count+=1
            if expected.get((ref,num))!=pad.GetNetname():errors.append('all_pad:'+ref+'.'+num)
    # Native values/MPNs/land identifiers must agree with the exported capture,
    # independently of pad-net agreement. A correct net alone cannot prove ratings.
    for comp in xml.findall('./components/comp'):
        ref=comp.get('ref')
        if ref not in f:continue
        fp=f[ref]
        if fp.GetValue()!=comp.findtext('value'):errors.append('value:'+ref)
        if fp.GetFPIDAsString()!=comp.findtext('footprint'):errors.append('landing:'+ref)
        native={z.GetName():z.GetText() for z in fp.GetFields()}
        for field in comp.findall('./fields/field'):
            if field.get('name') in ('MPN','Population') and native.get(field.get('name'))!=(field.text or ''):errors.append('metadata:'+ref+':'+field.get('name'))
    # Output reset pulls and buffer OE must be actual circuit paths.
    manifest=json.loads((P/'CTRL.electrical.json').read_text());parts={x['ref']:x for x in manifest['parts']}
    for net in ['INIT_OK','ARM','MUTE_RELEASE','PROGRESS','KEY','SLOT','AF_PWM','LEVEL_PWM']:
        if not any(x['ref'].startswith('R') and f[x['ref']].GetValue()=='10k' and set(n[x['ref']].values())=={net,'GND'} for x in parts.values()):errors.append('reset_pull:'+net)
    for ref in ['U41','U42','U43','U40','J4']:
        if parts[ref]['population']!='RF80' or next((x.GetText() for x in f[ref].GetFields() if x.GetName()=='Population'),'')!='RF80':errors.append('DNP:'+ref)
    for ref in ['U51','U52','U53','U50','J5']:
        if parts[ref]['population']!='RF2M' or next((x.GetText() for x in f[ref].GetFields() if x.GetName()=='Population'),'')!='RF2M':errors.append('DNP:'+ref)
    if f['R1'].GetValue()!='470k' or f['R2'].GetValue()!='47k':errors.append('battery_divider_rating')
    return errors,count,len(critical)
def main():
    b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));errors,pads,critical=verify(b);assert not errors,errors
    tests=[];fps={f.GetReference():f for f in b.GetFootprints()}
    def mutate(name,ref,pin,new):
        pad=next(a for a in fps[ref].Pads() if a.GetNumber()==str(pin));old=pad.GetNet();pad.SetNet(b.FindNet(new));e,_,_=verify(b);pad.SetNet(old);assert e,name;tests.append({'mutation':name,'detected_checks':e})
    for name,r,pin,net in [('reversed_IDC16','J4',1,'GND'),('reversed_IDC20','J5',1,'GND'),('swapped_RF80_I2C','J4',3,'RF80_SDA'),('swapped_RF2M_I2C','J5',3,'RF2M_I2C_SCL'),('mute_polarity_short','J4',13,'V3V3_RF80'),('strap_to_ARM','U10',15,'ARM'),('ARM_on_reset','U33',1,'V3V3'),('missing_ground','J5',18,'RF2M_ARM'),('source_unisolated','U43',6,'RTC80_SDA'),('status_lines_shorted','U60',4,'RF80_FAULT_N'),('analog_backfeed','U21',12,'PA_RAIL_ADC'),('PREPARE_confused','J5',20,'RF2M_PREPARE'),('power_GPIO_short','U50',3,'V3V3'),('coin_cell_charge_path','D20',1,'V3V3'),('USB_ESD_backfeed','U3',5,'USB_VBUS')]:mutate(name,r,pin,net)
    # Evaluate the gates using actual native pad-net identities, independently
    # of the capture generator. Every output must match the intended truth table.
    n=nets(b);count=0
    for bits in itertools.product([0,1],repeat=12):
        init,en,pack,band,arm,mute,key,slot,progress,pre,p80,p2=bits
        v={'GND':0,'V3V3':1,'INIT_OK':init,'MCU_EN':en,'PACK_ABSENT':not pack,'BAND2':band,'ARM':arm,'MUTE_RELEASE':mute,'KEY':key,'SLOT':slot,'PROGRESS':progress,'PREPARE':pre,'POWER80':p80,'POWER2M':p2,'BUS80':1,'BUS2M':1}
        def gate(ref,inputs,out,kind):
            args=[bool(v[n[ref][str(i)]]) for i in inputs];v[n[ref][str(out)]]=not args[0] if kind=='inv' else (not all(args) if kind=='nand' else all(args))
        for op in [('U32',[2],4,'inv'),('U33',[1,2,6],4,'nand'),('U34',[1],5,'inv'),('U34',[4],2,'inv'),('U35',[1,2],3,'nand'),('U35',[4,5],6,'nand'),('U36',[2],4,'inv'),('U37',[1,2],3,'and'),('U37',[4,5],6,'and')]:gate(*op)
        expected_safe=bool(init and en and pack)
        assert v['SAFE']==expected_safe
        assert (not v['OE80_N'])==bool(expected_safe and not band)
        assert (not v['OE2M_N'])==bool(expected_safe and band)
        assert not(not v['OE80_N'] and not v['OE2M_N'])
        assert v['BUS80_EN']==(not arm) and v['BUS2M_EN']==(not arm)
        for ref,power,oe in [('U41',p80,'OE80_N'),('U51',p2,'OE2M_N')]:
            # First physical244 channel carries ARM in both banks.
            output=bool(power and not v[n[ref]['1']] and v[n[ref]['2']])
            assert output==bool(power and expected_safe and (not band if ref=='U41' else band) and arm)
        count+=1
    # Population mutations alter actual native assembly fields.
    for ref in ['U41','U51']:
        fld=next(x for x in fps[ref].GetFields() if x.GetName()=='Population');old=fld.GetText();fld.SetText('ALL');e,_,_=verify(b);fld.SetText(old);assert 'DNP:'+ref in e;tests.append({'mutation':'wrong_population_'+ref,'detected_checks':e})
    for ref,new in [('R1','100k'),('U10','ESP32-S3-WROOM-1-N4R8'),('U40','TPS22919DCKR')]:
        old=fps[ref].GetValue();fps[ref].SetValue(new);e,_,_=verify(b);fps[ref].SetValue(old);assert e;tests.append({'mutation':'wrong_value_'+ref,'detected_checks':e})
    from m6_c1_analysis import fitted_part
    manifest=json.loads((P/'CTRL.electrical.json').read_text());parts={z['ref']:z for z in manifest['parts']}
    for ref in ['U42','R108','R109','R112','R113','R114','R115','R116','R117']:
        assert not fitted_part(parts[ref],'FOX_MIN'),ref
    for ref in ['U41','U43','U40','J4','R110','R111']:
        assert fitted_part(parts[ref],'FOX_MIN'),ref
    # Verify source RF trees remain exactly unchanged, including user's M4A work.
    preserved=json.loads((D/'frozen-RF-files.json').read_text()) if (D/'frozen-RF-files.json').exists() else None
    if preserved:
        for path,sha in preserved.items():
            f=Path(path);f=f if f.is_absolute() else ROOT/f
            assert hashlib.sha256(f.read_bytes()).hexdigest()==sha,str(f)
    report={'status':'PASS','native_pad_instances':pads,'independent_critical_package_maps':critical+1,'connector_contract_pins':36,'hardware_enable_combinations':count,'native_mutations':tests,'RF_baseline_files_unchanged':len(preserved) if preserved else 'NOT_CHECKED','physical_tests':'NOT_RUN'}
    (D/'electrical-regression.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k!='native_mutations'})
    # Actual GPIO and shift bit header for later firmware, no hardware is accessed.
    h='/* M6-C1 pin contract; physical validation NOT_RUN. No operating firmware. */\n#pragma once\n'
    for gpio,net in GPIO.items():
        if net!='STRAP_RESERVED':h+='#define CTL_'+net+' '+str(gpio)+'\n'
    for bit,net in enumerate(STATIC):h+='#define CTL_SHIFT_'+net+' '+str(bit)+'\n'
    (ROOT/'firmware/controller_hw/pins.h').write_text(h)
if __name__=='__main__':main()

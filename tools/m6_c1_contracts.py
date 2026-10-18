#!/usr/bin/python3
"""Extract the two frozen RF interfaces before controller capture/placement."""
import json, hashlib, subprocess, tempfile, csv, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'hardware/controller/review/M6-C1'
GPIO={0:'BOOT',1:'BAT_ADC',2:'PACK_ID_ADC',3:'STRAP_RESERVED',4:'MODULE_ID_ADC',5:'PA_RAIL_ADC',6:'AF_PWM',7:'LEVEL_PWM',8:'RTC80_SDA',9:'RTC80_SCL',10:'LORA_NSS',11:'SPI_MOSI',12:'SPI_SCK',13:'SPI_MISO',14:'INIT_OK',15:'LORA_BUSY',16:'LORA_DIO1',17:'RF2M_SDA',18:'RF2M_SCL',19:'USB_DM',20:'USB_DP',21:'RF2M_FAULT',35:'RF80_FAULT',36:'START_N',37:'USB_VBUS_N',38:'SHIFT_LATCH',39:'PROGRESS',40:'LORA_RESET',41:'ARM',42:'MUTE_RELEASE',43:'UART_TX',44:'UART_RX',45:'STRAP_RESERVED',46:'STRAP_RESERVED',47:'KEY',48:'SLOT'}
STATIC=['PA_REQ','FOX_REQ','PWR0','PWR1','PACK4_SOFT','PATH_TRAIN','PROFILE_FULL','PREPARE','PA_PREPARE','POWER80','POWER2M','BUS80','BUS2M','LED_ARM','LED_FAULT','BAND2']
def detail(row,band):
    n=row['module_net'];k=row['classification'];row['nominal_operating_V']='3.135..3.465 supply; referenced3.3V logic' if n!='GND' else '0V reference'
    row['absolute_V']='-0.3..3.6 at module logic supply/interface; never use5V signaling'
    row['fault_behavior']='withdraw ARM/mute release; deliberate revalidation/rearm required'
    row['maximum_current_contract']='controller allocated0.4mA DC per control, not IC absolute output rating'
    if n=='GND':
        row.update(absolute_V='GND reference; ground offset qualification required',input_current='shared signal/reference return; separate J301 harness carries intended PA return',maximum_current_contract='IDC conductor/contact and ground-offset limit; no intentional PA current',active_polarity='not applicable',module_may_drive_host_absent='passive common ground')
    elif n=='V3V3':
        row.update(input_current='150mA maximum design allocation per port; measure actual module',maximum_current_contract='150mA normal interface budget, sequential inrush qualification',active_polarity='switched rail high=logic powered; not permission to transmit')
    elif k=='open-drain I2C':
        row.update(input_current='module4.7k pull-up plus host-domain4.7k; sink target<3mA, account repeater offsets',maximum_current_contract='3mA design sink budget; verify actual VOL/rise time at100kHz',active_polarity='open drain, idleHIGH',fault_behavior='disable branch over SPI and disarm; RTC remains reachable after RF80 branch isolation')
    elif n=='FAULT_N':
        row.update(input_current='RF80 approximately1.5mA sink with2.2k/10k external network' if band=='RF80' else 'RF2M push-pull through local1k into10k host pull-down,~0.3mA HIGH',maximum_current_contract='2mA RF80 sink allocation; RF2M~0.3mA HIGH',fault_behavior='LOW expected while unarmed; LOW after arm is a fault. HIGH before arm is rejected. Never use alone for presence')
    elif k=='analog':
        row.update(input_current='ID33k pull-up current<=0.1mA; PA rail divider measurement high impedance',maximum_current_contract='ID<=0.1mA; ADC conditioned through powered-off TMUX with upstream100n filter',absolute_V='0..3.6V normal controller ADC path; TMUX1511 powered-off input limit5.5V; RF2M PA sense bounded by native120k/10k divider',active_polarity='analog voltage/resistor identity',fault_behavior='unknown/short/open/outdated/contradictory reading disarms; ADC calibration required')
    else:
        row['input_current']='100ohm series,10k host pull-down plus native'+('47k' if band=='RF80' else '100k')+' input pull-down; nominal HIGH draw~0.4mA'
        row['active_polarity']={'LEASE':'rising-edge software-progress lease','PROGRESS':'falling-edge software-progress heartbeat','ARM':'deliberate rising edge; LOW disarmed','CW_KEY':'HIGH keyed RF within local enable','KEY':'HIGH identification tone/key within slot','SLOT':'HIGH scheduled RF slot; independent of KEY','PA_REQ':'HIGH normal PA request; mutually exclusive FOX_REQ','FOX_REQ':'HIGH Foxoring request; mutually exclusive PA_REQ','PACK4_OK':'HIGH only validated4S full RF80 assembly; never constant HIGH','PATH_TRAIN':'HIGH training / LOW normal path','PROFILE_FULL':'HIGH full profile only normal path; training requiresLOW','PREPARE':'HIGH source preparation with MUTE_NHIGH and localSAFE_N','PA_PREPARE':'HIGH watt-converter precharge, distinct from PREPARE','AF_PWM':'3.3V312.5kHz8bit sine-reference PWM; safeLOW','LEVEL_PWM':'3.3V312.5kHz8bit carrier-level PWM; safeLOW','MUTE_N':'LOW inhibit / HIGH release after validation','PWR0':'first power bit; PWR0/PWR1=00Sprint,10extended,01full,11invalid','PWR1':'second power bit; PWR0/PWR1=00Sprint,10extended,01full,11invalid'}.get(n,row['active_polarity'])
    return row

def extract():
    OUT.mkdir(parents=True,exist_ok=True); result={}
    for band,path in [('RF80','hardware/80m/production/RF80_V1.electrical.json'),('RF2M','hardware/2m/RF2M.electrical.json')]:
        p=ROOT/path; data=json.loads(p.read_text()); j=next(x for x in data['parts'] if x['ref']=='J101')
        rows=[]
        for pin,net in j['pins'].items():
            direction='controller_to_module'; kind='digital'; default='LOW / inactive'; pull='10k controller pull-down plus module pull-down'
            if net=='GND':direction='return';kind='power';default='ground';pull='none'
            elif net=='V3V3':direction='controller_to_module';kind='power';default='OFF';pull='load switch; 150mA module budget'
            elif net in ('SCL','SDA','I2C_SDA','I2C_SCL'):direction='bidirectional';kind='open-drain I2C';default='isolated';pull='4.7k on each powered bus domain'
            elif net=='FAULT_N':direction='module_to_controller';kind='open-drain' if band=='RF80' else 'push-pull through local 1k';default='LOW when disarmed; not presence detection';pull='2.2k to module V3V3 plus10k host-side pull-down (low when absent)' if band=='RF80' else '10k controller pull-down, fitted in all variants'
            elif net in ('MODULE_ID','PA_RAIL_ADC'):direction='module_to_controller';kind='analog';default='isolated on controller power loss';pull='33k to host 3.3V for ID; PA rail native 120k/10k divider'
            elif net=='MUTE_N':default='LOW = inhibit';pull='10k controller plus local pull-down'
            rows.append(dict(pin=int(pin),module_net=net,controller_net=('V3V3_'+band if net=='V3V3' else 'GND' if net=='GND' else band+'_'+net),direction=direction,classification=kind,nominal_V=0 if net=='GND' else (('1.173/1.792/2.353' if net=='MODULE_ID' else '0.694 nominal rail;1.292 at16.8V') if kind=='analog' else 3.3),absolute_V='0..3.6 at logic connector; analog bounds in electrical review',pull=pull,reset_default=default,input_current='CMOS leakage; 100ohm series / 10k pull-down load about 0.33mA',unpowered='Ioff buffers, disabled powered-domain I2C repeaters; TMUX1511 analog powered-off protection',active_polarity='LOW inhibit' if net=='MUTE_N' else 'HIGH accepted only after deliberate ARM' if net=='FAULT_N' else 'rising ARM edge' if net=='ARM' else 'module-specific, see binding protocol',DC_load_mA=150 if net=='V3V3' else (0.4 if direction=='controller_to_module' and kind=='digital' else 'see pull/divider circuit'),module_may_drive_host_absent='PA rail sense may be present from independent pack; TMUX power-off protection' if net=='PA_RAIL_ADC' else 'passive ID only' if net=='MODULE_ID' else 'status/I2C isolated with either logic rail absent' if direction in ('module_to_controller','bidirectional') else 'no; controller-owned output',timing_contract='RF80 rising LEASE<=100ms, ARM-low20ms/quiet20ms, post-ARM250ms' if band=='RF80' else 'RF2M falling PROGRESS<=100ms, startup250ms/quiet10ms/post-ARM50ms; PREPARE source, PA_PREPARE converter',runtime='module-specific state machine; no hot plug while armed'))
        result[band]=dict(source=path,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),connector=j['mpn'],footprint=j['footprint'],pins=[detail(row,band) for row in rows])
    result['binding_corrections']=['RF80 power bits explicitly PWR0/PWR1: 00 Sprint, 10 extended, 01 full, 11 invalid. Older audit bit-order wording is ambiguous; native decode is authoritative.','RF2M MODULE_ID resistors 18.2k BOOST2S / 39.2k BUCK4S / 82k TRAIN_ONLY replace obsolete R0 10k/22k/47k contract.','RF2M FAULT_N is push-pull VALID_ARM, high after accepted arm; RF80 FAULT_N open-drain, low when unarmed.','RF80 I2C branch must be disconnected while armed, including RTC accesses.','RF2M native SRC_ON = PREPARE & SAFE_N & MUTE_N; CONV_EN = SRC_ON & PA_PREPARE. Source programming therefore requires released MUTE_N while ARM/SLOT/KEY remain low. PA_PREPARE is a distinct converter-precharge permission.']
    result['native_export_verification']=[]
    with tempfile.TemporaryDirectory(prefix='m6-contract-') as tmp:
        for band,sch in [('RF80','hardware/80m/production/RF80_V1.kicad_sch'),('RF2M','hardware/2m/RF2M.kicad_sch')]:
            out=Path(tmp)/(band+'.xml');subprocess.run(['kicad-cli','sch','export','netlist','--format','kicadxml','-o',str(out),str(ROOT/sch)],capture_output=True,check=True)
            frozen=OUT/'inputs';frozen.mkdir(exist_ok=True);(frozen/(band+'-interface.xml')).write_bytes(out.read_bytes())
            tree=ET.parse(out);pins={}
            for n in tree.findall('./nets/net'):
                for node in n.findall('node'):
                    if node.get('ref') in ('J101','J301'):pins.setdefault(node.get('ref'),{})[node.get('pin')]=n.get('name')
            expected={str(r['pin']):r['module_net'] for r in result[band]['pins']}
            assert pins['J101']==expected,(band,pins)
            result['native_export_verification'].append({'band':band,'source':sch,'schematic_sha256':hashlib.sha256((ROOT/sch).read_bytes()).hexdigest(),'connector_pins':pins,'native_XML_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'status':'MATCH'})
    (OUT/'RF-interface-contracts.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'GPIO-allocation.json').write_text(json.dumps({'mcu':'ESP32-S3-WROOM-1-N4','GPIO':GPIO,'shift_register_bits':dict(enumerate(STATIC))},indent=2)+'\n')
    with (OUT/'GPIO-allocation.csv').open('w') as f:
        w=csv.writer(f,lineterminator="\n");w.writerow(['ESP32_GPIO','signal','restriction'])
        for pin,net in GPIO.items():w.writerow([pin,net,'reserved strap, no RF function' if net=='STRAP_RESERVED' else 'BOOT strap/recovery only' if pin==0 else 'native USB only' if pin in [19,20] else 'N4 without octal PSRAM required' if pin in [35,36,37] else 'configure safe state before INIT_OK'])
    lines=['# M6-C1 complete GPIO allocation','', '| GPIO | Signal |','|---:|---|']
    lines += [f'|{pin}|{net}|' for pin,net in GPIO.items()]
    lines += ['', 'Static595 register bits (not extra MCU GPIO):','', '| Bit | Signal |','|---:|---|']
    lines += [f'|{bit}|{net}|' for bit,net in enumerate(STATIC)]
    lines += ['', 'I2C0=GPIO8/9, RTC and isolated RF80; I2C1=GPIO17/18, isolated RF2M. SPI=GPIO10–13 with independent595 latch38. LEDC0/1 share timer0 onGPIO6/7; use separate GPTimer/RMT resources for DDS sampling and slot/Morse edges. USB19/20 and UART43/44 are reserved. GPIO14 is the non-JTAG INIT permission; initialize JTAG-reused39–42 as safe GPIO before granting it. GPIO3/45/46 remain unused straps. Physical timing and operation NOT_RUN.']
    (OUT/'GPIO-allocation.md').write_text('\n'.join(lines)+'\n')
    return result
if __name__=='__main__':extract()

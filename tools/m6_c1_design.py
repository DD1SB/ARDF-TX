#!/usr/bin/python3
"""Deterministic pin-explicit M6-C1 capture. Writes controller files only."""
import sys, json, copy, types
from pathlib import Path
from m6_c1_contracts import extract, GPIO, STATIC
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/'hardware/controller'; D=P/'review/M6-C1'
# Reuse the established S-expression capture engine without changing RF history.
code=(ROOT/'tools/m5_2m_design.py').read_text().split('\nFP_R=')[0]
code=code.replace("ROOT / 'hardware/2m'","ROOT / 'hardware/controller'").replace('ARDF_2M','ARDF_CTL').replace('RF2M','CTRL').replace("DATE = '2026-10-15'","DATE = '2026-10-18'")
code=code.replace('pop not in ("ALL","NORMAL","BOOST2S")','pop in ("DEBUG","LORA_OPTION_OPEN")')
code=code.replace('y=65+(i//3)*65','y=75+(i//3)*48')
code=code.replace('ARDF-TX 2 m A2A evaluation schematic','ARDF-TX universal ESP32-S3 controller')
engine=types.ModuleType('m6_capture');engine.__file__=__file__;exec(code,engine.__dict__)
RFP='Resistor_SMD:R_0603_1608Metric'; CFP='Capacitor_SMD:C_0603_1608Metric'; SOT='Package_TO_SOT_SMD:SOT-23'; S6='Package_TO_SOT_SMD:SOT-23-6'; S5='Package_TO_SOT_SMD:SOT-23-5'; T14='Package_SO:TSSOP-14_4.4x5mm_P0.65mm'; T16='Package_SO:TSSOP-16_4.4x5mm_P0.65mm'; T20='Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm'
class Capture(engine.Design):
    def __init__(self):
        self.lib=engine.Library();self.parts={};self.sheets=[];self.root_uuid=engine.uid('M6-C1-controller-root');self.revision='M6-C1 candidate'
        for s in ['Device:R','Device:C','Device:D','Device:D_Schottky','Device:D_Zener','Device:D_TVS','Device:Fuse','Device:L','Device:LED','Switch:SW_Push','Device:Battery_Cell','power:PWR_FLAG']:
            self.lib.native(s)
        self.count={};self.current={};self.pinspec={}
    def get(self,block):
        n=self.count.get(block,0);page=n//18;name=block+('_'+str(page+1) if page else '')
        if name not in self.current:self.current[name]=self.sheet(name,block.replace('_',' ')+' / '+str(page+1))
        self.count[block]=n+1;i=n%18;return self.current[name],80+(i%3)*180,55+(i//3)*56
    def add(self,r,t,v,pins,fp,mpn,block='01_power',pop='ALL',cost=.03,src='',note='',prices=None,evidence='ESTIMATE',stock='Unquoted / check before procurement'):
        fmap=json.loads((P/'footprint-origins.json').read_text()) if (P/'footprint-origins.json').exists() else {}
        fp=fmap.get(fp,fp)
        observed={
            'TCA9517DR':({'1':1.09,'10':.809,'20':.809},'OBSERVED_2026-10-18','Mouser indexed stock6351..6900, MOQ1; unreserved'),
            'TMUX1511PWR':({'1':.568,'10':.401,'20':.401},'OBSERVED_2026-10-18','Mouser indexed55stock, MOQ1; unreserved'),
            'AP63203WU-7':({'1':1.217,'10':1.0856,'20':1.0856},'ESTIMATE_FX_OF_LCSC_USD_2026-10-18','LCSC C780769 indexed8165stock MOQ1; EUR budget at1EUR/USD allowance, not FX quote. Mouser0stock.'),
            'SN74LVC244APWR':({'1':.963,'10':.692,'20':.692},'ESTIMATE_COMPARATOR_E4_2026-10-18','Exact non-E4 stock/price OPEN; E4 package-matched comparator only')}
        if mpn in observed:prices,evidence,stock=observed[mpn]
        s,x,y=self.get(block);s.place(r,t,v,{str(k):v for k,v in pins.items()},x,y,fp,mpn,group=block,pop=pop,note=note,source=src,price=prices or {'1':cost,'10':cost,'20':cost},evidence=evidence,availability=stock)
        part=self.parts[r]
        part['moq']=1 if evidence.startswith('OBSERVED') else 'OPEN'
        if r in ['U10','U20']:
            part['supplier']='Mouser DE (indexed observation)'
            part['supplier_part_number']='356-ESP32-S3WROOM1N4' if r=='U10' else '428-203853-MG01'
        if mpn in ['TCA9517DR','TMUX1511PWR']:
            part['supplier']='Mouser EU (indexed observation)';part['supplier_part_number']='595-'+mpn;part['moq']=1
        if mpn=='AP63203WU-7':
            part['supplier']='LCSC (indexed observation)';part['supplier_part_number']='C780769';part['moq']=1
        return r
    def boxpart(self,r,v,pins,types,fp,mpn,block,pop='ALL',cost=.3,src='',note='',prices=None,evidence='ESTIMATE',stock='Unquoted / check before procurement'):
        sym='M6_'+r;self.lib.box(sym,{str(k):(str(k)+'_'+types.get(str(k),('IO','passive'))[0],types.get(str(k),('IO','passive'))[1]) for k in pins})
        return self.add(r,sym,v,pins,fp,mpn,block,pop,cost,src,note,prices,evidence,stock)
    def r(self,r,v,a,b,block,pop='ALL',cost=.01):
        values={'22':'22R','100':'100R','1k':'1KL','2.2k':'2K2L','4.7k':'4K7L','5.1k':'5K1L','10k':'10KL','33k':'33KL','47k':'47KL','100k':'100KL','330k':'330KL','470k':'470KL'}
        suffix=values[v];suffix=suffix if suffix.endswith('L') else suffix+'L'
        return self.add(r,'R',v,{1:a,2:b},RFP,'RC0603FR-07'+suffix,block,pop,cost,note='Yageo RC0603 1%, 0.1W')
    def c(self,r,v,a,b,block,pop='ALL',fp=CFP,mpn='CL10B104KB8NNNC',cost=.02):
        return self.add(r,'C',v,{1:a,2:b},fp,mpn,block,pop,cost)
    def dec(self,r,rail,block,pop='ALL'):self.c(r,'100n',rail,'GND',block,pop)

def build():
    contracts=extract();P.mkdir(parents=True,exist_ok=True);d=Capture();bi='01_power'
    d.boxpart('J1','PACK / GND / ID',{1:'PACK_RAW',2:'GND',3:'PACK_ID_RAW'},{},'ARDF_CTL:JST_XH_B3B_Standard','B3B-XH-A(LF)(SN)',bi,cost=.25,src='https://www.jst.co.uk/downloads/series/eXH_1.pdf',note='Controller branch only,1A fuse. PA packs use separate fused harness. Enlarged1.10mm standard finished holes; JST hard-FR4 guideline note2, first-part fit inspection.')
    d.add('F1','Fuse','1A 63V fast',{1:'PACK_RAW',2:'PACK_FUSED'},'ARDF_CTL:Fuse_Bourns_SF1206F','SF-1206F100-2',bi,cost=.45,src='https://www.bourns.com/docs/product-datasheets/sf-1206f.pdf',note='1A fast fuse,63VDC,50A interrupt;0.132ohm typ +/-25%. Manufacturer lands4.7mm overall/1.65mm gap/2.2mm width. Nonresettable; replace only after fault diagnosis.')
    d.add('D1','D_Schottky','100V 2A reverse block',{1:'PACK_PROT',2:'PACK_FUSED'},'Diode_SMD:D_SMA','STPS2H100A',bi,cost=.22,src='https://www.st.com/resource/en/datasheet/stps2h100.pdf')
    d.add('D4','D','Low leakage battery OR',{1:'VIN_SYS',2:'PACK_PROT'},'Diode_SMD:D_SMA','S1M-E3/61T',bi,cost=.06,src='https://www.vishay.com/docs/88503/s1a.pdf',note='Silicon rectifier, 5uA max reverse at25C /50uA at125C. Avoid Schottky reverse leakage falsely asserting pack presence on USB.')
    d.add('D2','D_Zener','18V unidirectional TVS',{1:'PACK_PROT',2:'GND'},'Diode_SMD:D_SMB','SMBJ18A',bi,cost=.14,src='https://www.littelfuse.com/media?resourcetype=datasheets&itemid=142b62cb-5ef8-4af6-8131-6df1d404ddc1',note='Cathode package pad1 positive, anode pad2 GND, AFTER reverse diode.')
    d.add('D3','D_Schottky','USB low-drop OR',{1:'VIN_SYS',2:'USB_LIMIT'},'Diode_SMD:D_SMA','STPS1L30A',bi,cost=.15,src='https://www.st.com/resource/en/datasheet/stps1l30.pdf',note='30V reverse, max0.395V at1A25C. D21 bounds reverse leakage at USB_LIMIT; no raw pack-to-USB path.')
    d.add('D21','D_Zener','USB reverse-leak clamp 5.1V',{1:'USB_LIMIT',2:'GND'},'Diode_SMD:D_SOD-123F','BZT52H-B5V1,115',bi,cost=.035,src='https://assets.nexperia.com/documents/data-sheet/BZT52H_SER.pdf',note='SOD123F pin1K pin2A. 5.00..5.20V at5mA, rdif60ohm. Bounds D3 leakage; hot clamp qualification remains NOT_RUN.')
    d.boxpart('U1','AP63203WU-7',{1:'V3V3',2:'VIN_SYS',3:'VIN_SYS',4:'GND',5:'BUCK_SW',6:'BUCK_BST'},{'1':('FB','input'),'2':('EN','input'),'3':('VIN','power_in'),'4':('GND','power_in'),'5':('SW','output'),'6':('BST','passive')},'Package_TO_SOT_SMD:TSOT-23-6','AP63203WU-7',bi,cost=.45,src='https://www.diodes.com/assets/Datasheets/AP63200-AP63201-AP63203-AP63205.pdf',note='3.8..32V recommended,35V DC absolute/40V for400ms only. Fixed 3.3V, 2A. 1.1MHz. FB senses output.')
    d.add('L1','L','4.7uH 4.6Arms',{1:'BUCK_SW',2:'V3V3'},'Inductor_SMD:L_Bourns_SRP5030T','SRP5030T-4R7M',bi,cost=.55,src='https://www.bourns.com/data/global/pdfs/SRP5030T.pdf')
    d.c('C1','100n','BUCK_BST','BUCK_SW',bi)
    for r in ['C2','C3']:d.c(r,'4.7u 50V','VIN_SYS','GND',bi,fp='Capacitor_SMD:C_1210_3225Metric',mpn='GRM32ER71H475KA88L',cost=.27)
    for r in ['C4','C5']:d.c(r,'22u 10V','V3V3','GND',bi,fp='Capacitor_SMD:C_1206_3216Metric',mpn='CL31A226KPHNNNE',cost=.12)
    d.dec('C6','V3V3',bi)
    d.r('R1','470k','PACK_PROT','BAT_DIV',bi);d.r('R2','47k','BAT_DIV','GND',bi);d.r('R3','10k','V3V3','PACK_ID_RAW',bi)
    # Battery-present is an independent USB-only inhibit, not battery-type validation.
    d.boxpart('Q1','MMBT3904',{1:'BATT_BASE',2:'GND',3:'PACK_ABSENT'},{'1':('B','input'),'2':('E','passive'),'3':('C','open_collector')},SOT,'MMBT3904LT1G',bi,cost=.025,src='https://www.onsemi.com/pdf/datasheet/mmbt3904lt1-d.pdf')
    d.r('R4','100k','PACK_PROT','BATT_BASE',bi);d.r('R5','100k','BATT_BASE','GND',bi);d.r('R6','10k','V3V3','PACK_ABSENT',bi);d.r('R7','10k','PACK_PROT','GND',bi)
    bj='02_USB_reset'
    usb={ 'A1':'GND','A4':'USB_VBUS','A5':'USB_CC1','A6':'USB_DP_CONN','A7':'USB_DM_CONN','A8':None,'A9':'USB_VBUS','A12':'GND','B1':'GND','B4':'USB_VBUS','B5':'USB_CC2','B6':'USB_DP_CONN','B7':'USB_DM_CONN','B8':None,'B9':'USB_VBUS','B12':'GND','SH':'GND'}
    d.boxpart('J2','USB-C native USB2',usb,{},'ARDF_CTL:USB4105_Standard','USB4105-GF-A',bj,cost=.55,src='https://gct.co/files/drawings/usb4105.pdf',note='All shield pads SH grounded. CC1/2 each 5.1k sink. No USB->pack path. Shield annular rings enlarged0.05mm.')
    d.r('R10','5.1k','USB_CC1','GND',bj);d.r('R11','5.1k','USB_CC2','GND',bj)
    d.boxpart('U2','TPS2553DBVR',{1:'USB_VBUS',2:'GND',3:'USB_VBUS',4:'USB_OC_N',5:'USB_ILIM',6:'USB_LIMIT'},{'1':('IN','power_in'),'2':('GND','power_in'),'3':('EN','input'),'4':('FAULT_N','open_collector'),'5':('ILIM','passive'),'6':('OUT','power_out')},S6,'TPS2553DBVR',bj,cost=.75,src='https://www.ti.com/lit/ds/symlink/tps2553.pdf',note='USB current limit ~0.3A with 100k; USB WiFi disabled. Enumeration/current compliance physical gate; no RF on USB only.')
    d.r('R63','10k','USB_VBUS','GND',bj)
    d.boxpart('Q2','MMBT3904 VBUS sense',{1:'USB_BASE',2:'GND',3:'USB_VBUS_N'},{'1':('B','input'),'2':('E','passive'),'3':('C','open_collector')},SOT,'MMBT3904LT1G',bj,cost=.025,src='https://www.onsemi.com/pdf/datasheet/mmbt3904lt1-d.pdf',note='GPIO37 inverted VBUS presence. USB PHY attaches only while VBUS present; RTC INT is unused; poll hundredths/time over I2C.')
    d.r('R64','100k','USB_VBUS','USB_BASE',bj);d.r('R65','100k','USB_BASE','GND',bj);d.r('R66','10k','V3V3','USB_VBUS_N',bj)
    d.r('R12','100k','USB_ILIM','GND',bj);d.r('R13','100k','USB_OC_N','V3V3',bj);d.dec('C10','V3V3',bj)
    d.c('C11','4.7u 10V','USB_VBUS','GND',bj,mpn='CL10A475KP8NNNC',cost=.045)
    d.boxpart('U3','USBLC6-2SC6',{1:'USB_DP_CONN',2:'GND',3:'USB_DM_CONN',4:'USB_DM_CONN',5:'V3V3',6:'USB_DP_CONN'},{},S6,'USBLC6-2SC6',bj,cost=.22,src='https://www.st.com/resource/en/datasheet/usblc6-2.pdf',note='Positive ESD rail pin5 biased from local3.3V with C10, NOT raw USB_VBUS. Prevents self-powered D+ pull-up charging absent VBUS through steering diode; datasheet VCC application.')
    d.r('R14','22','USB_DP_CONN','USB_DP',bj);d.r('R15','22','USB_DM_CONN','USB_DM',bj)
    d.boxpart('U4','TLV803EA30DBZR',{1:'GND',2:'MCU_EN',3:'V3V3'},{'1':('GND','power_in'),'2':('RESET_N','open_collector'),'3':('VDD','power_in')},SOT,'TLV803EA30DBZR',bj,cost=.25,src='https://www.ti.com/lit/ds/symlink/tlv803e.pdf',note='Standard DBZ pinout (not V/R pinout). Code30 is3.08V threshold, not3.0V; reset delay A200ms.')
    d.r('R16','10k','V3V3','MCU_EN',bj);d.c('C12','1u','MCU_EN','GND',bj,mpn='CL10A105KB8NNNC')
    d.r('R17','10k','V3V3','BOOT',bj);d.r('R18','10k','V3V3','START_N',bj)
    for ref,net,label in [('SW1','MCU_EN','RESET'),('SW2','BOOT','BOOT'),('SW3','START_N','START'),('SW4','MCU_EN','STOP / hold reset')]:
        d.add(ref,'SW_Push',label,{1:net,2:'GND'},'Button_Switch_SMD:SW_SPST_TL3342','TL3342F160QG',bj,cost=.12)
    bm='03_MCU'
    mpins={1:'GND',2:'V3V3',3:'MCU_EN',40:'GND',41:'GND'}; pmap={4:4,5:5,6:6,7:7,8:15,9:16,10:17,11:18,12:8,13:19,14:20,15:3,16:46,17:9,18:10,19:11,20:12,21:13,22:14,23:21,24:47,25:48,26:45,27:0,28:35,29:36,30:37,31:38,32:39,33:40,34:41,35:42,36:44,37:43,38:2,39:1}
    for pin,gpio in pmap.items():mpins[pin]=None if GPIO[gpio]=='STRAP_RESERVED' else GPIO[gpio]
    types={str(p):('GPIO'+str(g),'bidirectional') for p,g in pmap.items()};types.update({'1':('GND','power_in'),'2':('3V3','power_in'),'3':('EN','input'),'40':('GND','power_in'),'41':('GND_EP','power_in')})
    # MCU has a tall 41-pin box, put it on its own sheet to keep stubs readable.
    d.boxpart('U10','ESP32-S3-WROOM-1-N4',mpins,types,'ARDF_CTL:ESP32_S3_WROOM_1_Standard','ESP32-S3-WROOM-1-N4',bm,cost=4.48,src='https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf',note='4MB flash, no PSRAM. GPIO35/36/37 available. GPIO0 boot only; GPIO3/45/46 reserved. USB19/20. Standard KiCad thermal holes omitted; solid source solder lands retained, ground vias outside hidden land.',prices={'1':4.48,'10':3.88,'20':3.88},evidence='OBSERVED_2026-10-18',stock='Mouser index 3296, MOQ1; recheck before buying')
    d.count[bm]=3
    d.c('C20','10u 10V','V3V3','GND',bm,mpn='CL10A106KP8NNNC',cost=.08);d.dec('C21','V3V3',bm)
    d.boxpart('J3','UART recovery / GND',{1:'GND',2:'UART_TX',3:'UART_RX'},{},'ARDF_CTL:UART_61300311121','61300311121',bm,pop='DEBUG',cost=.1,note='3.3V UART, no5V supply. Native USB normal flashing path. Standard1.10mm finished holes, no tight process.')
    br='04_RTC_analog'
    rtc={1:'RTC_BACKUP',2:'RTC80_SDA',3:None,4:'GND',5:'GND',6:'V3V3',7:None,8:'RTC80_SCL'}
    d.boxpart('U20','RV-3032-C7 2.5ppm',rtc,{'1':('VBACKUP','power_in'),'2':('SDA','bidirectional'),'3':('INT_N','open_collector'),'4':('EVI','input'),'5':('VSS','power_in'),'6':('VDD','power_in'),'7':('CLKOUT','output'),'8':('SCL','input')},'ARDF_CTL:RV3032_C7','RV-3032-C7-32.768KHZ-2.5PPM-TA-QA',br,cost=3.66,src='https://www.microcrystal.com/fileadmin/Media/Products/RTC/App.Manual/RV-3032-C7_App-Manual.pdf',note='Program BSM=10 LSM, TCM=OFF, NCLKE=1. Factory backup disabled. Readback and validity required before ARM.',prices={'1':3.66,'10':2.75,'20':2.75},evidence='OBSERVED_2026-10-18',stock='Mouser index 4353, MOQ1')
    d.add('BT1','Battery_Cell','CR1220 primary',{1:'CELL_POS',2:'GND'},'Battery:BatteryHolder_Keystone_3000_1x12mm','3000',br,cost=.45,note='Holder only. Primary cell external line item. No charging.')
    d.boxpart('D20','BAS116 no cell charging',{1:'CELL_POS',2:None,3:'BACKUP_D'},{'1':('A','passive'),'2':('NC','no_connect'),'3':('K','passive')},SOT,'BAS116,115',br,cost=.06,src='https://assets.nexperia.com/documents/data-sheet/BAS116.pdf')
    d.r('R20','1k','BACKUP_D','RTC_BACKUP',br);d.dec('C22','RTC_BACKUP',br);d.dec('C23','V3V3',br)
    for ref,net in [('R22','RTC80_SDA'),('R23','RTC80_SCL'),('R24','RF2M_SDA'),('R25','RF2M_SCL')]:d.r(ref,'4.7k','V3V3',net,br)
    d.boxpart('U21','TMUX1511PWR',{1:'V3V3',2:'BAT_DIV',3:'BAT_ADC',4:'V3V3',5:'PACK_ID_RAW',6:'PACK_ID_ADC',7:'GND',8:'MODULE_ID_ADC',9:'RF2M_MODULE_ID',10:'V3V3',11:'PA_RAIL_ADC',12:'RF2M_PA_RAIL_ADC',13:'V3V3',14:'V3V3'},{'7':('GND','power_in'),'14':('VDD','power_in')},T14,'TMUX1511PWR',br,cost=.7,src='https://www.ti.com/lit/ds/symlink/tmux1511.pdf',note='Powered-off protected four analog channels. Signals remain <=5.5V while VDD absent. ADC input sampling caps, calibrated 11dB ADC1.')
    # Sampling/filter capacitors are UPSTREAM of powered-off isolation. No
    # charged100nF reservoir is left directly attached to an unpowered MCU pin.
    for ref,net in [('C24','BAT_DIV'),('C25','PACK_ID_RAW'),('C26','RF2M_MODULE_ID'),('C27','RF2M_PA_RAIL_ADC')]:d.c(ref,'100n',net,'GND',br)
    d.dec('C28','V3V3',br)
    d.r('R26','33k','V3V3','RF2M_MODULE_ID',br,pop='RF2M')
    bs='05_static_safety'
    # 595 output stage is NOT cleared by SRCLR. OE holds high until an explicit zero latch.
    for i,r in enumerate(['U30','U31']):
        outputs=STATIC[i*8:i*8+8];pins={1:outputs[1],2:outputs[2],3:outputs[3],4:outputs[4],5:outputs[5],6:outputs[6],7:outputs[7],8:'GND',9:'SHIFT_CHAIN' if i==0 else None,10:'MCU_EN',11:'SPI_SCK',12:'SHIFT_LATCH',13:'SAFE_OE_N',14:'SPI_MOSI' if i==0 else 'SHIFT_CHAIN',15:outputs[0],16:'V3V3'}
        typ={str(k):('Q','tri_state') for k in [1,2,3,4,5,6,7,15]};typ.update({'8':('GND','power_in'),'16':('VCC','power_in'),'9':('QH_S','output'),'10':('SRCLR_N','input'),'11':('SRCLK','input'),'12':('RCLK','input'),'13':('OE_N','input'),'14':('SER','input')})
        d.boxpart(r,'SN74HC595PWR',pins,typ,T16,'SN74HC595PWR',bs,cost=.18,src='https://www.ti.com/lit/ds/symlink/sn74hc595.pdf',note='Clear shift register does not clear storage latch; OE plus explicit zero latch is mandatory.');d.dec('C'+str(30+i),'V3V3',bs)
    for i,n in enumerate(STATIC):d.r('R'+str(30+i),'10k',n,'GND',bs)
    for i,n in enumerate(['INIT_OK','ARM','MUTE_RELEASE','PROGRESS','KEY','SLOT','AF_PWM','LEVEL_PWM','SHIFT_LATCH']):d.r('R'+str(50+i),'10k',n,'GND',bs)
    d.r('R59','10k','V3V3','SAFE_OE_N',bs)
    # Single-gate package maps are independent of schematic symbol conventions.
    d.boxpart('U32','SN74LVC1G04DBVR',{1:None,2:'PACK_ABSENT',3:'GND',4:'PACK_PRESENT',5:'V3V3'},{'2':('A','input'),'3':('GND','power_in'),'4':('Y','output'),'5':('VCC','power_in')},S5,'SN74LVC1G04DBVR',bs,cost=.1,src='https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf')
    d.boxpart('U33','SN74LVC1G10DBVR',{1:'INIT_OK',2:'MCU_EN',3:'GND',4:'SAFE_OE_N',5:'V3V3',6:'PACK_PRESENT'},{'1':('A','input'),'2':('B','input'),'3':('GND','power_in'),'4':('Y','output'),'5':('VCC','power_in'),'6':('C','input')},S6,'SN74LVC1G10DBVR',bs,cost=.1,src='https://www.ti.com/lit/ds/symlink/sn74lvc1g10.pdf')
    d.boxpart('U34','SN74LVC2G04DCKR',{1:'SAFE_OE_N',2:'BAND80',3:'GND',4:'BAND2',5:'SAFE',6:'V3V3'},{'1':('1A','input'),'2':('2Y','output'),'3':('GND','power_in'),'4':('2A','input'),'5':('1Y','output'),'6':('VCC','power_in')},'Package_TO_SOT_SMD:SOT-363_SC-70-6','SN74LVC2G04DCKR',bs,cost=.12,src='https://www.ti.com/lit/ds/symlink/sn74lvc2g04.pdf')
    d.boxpart('U35','SN74LVC00APWR',{1:'SAFE',2:'BAND80',3:'OE80_N',4:'SAFE',5:'BAND2',6:'OE2M_N',7:'GND',8:None,9:'GND',10:'GND',11:None,12:'GND',13:'GND',14:'V3V3'},{'1':('1A','input'),'2':('1B','input'),'3':('1Y','output'),'4':('2A','input'),'5':('2B','input'),'6':('2Y','output'),'7':('GND','power_in'),'8':('3Y','output'),'9':('3A','input'),'10':('3B','input'),'11':('4Y','output'),'12':('4A','input'),'13':('4B','input'),'14':('VCC','power_in')},T14,'SN74LVC00APWR',bs,cost=.14,src='https://www.ti.com/lit/ds/symlink/sn74lvc00a.pdf')
    d.boxpart('U36','SN74LVC1G04DBVR',{1:None,2:'ARM',3:'GND',4:'DISARMED',5:'V3V3'},{'2':('A','input'),'3':('GND','power_in'),'4':('Y','output'),'5':('VCC','power_in')},S5,'SN74LVC1G04DBVR',bs,cost=.1)
    # Both I2C branches forced disconnected while ARM is high. Cannot be bypassed by RTC polling.
    d.boxpart('U37','SN74LVC08APWR',{1:'BUS80',2:'DISARMED',3:'BUS80_EN',4:'BUS2M',5:'DISARMED',6:'BUS2M_EN',7:'GND',8:None,9:'GND',10:'GND',11:None,12:'GND',13:'GND',14:'V3V3'},{'1':('1A','input'),'2':('1B','input'),'3':('1Y','output'),'4':('2A','input'),'5':('2B','input'),'6':('2Y','output'),'7':('GND','power_in'),'8':('3Y','output'),'9':('3A','input'),'10':('3B','input'),'11':('4Y','output'),'12':('4A','input'),'13':('4B','input'),'14':('VCC','power_in')},T14,'SN74LVC08APWR',bs,cost=.14,src='https://www.ti.com/lit/ds/symlink/sn74lvc08a.pdf')
    for i in range(32,38):d.dec('C'+str(i),'V3V3',bs)
    for ref,net in [('D30','LED_ARM'),('D31','LED_FAULT'),('D32','V3V3')]:
        d.r('R'+str(60+int(ref[1:])-30),'2.2k',net,ref+'_A',bs);d.add(ref,'LED','status',{1:'GND',2:ref+'_A'},'LED_SMD:LED_0603_1608Metric','LTST-C190KGKT' if ref!='D31' else 'LTST-C190KRKT',bs,cost=.03)
    # Module ports: selected branch only, powered-off protection, series damping and default pulls.
    control={'RF80':[('ARM','ARM'),('CW_KEY','KEY'),('LEASE','PROGRESS'),('MUTE_N','MUTE_RELEASE'),('PA_REQ','PA_REQ'),('FOX_REQ','FOX_REQ'),('PWR0','PWR0'),('PWR1','PWR1'),('PACK4_OK','PACK4_SOFT')],
             'RF2M':[('ARM','ARM'),('SLOT','SLOT'),('KEY','KEY'),('PROGRESS','PROGRESS'),('MUTE_N','MUTE_RELEASE'),('PATH_TRAIN','PATH_TRAIN'),('PROFILE_FULL','PROFILE_FULL'),('AF_PWM','AF_PWM'),('LEVEL_PWM','LEVEL_PWM'),('PREPARE','PREPARE'),('PA_PREPARE','PA_PREPARE')]}
    serial=100
    for bidx,band in enumerate(['RF80','RF2M']):
        block='06_RF80' if bidx==0 else '07_RF2M';pop=band;rail='V3V3_'+band;oe='OE80_N' if bidx==0 else 'OE2M_N';base=40+bidx*10
        cn={row['pin']:row['controller_net'] for row in contracts[band]['pins']}
        fp='ARDF_CTL:IDC16_61201621621' if bidx==0 else 'ARDF_CTL:IDC20_61202021621'
        d.boxpart('J'+str(4+bidx),band+' keyed controller link',cn,{},fp,'61201621621' if bidx==0 else '61202021621',block,pop,cost=.7,src='https://www.we-online.com/components/products/datasheet/'+('61201621621' if bidx==0 else '61202021621')+'.pdf',note='Straight-through IDC cable, pin1-to-pin1. Physical key and cable continuity must be checked before connection.')
        d.boxpart('U'+str(base),'TPS22918DBVR',{1:'V3V3',2:'GND',3:'POWER80' if bidx==0 else 'POWER2M',4:None,5:rail,6:rail},{'1':('IN','power_in'),'2':('GND','power_in'),'3':('ON','input'),'5':('QOD','passive'),'6':('OUT','power_out')},'ARDF_CTL:SOT-23-6_CTL','TPS22918DBVR',block,pop,cost=.35,src='https://www.ti.com/lit/gpn/tps22918',note='3.3V only, max5.5V. CT pin4 OPEN per datasheet. QOD5 tiedOUT6. Use88mohm hot RON envelope; source sole V3V3 supply. No switch current limiter: buck current limit/reset/fuse provide fault shutdown.')
        d.dec('C'+str(base),rail,block,pop);d.c('C'+str(base+1),'1u',rail,'GND',block,pop,mpn='CL10A105KB8NNNC')
        # Octal 244 first eight controls, quad125 remainder (unused inputs grounded, outputs NC).
        controls=control[band];p244={1:oe,10:'GND',19:oe,20:rail};t244={'1':('OE1_N','input'),'10':('GND','power_in'),'19':('OE2_N','input'),'20':('VCC','power_in')}
        inout=[(2,18),(4,16),(6,14),(8,12),(11,9),(13,7),(15,5),(17,3)]
        for (sig,host),(a,y) in zip(controls[:8],inout):p244[a]=host;p244[y]=band+'_'+sig+'_BUF';t244[str(a)]=('A','input');t244[str(y)]=('Y','tri_state')
        d.boxpart('U'+str(base+1),'SN74LVC244APWR',p244,t244,T20,'SN74LVC244APWR',block,pop,cost=.2,src='https://www.ti.com/lit/ds/symlink/sn74lvc244a.pdf',note='Ioff isolation. OE pulled to local VCC independently of host power.')
        p125={7:'GND',14:rail};t125={'7':('GND','power_in'),'14':('VCC','power_in')}
        for i,(en,a,y) in enumerate([(1,2,3),(4,5,6),(10,9,8),(13,12,11)]):
            active=i<len(controls[8:]);p125[en]=oe if active else rail;p125[a]=controls[8+i][1] if active else 'GND';p125[y]=band+'_'+controls[8+i][0]+'_BUF' if active else None;t125[str(en)]=('OE_N','input');t125[str(a)]=('A','input');t125[str(y)]=('Y','tri_state')
        d.boxpart('U'+str(base+2),'SN74LVC125APWR',p125,t125,T14,'SN74LVC125APWR',block,pop,cost=.17,src='https://www.ti.com/lit/ds/symlink/sn74lvc125a.pdf')
        d.r('R'+str(base+40),'10k',rail,oe,block,pop)
        d.dec('C'+str(base+2),rail,block,pop);d.dec('C'+str(base+3),rail,block,pop)
        for sig,host in controls:
            net=band+'_'+sig;d.r('R'+str(serial),'100',net+'_BUF',net,block,pop);d.r('R'+str(serial+1),'10k',net,'GND',block,pop);serial+=2
        sda='RTC80_SDA' if bidx==0 else 'RF2M_SDA';scl='RTC80_SCL' if bidx==0 else 'RF2M_SCL'
        m_sda=band+('_SDA' if bidx==0 else '_I2C_SDA');m_scl=band+('_SCL' if bidx==0 else '_I2C_SCL')
        d.boxpart('U'+str(base+3),'TCA9517DR',{1:'V3V3',2:scl,3:sda,4:'GND',5:'BUS80_EN' if bidx==0 else 'BUS2M_EN',6:m_sda,7:m_scl,8:rail},{'1':('VCCA','power_in'),'2':('SCLA','bidirectional'),'3':('SDAA','bidirectional'),'4':('GND','power_in'),'5':('EN','input'),'6':('SDAB','bidirectional'),'7':('SCLB','bidirectional'),'8':('VCCB','power_in')},'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm','TCA9517DR',block,pop,cost=.6,src='https://www.ti.com/lit/ds/symlink/tca9517.pdf',note='SOIC selected for robust green-mask webs and manual assembly. Branch disable independent of I2C. B-side RF pull-ups on module. Check100kHz/cable rise time physically.')
        d.dec('C'+str(base+4),rail,block,pop);d.dec('C'+str(base+5),'V3V3',block,pop)
        d.r('R'+str(base+41),'10k' if bidx else '2.2k',band+'_FAULT_N','GND' if bidx else rail,block,'ALL' if bidx else pop)
    bf='08_status'
    d.boxpart('U60','SN74LVC2G17DCKR',{1:'RF80_FAULT_N',2:'RF2M_FAULT',3:'GND',4:'RF2M_FAULT_N',5:'RF80_FAULT',6:'V3V3'},{'1':('1A','input'),'2':('2Y','output'),'3':('GND','power_in'),'4':('2A','input'),'5':('1Y','output'),'6':('VCC','power_in')},'Package_TO_SOT_SMD:SOT-363_SC-70-6','SN74LVC2G17DCKR',bf,cost=.12,src='https://www.ti.com/lit/ds/symlink/sn74lvc2g17.pdf',note='Independent status channels, Ioff prevents GPIO back-power from powered RF boards.')
    d.dec('C60','V3V3',bf)
    d.r('R93','10k','RF80_FAULT_N','GND',bf)
    # Exact manufacturer module; sourcing suffix discrepancy remains an explicit optional-population hold.
    bl='09_LoRa';lp={1:'GND',2:'GND',3:'GND',4:'GND',5:'LORA_DIO1',6:None,7:None,8:None,9:None,10:'LORA_BUSY',11:'GND',12:'GND',13:'V3V3',14:'SPI_SCK',15:'SPI_MISO',16:'SPI_MOSI',17:'LORA_NSS',18:'LORA_RESET',19:'GND',20:'GND',21:'LORA_ANT',22:'GND'}
    d.boxpart('U70','Silicontra SX1262ZTR8-GC',lp,{'13':('VCC','power_in'),'5':('DIO1','output'),'10':('BUSY','output'),'14':('SCK','input'),'15':('MISO','tri_state'),'16':('MOSI','input'),'17':('NSS','input'),'18':('RST_N','input')},'ARDF_CTL:Silicontra_SX1262ZTR8_GC','SX1262ZTR8-GC',bl,pop='LORA_OPTION_OPEN',cost=5.6,src='https://www.silicontra.com/UploadFile/Soft/SX1262ZTR8-GC%28V1.0%29.pdf',note='OPTIONAL DNP: manufacturer ZTR8 vs distributor TR8 suffix not confirmed. Manufacturer dimension drawing lacks tolerances and ambiguous 1.12mm callout; footprint qualification OPEN. Do not populate without review.',prices={'1':5.6,'10':4.8,'20':4.8},evidence='ESTIMATE_FX_OF_OBSERVED_USD',stock='Distributor C42381682 lists different TR8 suffix, 170 indexed; NOT confirmed equivalent')
    d.r('R70','10k','V3V3','LORA_NSS',bl,'LORA_OPTION_OPEN');d.r('R71','10k','V3V3','LORA_RESET',bl,'LORA_OPTION_OPEN')
    d.dec('C70','V3V3',bl,'LORA_OPTION_OPEN');d.c('C71','10u 10V','V3V3','GND',bl,'LORA_OPTION_OPEN',mpn='CL10A106KP8NNNC',cost=.08)
    d.boxpart('J7','LoRa antenna U.FL',{1:'LORA_ANT',2:'GND'},{},'ARDF_CTL:UFL_Standard','U.FL-R-SMT-1(10)',bl,pop='LORA_OPTION_OPEN',cost=.7,src='https://www.hirose.com/product/series/U.FL',note='Pin1 signal; duplicated pin2 ground. Underbody copper keepout preserved, exposed-mask-only rectangle omitted. External868MHz antenna; optional module footprint review OPEN.')
    # Small physical measurement access, no debug instruments on product.
    for ref,net in [('TP1','V3V3'),('TP2','GND'),('TP3','VIN_SYS'),('TP4','SAFE_OE_N')]:
        typ=d.lib.box('M6_'+ref,{'1':(net,'passive')});d.add(ref,typ,net,{1:net},'TestPoint:TestPoint_Pad_D1.0mm', 'PCB_FEATURE','10_test',pop='ALL',cost=0)
    # Supply roots explicitly flagged for ERC, representing bounded external sources/passive feeds.
    for i,net in enumerate(['GND','PACK_RAW','USB_VBUS','VIN_SYS','V3V3','RTC_BACKUP']):
        s,x,y=d.get('10_test');s.place('#FLG'+str(i+1),'PWR_FLAG','PWR_FLAG',{'1':net},x,y,'','',group='power_flag',pop='ALL')
    d.save()
    # Replace inherited root commentary with the actual controller scope.
    f=P/'CTRL.kicad_sch';text=f.read_text();start=text.index('(text ');end=text.index(' (embedded_fonts',start)
    text=text[:start]+'(text '+engine.q('M6-C1 UNIVERSAL CONTROLLER / ENGINEERING CANDIDATE\nESP32-S3-WROOM-1-N4 / RV-3032-C7 / isolated RF80 + RF2M contracts\nNo manufacturing or operational release. All physical tests NOT_RUN.\nLoRa optional population/land pattern sourcing hold; see review decision.')+' (at 20 15 0)(effects(font(size 1.3 1.3))(justify left top))(uuid '+engine.q(engine.uid('M6-root-note'))+'))'+text[end:];f.write_text(text)
    # Actual pin identity export is separate from aesthetic symbol drawings.
    (D/'capture-pin-assertions.json').write_text(json.dumps({r:{'mpn':p['mpn'],'footprint':p['footprint'],'pins':p['pins']} for r,p in d.parts.items() if r.startswith(('U','J','Q','D'))},indent=2)+'\n')
    print('Captured',len(d.parts),'components,',len(d.sheets),'sheets')
if __name__=='__main__':build()

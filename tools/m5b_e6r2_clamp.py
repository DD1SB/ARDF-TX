"""Native correction proved useful by the nominal nonlinear ngspice fixture.
Q404 normal-key clamp separated from Q405 emergency command clamp, avoiding
normal-SPACE base/collector injection into the precision command input.
"""
import json,math,xml.etree.ElementTree as ET
import m5a_r1_design as c
from m5b_e6r2_common import *
from m5b_e6r2_design import pin_label,prop
HELD=[]
def main():
 guard();j=manifest();parts={a['ref']:a for a in j['parts']};assert 'R985' not in parts
 parts['Q405']['pins']['1']='MOD_COMMAND_OFF_BASE'
 fn=HW/'05_am.kicad_sch';sx=c.parse(fn.read_text());pin_label(sx,'Q405','1','MOD_COMMAND_OFF_BASE');fn.write_text(c.dump(sx)+'\n')
 c.DEST=HW;c.DATE=DATE;d=c.Design();d.parts=parts;d.revision=REV;root=c.parse((HW/'RF2M.kicad_sch').read_text());d.root_uuid=c.child(root,'uuid')[1]
 lib=c.parse((HW/'ARDF_2M.kicad_sym').read_text());d.lib.defs.update({x[1]:x for x in c.children(lib,'symbol')})
 s=d.sheet('13_carrier_keying','Carrier keying')
 for r,value,a,z,x,mpn in [('R985','10k','NORMAL_OFF','MOD_COMMAND_OFF_BASE',62,'RT0603BRD0710KL'),('R986','100k','MOD_COMMAND_OFF_BASE','GND',174,'RT0603BRD07100KL')]:
  s.place(r,'R',value,{'1':a,'2':z},x,379,'ARDF_2M:R_0603_1608Metric_E3',mpn,'carrier_keying','NORMAL',price={'1':.04},source='https://www.yageo.com/en/ProductCategory/Resistors',note='Separate Q405 emergency input clamp from normal Q404 key clamp; prevents normal SPACE command injection.')
 fn=HW/'13_carrier_keying.kicad_sch';sx=c.parse(fn.read_text())
 for item in s.items:sx.append(c.parse(item))
 for sy in c.children(sx,'symbol'):
  if prop(sy,'Reference')[2]=='R970':prop(sy,'Engineering_Note')[2]='50mohm1%1W. Kelvin probe directly at R970 terminations; TP970/TP502 are coarse voltage checks. Outer feedback senses downstream VPA.'
 fn.write_text(c.dump(sx)+'\n');parts['R970']['note']='50mohm1%1W. Kelvin probe directly at R970 terminations; TP970/TP502 are coarse voltage checks. Outer feedback senses downstream VPA.'
 j['parts']=list(d.parts.values());j['placements']['13_carrier_keying'].extend(s.placements);(HW/'RF2M.electrical.json').write_text(json.dumps(j,indent=2)+'\n')
 run=subprocess.run(['kicad-cli','sch','export','netlist','--format','kicadxml','-o',str(OUT/'RF2M.net.xml'),str(HW/'RF2M.kicad_sch')],capture_output=True,text=True);assert run.returncode==0,run.stderr
 tree=ET.parse(OUT/'RF2M.net.xml');comps={a.get('ref'):a for a in tree.findall('./components/comp')}
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs=fps(b);b.Add(p.NETINFO_ITEM(b,'MOD_COMMAND_OFF_BASE'))
 pad=next(a for a in fs['Q405'].Pads() if a.GetNumber()=='1');bb=pad.GetBoundingBox();bb.Inflate(MM(.2));removed=[]
 for t in list(b.GetTracks()):
  if t.GetNetname()=='MOD_OFF_BASE' and t.GetBoundingBox().Intersects(bb):removed.append(t.m_Uuid.AsString());b.Remove(t);HELD.append(t)
 pad.SetNet(b.FindNet('MOD_COMMAND_OFF_BASE'))
 for r,x,y in [('R985',121.,72.),('R986',125.,72.)]:
  part=d.parts[r];f=p.FootprintLoad(str(HW/'ARDF_2M.pretty'),'R_0603_1608Metric_E3');f.SetReference(r);f.SetValue(part['value']);f.SetFPID(p.LIB_ID('ARDF_2M','R_0603_1608Metric_E3'));co=comps[r];f.SetPath(p.KIID_PATH(co.find('sheetpath').get('tstamps')+co.findtext('tstamps')))
  for fld in f.GetFields():
   if fld.GetName()=='MPN':fld.SetText(part['mpn'])
   if fld.GetName()=='Population':fld.SetText('NORMAL')
  for a in f.Pads():a.SetNet(b.FindNet(part['pins'][a.GetNumber()]))
  f.SetPosition(pt(x,y));f.SetDNP(False);b.Add(f)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b)
 save('command-clamp-correction.json',dict(native_changes={'Q405.1':'MOD_COMMAND_OFF_BASE','R985':'10k NORMAL_OFF to MOD_COMMAND_OFF_BASE','R986':'100k MOD_COMMAND_OFF_BASE to GND'},before_space_current_A=.04446,after_space_current_A_model=9.1e-11,qualification='SPICE model-level benefit; actual SPACE currents remain first-article measurements',removed_routes=removed))
 print('Separate normal-key and emergency command clamps implemented in native sources')
if __name__=='__main__':main()

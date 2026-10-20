#!/usr/bin/python3
"""Audit manufacturer DXF facts; index private reference hashes, never copy them.
Usage: /usr/bin/python3 tools/m6_l2_references.py /path/to/reference-cache
"""
import sys,json,hashlib,math
from pathlib import Path
import pcbnew as p
from m6_l2_design import P,D
URLS={
 'FOXPRO2.asm':'https://df1fo.darc.de/ASM/FOXPRO2.asm',
 'FJTX.asm':'https://df1fo.darc.de/ASM/FJTX.asm',
 'Zeitsteuerung2G.doc':'https://df1fo.darc.de/DOC/Zeitsteuerung2G.doc',
 'esp32.pdf':'https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf',
 '1-footprint.dxf':'https://www.espressif.com/sites/default/files/modules-dxf/ESP32-S3-WROOM-1%20PCB%20Footprint.dxf',
 '1U-footprint.dxf':'https://www.espressif.com/sites/default/files/modules-dxf/ESP32-S3-WROOM-1U%20PCB%20Footprint.dxf',
 'ESP32-S3-WROOM-1U.step':'https://www.espressif.com/sites/default/files/3dmodel/ESP32-S3-WROOM-1U%203D%20Model.STEP',
 'tca9534a.pdf':'https://www.ti.com/lit/ds/symlink/tca9534a.pdf',
 'tca9517.pdf':'https://www.ti.com/lit/ds/symlink/tca9517.pdf',
 'lm66100.pdf':'https://www.ti.com/lit/ds/symlink/lm66100.pdf',
 'sn74lvc2g04.pdf':'https://www.ti.com/lit/ds/symlink/sn74lvc2g04.pdf',
 'rv3032-app-manual.pdf':'https://www.microcrystal.com/fileadmin/Media/Products/RTC/App.Manual/RV-3032-C7_App-Manual.pdf',
 'mmbt3904.pdf':'https://www.onsemi.com/pdf/datasheet/mmbt3904lt1-d.pdf',
 'bss138bk.pdf':'https://assets.nexperia.com/documents/data-sheet/BSS138BK.pdf',
 'bzx84.pdf':'https://assets.nexperia.com/documents/data-sheet/BZX84_SER.pdf',
 'pesd1ivn24.pdf':'https://assets.nexperia.com/documents/data-sheet/PESD1IVN24-A.pdf',
 '10n.pdf':'https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/609/CL10B103KB8NNNC_Spec.pdf',
 'bas316.pdf':'https://assets.nexperia.com/documents/data-sheet/BAS316.pdf',
 'KB3SPRS.pdf':'https://cdn-reichelt.de/documents/datenblatt/C160/KB3SPRS.pdf'}
def rectangles(path):
 lines=path.read_text().splitlines();tokens=list(zip(map(str.strip,lines[::2]),map(str.strip,lines[1::2])))
 start=tokens.index(('2','ENTITIES'));es=[]
 for k,v in tokens[start+1:]:
  if (k,v)==('0','ENDSEC'):break
  if k=='0':es.append([v,[]])
  else:es[-1][1].append((k,v))
 result=[]
 for typ,props in es:
  if typ!='LWPOLYLINE':continue
  xs=[float(v) for k,v in props if k=='10'];ys=[float(v) for k,v in props if k=='20']
  result.append(dict(cx=(max(xs)+min(xs))/2,cy=(max(ys)+min(ys))/2,w=max(xs)-min(xs),h=max(ys)-min(ys)))
 return result
def main():
 cache=Path(sys.argv[1]);sources=[]
 for name,url in URLS.items():
  f=cache/name;sources.append(dict(file=name,url=url,retrieved='2026-10-20',sha256=hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None,access='retrieved locally' if f.exists() else 'Not in local cache; official URL supplied for independent source review. No local file hash claimed.',redistributed=False))
 (D/'source-register.json').write_text(json.dumps(dict(sources=sources,licensing='DF1FO originals are third-party technical references, not MIT project software. Manufacturer CAD/datasheets retain their own rights. No full originals are included.'),indent=2)+'\n')
 b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));fp=next(f for f in b.GetFootprints() if f.GetReference()=='U10');pads={a.GetNumber():a for a in fp.Pads() if a.GetNumber()};reports=[]
 for variant in ['1','1U']:
  rects=rectangles(cache/(variant+'-footprint.dxf'))
  # The drawing has an extra legend rectangle. Select the two14-land rows,
  # then align the actual pin1 centre to the current native pad1 centre.
  rows={}
  for r in rects:
   if abs(r['w']-1.5)<1e-4 and abs(r['h']-.9)<1e-4:rows.setdefault(round(r['cx'],4),[]).append(r)
  rows=sorted((x,rs) for x,rs in rows.items() if len(rs)==14);assert len(rows)==2
  x0=rows[0][0];y0=max(r['cy'] for r in rows[0][1]);a=pads['1'];origin=(p.ToMM(a.GetPosition().x),p.ToMM(a.GetPosition().y));matches=[]
  for i in range(1,41):
   a=pads[str(i)];x,y=map(p.ToMM,a.GetPosition());width,height=map(p.ToMM,a.GetSize());angle=a.GetOrientationDegrees()%180
   if abs(angle-90)<.01:width,height=height,width
   hits=[r for r in rects if math.hypot(origin[0]+r['cx']-x0-x,origin[1]-(r['cy']-y0)-y)<.01 and abs(r['w']-width)<.001 and abs(r['h']-height)<.001]
   assert len(hits)==1,(variant,i,hits);matches.append(dict(pin=i,native_x_mm=x,native_y_mm=y,matched_manufacturer_land=True))
  windows=[r for r in rects if abs(r['w']-.9)<.001 and abs(r['h']-.9)<.001];assert len(windows)==9
  paste=[a for a in fp.Pads() if not a.GetNumber() and a.IsOnLayer(p.F_Paste)];assert len(paste)==9
  for a in paste:
   x,y=map(p.ToMM,a.GetPosition());assert any(math.hypot(origin[0]+r['cx']-x0-x,origin[1]-(r['cy']-y0)-y)<.01 for r in windows)
  reports.append(dict(manufacturer_variant=variant,perimeter_matches=matches,EP_window_count=9,window_size_mm=[.9,.9],EP_envelope_mm=[3.7,3.7]))
 ep=pads['41'];assert tuple(map(p.ToMM,ep.GetSize()))==(3.7,3.7)
 report=dict(status='PASS',source='Separate manufacturer1 and1U DXFs, Espressif combined datasheetv1.8 Fig11-1/11-2',
  comparisons=reports,native_solid_EP_mm=[3.7,3.7],paste_area_mm2=9*.9*.9,paste_fraction=9*.9*.9/(3.7*3.7),
  EP_implementation='Solid copper/continuous mask opening, nine0.9mm paste windows; optional thermal holes omitted. Perimeter lands and paste window centres match both manufacturer drawings. This is an explicit exposed-pad process choice, not identical body geometry.',
  body_mm={'WROOM1':[18,25.5],'WROOM1U':[18,19.2]},pin1='Top-left viewed from component top',physical='NOT_RUN')
 (D/'ESP32-footprint-DXF-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('Two manufacturer DXFs:80 perimeter and18 paste windows match native; EP3.7mm PASS')
if __name__=='__main__':main()

"""Negative controls on actual reviewed STEP/CAM/BOM data."""
import unittest,re,csv,io
import compare as c
class ComparisonNegatives(unittest.TestCase):
 def test_STEP_coordinate_change_rejected(self):
  old=(c.OLD/'hardware/2m/ARDF_2M.3dshapes/E6R2_unified_cooling.step').read_bytes()
  changed=re.sub(rb"(CARTESIAN_POINT\('',\()[^,]+",rb'\g<1>0.123456',old,count=1)
  self.assertNotEqual(old,changed);self.assertNotEqual(c.step(old),c.step(changed))
 def test_per_shape_color_change_rejected(self):
  old=(c.OLD/'hardware/2m/ARDF_2M.3dshapes/E6R2_unified_cooling.step').read_bytes()
  changed=re.sub(rb"(COLOUR_RGB\('',)[^,]+",rb'\g<1>0.123456',old,count=1)
  self.assertNotEqual(old,changed);self.assertNotEqual(c.step(old),c.step(changed))
 def test_Gerber_coordinate_change_rejected(self):
  old=(c.OLD/c.REL/'gerbers/RF2M-F_Cu.gtl').read_bytes()
  changed=re.sub(rb'X(-?\d+)Y',lambda m:b'X'+str(int(m.group(1))+1).encode()+b'Y',old,count=1)
  self.assertNotEqual(old,changed);self.assertNotEqual(c.cam(old),c.cam(changed))
 def test_drill_tool_change_rejected(self):
  old=(c.OLD/c.REL/'gerbers/RF2M-PTH.drl').read_bytes()
  changed=re.sub(rb'(T\d+C)([\d.]+)',lambda m:m.group(1)+str(float(m.group(2))+.1).encode(),old,count=1)
  self.assertNotEqual(old,changed);self.assertNotEqual(c.cam(old),c.cam(changed))
 def test_BOM_component_change_rejected(self):
  name='BOM_BUCK4S.csv';old=(c.OLD/c.REL/name).read_bytes();rows=list(csv.DictReader(io.StringIO((c.NEW/c.REL/name).read_text())))
  next(r for r in rows if r['ref']=='C970')['MPN']='WRONG_COMPONENT'
  text=io.StringIO();w=csv.DictWriter(text,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
  with self.assertRaises(AssertionError):c.entry(name,old,text.getvalue().encode())
if __name__=='__main__':unittest.main(verbosity=2)

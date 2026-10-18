#!/usr/bin/python3
"""Manufacturer-backed SF1206F landing; retains F1 position and both nets."""
import sys
from m6_c1_pcb import *
def main():
 b=Board(True);f=b.f['F1'];f.SetFPID(pcb.LIB_ID('ARDF_CTL','Fuse_Bourns_SF1206F'));f.SetValue('1A 63V fast');cx,cy=xy(f.GetPosition());assert f.GetOrientationDegrees()==0
 for a in f.Pads():
  a.SetSize(pt(1.525,2.2));a.SetPosition(pt(cx+(-1 if a.GetNumber()=='1' else 1)*1.5875,cy));a.SetRoundRectRadiusRatio(.1)
 for g in f.GraphicalItems():
  if g.GetLayer()==pcb.F_CrtYd:g.SetStart(pt(cx-2.6,cy-1.35));g.SetEnd(pt(cx+2.6,cy+1.35))
 io=pcb.PCB_IO_KICAD_SEXPR();io.FootprintSave(str(P/'ARDF_CTL.pretty'),f);b.save();print('F1 manufacturer land spans4.7mm,1.65mm gap,2.2mm width')
if __name__=='__main__':main()

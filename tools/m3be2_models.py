#!/usr/bin/env python3
"""ST-specific dimensional envelope, explicit orientation; not production supplier CAD."""
from m3b_models import box,D

def main():
 # PCB localY becomes VRML -Y. Model is then rotated with footprint180deg.
 body=box((7.8,2.9,11.05),(2.28,.375,7.525),'0.16 0.16 0.16')
 # Bright face marker identifies the drawing face, not a trademark/part marking.
 body+=box((5.5,.05,1.0),(2.28,1.85,11.5),'0.8 0.5 0.1')
 for x in (0,2.28,4.56):body+=box((.88,.63,5.0),(x,0,-.5),'0.65 0.65 0.65')
 (D/'ST_BD140_envelope.wrl').write_text('#VRML V2.0 utf8\n# ST BD140 Rev5 drawing0016114E max body7.8x2.9x11.05mm. Own envelope, NOT supplier CAD.\n# Body bottom2mm above PCB; leads permit trimming. Gold stripe=drawing face toward local-PCB Y; installed180deg gives global+Y.\n'+body)
if __name__=='__main__':main()

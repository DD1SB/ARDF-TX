"""Recompute the unchanged source/via path with the proposed insulating sheet."""
from m5b_e6_common import *
from m5b_e4r1_thermal import solve


def main():
    guard();rows=[]
    for name,plate,cu,loss,timp in [('nominal',18,35,0,.45),('conservative',10,30,4,.65),('poor_pressure',10,30,8,1.)]:
        effective=.000127/(timp*.00064516)
        r,meta=solve(plate=plate,cu=cu,loss=loss,tim_mm=.127,tim_k=effective,step=.2)
        rows.append(dict(name=name,plating_um=plate,copper_um=cu,ineffective_inner_vias=loss,
                         interface_impedance_K_in2_W=timp,effective_TIM_k_W_mK=effective,
                         source_to_bar_K_W=r,meta=meta))
    save('E6-source-path-FVM.json',dict(status='CALCULATED_NOT_MEASURED',
        source='Native E5 source geometry retained; E4R1 translation-invariant FVM',
        solver_sha256=sha(ROOT/'tools/m5b_e4r1_thermal.py'),native_before_E6_sha256=sha(HW/'RF2M.kicad_pcb'),
        interface='BERGQUIST SIL PAD TSP1600 .127mm; effective impedance includes contacts, never add them twice',
        manufacturer_impedance_K_in2_W={'50psi':.45,'25psi':.6,'10psi':.92},
        engineering_margins='Conservative0.65vs0.60@25psi and poor1.00vs0.92@10psi; pressure/flatness not measured',cases=rows))
    alternatives=[]
    for name,mm,k in [('E5_grease_conservative',.15,6.),('KERATHERM_bulk_only_not_contact_qualified',.25,6.5),
                      ('KERATHERM_double_resistance_contact_allowance',.25,3.25),
                      ('KERATHERM_thicker_triple_resistance_allowance',.3,6.5/3)]:
        r,meta=solve(plate=10,cu=30,loss=4,tim_mm=mm,tim_k=k,step=.2)
        alternatives.append(dict(name=name,interface_mm=mm,effective_k_W_mK=k,source_to_bar_K_W=r,
                                 limitation='Assumed contact allowance, not a qualified assembly impedance',meta=meta))
    save('source-interface-alternatives.json',dict(status='SENSITIVITY_NOT_SELECTED_OR_QUALIFIED',
        common_boundary='10um via wall,30um copper,4 ineffective inner vias; standard unfilled E5 geometry',
        alternatives=alternatives,physical='NOT_RUN'))
    print('Source path scenarios',[(x['name'],round(x['source_to_bar_K_W'],3)) for x in rows])
    print('Alternatives',[(x['name'],round(x['source_to_bar_K_W'],3)) for x in alternatives])


if __name__=='__main__':main()

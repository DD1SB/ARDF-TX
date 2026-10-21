"""Integer microsecond Morse scheduling; generated independently of E6's floats.

PARIS dit=round(1200000/WPM), matching controller timing fixture. Standard 1/3/7
element/letter/repeated-word gaps. Finite slots clip at hard boundaries; optional
CW-ID is a separate word. No unearned twenty-percent beacon duty is allowed.
"""
import csv
from fractions import Fraction
from m5b_e6r1_common import *

CODES={'M':'--','O':'---','E':'.','I':'..','S':'...','H':'....','5':'.....',
       'D':'-..','1':'.----','B':'-...','F':'..-.'}

def units(text):
    result=[]
    words=text.split()
    for wi,word in enumerate(words):
        for ci,c in enumerate(word):
            if ci:result.append((3,False,'letter'))
            for si,symbol in enumerate(CODES[c]):
                if si:result.append((1,False,'element'))
                result.append((1 if symbol=='.' else 3,True,symbol))
        result.append((7,False,'word'))
    return result

def schedule(text,wpm,slot_s,cycle_s):
    if not 8<=wpm<=15:raise ValueError('Supported8..15WPM')
    dit=round(1200000/wpm);limit=round(slot_s*1000000);period=round(cycle_s*1000000)
    assert 0<limit<=period
    t=0;rows=[]
    while t<limit:
        for count,mark,kind in units(text):
            end=min(limit,t+count*dit)
            if end<=t:break
            rows.append(dict(start_us=t,end_us=end,state='mark' if mark else 'space',kind=kind))
            t=end
            if t==limit:break
    if period>limit:rows.append(dict(start_us=limit,end_us=period,state='off',kind='inactive_slot'))
    return rows

def stats(text,wpm,slot,cycle):
    s=schedule(text,wpm,slot,cycle);mark=sum(z['end_us']-z['start_us'] for z in s if z['state']=='mark')
    full=units(text);mu=sum(t for t,m,k in full if m);allunits=sum(t for t,m,k in full)
    return dict(identifier=text,WPM=wpm,dit_us=round(1200000/wpm),slot_s=slot,cycle_s=cycle,
        repeating_word_MARK_units=mu,repeating_word_total_units=allunits,
        repeating_word_MARK_fraction=str(Fraction(mu,allunits)),finite_slot_MARK_us=mark,
        finite_slot_SPACE_us=round(slot*1000000)-mark,finite_slot_MARK_fraction=mark/(slot*1000000),
        full_cycle_MARK_fraction=mark/(cycle*1000000),mark_intervals=sum(z['state']=='mark' for z in s))

def main():
    guard();rows=[]
    for wpm in range(8,16):
        for text in ['MOE','MOI','MOS','MOH','MO5','MO','S','MO5 DD1SB']:
            for mode,slot,cycle in [('Classic',60,300),('Sprint',12,60),('Beacon',60,60)]:
                rows.append(dict(mode=mode,**stats(text,wpm,slot,cycle)))
    save('morse-duty.json',dict(integer_timer_Hz=1000000,repeat_gap_units=7,rows=rows,
        CW_ID_policy='Representative DD1SB appended as a word; actual licensed identifier/configuration is authoritative',
        sprint='MOE..MO5 at10/15WPM example; suffixF labels group, not an additional transmitted MorseF',
        boundary='Logical schedule hard clips at SLOT. Interior raised-cosine ramps straddle logical edges, preserving their50percent timings; boundary ramps stay inside SLOT.',physical='NOT_RUN'))
    with (OUT/'morse-duty.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    for t in ['MOE','MOI','MOS','MOH','MO5','MO','S']:
        z=stats(t,12,60,60);print(t,z['repeating_word_MARK_fraction'],z['finite_slot_MARK_fraction'])

if __name__=='__main__':main()

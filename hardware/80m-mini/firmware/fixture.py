#!/usr/bin/env python3
"""Create universal per-unit settings; optionally exchange frames over 3V UART.

No programming, RF arming or hardware activation occurs when generating files.
Serial access requires an explicit subcommand and pyserial, on the bench only.
"""
import argparse, binascii, json, struct
from pathlib import Path
FMT='<I7B4IIIihHH'
ROLES=['slow-MOE','slow-MOI','slow-MOS','slow-MOH','slow-MO5','fast-MOE','fast-MOI','fast-MOS','fast-MOH','fast-MO5','spectator-S','finish-MO']
def crc(data):return binascii.crc_hqx(data,0xffff)
def encode(c):
 role=c['role']; profile=c.get('profile',0);mode=c.get('mode',0)
 identifier=c.get('identifier',role%5 if role<10 else role-5)
 values=[0x314d3830,1,role,mode,profile,c.get('slow_wpm',10),c.get('fast_wpm',15),identifier,*c.get('frequency',[3530000,3550000,3570000,3600000]),c.get('delay_s',60),c.get('run_s',43200),c.get('carrier_ppb',0),c.get('timing_ppm',0),c.get('battery_scale',4500),0]
 data=struct.pack(FMT,*values);return data[:-2]+struct.pack('<H',crc(data[:-2]))
def frame(command,payload=b''):
 data=bytes([0xa5,command,len(payload)])+payload;return data+struct.pack('<H',crc(data))
def exchange(port,command,payload=b''):
 import serial
 with serial.Serial(port,9600,timeout=2) as s:
  s.reset_input_buffer();s.write(frame(command,payload));h=s.read(3)
  if len(h)!=3 or h[:2]!=bytes([0xa5,command|0x80]):raise RuntimeError('No matching reply')
  tail=s.read(h[2]+2)
  if len(tail)!=h[2]+2 or crc(h+tail[:-2])!=int.from_bytes(tail[-2:],'little'):raise RuntimeError('Invalid reply CRC')
  if command!=2 and tail[:-2]!=b'\0':raise RuntimeError('Device rejected command')
  return tail[:-2]
def main():
 ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest='cmd',required=True)
 s=sub.add_parser('fleet');s.add_argument('directory',type=Path)
 s=sub.add_parser('encode');s.add_argument('config',type=Path);s.add_argument('output',type=Path)
 for command in ['read','write','arm','stop']:
  s=sub.add_parser(command);s.add_argument('port')
  if command=='write':s.add_argument('config',type=Path)
 args=ap.parse_args()
 if args.cmd=='fleet':
  args.directory.mkdir(parents=True,exist_ok=True)
  for i,role in enumerate(ROLES):
   c={'role':i,'name':role,'mode':0,'profile':0,'delay_s':60,'run_s':43200}
   p=args.directory/role;p.with_suffix('.json').write_text(json.dumps(c,indent=2)+'\n');p.with_suffix('.bin').write_bytes(encode(c))
 elif args.cmd=='encode':args.output.write_bytes(encode(json.loads(args.config.read_text())))
 elif args.cmd=='write':
  payload=encode(json.loads(args.config.read_text()));exchange(args.port,1,payload)
  if exchange(args.port,2)!=payload:raise RuntimeError('EEPROM readback mismatch')
 else:
  payload=exchange(args.port,{'read':2,'arm':3,'stop':4}[args.cmd]);print(payload.hex())
if __name__=='__main__':main()

"""Independent timed FoxPro2 peer against the compiled C11 implementation.

Vectors and peer framing are calculated here, not with fp_encode. Technical
reference: DF1FO FJTX command descriptions and FOXPRO2 workflows, not copied code.
All simulated RF evidence is test-only; physical interoperability is NOT_RUN.
"""
import ctypes as C
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from fractions import Fraction

HERE=Path(__file__).resolve().parent
def frame(cmd,data,response=False):
    # Explicit XOR of THREE four-bit values plus the direction discriminator.
    checksum=(cmd^(data//16)^(data%16)^(5 if response else 10))%16
    return checksum*4096+cmd*256+data
def wire(word):return [0]+[(word>>n)&1 for n in range(15,-1,-1)]+[1]
def unpack(word,response=True):
    command=(word//256)%16;data=word%256
    if word!=frame(command,data,response):raise ValueError('checksum')
    return command,data

class FoxProSimulator:
    cadence=Fraction(100000,3) # microseconds,30 protocol steps/second
    bit=Fraction(2500,3)
    def __init__(self,lib):self.lib=lib
    def command(self,cmd,data):return self.lib.bridge_command(frame(cmd,data))
    def read(self,index):
        out=self.command(15,index)
        if out<0:raise TimeoutError('no transmitter response')
        cmd,value=unpack(out)
        if cmd!=index:raise ValueError('wrong response register')
        return value
    def step(self):self.lib.bridge_advance(33333)
    def load(self,status):
        for cmd,value in enumerate(status):self.command(cmd,value);self.step()
    def verify(self,status):
        actual=[]
        for i in range(10):actual.append(self.read(i));self.step()
        return actual==status
    def clone(self):return [self.read(i) for i in range(10)]
    def cwid_write(self,values):
        self.command(13,1);self.step()
        for v in values:self.command(14,v);self.step()
    def cwid_read(self):
        self.read(11) # specified reset-to1 side effect
        return [self.read(14) for _ in range(18)]

class FoxPro2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix='m6l2-foxpro-')
        dll=Path(cls.tmp.name)/'foxpro.so'
        subprocess.run(['cc','-std=c11','-Wall','-Wextra','-Werror','-shared','-fPIC',
                        'foxpro2.c','foxpro2_transport.c','test_foxpro2_bridge.c','-o',str(dll)],cwd=HERE,check=True)
        cls.lib=C.CDLL(str(dll));cls.lib.bridge_advance.argtypes=[C.c_uint64];cls.lib.bridge_set_time.argtypes=[C.c_uint64]
        cls.lib.fp_encode.argtypes=[C.c_uint8,C.c_uint8,C.c_bool];cls.lib.fp_encode.restype=C.c_uint16
        cls.lib.fp_decode.argtypes=[C.c_uint16,C.c_bool,C.c_void_p,C.c_void_p]
        cls.lib.fp_esp32_sample_cycles.argtypes=[C.c_uint32];cls.lib.fp_esp32_sample_cycles.restype=C.c_uint32
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def setUp(self):self.lib.bridge_init();self.peer=FoxProSimulator(self.lib)
    def get(self,i):return self.lib.bridge_get(i)
    def receive(self,bits):
        found=[]
        for bit in bits:
            for _ in range(4):
                result=self.lib.bridge_receive(bit)
                if result>=0:found.append(result)
        return found
    def test_01_exact_1200_timing_and_18_bits(self):
        self.assertEqual(self.peer.bit*18,15000)
        self.assertEqual(wire(0xa000),[0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1])
        self.assertEqual(sum(self.lib.fp_esp32_sample_cycles(i) for i in range(4800)),80000000)
        self.assertEqual(self.receive(wire(0xa000)),[0xa000])
    def test_02_all_payloads_and_directions(self):
        for response in [False,True]:
            for cmd in range(16):
                for data in range(256):
                    expected=frame(cmd,data,response)
                    self.assertEqual(self.lib.fp_encode(cmd,data,response),expected)
                    self.assertTrue(self.lib.fp_decode(expected,response,None,None))
                    self.assertFalse(self.lib.fp_decode(expected,not response,None,None))
    def test_03_known_vectors_and_bit_order(self):
        # Independently hand-calculated: A^F^0^B=E;5^B^7^1=8.
        self.assertEqual(frame(15,11),0xef0b);self.assertEqual(frame(11,0x71,True),0x8b71)
        for word in [0x0001,0x8000,0xef0b,0x8b71,0xffff]:
            self.assertEqual(self.receive(wire(word)),[word])
    def test_04_invalid_checksum_and_every_single_bit(self):
        value=frame(11,0x51)
        for bit in range(16):
            self.lib.bridge_command(value^(1<<bit));self.assertEqual(self.peer.read(11),0x71)
        self.assertEqual(self.get(0),16)
    def test_05_missing_stop(self):
        self.assertEqual(self.receive(wire(frame(11,0x51))[:-1]+[0]),[])
        self.assertEqual(self.get(7),1)
    def test_06_incomplete_and_reset(self):
        self.assertEqual(self.receive(wire(frame(11,0x51))[:8]),[])
        self.lib.bridge_reset();self.assertEqual(self.receive(wire(frame(15,11))),[frame(15,11)])
    def test_07_held_low(self):
        self.assertEqual(self.receive([0]*150),[]);self.assertGreater(self.get(7),0)
        self.assertEqual(self.receive([1]*2+wire(frame(15,11))),[frame(15,11)])
    def test_08_stuck_high(self):self.assertEqual(self.receive([1]*150),[])
    def test_09_concurrent_transmitters(self):
        a,b=wire(frame(11,0x51)),wire(frame(11,0x72))
        words=self.receive([x&y for x,y in zip(a,b)])
        self.assertEqual(len(words),1)
        self.lib.bridge_command(words[0]);self.assertNotEqual(self.peer.read(11),0x51)
        # Four checksum bits cannot detect identical concurrent frames.
        self.lib.bridge_init();self.assertEqual(self.receive(a),[frame(11,0x51)])
    def test_10_interrupted_status_load(self):
        self.peer.command(0,72);self.peer.command(1,0x50)
        self.lib.bridge_advance(1000001);self.peer.command(9,90)
        self.assertEqual(self.get(3),0);self.assertGreater(self.get(0),0)
    def test_11_readback_timeout(self):
        self.peer.command(13,19)
        with self.assertRaises(TimeoutError):self.peer.read(14)
    def test_12_expected_cadence_identify(self):
        self.assertEqual(self.peer.read(11),0x71);self.peer.step()
        self.assertEqual(self.peer.read(12),0x15);self.peer.step()
        self.assertEqual(self.peer.read(14),7)
    def test_13_status_load_verify_and_snapshot(self):
        status=[72,0x50,0,1,255,255,255,255,78,90]
        self.peer.load(status);self.assertEqual(self.get(3),1)
        self.assertTrue(self.peer.verify(status))
        # Cross a wall-clock second while reading: one coherent snapshot.
        self.lib.bridge_advance(200000);first=self.peer.read(0)
        self.lib.bridge_advance(250000);self.assertEqual(self.peer.read(1),0x50)
        self.assertEqual(self.peer.read(2),0);self.assertEqual(first,72)
    def test_14_foxid_encodings(self):
        for speed in range(4):
            for modulation in range(4):
                for fox in range(8):
                    value=speed*64+modulation*16+fox
                    self.peer.command(11,value);self.assertEqual(self.peer.read(11),value)
        self.peer.command(11,0xff);self.assertEqual(self.peer.read(11),0xf7)
    def test_15_cwid_roundtrip_and_one_persistence(self):
        payload=[0x0a,20]+list(range(16))
        self.peer.cwid_write(payload);self.assertEqual(self.peer.cwid_read(),payload)
        self.assertEqual(self.get(2),0);self.lib.bridge_advance(500001);self.assertEqual(self.get(2),1)
        self.assertEqual([self.lib.bridge_committed(i) for i in range(1,19)],payload)
    def test_16_cwid_bounds_and_incomplete(self):
        for pointer in [0,19,127,255]:
            self.peer.command(13,pointer);self.peer.command(14,255)
            self.assertEqual(self.get(5),pointer)
        self.peer.cwid_write([0x80]);self.lib.bridge_advance(500001)
        self.assertEqual(self.get(2),0)
    def test_17_eeprom_pointer_increment(self):
        self.assertEqual(self.peer.read(11),0x71);self.assertEqual(self.get(5),1)
        for n in range(18):self.peer.read(14);self.assertEqual(self.get(5),n+2)
        with self.assertRaises(TimeoutError):self.peer.read(14)
        self.assertEqual(self.get(5),19)
    def test_18_read_clone(self):
        for slot in range(4):
            for foxes in [1,5]:
                s=[72,foxes*16,slot*64,1,255,255,255,255,78,90]
                self.peer.load(s);self.assertEqual(self.peer.clone(),s)
    def test_19_invalid_programs(self):
        s=[72,0x50,0,1,255,255,255,255,78,90]
        for index,value in [(0,144),(1,0),(1,0x5a),(2,63),(3,0x81),(3,6),(4,144),(8,90)]:
            bad=s.copy();bad[index]=value;self.peer.load(bad)
            self.assertEqual(self.get(3),0)
    def test_20_unsupported_calibration_and_register(self):
        self.peer.command(12,0)
        with self.assertRaises(TimeoutError):self.peer.read(15)
        self.assertEqual(self.get(1),2);self.assertEqual(self.get(4),0)
    def test_21_unsafe_test_interlocks(self):
        for missing in range(9):
            self.lib.bridge_safety(0x1ff^(1<<missing));self.peer.command(10,16)
        self.assertEqual(self.get(4),0)
        self.lib.bridge_safety(0x1ff);self.peer.command(10,255);self.assertEqual(self.get(4),0)
        self.peer.command(10,17);self.assertEqual(self.get(4),1);self.assertEqual(self.get(6),1)
        self.lib.bridge_advance(30000001);self.assertEqual(self.peer.read(10),0)
    def test_22_reset_discards_transaction(self):
        self.peer.command(11,0x51);self.peer.command(0,72);self.lib.bridge_reset()
        self.lib.bridge_advance(1000000);self.assertEqual(self.peer.read(11),0x71)
        self.assertEqual(self.get(2),0);self.assertEqual(self.get(3),0)
    def test_23_boot_activity_has_no_output(self):
        for b in wire(frame(15,11)):
            for _ in range(4):self.assertEqual(self.lib.bridge_tick(b),0)
    def test_24_unknown_module_and_usb(self):
        for bits in [0,1,0x1ff^2,0x1ff^256]:
            self.lib.bridge_safety(bits);self.peer.command(10,16);self.assertEqual(self.get(4),0)
    def test_25_rtc_phase_and_safety(self):
        self.lib.bridge_advance(333334);self.assertEqual(self.peer.read(13),10)
        self.lib.bridge_safety(1) # armed: configuration cannot change clock or schedule
        self.peer.load([0,0x50,0,1,255,255,255,255,78,90]);self.assertEqual(self.get(3),0)
        self.assertEqual(self.peer.read(0),72)
    def test_26_transport_response_and_turnaround(self):
        self.lib.bridge_select(1)
        levels=[]
        for b in wire(frame(15,11)):
            for _ in range(4):levels.append(self.lib.bridge_tick(b))
        # Stop bit must remain released through request completion.
        self.assertEqual(levels[-4:],[0,0,0,0])
        for _ in range(80):levels.append(self.lib.bridge_tick(1))
        start=next(i for i,sink in enumerate(levels) if sink)
        actual=[1-levels[start+4*i+2] for i in range(18)]
        self.assertEqual(actual,wire(frame(11,0x71,True)))
        self.assertLess(Fraction(start+72,4)*self.peer.bit,self.peer.cadence)
    def test_27_transport_collision(self):
        self.lib.bridge_select(1)
        for b in wire(frame(15,11)):
            for _ in range(4):self.lib.bridge_tick(b)
        for _ in range(80):self.lib.bridge_tick(0)
        self.assertGreater(self.get(8),0)
    def test_28_monotonic_test_deadline_and_live_fault(self):
        self.lib.bridge_safety(0x1ff);self.peer.command(10,17)
        self.lib.bridge_set_time(0);self.lib.bridge_advance(30000001)
        self.assertEqual(self.get(6),0)
        self.peer.command(10,17);self.lib.bridge_safety(0x1ff^32)
        self.lib.bridge_advance(1);self.assertEqual(self.get(6),0)
    def test_29_persistence_rate_limit(self):
        self.peer.command(11,0x51);self.lib.bridge_advance(500001)
        for fox in range(1,8):
            self.peer.command(11,0x50+fox);self.lib.bridge_advance(600000)
        self.assertEqual(self.get(2),1)
        self.lib.bridge_advance(10000000);self.assertEqual(self.get(2),2)

if __name__=='__main__':unittest.main(verbosity=2)

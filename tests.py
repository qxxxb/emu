import unittest
from emu import *
import io


class TestIns(unittest.TestCase):
    def test_from_bytes(self):
        exp_bytes = b'\x08\xe0:'
        ins = Ins.from_bytes(exp_bytes)
        exp_ins = Ins.from_values(Op.ADDI, Cond.UN, 14, 0, 58)
        self.assertEqual(ins, exp_ins)


class TestEmu(unittest.TestCase):
    def test_add(self):
        emu = Emu()
        emu.mem[1] = 5
        emu.mem[2] = 7
        ins = Ins.from_values(Op.ADD, Cond.UN, 3, 1, 2)
        emu.execute(ins)
        self.assertEqual(emu.mem[3], 12)

        # Almost overflow
        emu = Emu()
        emu.mem[1] = 0o77 - 5
        emu.mem[2] = 5
        ins = Ins.from_values(Op.ADD, Cond.UN, 3, 1, 2)
        emu.execute(ins)
        self.assertEqual(emu.mem[3], 0o77)

        # Overflow
        emu = Emu()
        emu.mem[1] = 0o77 - 5
        emu.mem[2] = 7
        ins = Ins.from_values(Op.ADD, Cond.UN, 3, 1, 2)
        emu.execute(ins)
        self.assertEqual(emu.mem[3], 1)

    def test_addi(self):
        emu = Emu()
        emu.mem[1] = 5
        ins = Ins.from_values(Op.ADDI, Cond.UN, 3, 1, 7)
        emu.execute(ins)
        self.assertEqual(emu.mem[3], 12)

    def test_sub(self):
        emu = Emu()
        emu.mem[1] = 13
        emu.mem[2] = 8
        ins = Ins.from_values(Op.SUB, Cond.UN, 3, 1, 2)
        emu.execute(ins)
        self.assertEqual(emu.mem[3], 5)

        # Almost underflow
        emu = Emu()
        emu.mem[1] = 13
        emu.mem[2] = 13
        ins = Ins.from_values(Op.SUB, Cond.UN, 3, 1, 2)
        emu.execute(ins)
        self.assertEqual(emu.mem[3], 0)

        # Underflow
        emu = Emu()
        emu.mem[1] = 13
        emu.mem[2] = 14
        ins = Ins.from_values(Op.SUB, Cond.UN, 3, 1, 2)
        emu.execute(ins)
        self.assertEqual(emu.mem[3], from_int(-1))

    def test_cmp_eq(self):
        emu = Emu()
        emu.mem[1] = 5
        emu.mem[2] = 7
        ins = Ins.from_cmp(Cond.UN, CmpType.RA_RB, Cm.EQ, 1, 2)
        emu.execute(ins)
        self.assertFalse(emu.cf)

        emu = Emu()
        emu.mem[1] = 5
        ins = Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, 1, 7)
        emu.execute(ins)
        self.assertFalse(emu.cf)

        emu = Emu()
        emu.mem[1] = 5
        emu.mem[2] = 5
        ins = Ins.from_cmp(Cond.UN, CmpType.RA_RB, Cm.EQ, 1, 2)
        emu.execute(ins)
        self.assertTrue(emu.cf)

    def test_cmp_sl_pos_pos(self):
        emu = Emu()
        emu.mem[1] = 5
        emu.mem[2] = 7
        ins = Ins.from_cmp(Cond.UN, CmpType.RA_RB, Cm.SL, 1, 2)
        emu.execute(ins)
        self.assertTrue(emu.cf)

        emu = Emu()
        emu.mem[1] = 5
        emu.mem[2] = 5
        ins = Ins.from_cmp(Cond.UN, CmpType.RA_RB, Cm.SL, 1, 2)
        emu.execute(ins)
        self.assertFalse(emu.cf)

    def test_cmp_sl_pos_neg(self):
        emu = Emu()
        emu.mem[1] = 5
        emu.mem[2] = from_int(-7)
        ins = Ins.from_cmp(Cond.UN, CmpType.RA_RB, Cm.SL, 1, 2)
        emu.execute(ins)
        self.assertFalse(emu.cf)

        emu = Emu()
        emu.mem[1] = from_int(-5)
        emu.mem[2] = 5
        ins = Ins.from_cmp(Cond.UN, CmpType.RA_RB, Cm.SL, 1, 2)
        emu.execute(ins)
        self.assertTrue(emu.cf)

    def test_cmp_sl_neg_neg(self):
        emu = Emu()
        emu.mem[1] = from_int(-5)
        emu.mem[2] = from_int(-7)
        ins = Ins.from_cmp(Cond.UN, CmpType.RA_RB, Cm.SL, 1, 2)
        emu.execute(ins)
        self.assertFalse(emu.cf)

        emu = Emu()
        emu.mem[1] = from_int(-13)
        emu.mem[2] = from_int(-5)
        ins = Ins.from_cmp(Cond.UN, CmpType.RA_RB, Cm.SL, 1, 2)
        emu.execute(ins)
        self.assertTrue(emu.cf)

    def test_op_cond(self):
        emu = Emu()
        emu.mem[1] = 5
        emu.mem[2] = 5
        ins_cmp = Ins.from_cmp(Cond.UN, CmpType.RA_RB, Cm.EQ, 1, 2)
        emu.execute(ins_cmp)

        # Should execute
        emu.mem[3] = 5
        emu.mem[4] = 7
        ins_un = Ins.from_values(Op.ADD, Cond.UN, 5, 3, 4)
        emu.execute(ins_un)

        # Should execute
        emu.mem[6] = 5
        emu.mem[7] = 7
        ins_tr = Ins.from_values(Op.ADD, Cond.TR, 8, 6, 7)
        emu.execute(ins_tr)

        # Should not execute
        emu.mem[9] = 5
        emu.mem[10] = 7
        ins_fa = Ins.from_values(Op.ADD, Cond.FA, 11, 9, 10)
        emu.execute(ins_fa)

        self.assertEqual(emu.mem[5], 12)
        self.assertEqual(emu.mem[8], 12)
        self.assertEqual(emu.mem[11], 0)

    def test_sar(self):
        self.assertEqual(sar(0b001011, 0), 0b001011)
        self.assertEqual(sar(0b001011, 1), 0b000101)
        self.assertEqual(sar(0b001011, 2), 0b000010)
        self.assertEqual(sar(0b001011, 3), 0b000001)
        self.assertEqual(sar(0b001011, 4), 0b000000)
        self.assertEqual(sar(0b001011, 5), 0b000000)
        self.assertEqual(sar(0b001011, 6), 0b000000)
        self.assertEqual(sar(0b001011, 7), 0b000000)

        self.assertEqual(sar(0b101011, 0), 0b101011)
        self.assertEqual(sar(0b101011, 1), 0b110101)
        self.assertEqual(sar(0b101011, 2), 0b111010)
        self.assertEqual(sar(0b101011, 3), 0b111101)
        self.assertEqual(sar(0b101011, 4), 0b111110)
        self.assertEqual(sar(0b101011, 5), 0b111111)
        self.assertEqual(sar(0b101011, 6), 0b111111)
        self.assertEqual(sar(0b101011, 7), 0b111111)

    def test_rol(self):
        self.assertEqual(rol(0b001011, 0), 0b001011)
        self.assertEqual(rol(0b001011, 1), 0b100101)
        self.assertEqual(rol(0b001011, 2), 0b110010)
        self.assertEqual(rol(0b001011, 3), 0b011001)
        self.assertEqual(rol(0b001011, 4), 0b101100)
        self.assertEqual(rol(0b001011, 5), 0b010110)
        self.assertEqual(rol(0b001011, 6), 0b001011)
        self.assertEqual(rol(0b001011, 7), 0b100101)

    def test_shi(self):
        # SHL
        emu = Emu()
        emu.mem[1] = 3
        ins = Ins.from_shi(Cond.UN, 2, 1, ShiType.SHL, 2)
        emu.execute(ins)
        self.assertEqual(emu.mem[2], 3 << 2)

        # SHR
        emu = Emu()
        emu.mem[1] = 0b101110
        ins = Ins.from_shi(Cond.UN, 2, 1, ShiType.SHR, 2)
        emu.execute(ins)
        self.assertEqual(emu.mem[2], 0b001011)

        # SAR
        emu = Emu()
        emu.mem[1] = 0b101110
        ins = Ins.from_shi(Cond.UN, 2, 1, ShiType.SAR, 3)
        emu.execute(ins)
        self.assertEqual(emu.mem[2], sar(0b101110, 3))

        # ROL
        emu = Emu()
        emu.mem[1] = 0b101110
        ins = Ins.from_shi(Cond.UN, 2, 1, ShiType.ROL, 4)
        emu.execute(ins)
        self.assertEqual(emu.mem[2], rol(0b101110, 4))

    def test_ld(self):
        # LD without offset
        emu = Emu()
        emu.mem[1] = 3
        emu.mem[3] = 7
        ins = Ins.from_values(Op.LD, Cond.UN, 2, 1, 0)
        emu.execute(ins)
        self.assertEqual(emu.mem[2], 7)

        # LD with offset
        emu = Emu()
        emu.mem[1] = 5
        emu.mem[3] = 7
        ins = Ins.from_values(Op.LD, Cond.UN, 2, 1, from_int(-2))
        emu.execute(ins)
        self.assertEqual(emu.mem[2], 7)

    def test_st(self):
        # ST without offset
        emu = Emu()
        emu.mem[1] = 19
        emu.mem[3] = 2
        ins = Ins.from_values(Op.ST, Cond.UN, 1, 3, 0)
        emu.execute(ins)
        self.assertEqual(emu.mem[2], 19)

        # ST with offset
        emu = Emu()
        emu.mem[1] = 19
        emu.mem[3] = 7
        ins = Ins.from_values(Op.ST, Cond.UN, 1, 3, from_int(-5))
        emu.execute(ins)
        self.assertEqual(emu.mem[2], 19)

    def test_fm(self):
        # Unsigned, 0 fractional bits
        emu = Emu()
        emu.mem[1] = 20
        emu.mem[2] = 5
        ins = Ins.from_fm(Cond.UN, 1, 2, FmType.U, 0)
        emu.execute(ins)
        self.assertEqual(emu.mem[1], (20 * 5) & 0b111111)

        # Unsigned, 3 fractional bits
        emu = Emu()
        emu.mem[1] = 20
        emu.mem[2] = 5
        ins = Ins.from_fm(Cond.UN, 1, 2, FmType.U, 3)
        emu.execute(ins)
        self.assertEqual(emu.mem[1], ((20 * 5) >> 3) & 0b111111)

        # Signed, 0 fractional bits
        emu = Emu()
        emu.mem[1] = 20
        emu.mem[2] = 5
        ins = Ins.from_fm(Cond.UN, 1, 2, FmType.S, 0)
        emu.execute(ins)
        self.assertEqual(emu.mem[1], (20 * 5) & 0b111111)

        # Signed, 3 fractional bits
        emu = Emu()
        emu.mem[1] = 20
        emu.mem[2] = 5
        ins = Ins.from_fm(Cond.UN, 1, 2, FmType.S, 3)
        emu.execute(ins)
        self.assertEqual(emu.mem[1], sar((20 * 5), 3, 12) & 0b111111)

        # Signed, 9 fractional bits
        emu = Emu()
        emu.mem[1] = 0o77
        emu.mem[2] = 0o77
        ins = Ins.from_fm(Cond.UN, 1, 2, FmType.S, 9)
        emu.execute(ins)
        self.assertEqual(emu.mem[1], sar((0o77 * 0o77), 9, 12) & 0b111111)

    def test_control_flow(self):
        emu = Emu()
        emu.mem[1] = 33
        emu.mem[2] = 44
        emu.tape = Tape.from_inss([
            Ins.from_values(Op.ADD, Cond.UN, 14, 0, 58),  # 0
            Ins.from_values(Op.ADD, Cond.UN, 15, 0, 0),  # 1
            Ins.from_values(Op.LBL, Cond.UN, 16, 3, 0),  # 2
            Ins.from_values(Op.LBL, Cond.UN, 8, 9, 0),  # 3
            Ins.from_values(Op.ADD, Cond.UN, 12, 0, 56),  # 4
            Ins.from_values(Op.JDN, Cond.UN, 16, 5, 1),  # 5 -->
            Ins.from_values(Op.ADD, Cond.UN, 13, 0, 0),  # 6
            Ins.from_values(Op.LBL, Cond.UN, 16, 5, 2),  # 7
            Ins.from_values(Op.ADD, Cond.UN, 11, 0, 0),  # 8
            Ins.from_values(Op.ADD, Cond.UN, 16, 0, 0),  # 9
            Ins.from_values(Op.LBL, Cond.UN, 16, 5, 33),  # 10 <--
            Ins.from_values(Op.JUP, Cond.UN, 10, 0, 2),  # 11 -->
            Ins.from_values(Op.ADD, Cond.UN, 18, 0, 0),  # 12
            Ins.from_values(Op.ADD, Cond.UN, 19, 0, 0),  # 13
            Ins.from_values(Op.ADD, Cond.UN, 20, 0, 0),  # 14
            Ins.from_values(Op.LBL, Cond.UN, 10, 0, 44),  # 15 <--
            Ins.from_values(Op.ADD, Cond.UN, 21, 0, 0),  # 16
            Ins.invalid(),  # 17
            Ins.from_values(Op.ADD, Cond.UN, 22, 0, 0),  # 18
            Ins.from_values(Op.ADD, Cond.UN, 23, 0, 0),  # 19
        ])
        inss = emu.run(log_inss=True)

        self.assertEqual(
            inss,
            [0, 1, 2, 3, 4, 5, 11, 16, 17]
        )

    def test_jup_vs_jdn(self):
        emu = Emu()
        emu.mem[63] = 33
        emu.tape = Tape.from_inss([
            Ins.from_values(Op.ADD, Cond.UN, 10, 0, 0),  # 0
            Ins.from_values(Op.ADD, Cond.UN, 10, 0, 0),  # 1
            Ins.from_values(Op.LBL, Cond.UN, 16, 3, 33),  # 2
            Ins.from_values(Op.ADD, Cond.UN, 10, 0, 0),  # 3
            Ins.from_values(Op.ADD, Cond.UN, 10, 0, 0),  # 4
            Ins.from_values(Op.ADD, Cond.UN, 10, 0, 0),  # 5
            Ins.from_values(Op.JDN, Cond.UN, 16, 3, 63),  # 6 -->
            Ins.from_values(Op.ADD, Cond.UN, 10, 0, 0),  # 7
            Ins.from_values(Op.ADD, Cond.UN, 10, 0, 0),  # 8
            Ins.from_values(Op.ADD, Cond.UN, 10, 0, 0),  # 9
            Ins.from_values(Op.LBL, Cond.UN, 16, 3, 33),  # 10 <--
            Ins.invalid(),  # 11
        ])
        inss = emu.run(log_inss=True)

        self.assertEqual(
            inss,
            [0, 1, 2, 3, 4, 5, 6, 11]
        )

    def test_io_serial_write(self):
        emu = Emu()
        out = io.StringIO()

        # TODO: Broken
        emu.out = out

        emu.mem[1] = 0o12
        ins = Ins.from_io(Cond.UN, 0, IoDevice.SERIAL_WRITE, 1)
        emu.execute(ins)

        output = out.getvalue()
        self.assertEqual(output, 'A')

    def test_io_clock(self):
        emu = Emu()
        out = io.StringIO()
        emu.out = out

        # Just check that these run properly for now
        ins = Ins.from_io(Cond.UN, 1, IoDevice.CLOCK_LO_CS, 0)
        emu.execute(ins)
        ins = Ins.from_io(Cond.UN, 1, IoDevice.CLOCK_HI_CS, 0)
        emu.execute(ins)


if __name__ == '__main__':
    unittest.main()

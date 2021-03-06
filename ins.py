from Crypto.Util.number import bytes_to_long, long_to_bytes
from enum import Enum


class Op(Enum):
    '''OPC op'''
    ADD = 0o000
    ADDI = 0o001  # Add immediate
    SUB = 0o002
    CMP = 0o003
    OR = 0o004
    ORI = 0o005
    XOR = 0o006
    XORI = 0o007
    AND = 0o010
    ANDI = 0o011
    SHI = 0o012  # Shift/Rotate by immediate
    SHL = 0o013  # Shift left
    SHR = 0o014  # Shift right
    LD = 0o015  # Load
    ST = 0o016  # Store
    LBL = 0o017  # Label
    JUP = 0o020  # Jump upwards
    JDN = 0o021  # Jump downwards
    IO = 0o022
    FM = 0o023  # Fixed-point multiply
    HLT = 0o024  # Halt


class Cond(Enum):
    '''OPC condition'''
    UN = 0  # Unconditional
    TR = 1  # When cf is true
    FA = 2  # When cf is false


class CmpType(Enum):
    '''Comparison types'''
    RA_RB = 0o0
    RB_RA = 0o1
    RA_IB = 0o2
    IA_RB = 0o3


class Cm(Enum):
    '''Comparison mnemonics'''
    TR = 0o0  # True
    FA = 0o1  # False
    EQ = 0o2  # Equal
    NE = 0o3  # Not Equal
    SL = 0o4  # Signed less than
    SG = 0o5  # Signed greater than
    UL = 0o6  # Unsigned less than
    UG = 0o7  # Unsigned greater than


class ShiType(Enum):
    '''Shift/rotate by immediate variants'''
    SHLI = 0o0  # Logical left shift
    SHRI = 0o1  # Logical right shift
    SARI = 0o2  # Arithmetic right shift
    ROLI = 0o3  # Rotate


class FmType(Enum):
    '''Fixed-point multiplication variants'''
    U = 0o0  # Signed
    S = 0o2  # Unsigned


class IoDevice(Enum):
    '''Io device (specified by ix)'''
    SERIAL_INCOMING = 0o000
    SERIAL_READ = 0o001
    SERIAL_WRITE = 0o002
    CLOCK_LO_CS = 0o003
    CLOCK_HI_CS = 0o004
    ENET_INCOMING = 0o010
    ENET_RECV = 0o011
    ENET_SEND = 0o012
    ENET_CONN_CTRL = 0o013
    MEM_ADDR_HI = 0o020
    MEM_ADDR_MID = 0o021
    MEM_ADDR_LO = 0o022
    MEM_READ = 0o023
    MEM_WRITE = 0o024
    GPU_X = 0o025
    GPU_Y = 0o026
    GPU_DRAW = 0o027
    DPAD = 0o030


class Ins:
    '''
    Instruction: op, condition, A, B, C

    Each instruction is 24 bits.
    - 4 parts that are 6 bits each:
        - OPC, A, B, C
    - OPC broken into op and condition
    '''

    def check(self):
        '''Check the instruction to make sure the fields within bounds'''
        assert 0 <= self.op.value < 21
        assert 0 <= self.cond.value < 3
        assert 0 <= self.a < 64
        assert 0 <= self.b < 64
        assert 0 <= self.c < 64

    @classmethod
    def from_values(cls, op, cond, a, b, c):
        ans = cls()
        ans.op, ans.cond = op, cond
        ans.a, ans.b, ans.c = a, b, c
        ans.check()
        return ans

    def as_values(self):
        return (self.op, self.cond, self.a, self.b, self.c)

    @classmethod
    def halt(cls):
        ans = cls()
        ans.op, ans.cond = Op.HLT, Cond.UN
        ans.a, ans.b, ans.c = 0, 0, 0
        ans.check()
        return ans

    @classmethod
    def from_cmp(cls, cond, cmp_type, cm, a, b):
        ans = cls()
        ans.op = Op.CMP
        ans.cond = cond
        ans.a = (cmp_type.value << 3) + cm.value
        # Not a mistake, the vars `a` and `b` go to `b` and `c`
        ans.b, ans.c = a, b
        ans.check()
        return ans

    def as_cmp(self):
        assert self.op == Op.CMP
        cmp_type = CmpType(self.a >> 3)
        cm = Cm(self.a & 0b111)
        return (cmp_type, cm, self.b, self.c)

    @classmethod
    def from_shi(cls, cond, rd, ra, shi_type, ib):
        ans = cls()
        ans.op = Op.SHI
        ans.cond = cond
        ans.a = rd
        ans.b = ra
        ans.c = (shi_type.value << 3) + ib
        assert 0 <= ib < 8
        ans.check()
        return ans

    def as_shi(self):
        assert self.op == Op.SHI
        rd, ra = self.a, self.b
        shi_type = ShiType(self.c >> 3)
        ib = self.c & 0b111
        return (shi_type, rd, ra, ib)

    @classmethod
    def from_fm(cls, cond, rd, ra, fm_type, pr):
        ans = cls()
        ans.op = Op.FM
        ans.cond = cond
        ans.a = rd
        ans.b = ra
        ans.c = (fm_type.value << 4) + pr
        assert 0 <= pr < 16
        ans.check()
        return ans

    def as_fm(self):
        assert self.op == Op.FM
        rd, ra = self.a, self.b
        fm_type = FmType(self.c >> 4)
        pr = self.c & 0b1111
        return (fm_type, pr, rd, ra)

    def partial_jump_key(self):
        assert self.op in {Op.LBL, Op.JDN, Op.JUP}
        return (64 * self.a) + self.b

    def label_key(self):
        assert self.op == Op.LBL
        return (self.partial_jump_key(), self.c)

    @classmethod
    def from_io(cls, cond, rd, ix, rs):
        ans = cls()
        ans.op = Op.IO
        ans.cond = cond
        ans.a = rd
        ans.b = ix.value
        ans.c = rs
        ans.check()
        return ans

    def as_io(self):
        assert self.op == Op.IO
        rd, ix, rs = self.a, self.b, self.c
        ix = IoDevice(ix)
        return (rd, ix, rs)

    @classmethod
    def from_bytes(cls, ins_bytes):
        ans = cls()
        n = bytes_to_long(ins_bytes)

        def get_part(n, i):
            '''Get 6-bit part at i starting at MSB'''
            i = 4 - (i + 1)
            i *= 6
            mask = 0b111111 << i
            ans = n & mask
            return ans >> i

        opc = get_part(n, 0)
        ans.a = get_part(n, 1)
        ans.b = get_part(n, 2)
        ans.c = get_part(n, 3)

        # If opc is 0, invalid instruction and halt the computer
        # Otherwise:
        # opc = 21*cond + op + 1
        if opc == 0:
            return Ins.halt()
        else:
            # opc - 1 = 21*cond + op
            # imm = 21*cond + op
            imm = opc - 1
            op = imm % 21
            cond = imm // 21

            ans.op = Op(op)
            ans.cond = Cond(cond)

        ans.check()
        return ans

    def to_bytes(self):
        opc = (self.cond.value * 21) + self.op.value + 1
        ans = opc << (6 * 3) | self.a << (6 * 2) | self.b << 6 | self.c
        return long_to_bytes(ans)

    def __repr__(self):
        return str(self.as_values())

    def __eq__(self, other):
        return self.as_values() == other.as_values()

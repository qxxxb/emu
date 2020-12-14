import base64
import logging
from ins import *
import sys
from string import digits, ascii_uppercase
import pickle
import time


# Whether save the machine state when the key is requested
make_pickle = False


class Tape:
    '''
    Tape is just a looped array of instructions.
    '''

    @classmethod
    def from_inss(cls, inss):
        '''Create tape from instructions'''
        ans = cls()
        ans.data = inss
        return ans

    @classmethod
    def from_bytes(cls, rom):
        ans = cls()
        # Each instruction is 24 bits, which is 3 bytes
        ans.data = []
        for i in range(0, len(rom), 3):
            ins_bytes = rom[i: i + 3]
            ans.data.append(Ins.from_bytes(ins_bytes))

        return ans

    def __getitem__(self, i):
        return self.data[i]

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return str(self.data)


class Mem:
    '''
    Array of 64 6-bit elements.
    '''

    def __init__(self):
        self.data = [0] * 64

    def __getitem__(self, i):
        assert 0 <= self.data[i] < 64
        return self.data[i]

    def __setitem__(self, i, v):
        assert 0 <= v < 64
        if i != 0:
            self.data[i] = v

    def __len__(self):
        return len(self.data)


def twos_comp(n, bits=6):
    neg = n ^ Emu.mask
    return (neg + 1) & Emu.mask


def to_int(n, bits=6):
    '''Turn a two's complement number into a Python int'''
    if (n & (1 << (bits - 1))) != 0:
        n = n - (1 << bits)
    return n


def bit_string(n, bits=6):
    return format(n % (1 << bits), '0{}b'.format(bits))


def from_int(n, bits=6):
    '''Turn a Python int to a two''s complement number'''
    return int(bit_string(n), 2)


def sar(n, d, bits=6):
    '''Arithmetic right shift'''
    sign = n & (1 << (bits - 1))
    if sign == 0:
        return n >> d
    else:
        inv_s = max(bits - d, 0)
        sign_mask = (1 << bits) - (1 << inv_s)
        return (n >> d) | sign_mask


def rol(n, d, bits=6):
    '''Rotate bits left'''
    s = bit_string(n)
    d = d % bits
    s = s[-d:] + s[:-d]
    return int(s, 2)


# `x` is a placeholder for an invalid character
serial_dict = digits + ascii_uppercase + ' +-*/<=>()[]{}#$_?|^&!~,.:\nx'


def chr_from_serial(n):
    return serial_dict[n]


def serial_from_chr(c):
    return serial_dict.index(c)


class Emu:
    mask = 0b111111

    def __init__(self):
        self.mem = Mem()
        self.pc = 0
        self.halted = False
        self.cf = False
        self.clock = 0
        self.buffer = ''

        # For some reason, pickle can't work with file streams
        if not make_pickle:
            self.out = sys.stdout

    @classmethod
    def from_filename(cls, filename):
        ans = cls()
        s = open(filename).read().strip()
        s = base64.b64decode(s)
        ans.tape = Tape.from_bytes(s)
        return ans

    # Ops

    def op_inv(self, ins):
        logging.warning('Invalid instruction')
        self.halted = True

    # Arithmetic and logic

    def op_add(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.mem[rd] = (self.mem[ra] + self.mem[rb]) & Emu.mask

    def op_addi(self, ins):
        rd, ra, ib = ins.a, ins.b, ins.c
        self.mem[rd] = (self.mem[ra] + ib) & Emu.mask

    def op_sub(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.mem[rd] = (self.mem[ra] + twos_comp(self.mem[rb])) & Emu.mask

    def op_or(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.mem[rd] = (self.mem[ra] | twos_comp(self.mem[rb])) & Emu.mask

    def op_ori(self, ins):
        rd, ra, ib = ins.a, ins.b, ins.c
        self.mem[rd] = (self.mem[ra] | ib) & Emu.mask

    def op_xor(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.mem[rd] = (self.mem[ra] ^ twos_comp(self.mem[rb])) & Emu.mask

    def op_xori(self, ins):
        rd, ra, ib = ins.a, ins.b, ins.c
        self.mem[rd] = (self.mem[ra] ^ ib) & Emu.mask

    def op_and(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.mem[rd] = (self.mem[ra] & twos_comp(self.mem[rb])) & Emu.mask

    def op_andi(self, ins):
        rd, ra, ib = ins.a, ins.b, ins.c
        self.mem[rd] = (self.mem[ra] & ib) & Emu.mask

    def op_shl(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.mem[rd] = (self.mem[ra] << self.mem[rb]) & Emu.mask

    def op_shr(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.mem[rd] = (self.mem[ra] >> self.mem[rb]) & Emu.mask

    # Comparison

    def op_cmp(self, ins):
        (cmp_type, cm, a, b) = ins.as_cmp()

        # Determine left and right sides of comparison
        if cmp_type == CmpType.RA_RB:
            left = self.mem[a]
            right = self.mem[b]
        elif cmp_type == CmpType.RB_RA:
            left = self.mem[b]
            right = self.mem[a]
        elif cmp_type == CmpType.RA_IB:
            left = self.mem[a]
            right = b
        elif cmp_type == CmpType.IA_RB:
            left = a
            right = self.mem[b]

        # Do comparison
        if cm == Cm.TR:
            self.cf = True
        elif cm == Cm.FA:
            self.cf = False
        elif cm == Cm.EQ:
            self.cf = left == right
        elif cm == Cm.NE:
            self.cf = left != right
        elif cm == Cm.SL:
            self.cf = to_int(left) < to_int(right)
        elif cm == Cm.SG:
            self.cf = to_int(left) > to_int(right)
        elif cm == Cm.UL:
            self.cf = left < right
        elif cm == Cm.UG:
            self.cf = left > right
        else:
            raise ValueError('Unhandled cm: {}'.format(cm))

    def op_shi(self, ins):
        (shi_type, rd, ra, ib) = ins.as_shi()

        if shi_type == ShiType.SHL:
            self.mem[rd] = (self.mem[ra] << ib) & Emu.mask
        elif shi_type == ShiType.SHR:
            self.mem[rd] = (self.mem[ra] >> ib) & Emu.mask
        elif shi_type == ShiType.SAR:
            self.mem[rd] = (sar(self.mem[ra], ib)) & Emu.mask
        elif shi_type == ShiType.ROL:
            self.mem[rd] = (rol(self.mem[ra], ib)) & Emu.mask
        else:
            raise ValueError('Unhandled shi_type: {}'.format(shi_type))

    def op_ld(self, ins):
        rd, ra, ib = ins.a, ins.b, ins.c
        rs = (self.mem[ra] + ib) & Emu.mask
        self.mem[rd] = self.mem[rs]

    def op_st(self, ins):
        rs, ra, ib = ins.a, ins.b, ins.c
        rd = (self.mem[ra] + ib) & Emu.mask
        self.mem[rd] = self.mem[rs]

    def op_fm(self, ins):
        (fm_type, pr, rd, ra) = ins.as_fm()

        # 12 bit buffer
        ans = (self.mem[rd] * self.mem[ra]) & 0o7777
        if fm_type == FmType.U:
            ans = ans >> pr
        else:
            ans = sar(ans, pr, bits=12)

        # Reduce back to 6 bits
        ans = ans & Emu.mask
        self.mem[rd] = ans

    def op_lbl(self, ins):
        # Do nothing
        pass

    def op_jup(self, ins, reverse=False):
        key = (ins.partial_jump_key(), self.mem[ins.c])

        # Search for the label matching key
        start = self.pc
        i = start
        while True:
            if reverse:
                i = (i + 1) % len(self.tape)
            else:
                i = (i - 1) % len(self.tape)

            if i == start:
                raise ValueError('Couldn''t find label: {}'.format(key))

            ch_ins = self.tape[i]  # Check instruction
            if ch_ins.op == Op.LBL and \
                    self.should_execute(ch_ins) and \
                    ch_ins.label_key() == key:
                self.pc = i
                return

    def op_jdn(self, ins):
        self.op_jup(ins, reverse=True)

    def op_io(self, ins):
        (rd, ix, rs) = ins.as_io()
        if ix == IoDevice.SERIAL_INCOMING:
            if make_pickle:
                # After printing the mandelprot, it will ask for a key.
                # Here, we save the machine state here so we can analyze it
                # more closely.
                with open('emu_state.pkl', 'wb') as f:
                    pickle.dump(emu, f)

            # Read more input if we don't have any in the buffer
            while len(self.buffer) == 0:
                s = input('> ')
                self.buffer += s

            # Send the length of buffer
            self.mem[rd] = from_int(len(self.buffer)) & Emu.mask
        elif ix == IoDevice.SERIAL_READ:
            # Read more input if we don't have any in the buffer
            while len(self.buffer) == 0:
                s = input('> ')
                self.buffer += s

            # Pop the first char and send it
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            self.mem[rd] = from_int(serial_from_chr(c)) & Emu.mask
        elif ix == IoDevice.SERIAL_WRITE:
            c = chr_from_serial(self.mem[rs])

            if make_pickle:
                out = sys.stdout
            else:
                out = self.out

            out.write(c)
            out.flush()
        elif ix == IoDevice.CLOCK_LO_CS:
            ans = self.clock & 0o77  # Lower 6 bits of clock
            self.mem[rd] = ans
        elif ix == IoDevice.CLOCK_HI_CS:
            # Upper 6 bits of clock
            ans = self.clock & 0o7700
            ans = ans >> 6
            self.mem[rd] = ans
        else:
            logging.warning('Unknown IO device')
            self.halted = True

    op_switch = {
        Op.INV: op_inv,
        Op.ADD: op_add,
        Op.ADDI: op_addi,
        Op.SUB: op_sub,
        Op.OR: op_or,
        Op.ORI: op_ori,
        Op.XOR: op_xor,
        Op.XORI: op_xori,
        Op.AND: op_and,
        Op.ANDI: op_andi,
        Op.SHL: op_shl,
        Op.SHR: op_shr,
        Op.CMP: op_cmp,
        Op.SHI: op_shi,
        Op.LD: op_ld,
        Op.ST: op_st,
        Op.FM: op_fm,
        Op.LBL: op_lbl,
        Op.JUP: op_jup,
        Op.JDN: op_jdn,
        Op.IO: op_io,
    }

    def should_execute(self, ins):
        return \
            (ins.cond == Cond.UN) or \
            (ins.cond == Cond.TR and self.cf) or \
            (ins.cond == Cond.FA and not self.cf)

    def execute(self, ins):
        if self.should_execute(ins):
            if ins.op in Emu.op_switch:
                op_func = Emu.op_switch[ins.op]
                op_func(self, ins)
            else:
                raise ValueError('Unhandled op: {}'.format(ins.op))

    def run(self, log_inss=False):
        if log_inss:
            # Keep a log of instructions executed
            inss_log = []

        start = time.time()
        self.clock = 0

        while not self.halted:
            ins = self.tape[self.pc]

            if log_inss:
                inss_log.append(self.pc)

            self.execute(ins)
            self.pc = (self.pc + 1) % len(self.tape)  # Tape is looped

            now = time.time()
            elapsed = now - start
            elapsed = round(elapsed, 2)
            elapsed = int(elapsed * 100)

            # TODO: Is it really not supposed to wrap around?
            self.clock = max(elapsed, 0o7777)
            # self.clock = (self.clock + 1) & 0o7777

        if log_inss:
            return inss_log


if __name__ == '__main__':
    emu = Emu.from_filename('mandelflag.rom')
    emu.run()

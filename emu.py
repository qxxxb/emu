import base64
import logging
import sys
from string import digits, ascii_uppercase
import time
import traceback

from ins import *
from disasm import *


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


class Regs:
    '''
    64 registers that are 6-bit elements each.
    '''

    def __init__(self):
        self.data = [0] * 64

    def dump(self):
        n = 8
        for i in range(0, len(self.data), n):
            xs = self.data[i:i + n]
            xs = [str(x).rjust(2) for x in xs]
            print(' '.join(xs))

    def __getitem__(self, i):
        assert 0 <= self.data[i] < 64
        return self.data[i]

    def __setitem__(self, i, v):
        if i != 0:
            self.data[i] = v & 0o77

    def __len__(self):
        return len(self.data)


def twos_comp(n, bits=6):
    mask = (1 << bits) - 1
    neg = n ^ mask
    return (neg + 1) & mask


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


def str_from_serial(ns):
    return ''.join([chr_from_serial(n) for n in ns])


def serial_from_chr(c):
    return serial_dict.index(c)


def serial_from_str(s):
    return bytearray([serial_from_chr(c) for c in s])


class Emu:
    def __init__(self):
        self.regs = Regs()
        self.pc = 0
        self.halted = False
        self.cf = False
        self.clock = 0
        self.buffer = ''
        self.out = sys.stdout

    @classmethod
    def from_filename(cls, filename):
        ans = cls()
        s = open(filename).read().strip()
        s = base64.b64decode(s)
        ans.tape = Tape.from_bytes(s)
        return ans

    # Ops

    def op_hlt(self, ins):
        self.halted = True

    # Arithmetic and logic

    def op_add(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.regs[rd] = self.regs[ra] + self.regs[rb]

    def op_addi(self, ins):
        rd, ra, ib = ins.a, ins.b, ins.c
        self.regs[rd] = self.regs[ra] + ib

    def op_sub(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.regs[rd] = self.regs[ra] + twos_comp(self.regs[rb])

    def op_or(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.regs[rd] = self.regs[ra] | self.regs[rb]

    def op_ori(self, ins):
        rd, ra, ib = ins.a, ins.b, ins.c
        self.regs[rd] = self.regs[ra] | ib

    def op_xor(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.regs[rd] = self.regs[ra] ^ twos_comp(self.regs[rb])

    def op_xori(self, ins):
        rd, ra, ib = ins.a, ins.b, ins.c
        self.regs[rd] = self.regs[ra] ^ ib

    def op_and(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.regs[rd] = self.regs[ra] & twos_comp(self.regs[rb])

    def op_andi(self, ins):
        rd, ra, ib = ins.a, ins.b, ins.c
        self.regs[rd] = self.regs[ra] & ib

    def op_shl(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.regs[rd] = self.regs[ra] << self.regs[rb]

    def op_shr(self, ins):
        rd, ra, rb = ins.a, ins.b, ins.c
        self.regs[rd] = self.regs[ra] >> self.regs[rb]

    # Comparison

    def op_cmp(self, ins):
        (cmp_type, cm, a, b) = ins.as_cmp()

        # Determine left and right sides of comparison
        if cmp_type == CmpType.RA_RB:
            left = self.regs[a]
            right = self.regs[b]
        elif cmp_type == CmpType.RB_RA:
            left = self.regs[b]
            right = self.regs[a]
        elif cmp_type == CmpType.RA_IB:
            left = self.regs[a]
            right = b
        elif cmp_type == CmpType.IA_RB:
            left = a
            right = self.regs[b]

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

        if shi_type == ShiType.SHLI:
            self.regs[rd] = self.regs[ra] << ib
        elif shi_type == ShiType.SHRI:
            self.regs[rd] = self.regs[ra] >> ib
        elif shi_type == ShiType.SARI:
            self.regs[rd] = sar(self.regs[ra], ib)
        elif shi_type == ShiType.ROLI:
            self.regs[rd] = rol(self.regs[ra], ib)
        else:
            raise ValueError('Unhandled shi_type: {}'.format(shi_type))

    def op_ld(self, ins):
        rd, ra, ib = ins.a, ins.b, ins.c
        rs = (self.regs[ra] + ib) & 0o77
        self.regs[rd] = self.regs[rs]

    def op_st(self, ins):
        rs, ra, ib = ins.a, ins.b, ins.c
        rd = (self.regs[ra] + ib) & 0o77
        self.regs[rd] = self.regs[rs]

    def op_fm(self, ins):
        (fm_type, pr, rd, ra) = ins.as_fm()

        # 12 bit buffer
        ans = (self.regs[rd] * self.regs[ra]) & 0o7777
        if fm_type == FmType.U:
            ans = ans >> pr
        else:
            ans = sar(ans, pr, bits=12)

        # `ans` will be deduce back to 6 bits when stored
        self.regs[rd] = ans

    def op_lbl(self, ins):
        # Do nothing
        pass

    def op_jup(self, ins, reverse=False):
        key = (ins.partial_jump_key(), self.regs[ins.c])

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

        def get_input():
            s = input('> ') + '\n'
            self.buffer += s

        if ix == IoDevice.SERIAL_INCOMING:
            # Optionally read more input if we don't have any in the buffer
            if len(self.buffer) == 0:
                get_input()

            # Send the length of buffer
            self.regs[rd] = from_int(len(self.buffer))
        elif ix == IoDevice.SERIAL_READ:
            # Optionally read more input if we don't have any in the buffer
            if len(self.buffer) == 0:
                get_input()

            # Pop the first char and send it
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            self.regs[rd] = from_int(serial_from_chr(c))
        elif ix == IoDevice.SERIAL_WRITE:
            c = chr_from_serial(self.regs[rs])
            self.out.write(c)
            self.out.flush()
        elif ix == IoDevice.CLOCK_LO_CS:
            self.regs[rd] = self.clock & 0o77  # Lower 6 bits of clock
        elif ix == IoDevice.CLOCK_HI_CS:
            # Upper 6 bits of clock
            self.regs[rd] = (self.clock & 0o7700) >> 6
        else:
            logging.warning('Unknown IO device')
            self.halted = True

    op_switch = {
        Op.HLT: op_hlt,
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

            # Clock is not supposed to overflow or wrap around.
            # This means that the program must run in under 40.95 seconds.
            self.clock = max(elapsed, 0o7777)

        if log_inss:
            return inss_log

    def execute_dbg_cmd(self, cmd):
        '''Return value: whether to go to the next instruction or not'''
        cmd = cmd.split()
        if len(cmd) == 0:
            print('No cmd')
            return False

        try:
            if cmd[0] == 'p':
                i = int(cmd[1])
                print('[{}] = {}'.format(i, self.regs[i]))
            elif cmd[0] == 'reg':
                self.regs.dump()
            elif cmd[0] == 'l':
                inss = self.tape[self.pc: self.pc + 5]
                disasm = Disasm.disasm_tape(inss)
                print(disasm)
            elif cmd[0] in {'n', 's'}:
                return True
            elif cmd[0] == 'q':
                self.halted = True
                return True
            elif cmd[0] == 'c':
                self.stepping = False
                return True
            else:
                print('Unknown cmd')
                return False
        except ValueError:
            print('Error processing cmd')
            return False

    def run_dbg(self):
        self.clock = 0
        self.stepping = True
        prev_cmd = None

        while not self.halted:
            ins = self.tape[self.pc]
            print('{}: {}'.format(self.pc, Disasm.disasm(ins)))

            if self.stepping:
                while True:
                    cmd = input('edb> ')
                    if cmd == '' and prev_cmd:
                        cmd = prev_cmd

                    go_next = self.execute_dbg_cmd(cmd)
                    prev_cmd = cmd
                    if go_next:
                        break

            self.execute(ins)
            self.pc = (self.pc + 1) % len(self.tape)  # Tape is looped

            # Use fake clock where each instruction takes one centisecond
            self.clock = max(self.clock + 1, 0o7777)


if __name__ == '__main__':
    use_dbg = False
    run_server = False

    if len(sys.argv) >= 2:
        run_server = 's' in sys.argv[1]
        use_dbg = 'd' in sys.argv[1]

    if run_server:
        filename = 'talkative-server-redacted.rom'
    else:
        filename = 'talkative-client.rom'

    emu = Emu.from_filename(filename)

    try:
        if use_dbg:
            emu.run_dbg()
        else:
            emu.run()
    except KeyboardInterrupt:
        traceback.print_exc(file=sys.stdout)
        # Print the PC before we quit
        print('EMU PC:', emu.pc)
        sys.exit(1)

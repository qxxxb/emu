import base64
import logging
import sys
from string import digits, ascii_uppercase
import traceback
import time

from ins import *
from disasm import *
import gpu


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

    def to_bytes(self):
        ans = [ins.to_bytes() for ins in self.data]
        return b''.join(ans)

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


class Mem:
    '''
    2**18 16-bit words.
    '''

    def __init__(self):
        self.data = [0] * (2**18)
        self.addr = 0  # 18-bit index for `self.data`

    def dump(self):
        # Warning: very big
        n = 8
        for i in range(0, len(self.data), n):
            xs = self.data[i:i + n]
            xs = [str(x).rjust(2) for x in xs]
            print(' '.join(xs))

    def __getitem__(self, i):
        assert 0 <= self.data[i] < 64
        return self.data[i]

    def __setitem__(self, i, v):
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
    def __init__(self, use_gpu=False):
        self.regs = Regs()
        self.mem = Mem()

        self.use_gpu = use_gpu
        if use_gpu:
            self.gpu = gpu.Gpu()
            self.gpu.start()

        self.pc = 0
        self.halted = False
        self.cf = False
        self.clock = 0

        self.buffer = ''
        self.out = sys.stdout

    @classmethod
    def from_filename(cls, filename, use_gpu=False):
        ans = cls(use_gpu)
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
                # We always increment the PC after executing an instruction.
                # To offset that, we subtract 1 here.
                self.pc = i - 1
                return

    def op_jdn(self, ins):
        self.op_jup(ins, reverse=True)

    def get_input(self):
        s = input('> ')
        self.buffer += s

    def op_io_serial_incoming(self, ins):
        (rd, ix_, rs_) = ins.as_io()

        # Optionally read more input if we don't have any in the buffer
        if len(self.buffer) == 0:
            self.get_input()

        # Send the length of buffer
        self.regs[rd] = from_int(len(self.buffer))

    def op_io_serial_read(self, ins):
        (rd, ix_, rs_) = ins.as_io()

        # Optionally read more input if we don't have any in the buffer
        if len(self.buffer) == 0:
            self.get_input()

        # Pop the first char and send it
        c = self.buffer[0]
        self.buffer = self.buffer[1:]
        self.regs[rd] = from_int(serial_from_chr(c))

    def op_io_serial_write(self, ins):
        (rd_, ix_, rs) = ins.as_io()
        c = chr_from_serial(self.regs[rs])
        self.out.write(c)
        self.out.flush()

    def reset_clock(self):
        self.start = time.time()
        self.clock == 0
        if self.use_gpu:
            should_halt = self.gpu.update()
            if should_halt:
                self.halted = True

    def op_io_clock_lo_cs(self, ins):
        (rd, ix_, rs) = ins.as_io()
        if rs == 0:
            # Get lower 6 bits of clock
            self.regs[rd] = self.clock & 0o77
        else:
            self.reset_clock()

    def op_io_clock_hi_cs(self, ins):
        (rd, ix_, rs) = ins.as_io()
        if rs == 0:
            # Get upper 6 bits of clock
            self.regs[rd] = (self.clock & 0o7700) >> 6
        else:
            self.reset_clock()

    def op_io_mem_addr_lo(self, ins):
        (rd_, ix_, rs) = ins.as_io()
        # Clear lower bits without clearing upper bits
        mask = (0o77 << 6) + (0o77 << (6 * 2))
        self.mem.addr &= mask
        self.mem.addr |= self.regs[rs]

    def op_io_mem_addr_mid(self, ins):
        (rd_, ix_, rs) = ins.as_io()
        mask = 0o77 + (0o77 << (6 * 2))
        self.mem.addr &= mask
        self.mem.addr |= (self.regs[rs] << 6)

    def op_io_mem_addr_hi(self, ins):
        (rd_, ix_, rs) = ins.as_io()
        mask = 0o77 + (0o77 << 6)
        self.mem.addr &= mask
        self.mem.addr |= (self.regs[rs] << (6 * 2))

    def op_io_mem_read(self, ins):
        (rd, ix_, rs_) = ins.as_io()
        self.regs[rd] = self.mem[self.mem.addr]
        self.mem.addr = (self.mem.addr + 1) % len(self.mem)

    def op_io_mem_write(self, ins):
        (rd_, ix_, rs) = ins.as_io()
        self.mem[self.mem.addr] = self.regs[rs]
        self.mem.addr = (self.mem.addr + 1) % len(self.mem)

    def op_gpu_x(self, ins):
        (rd_, ix_, rs) = ins.as_io()
        self.gpu.set_x(self.regs[rs])

    def op_gpu_y(self, ins):
        (rd_, ix_, rs) = ins.as_io()
        self.gpu.set_y(self.regs[rs])

    def op_gpu_draw(self, ins):
        (rd_, ix, rs) = ins.as_io()
        self.gpu.draw(self.regs[rs])

    op_io_switch = {
        IoDevice.SERIAL_INCOMING: op_io_serial_incoming,
        IoDevice.SERIAL_READ: op_io_serial_read,
        IoDevice.SERIAL_WRITE: op_io_serial_write,
        IoDevice.CLOCK_LO_CS: op_io_clock_lo_cs,
        IoDevice.CLOCK_HI_CS: op_io_clock_hi_cs,
        IoDevice.MEM_ADDR_HI: op_io_mem_addr_hi,
        IoDevice.MEM_ADDR_MID: op_io_mem_addr_mid,
        IoDevice.MEM_ADDR_LO: op_io_mem_addr_lo,
        IoDevice.MEM_READ: op_io_mem_read,
        IoDevice.MEM_WRITE: op_io_mem_write,
        IoDevice.GPU_X: op_gpu_x,
        IoDevice.GPU_Y: op_gpu_y,
        IoDevice.GPU_DRAW: op_gpu_draw,
    }

    def op_io(self, ins):
        (rd_, ix, rs_) = ins.as_io()
        if ix in Emu.op_io_switch:
            op_io_func = Emu.op_io_switch[ix]
            op_io_func(self, ins)
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

        self.start = time.time()
        self.clock = 0

        while not self.halted:
            ins = self.tape[self.pc]

            if log_inss:
                inss_log.append(self.pc)

            # 19483
            self.execute(ins)
            self.pc = (self.pc + 1) % len(self.tape)  # Tape is looped

            now = time.time()
            elapsed = now - self.start
            elapsed = round(elapsed, 2)
            elapsed = int(elapsed * 100)

            # Clock does not wrap
            self.clock = min(elapsed, 0o7777)

        if self.use_gpu:
            self.gpu.quit()

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
                print('regs[{}] = {}'.format(i, self.regs[i]))
            elif cmd[0] == 'x':
                i = int(cmd[1])
                print('mem[{}] = {}'.format(i, self.mem[i]))
            elif cmd[0] == 'xi':
                print('mem.addr = {}'.format(self.mem.addr))
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
            self.clock = min(self.clock + 1, 0o7777)

    def save_tape(self, filename):
        with open(filename, 'w') as f:
            b = self.tape.to_bytes()
            s = base64.b64encode(b).decode()
            f.write(s)


if __name__ == '__main__':
    assert len(sys.argv) >= 2
    filename = sys.argv[1]

    emu = Emu.from_filename(filename, use_gpu=True)

    try:
        emu.run()
    except KeyboardInterrupt:
        traceback.print_exc(file=sys.stdout)
        # Print the PC before we quit
        print('EMU PC:', emu.pc)
        sys.exit(1)

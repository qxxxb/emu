from ins import *
from emu import *


class Disasm:
    @staticmethod
    def cond_prefix(ins):
        if ins.cond == Cond.UN:
            return ' '
        elif ins.cond == Cond.TR:
            return '+'
        elif ins.cond == Cond.FA:
            return '-'

    @staticmethod
    def disasm_hlt(ins):
        return '  ' + 'HLT'

    @staticmethod
    def disasm_values(ins):
        # TODO: Remove this
        return str(ins)

    @staticmethod
    def disasm_rrr(ins):
        return '{} {:<6} r{}, r{}, r{}'.format(
            Disasm.cond_prefix(ins),
            ins.op.name,
            ins.a, ins.b, ins.c
        )

    @staticmethod
    def disasm_rri(ins):
        return '{} {:<6} r{}, r{}, {}'.format(
            Disasm.cond_prefix(ins),
            ins.op.name,
            ins.a, ins.b, ins.c
        )

    @staticmethod
    def disasm_cmp(ins):
        (cmp_type, cm, a, b) = ins.as_cmp()

        if cmp_type == CmpType.RA_RB:
            s = 'r{}, r{}'.format(a, b)
        elif cmp_type == CmpType.RB_RA:
            s = 'r{}, r{}'.format(b, a)
        elif cmp_type == CmpType.RA_IB:
            s = 'r{}, {}'.format(a, b)
        elif cmp_type == CmpType.IA_RB:
            s = '{}, r{}'.format(a, b)

        return '{} {:<6} {}'.format(
            Disasm.cond_prefix(ins),
            ins.op.name + cm.name,
            s
        )

    @staticmethod
    def disasm_shi(ins):
        (shi_type, rd, ra, ib) = ins.as_shi()
        return '{} {:<6} r{}, r{}, {}'.format(
            Disasm.cond_prefix(ins),
            shi_type.name,
            rd, ra, ib
        )

    @staticmethod
    def disasm_ld(ins):
        rd, ra, ib = ins.a, ins.b, ins.c
        return '{} {:<6} r{}, [r{}+{}]'.format(
            Disasm.cond_prefix(ins),
            ins.op.name,
            rd, ra, ib
        )

    @staticmethod
    def disasm_st(ins):
        rs, ra, ib = ins.a, ins.b, ins.c
        return '{} {:<6} [r{}+{}], r{}'.format(
            Disasm.cond_prefix(ins),
            ins.op.name,
            ra, ib, rs
        )

    @staticmethod
    def disasm_fm(ins):
        (fm_type, pr, rd, ra) = ins.as_fm()
        return '{} {:<6} r{}, r{}'.format(
            Disasm.cond_prefix(ins),
            '{}/{}'.format(ins.op.name + fm_type.name, pr),
            rd, ra
        )

    @staticmethod
    def disasm_lbl(ins):
        lab, lc = ins.label_key()
        return '{} {:<6} {}, {}'.format(
            Disasm.cond_prefix(ins),
            ins.op.name,
            lab, lc
        )

    @staticmethod
    def disasm_jump(ins):
        lab, rc = ins.partial_jump_key(), ins.c
        return '{} {:<6} {}, r{}'.format(
            Disasm.cond_prefix(ins),
            ins.op.name,
            lab, rc
        )

    @staticmethod
    def disasm_io(ins):
        (rd, ix, rs) = ins.as_io()
        return '{} {:<6} r{}, {}, r{}'.format(
            Disasm.cond_prefix(ins),
            ins.op.name,
            rd, ix.name, rs
        )

    disasm_switch = {
        Op.HLT: disasm_hlt.__func__,
        Op.ADD: disasm_rrr.__func__,
        Op.ADDI: disasm_rri.__func__,
        Op.SUB: disasm_rrr.__func__,
        Op.OR: disasm_rrr.__func__,
        Op.ORI: disasm_rri.__func__,
        Op.XOR: disasm_rrr.__func__,
        Op.XORI: disasm_rri.__func__,
        Op.AND: disasm_rrr.__func__,
        Op.ANDI: disasm_rri.__func__,
        Op.SHL: disasm_rrr.__func__,
        Op.SHR: disasm_rrr.__func__,
        Op.CMP: disasm_cmp.__func__,
        Op.SHI: disasm_shi.__func__,
        Op.LD: disasm_ld.__func__,
        Op.ST: disasm_st.__func__,
        Op.FM: disasm_fm.__func__,
        Op.LBL: disasm_lbl.__func__,
        Op.JUP: disasm_jump.__func__,
        Op.JDN: disasm_jump.__func__,
        Op.IO: disasm_io.__func__,
    }

    @staticmethod
    def disasm(ins):
        disasm_func = Disasm.disasm_switch.get(ins.op, Disasm.disasm_values)
        return disasm_func(ins)

    @staticmethod
    def disasm_tape(tape, out=sys.stdout, raw=False):
        for i in range(len(tape)):
            ins = tape[i]
            if raw:
                out.write(str(ins) + '\n')
            else:
                out.write('{:0>3}: {}\n'.format(i, Disasm.disasm(ins)))

    @staticmethod
    def disasm_tape_to_file(tape, filename, raw=False):
        with open(filename, 'w') as f:
            Disasm.disasm_tape(tape, f, raw)


if __name__ == '__main__':
    emu = Emu.from_filename('win.rom')
    Disasm.disasm_tape_to_file(emu.tape, 'win.asm')

#     emu = Emu.from_filename('talkative-server.rom')
#     Disasm.disasm_tape_to_file(emu.tape, 'talkative-server.asm')

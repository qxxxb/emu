# I didn't really read/change this file


def disasm(ins):
    cmarr = ["tr", "fa", "eq", "ne", "sl", "sg", "ul", "ug"]

    ans = ""
    valid, op, cond, a, b, c = ins.get()
    if not valid:
        return "Invalid instruction"

    if cond == 1:
        ans += "+ "
    elif cond == 2:
        ans += "- "
    else:
        ans += "  "
    if op == 0:
        ans += f"add r{a}, r{b}, r{c}"
    elif op == 1:
        ans += f"add r{a}, r{b}, {c}"
    elif op == 2:
        ans += f"sub r{a}, r{b}, r{c}"
    elif op == 3:
        cmptype = a//8
        cm = a % 8
        if cmptype == 0:
            ans += f"cmp{cmarr[cm]} r{b}, r{c}"
        if cmptype == 1:
            ans += f"cmp{cmarr[cm]} r{c}, r{b}"
        if cmptype == 2:
            ans += f"cmp{cmarr[cm]} r{b}, {c}"
        if cmptype == 3:
            ans += f"cmp{cmarr[cm]} {b}, r{c}"
    elif op == 4:
        ans += f"or r{a}, r{b}, r{c}"
    elif op == 5:
        ans += f"or r{a}, r{b}, {c}"
    elif op == 6:
        ans += f"xor r{a}, r{b}, r{c}"
    elif op == 7:
        ans += f"xor r{a}, r{b}, {c}"
    elif op == 8:
        ans += f"and r{a}, r{b}, r{c}"
    elif op == 9:
        ans += f"and r{a}, r{b}, {c}"
    elif op == 10:
        shifttype = c//8
        ib = c % 8
        if shifttype == 0:
            ans += f"shl r{a}, r{b}, {ib}"
        elif shifttype == 1:
            ans += f"shr r{a}, r{b}, {ib}"
        elif shifttype == 2:
            ans += f"sar r{a}, r{b}, {ib}"
        elif shifttype == 3:
            ans += f"rol r{a}, r{b}, {ib}"
    elif op == 11:
        ans += f"shl r{a}, r{b}, r{c}"
    elif op == 12:
        ans += f"shr r{a}, r{b}, r{c}"
    elif op == 13:
        brackets = "[" + (f"r{b}", "")[b == 0] + "+" * \
            (b != 0 and c != 0) + (f"{c}", "")[c == 0] + "]"
        ans += f"ld r{a}, {brackets}"
    elif op == 14:
        brackets = "[" + (f"r{b}", "")[b == 0] + "+" * \
            (b != 0 and c != 0) + (f"{c}", "")[c == 0] + "]"
        ans += f"st {brackets}, r{a}"
    elif op == 15:
        lab = (64*a+b) % 4096
        ans += f"lbl {lab}, {c}"
    elif op == 16:
        lab = (64*a+b) % 4096
        ans += f"jup {lab}, r{c}"
    elif op == 17:
        lab = (64*a+b) % 4096
        ans += f'jdn {lab}, r{c}'
    elif op == 18:
        if a == 0 and c == 0:
            ans += f"io {b}"
            return ans
        if c == 0:
            ans += f"io r{a}, {b}"
            return ans
        if a == 0:
            ans += f"io {b}, r{c}"
            return ans
        ans += f"io r{a}, {b}, r{c}"
    elif op == 19:
        multype = c//16
        pr = c % 16
        if multype == 0:
            ans += f"fmu/{pr} r{a}, r{b}"
        if multype == 1:
            ans += f"fms/{pr} r{a}, r{b}"
    elif op == 20:
        ans += "hlt"
    return ans


def disasm_tape(tape):
    for i in range(len(tape)):
        ins = tape[i]
        print(disasm(ins))

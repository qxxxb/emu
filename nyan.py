from PIL import Image
import numpy as np
from ins import *
from emu import *
from pprint import pprint

frames = []
for i in range(1, 12):
    im = Image.open('frames/f-' + str(i) + '.png').convert('RGBA')
    pxs = np.asarray(im)
    frames.append(pxs)

bg_color = 0b000110

def unscale_color(c):
    r, g, b, a = c
    if a == 0:
        return bg_color

    r //= 64
    g //= 64
    b //= 64
    return (r << 4) | (g << 2) | b

def mem_write_imm(i):
    return [
        Ins.from_values(Op.ADDI, Cond.UN, 1, 0, i),
        Ins.from_io(Cond.UN, 0, IoDevice.MEM_WRITE, 1),
    ]

tape = []
for f in frames:
    for row in f:
        for px in row:
            c = unscale_color(px)
            tape += mem_write_imm(c)

pprint(tape[:16])

# Draw

rs = {
    'gpu_x': 1,
    'gpu_y': 2,
    'frame_i': 3,
}

n_temp = 0

def temp_reg():
    global n_temp
    ans = len(rs) + n_temp + 1
    n_temp += 1
    return ans

label_i = 0
def new_label():
    global label_i
    a = label_i // 64
    b = label_i % 64
    label_i += 1
    return (a, b)

width = 34
height = 26
n_frames = 11

def draw_row():
    color = temp_reg()
    x = temp_reg()  # gpu_x + offset
    (la, lb) = new_label()

    return [
        # Loop through GPU X from 0..width
        Ins.from_values(Op.ADDI, Cond.UN, rs['gpu_x'], 0, 0),
        Ins.from_values(Op.LBL, Cond.UN, la, lb, 0),

        # offset = 14
        Ins.from_values(Op.ADDI, Cond.UN, x, rs['gpu_x'], 14),
        Ins.from_io(Cond.UN, 0, IoDevice.GPU_X, x),

        Ins.from_io(Cond.UN, color, IoDevice.MEM_READ, 0),
        Ins.from_io(Cond.UN, 0, IoDevice.GPU_DRAW, color),

        Ins.from_values(Op.ADDI, Cond.UN, rs['gpu_x'], rs['gpu_x'], 1),
        Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, rs['gpu_x'], width),
        Ins.from_values(Op.JUP, Cond.FA, la, lb, 0),
    ]

def draw_frame():
    ans = []

    y = temp_reg()  # gpu_y + offset
    (la, lb) = new_label()

    ans += [
        # Loop through GPU Y from 0..height
        Ins.from_values(Op.ADDI, Cond.UN, rs['gpu_y'], 0, 0),
        Ins.from_values(Op.LBL, Cond.UN, la, lb, 0),

        Ins.from_values(Op.ADDI, Cond.UN, y, rs['gpu_y'], 18),
        Ins.from_io(Cond.UN, 0, IoDevice.GPU_Y, y),
    ]

    ans += draw_row()

    ans += [
        Ins.from_values(Op.ADDI, Cond.UN, rs['gpu_y'], rs['gpu_y'], 1),
        Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, rs['gpu_y'], height),
        Ins.from_values(Op.JUP, Cond.FA, la, lb, 0),
    ]

    return ans

def draw_frames():
    ans = []
    (la, lb) = new_label()
    wait = new_label()
    cl = temp_reg()  # Clock reset

    ans += [
        # Loop frame index from 0..n_frames
        Ins.from_values(Op.ADDI, Cond.UN, rs['frame_i'], 0, 0),
        Ins.from_values(Op.LBL, Cond.UN, la, lb, 0),
    ]

    ans += draw_frame()

    ans += [
        # Reset clock to draw frame
        Ins.from_values(Op.ADDI, Cond.UN, cl, 0, 1),
        Ins.from_io(Cond.UN, 0, IoDevice.CLOCK_LO_CS, cl),

        # Wait before drawing next frame
        Ins.from_values(Op.LBL, Cond.UN, wait[0], wait[1], 0),
        Ins.from_io(Cond.UN, cl, IoDevice.CLOCK_LO_CS, 0),
        Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.UL, cl, 8),
        Ins.from_values(Op.JUP, Cond.TR, wait[0], wait[1], 0),

        Ins.from_values(Op.ADDI, Cond.UN, rs['frame_i'], rs['frame_i'], 1),
        Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, rs['frame_i'], n_frames),
        Ins.from_values(Op.JUP, Cond.FA, la, lb, 0),

        # Loop

        # Set frame index to 0
        Ins.from_values(Op.ADDI, Cond.UN, rs['frame_i'], 0, 0),

        # Reset memory pointer
        Ins.from_io(Cond.UN, 0, IoDevice.MEM_ADDR_HI, 0),
        Ins.from_io(Cond.UN, 0, IoDevice.MEM_ADDR_MID, 0),
        Ins.from_io(Cond.UN, 0, IoDevice.MEM_ADDR_LO, 0),

        Ins.from_values(Op.JUP, Cond.UN, la, lb, 0),
    ]

    return ans

def clear_screen():
    (lax, lbx) = new_label()
    (lay, lby) = new_label()
    bg = temp_reg()

    return [
        Ins.from_values(Op.ADDI, Cond.UN, bg, 0, bg_color),
        Ins.from_values(Op.ADDI, Cond.UN, rs['gpu_x'], 0, 0),

        # 0993:   LBL    1026, 0
        Ins.from_values(Op.LBL, Cond.UN, lax, lbx, 0),
        # 0994:   IO     r0, GPU_X, r1
        Ins.from_io(Cond.UN, 0, IoDevice.GPU_X, rs['gpu_x']),

        # 0995:   ADDI   r2, r0, 0
        Ins.from_values(Op.ADDI, Cond.UN, rs['gpu_y'], 0, 0),
        # 0996:   LBL    1027, 0
        Ins.from_values(Op.LBL, Cond.UN, lay, lby, 0),

        # 0997:   IO     r0, GPU_Y, r2
        Ins.from_io(Cond.UN, 0, IoDevice.GPU_Y, rs['gpu_y']),
        # 0998:   IO     r0, GPU_DRAW, r3
        Ins.from_io(Cond.UN, 0, IoDevice.GPU_DRAW, bg),

        # 0999:   ADDI   r2, r2, 1
        Ins.from_values(Op.ADDI, Cond.UN, rs['gpu_y'], rs['gpu_y'], 1),
        # 1000:   CMPEQ  r2, 0
        Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, rs['gpu_y'], 0),
        # 1001: - JUP    1027, r0
        Ins.from_values(Op.JUP, Cond.FA, lay, lby, 0),

        # 1002:   ADDI   r1, r1, 1
        Ins.from_values(Op.ADDI, Cond.UN, rs['gpu_x'], rs['gpu_x'], 1),
        # 1003:   CMPEQ  r1, 0
        Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, rs['gpu_x'], 0),
        # 1004: - JUP    1026, r0
        Ins.from_values(Op.JUP, Cond.FA, lax, lbx, 0),
    ]

tape += clear_screen()
tape += draw_frames()
tape += [Ins.halt()]

emu = Emu(use_gpu=True)
emu.tape = Tape.from_inss(tape)
emu.save_tape('nyan.rom')

try:
    emu.run()
except KeyboardInterrupt:
    traceback.print_exc(file=sys.stdout)
    # Print the PC before we quit
    print('EMU PC:', emu.pc)
    sys.exit(1)

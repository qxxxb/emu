import time
from ins import *
from emu import *

# Stripes

# r2: GPU Y
# r1: GPU X
emu = Emu(use_gpu=True)
emu.tape = Tape.from_inss([
    Ins.from_values(Op.LBL, Cond.UN, 0, 0, 0),

    # Loop through GPU Y from 0..63 {
    Ins.from_values(Op.LBL, Cond.UN, 0, 2, 0),
    Ins.from_io(Cond.UN, 0, IoDevice.GPU_Y, 2),

    # Loop through GPU X from 0..63
    Ins.from_values(Op.LBL, Cond.UN, 0, 1, 0),
    Ins.from_io(Cond.UN, 0, IoDevice.GPU_X, 1),
    Ins.from_io(Cond.UN, 0, IoDevice.GPU_DRAW, 1),
    Ins.from_values(Op.ADDI, Cond.UN, 1, 1, 1),
    Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, 1, 0),
    Ins.from_values(Op.JUP, Cond.FA, 0, 1, 0),
    # }

    Ins.from_values(Op.ADDI, Cond.UN, 2, 2, 1),
    Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, 2, 0),
    Ins.from_values(Op.JUP, Cond.FA, 0, 2, 0),
    # }
])

# Each frame is completed when PC == 0
emu.gpu_update_ins = 0
emu.run()

print('Starting next program')
time.sleep(0.5)

# Rolling stripes

# r3: Color offset
# r2: GPU Y
# r1: GPU X
emu = Emu(use_gpu=True)
emu.tape = Tape.from_inss([
    Ins.from_values(Op.LBL, Cond.UN, 0, 0, 0),

    # Loop through GPU Y from 0..63 {
    Ins.from_values(Op.LBL, Cond.UN, 0, 2, 0),
    Ins.from_io(Cond.UN, 0, IoDevice.GPU_Y, 2),

    # Loop through GPU X from 0..63
    Ins.from_values(Op.LBL, Cond.UN, 0, 1, 0),
    Ins.from_io(Cond.UN, 0, IoDevice.GPU_X, 1),

    # Draw X + color_offset
    Ins.from_values(Op.ADD, Cond.UN, 4, 1, 3),
    Ins.from_io(Cond.UN, 0, IoDevice.GPU_DRAW, 4),

    Ins.from_values(Op.ADDI, Cond.UN, 1, 1, 1),
    Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, 1, 0),
    Ins.from_values(Op.JUP, Cond.FA, 0, 1, 0),
    # }

    Ins.from_values(Op.ADDI, Cond.UN, 2, 2, 1),
    Ins.from_cmp(Cond.UN, CmpType.RA_IB, Cm.EQ, 2, 0),
    Ins.from_values(Op.JUP, Cond.FA, 0, 2, 0),
    # }

    Ins.from_values(Op.ADDI, Cond.UN, 3, 3, 1),
])

# Each frame is completed when PC == 0
emu.gpu_update_ins = 0
emu.run()

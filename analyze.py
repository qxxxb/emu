from emu import *
import pickle
import itertools
import copy
import sys
import io

with open('emu_state.pkl', 'rb') as f:
    emu = pickle.load(f)

bruteforce = True
if bruteforce:
    # Bruteforce the key (we found it to be 'Y#')
    flags = []
    for bigram in itertools.product(serial_dict, repeat=2):
        payload = ''.join(bigram) + 'AA'
        m = copy.deepcopy(emu)
        out = io.StringIO()
        m.out = out
        m.buffer = payload
        print('"{}"'.format(payload))
        m.run()
        output = out.getvalue()
        if 'X-MAS' in output:
            flags.append((payload, output))

    print(flags)
else:
    # Run the program with a user-supplied key
    m = copy.deepcopy(emu)
    m.out = sys.stdout
    m.buffer = sys.argv[1]
    m.run()

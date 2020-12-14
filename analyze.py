from emu import *
import pickle
import itertools
import copy
import sys
import io

# Analyze the saved machine state and brute-force the key

with open('emu_state.pkl', 'rb') as f:
    emu = pickle.load(f)

if len(sys.argv) >= 2:
    # Run the program with a user-supplied key
    m = copy.deepcopy(emu)
    m.out = sys.stdout
    m.buffer = sys.argv[1]
    m.run()
else:
    # Bruteforce the key (we found it to be 'Y#')
    for bigram in itertools.product(serial_dict, repeat=2):
        payload = ''.join(bigram) + 'AA'
        m = copy.deepcopy(emu)
        out = io.StringIO()
        m.out = out
        m.buffer = payload
        m.run()
        output = out.getvalue()
        print(payload, output)
        if 'X-MAS' in output:
            break

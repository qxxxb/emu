# EMU 1.0

Current output (PyPy highly recommend for performance):
```
$ ~/Downloads/pypy3.7-v7.3.3-linux64/bin/pypy3 emu.py
................................................................................................................................
................................................................................................................................
................................................................................................................................
................................................................................................................................
................................................................................................................................
........................................................................,,,,,,,,,,,.............................................
................................................................,,,,,,,,,,,,,,,,,,,,,,,,,,......................................
...........................................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.................................
.......................................................,,,,,,,,,,,,,,,,,,,,,---,,,,,,,,,,,,,,,,,,,..............................
....................................................,,,,,,,,,,,,,,,,,,,,,,,,--~--,,,,,,,,,,,,,,,,,,,............................
.................................................,,,,,,,,,,,,,,,,,,,,,,,,,,,--##------,,,,,,,,,,,,,,,,..........................
..............................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,----~#-~##--,,,,,,,,,,,,,,,,,........................
...........................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-------~#~-----,,,,,,,,,,,,,,,,,,......................
........................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---#--#####~----,,,,,,,,,,,,,,,,,,,,....................
.....................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---###########~#~---,,,,,,,,,,,,,,,,,,,...................
...................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,------~###########~----,,,,,,,,,,,,,,,,,,,..................
................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-----------#############------,,,,,,,,,,,,,,,,,,.................
.............................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-----~----------~###########~---------------,,,,,,,,,,................
..........................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---###~~---#####################~###--------#--,,,,,,,,,...............
......................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---##################################~~-~##~~###,,,,,,,,,,..............
...................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,------~##########################################-,,,,,,,,,,,.............
...............,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,--------~#########################################--,,,,,,,,,,,,............
...........,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,------~############################################~----,,,,,,,,,,,,...........
........,,,,,,,,,,,,,,,,,,,,,---------------------------~#############################################----,,,,,,,,,,,...........
.....,,,,,,,,,,,,,,,,,,,,,,,,--~#--------#~------------##################################################~-,,,,,,,,,,,..........
...,,,,,,,,,,,,,,,,,,,,,,,,,,---#~#~#---~###~-#-------~##################################################--,,,,,,,,,,,..........
..,,,,,,,,,,,,,,,,,,,,,,,,,------~###############~---~#################################################---,,,,,,,,,,,,,.........
,,,,,,,,,,,,,,,,,,,,,,,,,,-------~#################~~####################################################-,,,,,,,,,,,,,.........
,,,,,,,,,,,,,,,,,,,,,,,,-------~#######################################################################---,,,,,,,,,,,,,.........
,,,,,,,,,,,,,,,,,,,,,----~----~#########################################################################-,,,,,,,,,,,,,,,........
,,,,,,,,,,,,,,,,,--------~############################################################################---,,,,,,,,,,,,,,,........
,,,,,,,---------------#-~###########################################################################~---,,,,,,,,,,,,,,,,........
##################################################################################################~-----,,,,,,,,,,,,,,,,........
,,,,,,,---------------#-~###########################################################################~---,,,,,,,,,,,,,,,,........
,,,,,,,,,,,,,,,,,--------~############################################################################---,,,,,,,,,,,,,,,........
,,,,,,,,,,,,,,,,,,,,,----~----~#########################################################################-,,,,,,,,,,,,,,,........
,,,,,,,,,,,,,,,,,,,,,,,,-------~#######################################################################---,,,,,,,,,,,,,.........
,,,,,,,,,,,,,,,,,,,,,,,,,,-------~#################~~####################################################-,,,,,,,,,,,,,.........
..,,,,,,,,,,,,,,,,,,,,,,,,,------~###############~---~#################################################---,,,,,,,,,,,,,.........
...,,,,,,,,,,,,,,,,,,,,,,,,,,---#~#~#---~###~-#-------~##################################################--,,,,,,,,,,,..........
.....,,,,,,,,,,,,,,,,,,,,,,,,--~#--------#~------------##################################################~-,,,,,,,,,,,..........
........,,,,,,,,,,,,,,,,,,,,,---------------------------~#############################################----,,,,,,,,,,,...........
...........,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,------~############################################~----,,,,,,,,,,,,...........
...............,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,--------~#########################################--,,,,,,,,,,,,............
...................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,------~##########################################-,,,,,,,,,,,.............
......................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---##################################~~-~##~~###,,,,,,,,,,..............
..........................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---###~~---#####################~###--------#--,,,,,,,,,...............
.............................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-----~----------~###########~---------------,,,,,,,,,,................
................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-----------#############------,,,,,,,,,,,,,,,,,,.................
...................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,------~###########~----,,,,,,,,,,,,,,,,,,,..................
.....................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---###########~#~---,,,,,,,,,,,,,,,,,,,...................
........................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,---#--#####~----,,,,,,,,,,,,,,,,,,,,....................
...........................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,-------~#~-----,,,,,,,,,,,,,,,,,,......................
..............................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,----~#-~##--,,,,,,,,,,,,,,,,,........................
.................................................,,,,,,,,,,,,,,,,,,,,,,,,,,,--##------,,,,,,,,,,,,,,,,..........................
....................................................,,,,,,,,,,,,,,,,,,,,,,,,--~--,,,,,,,,,,,,,,,,,,,............................
.......................................................,,,,,,,,,,,,,,,,,,,,,---,,,,,,,,,,,,,,,,,,,..............................
...........................................................,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.................................
................................................................,,,,,,,,,,,,,,,,,,,,,,,,,,......................................
........................................................................,,,,,,,,,,,.............................................
................................................................................................................................
................................................................................................................................
................................................................................................................................
................................................................................................................................
HEY
HEY KID
WANT SUM...FLAG?
> Y#SS
X-MAS{EMU~L3G3NDx
x
x
R_D1E}WARNING:root:Invalid instruction (False, <Op.INV: 20>, 0, 0, 0, 0)
```

Note that `Invalid instruction` is expected. Attempting to execute an invalid
instruction is the only way to stop the program.

Only the first chars of the key (`Y#SS`) are used. However, the program
requires there to be more than 3 chars in the key for some reason. This seems
weird and might me a mistake.

Since the only relevant portion of the key are the first two chars, I was able
to bruteforce it without having to reverse the program.

But due to some unknown bug, we're missing six chars in the flag:
```
X-MAS{EMU~L3G3ND??????R_D1E}
```

These are the registers where each char is printed from:
```
[3] X - M A S { E M U ~ L 3
[2] G 3 N D
[7] x \n x \n x \n
[2] R _ D 1 E }
```

There's only one `io 2, r7` instruction in the program. Here's the relevant
disassembly (full disassembly in `disasm.txt`):
```
  lbl 1539, 0
  add r7, r0, 0
  add r12, r0, 0
  lbl 1541, 0
  shl r7, r7, 1
  ld r8, [r12+1]
  and r8, r8, 1
  or r7, r7, r8
  ld r8, [r12+1]
  shr r8, r8, 1
  st [r12+1], r8
  add r12, r12, 1
  cmpeq r12, 6
- jup 1541, r0
  io 2, r7
  add r10, r10, 1
  cmpeq r10, 6
- jup 1539, r0
```

That said, it's hard to say where exactly the bug is. Chances are that it's
going to be very hard to find.

## Tests

Unit tests are available:
```
$ python3 tests.py
......WARNING:root:Invalid instruction (False, <Op.INV: 20>, 0, 0, 0, 0)
....WARNING:root:Invalid instruction (False, <Op.INV: 20>, 0, 0, 0, 0)
.........
----------------------------------------------------------------------
Ran 19 tests in 0.002s

OK
```
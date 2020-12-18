000:   ADDI   r12, r0, 61
001:   ADDI   r13, r0, 36
002:   LBL    512, 0
003:   ADDI   r1, r0, 2
004:   IO     r0, ENET_CONN_CTRL, r1
005:   IO     r1, ENET_INCOMING, r0
006:   CMPUL  r1, 40
007: + JUP    512, r0 # If we have less than 40 chars, keep reading

008:   ADDI   r50, r0, 62 # Store the first 4 chars (username?)
009:   IO     r8, ENET_RECV, r0
010:   IO     r9, ENET_RECV, r0
011:   IO     r10, ENET_RECV, r0
012:   IO     r11, ENET_RECV, r0
013:   ADDI   r2, r0, 14

# Recv payload to registers r14 to r50 (exclusive)
014:   LBL    513, 0
015:   IO     r1, ENET_RECV, r0
016:   ST     [r2+0], r1
017:   ADDI   r2, r2, 1
018:   CMPUL  r2, 50
019: + JUP    513, r0

# Print to username and payload
020:   ADDI   r2, r0, 8
021:   LBL    513, 0
022:   LD     r1, [r2+0]
023:   IO     r0, SERIAL_WRITE, r1
024:   ADDI   r2, r2, 1
025:   CMPUL  r2, 51
026: + JUP    513, r0

027:   CMPEQ  r0, r0
028: + CMPEQ  r24, 36 # Must pass all these checks
029: + CMPEQ  r21, 36
030: + CMPEQ  r40, 10
031: + CMPEQ  r45, 21
032: + CMPEQ  r11, 28
033: + CMPEQ  r27, 29
034: + CMPEQ  r23, 14
035: + CMPEQ  r39, 22
036: + CMPEQ  r34, 10
037: + CMPEQ  r29, 14
038: + CMPEQ  r14, 18
039: + CMPEQ  r35, 23
040: + CMPEQ  r43, 21
041: + CMPEQ  r9, 22
042: + CMPEQ  r8, 34
043: + CMPEQ  r17, 18
044: + CMPEQ  r18, 16
045: + CMPEQ  r36, 36
046: + CMPEQ  r47, 21
047: + CMPEQ  r20, 29
048: + CMPEQ  r44, 24
049: + CMPEQ  r16, 22
050: + CMPEQ  r15, 36
051: + CMPEQ  r22, 11
052: + CMPEQ  r38, 38
053: + CMPEQ  r48, 24
054: + CMPEQ  r26, 14
055: + CMPEQ  r49, 21
056: + CMPEQ  r37, 33
057: + CMPEQ  r46, 24
058: + CMPEQ  r32, 29
059: + CMPEQ  r25, 11
060: + CMPEQ  r41, 28
061: + CMPEQ  r19, 17
062: + CMPEQ  r33, 17
063: + CMPEQ  r31, 36
064: + CMPEQ  r28, 29
065: + CMPEQ  r10, 10
066: + CMPEQ  r42, 36
067: + CMPEQ  r30, 27
068: + JDN    4095, r0 # Jump to flag

069:   ADDI   r1, r0, 1 # Disconnect (probably)
070:   IO     r0, ENET_CONN_CTRL, r1
071:   LBL    513, 0
072:   ADDI   r1, r0, 33
073:   IO     r0, SERIAL_WRITE, r1
074:   ADDI   r1, r0, 2
075:   IO     r1, ENET_CONN_CTRL, r1
076:   CMPEQ  r1, 1
077: + JDN    513, r0
078:   ADDI   r2, r0, 8
079:   LBL    514, 0 # Print {username}: {payload}
080:   LD     r1, [r2+0]
081:   IO     r0, ENET_SEND, r1
082:   ADDI   r2, r2, 1
083:   CMPUL  r2, 51
084: + JUP    514, r0
085:   JUP    513, r0
086:   LBL    513, 0
087:   JDN    512, r0

088:   LBL    4095, 0 # Flag starts here
089:   ADDI   r8, r0, 33
090:   ADDI   r9, r0, 38
091:   ADDI   r10, r0, 22
092:   ADDI   r11, r0, 10
093:   ADDI   r12, r0, 28
094:   ADDI   r13, r0, 48
# From here it's redacted

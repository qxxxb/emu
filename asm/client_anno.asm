# Prompt username {Enter at least 4 chars}
000:   ADDI   r1, r0, 30
001:   IO     r0, SERIAL_WRITE, r1
002:   ADDI   r1, r0, 28
003:   IO     r0, SERIAL_WRITE, r1
004:   ADDI   r1, r0, 14
005:   IO     r0, SERIAL_WRITE, r1
006:   ADDI   r1, r0, 27
007:   IO     r0, SERIAL_WRITE, r1
008:   ADDI   r1, r0, 23
009:   IO     r0, SERIAL_WRITE, r1
010:   ADDI   r1, r0, 10
011:   IO     r0, SERIAL_WRITE, r1
012:   ADDI   r1, r0, 22
013:   IO     r0, SERIAL_WRITE, r1
014:   ADDI   r1, r0, 14
015:   IO     r0, SERIAL_WRITE, r1
016:   ADDI   r1, r0, 53
017:   IO     r0, SERIAL_WRITE, r1
018:   ADDI   r1, r0, 36
019:   IO     r0, SERIAL_WRITE, r1
020:   LBL    512, 0
021:   IO     r1, SERIAL_INCOMING, r0
022:   CMPUL  r1, 4
023: + JUP    512, r0

# Save username to memory
024:   ADDI   r2, r0, 14
025:   IO     r10, SERIAL_READ, r0
026:   IO     r11, SERIAL_READ, r0
027:   IO     r12, SERIAL_READ, r0
028:   IO     r13, SERIAL_READ, r0

029:   LBL    513, 0
030:   IO     r1, SERIAL_READ, r0
031:   CMPEQ  r1, 62
032: - JUP    513, r0 # Read until newline

# Read from user input
033:   LBL    512, 0
034:   IO     r1, SERIAL_INCOMING, r0
035:   CMPEQ  r1, 0
036: + JDN    513, r0 # If we have no more bytes, recv from the connection

037:   IO     r1, SERIAL_READ, r0
038:   ST     [r2+0], r1 # Store starting r14
039:   ADDI   r2, r2, 1 # Increment index
040:   CMPNE  r1, 62
041: - ADDI   r1, r0, 36 # If it's a newline, make it into a space
042: - ADDI   r1, r0, 36 # Not sure why this is here twice
043: - ST     [r2+0], r1
044: + CMPUL  r2, 50 # If we've wrote past r50, don't send (just recv)
045: + JDN    513, r0

# Send bytes between r10 and [r2] (at least the username)
046:   ADDI   r3, r0, 10 # Start at username
047:   LBL    514, 0
048:   LD     r1, [r3+0]
049:   IO     r0, ENET_SEND, r1 # Send char
050:   ADDI   r3, r3, 1
051:   CMPUL  r3, r2
052: + JUP    514, r0

# Send spaces until r50 is reached
053:   ADDI   r1, r0, 36 # r1 = ' ' (space char)
054:   LBL    514, 0
055:   CMPUL  r3, 50
056: - JDN    514, r0 # Break if reached r50
057:   IO     r0, ENET_SEND, r1 # Send space
058:   ADDI   r3, r3, 1
059:   JUP    514, r0
060:   LBL    514, 0
061:   ADDI   r2, r0, 14 # Reset r2 to be register after username

# Recv from the connection
062:   LBL    513, 0
063:   IO     r1, ENET_INCOMING, r0
064:   CMPEQ  r1, 0
065: + JUP    512, r0 # If no bytes to receive, go read input from the user
066:   IO     r1, ENET_RECV, r0 # Otherwise, receive a char
067:   IO     r0, SERIAL_WRITE, r1 # Print it
068:   JUP    513, r0 # Loop
069:   JUP    512, r0 # This only reached from reverse (looped tape)

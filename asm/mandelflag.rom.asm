0000:   ADDI   r14, r0, 58
0001:   ADDI   r15, r0, 0
0002: - LBL    1027, 0
0003:   LBL    521, 0
0004:   ADDI   r12, r0, 56
0005:   ADDI   r13, r0, 0
0006:   LBL    522, 0
0007:   ADDI   r11, r0, 15
0008:   ADDI   r16, r0, 0
0009:   ADDI   r17, r0, 0
0010:   ADDI   r18, r0, 0
0011:   ADDI   r19, r0, 0
0012:   LBL    523, 0
0013: - LBL    1027, 0
0014:   ADDI   r3, r18, 0
0015:   ADDI   r4, r19, 0
0016:   ADDI   r5, r18, 0
0017:   ADDI   r6, r19, 0
0018:   ADDI   r63, r0, 1
0019:   JDN    1031, r0
0020:   LBL    1026, 1
0021:   CMPUG  r1, 31
0022: + JDN    1027, r0
0023:   ADDI   r20, r1, 0
0024:   ADDI   r21, r2, 0
0025:   SUB    r2, r0, r2
0026:   SUB    r1, r0, r1
0027:   CMPNE  r2, 0
0028: + ADDI   r1, r1, 63
0029:   ADDI   r22, r1, 0
0030:   ADDI   r23, r2, 0
0031:   ADDI   r3, r16, 0
0032:   ADDI   r4, r17, 0
0033:   ADDI   r5, r16, 0
0034:   ADDI   r6, r17, 0
0035:   ADDI   r63, r0, 2
0036:   JDN    1031, r0
0037:   LBL    1026, 2
0038:   CMPUG  r1, 31
0039: + JDN    1027, r0
0040:   ADD    r21, r21, r2
0041:   CMPUL  r21, r2
0042: + ADDI   r20, r20, 1
0043:   ADD    r20, r20, r1
0044:   CMPUG  r20, 31
0045: + LBL    1027, 0
0046: + JDN    524, r0
0047:   ADD    r23, r23, r2
0048:   CMPUL  r23, r2
0049: + ADDI   r22, r22, 1
0050:   ADD    r22, r22, r1
0051:   ADDI   r3, r18, 0
0052:   ADDI   r4, r19, 0
0053:   ADDI   r5, r16, 0
0054:   ADDI   r6, r17, 0
0055:   ADDI   r63, r0, 3
0056:   JDN    1031, r0
0057:   LBL    1026, 3
0058:   ADDI   r18, r1, 0
0059:   ADDI   r19, r2, 0
0060:   ADD    r19, r19, r2
0061:   CMPUL  r19, r2
0062: + ADDI   r18, r18, 1
0063:   ADD    r18, r18, r1
0064:   ADD    r17, r23, r13
0065:   CMPUL  r17, r13
0066: + ADDI   r22, r22, 1
0067:   ADD    r16, r22, r12
0068:   ADD    r19, r19, r15
0069:   CMPUL  r19, r15
0070: + ADDI   r18, r18, 1
0071:   ADD    r18, r18, r14
0072:   ADDI   r11, r11, 63
0073:   CMPNE  r11, 0
0074: + JUP    523, r0
0075:   LBL    524, 0
0076:   CMPUL  r11, 1
0077: + ADDI   r11, r0, 50
0078: + JDN    735, r0
0079:   CMPUG  4, r11
0080: + ADDI   r11, r0, 58
0081: + JDN    735, r0
0082:   CMPUL  r11, 9
0083: + ADDI   r11, r0, 38
0084: + JDN    735, r0
0085:   CMPUG  12, r11
0086: + ADDI   r11, r0, 59
0087: + JDN    735, r0
0088:   CMPUL  r11, 15
0089: + ADDI   r11, r0, 60
0090: + JDN    735, r0
0091:   CMPUG  18, r11
0092: + ADDI   r11, r0, 52
0093: + JDN    735, r0
0094:   ADDI   r11, r0, 36
0095:   LBL    735, 0
0096:   IO     r0, SERIAL_WRITE, r11
0097:   ADDI   r13, r13, 6
0098:   CMPUL  r13, 6
0099: + ADDI   r12, r12, 1
0100: - LBL    1027, 0
0101:   CMPNE  r12, 4
0102: + JUP    522, r0
0103:   ADDI   r1, r0, 62
0104:   IO     r0, SERIAL_WRITE, r1
0105:   ADDI   r15, r15, 12
0106:   CMPUL  r15, 12
0107: + ADDI   r14, r14, 1
0108:   CMPNE  r14, 6
0109: + JDN    521, r0
0110:   ADDI   r53, r0, 13
0111:   JDN    734, r0
0112: - LBL    1027, 0
0113:   LBL    1031, 0
0114:   ADDI   r8, r0, 0
0115:   ADDI   r1, r0, 0
0116:   ADDI   r2, r0, 0
0117:   CMPSL  r3, r0
0118: + XORI   r8, r8, 1
0119: + XORI   r4, r4, 63
0120: + XORI   r3, r3, 63
0121: + ADDI   r4, r4, 1
0122: + CMPEQ  r4, 0
0123: + ADDI   r3, r3, 1
0124:   CMPSL  r5, 0
0125: + XORI   r8, r8, 1
0126: + XORI   r6, r6, 63
0127: + XORI   r5, r5, 63
0128: + ADDI   r6, r6, 1
0129: + CMPEQ  r6, 0
0130: + ADDI   r5, r5, 1
0131:   SHLI   r7, r3, 2
0132:   SHLI   r9, r5, 2
0133:   FMU/0  r7, r9
0134:   ADDI   r9, r0, 0
0135:   ADD    r2, r2, r7
0136:   CMPUL  r2, r7
0137: + ADDI   r9, r9, 1
0138:   ADD    r7, r0, r3
0139:   FMU/2  r7, r6
0140:   ADD    r2, r2, r7
0141:   CMPUL  r2, r7
0142: + ADDI   r9, r9, 1
0143:   ADD    r7, r0, r4
0144:   FMU/2  r7, r5
0145:   ADD    r2, r2, r7
0146:   CMPUL  r2, r7
0147: + ADDI   r9, r9, 1
0148:   ADD    r7, r0, r4
0149:   FMU/8  r7, r6
0150:   ADD    r2, r2, r7
0151:   CMPUL  r2, r7
0152: + ADDI   r9, r9, 1
0153:   ADDI   r1, r9, 0
0154:   ADDI   r9, r0, 0
0155:   ADD    r7, r0, r3
0156:   FMU/2  r7, r5
0157:   ADD    r1, r1, r7
0158:   CMPUL  r1, r7
0159: + JUP    1027, r0
0160:   ADD    r7, r0, r3
0161:   FMU/8  r7, r6
0162:   ADD    r1, r1, r7
0163:   CMPUL  r1, r7
0164: + JUP    1027, r0
0165:   ADD    r7, r0, r4
0166:   FMU/8  r7, r5
0167:   ADD    r1, r1, r7
0168:   CMPUL  r1, r7
0169:   ADDI   r52, r0, 23
0170: + JDN    1027, r0
0171:   ADDI   r9, r3, 0
0172:   FMU/8  r9, r5
0173:   CMPNE  r9, 0
0174: + JDN    1027, r0
0175:   CMPNE  r8, 0
0176: + XORI   r2, r2, 63
0177: + XORI   r1, r1, 63
0178: + ADDI   r2, r2, 1
0179: + CMPEQ  r2, 0
0180: + ADDI   r1, r1, 1
0181:   JUP    1026, r63
0182:   LBL    734, 0
0183:   ADDI   r1, r0, 17
0184:   IO     r0, SERIAL_WRITE, r1
0185:   ADDI   r1, r0, 14
0186:   IO     r0, SERIAL_WRITE, r1
0187:   ADDI   r1, r0, 34
0188:   IO     r0, SERIAL_WRITE, r1
0189:   ADDI   r1, r0, 62
0190:   IO     r0, SERIAL_WRITE, r1
0191:   IO     r0, CLOCK_HI_CS, r1
0192:   LBL    1536, 0
0193:   IO     r1, CLOCK_HI_CS, r0
0194:   CMPUG  r1, 1
0195: - JUP    1536, r0
0196:   ADDI   r1, r0, 17
0197:   IO     r0, SERIAL_WRITE, r1
0198:   ADDI   r1, r0, 14
0199:   IO     r0, SERIAL_WRITE, r1
0200:   ADDI   r1, r0, 34
0201:   IO     r0, SERIAL_WRITE, r1
0202:   ADDI   r1, r0, 36
0203:   IO     r0, SERIAL_WRITE, r1
0204:   ADDI   r51, r0, 14
0205:   ADDI   r1, r0, 20
0206:   IO     r0, SERIAL_WRITE, r1
0207:   ADDI   r1, r0, 18
0208:   IO     r0, SERIAL_WRITE, r1
0209:   ADDI   r1, r0, 13
0210:   IO     r0, SERIAL_WRITE, r1
0211:   ADDI   r1, r0, 62
0212:   IO     r0, SERIAL_WRITE, r1
0213:   IO     r0, CLOCK_HI_CS, r1
0214:   LBL    1536, 0
0215:   IO     r1, CLOCK_HI_CS, r0
0216:   CMPUG  r1, 1
0217: - JUP    1536, r0
0218:   ADDI   r1, r0, 32
0219:   IO     r0, SERIAL_WRITE, r1
0220:   ADDI   r1, r0, 10
0221:   IO     r0, SERIAL_WRITE, r1
0222:   ADDI   r1, r0, 23
0223:   IO     r0, SERIAL_WRITE, r1
0224:   ADDI   r1, r0, 29
0225:   IO     r0, SERIAL_WRITE, r1
0226:   ADDI   r1, r0, 36
0227:   IO     r0, SERIAL_WRITE, r1
0228:   ADDI   r1, r0, 28
0229:   IO     r0, SERIAL_WRITE, r1
0230:   ADDI   r1, r0, 30
0231:   IO     r0, SERIAL_WRITE, r1
0232:   ADDI   r1, r0, 22
0233:   IO     r0, SERIAL_WRITE, r1
0234:   ADDI   r1, r0, 60
0235:   IO     r0, SERIAL_WRITE, r1
0236:   IO     r0, SERIAL_WRITE, r1
0237:   IO     r0, SERIAL_WRITE, r1
0238:   IO     r0, CLOCK_HI_CS, r1
0239:   LBL    1536, 0
0240:   IO     r1, CLOCK_HI_CS, r0
0241:   CMPUG  r1, 1
0242: - JUP    1536, r0
0243:   ADDI   r1, r0, 15
0244:   IO     r0, SERIAL_WRITE, r1
0245:   ADDI   r1, r0, 21
0246:   IO     r0, SERIAL_WRITE, r1
0247:   ADDI   r1, r0, 10
0248:   IO     r0, SERIAL_WRITE, r1
0249:   ADDI   r1, r0, 16
0250:   IO     r0, SERIAL_WRITE, r1
0251:   ADDI   r1, r0, 53
0252:   IO     r0, SERIAL_WRITE, r1
0253:   ADDI   r1, r0, 36
0254:   IO     r0, SERIAL_WRITE, r1
0255:   ADDI   r1, r0, 62
0256:   IO     r0, SERIAL_WRITE, r1
0257:   LBL    1537, 0
0258:   IO     r1, SERIAL_INCOMING, r0
0259:   CMPUG  r1, 3
0260: - JUP    1537, r0
0261:   IO     r60, SERIAL_READ, r0
0262:   IO     r61, SERIAL_READ, r0
0263:   IO     r0, SERIAL_READ, r0
0264:   IO     r0, SERIAL_READ, r0
0265:   ADDI   r2, r0, 0
0266:   LBL    1539, 0
0267:   ADD    r1, r2, r60
0268:   ADDI   r63, r0, 1
0269:   JDN    1538, r0
0270:   LBL    1540, 1
0271:   ADD    r3, r0, r1
0272:   XOR    r1, r2, r61
0273:   ADDI   r63, r0, 2
0274:   JDN    1538, r0
0275:   LBL    1540, 2
0276:   SUB    r3, r3, r1
0277:   IO     r0, SERIAL_WRITE, r3
0278:   ST     [r2+40], r3
0279:   ADDI   r2, r2, 1
0280:   CMPEQ  r2, 12
0281: - JUP    1539, r0
0282:   ADDI   r1, r0, 0
0283:   ADDI   r50, r0, 16
0284:   LBL    1539, 0
0285:   LD     r2, [r1+50]
0286:   IO     r0, SERIAL_WRITE, r2
0287:   ADDI   r1, r1, 1
0288:   CMPEQ  r1, 4
0289: - JUP    1539, r0
0290:   ADDI   r1, r0, 10
0291:   ADDI   r2, r0, 30
0292:   ADDI   r3, r0, 50
0293:   ADDI   r4, r0, 53
0294:   ADDI   r5, r0, 62
0295:   ADDI   r6, r0, 21
0296:   ADDI   r10, r0, 0
0297:   LBL    1539, 0
0298:   ADDI   r7, r0, 0
0299:   ADDI   r12, r0, 0
0300:   LBL    1541, 0
0301:   SHLI   r7, r7, 1
0302:   LD     r8, [r12+1]
0303:   ANDI   r8, r8, 1
0304:   OR     r7, r7, r8
0305:   LD     r8, [r12+1]
0306:   SHRI   r8, r8, 1
0307:   ST     [r12+1], r8
0308:   ADDI   r12, r12, 1
0309:   CMPEQ  r12, 6
0310: - JUP    1541, r0
0311:   IO     r0, SERIAL_WRITE, r7
0312:   ADDI   r10, r10, 1
0313:   CMPEQ  r10, 6
0314: - JUP    1539, r0
0315:   JUP    1542, r0
0316:   LBL    1543, 0
0317:   HLT
0318:   LBL    1538, 0
0319:   CMPEQ  r1, 35
0320: + XORI   r1, r1, 40
0321: + JUP    1540, r63
0322:   CMPEQ  r1, 29
0323: + XORI   r1, r1, 41
0324: + JUP    1540, r63
0325:   CMPEQ  r1, 34
0326: + XORI   r1, r1, 52
0327: + JUP    1540, r63
0328:   CMPEQ  r1, 16
0329: + XORI   r1, r1, 8
0330: + JUP    1540, r63
0331:   CMPEQ  r1, 12
0332: + XORI   r1, r1, 54
0333: + JUP    1540, r63
0334:   CMPEQ  r1, 13
0335: + XORI   r1, r1, 5
0336: + JUP    1540, r63
0337:   CMPEQ  r1, 50
0338: + XORI   r1, r1, 18
0339: + JUP    1540, r63
0340:   CMPEQ  r1, 0
0341: + XORI   r1, r1, 7
0342: + JUP    1540, r63
0343:   CMPEQ  r1, 42
0344: + XORI   r1, r1, 35
0345: + JUP    1540, r63
0346:   CMPEQ  r1, 49
0347: + XORI   r1, r1, 21
0348: + JUP    1540, r63
0349:   CMPEQ  r1, 48
0350: + XORI   r1, r1, 11
0351: + JUP    1540, r63
0352:   CMPEQ  r1, 31
0353: + XORI   r1, r1, 54
0354: + JUP    1540, r63
0355:   CMPEQ  r1, 14
0356: + XORI   r1, r1, 59
0357: + JUP    1540, r63
0358:   CMPEQ  r1, 28
0359: + XORI   r1, r1, 43
0360: + JUP    1540, r63
0361:   CMPEQ  r1, 18
0362: + XORI   r1, r1, 20
0363: + JUP    1540, r63
0364:   CMPEQ  r1, 61
0365: + XORI   r1, r1, 3
0366: + JUP    1540, r63
0367:   CMPEQ  r1, 7
0368: + XORI   r1, r1, 4
0369: + JUP    1540, r63
0370:   CMPEQ  r1, 53
0371: + XORI   r1, r1, 34
0372: + JUP    1540, r63
0373:   CMPEQ  r1, 51
0374: + XORI   r1, r1, 32
0375: + JUP    1540, r63
0376:   CMPEQ  r1, 54
0377: + XORI   r1, r1, 44
0378: + JUP    1540, r63
0379:   CMPEQ  r1, 23
0380: + XORI   r1, r1, 43
0381: + JUP    1540, r63
0382:   CMPEQ  r1, 63
0383: + XORI   r1, r1, 29
0384: + JUP    1540, r63
0385:   CMPEQ  r1, 9
0386: + XORI   r1, r1, 16
0387: + JUP    1540, r63
0388:   CMPEQ  r1, 26
0389: + XORI   r1, r1, 30
0390: + JUP    1540, r63
0391:   CMPEQ  r1, 59
0392: + XORI   r1, r1, 46
0393: + JUP    1540, r63
0394:   CMPEQ  r1, 3
0395: + XORI   r1, r1, 14
0396: + JUP    1540, r63
0397:   CMPEQ  r1, 6
0398: + XORI   r1, r1, 45
0399: + JUP    1540, r63
0400:   CMPEQ  r1, 32
0401: + XORI   r1, r1, 31
0402: + JUP    1540, r63
0403:   CMPEQ  r1, 2
0404: + XORI   r1, r1, 42
0405: + JUP    1540, r63
0406:   CMPEQ  r1, 41
0407: + XORI   r1, r1, 6
0408: + JUP    1540, r63
0409:   CMPEQ  r1, 25
0410: + XORI   r1, r1, 41
0411: + JUP    1540, r63
0412:   CMPEQ  r1, 55
0413: + XORI   r1, r1, 14
0414: + JUP    1540, r63
0415:   CMPEQ  r1, 20
0416: + XORI   r1, r1, 58
0417: + JUP    1540, r63
0418:   CMPEQ  r1, 10
0419: + XORI   r1, r1, 15
0420: + JUP    1540, r63
0421:   CMPEQ  r1, 27
0422: + XORI   r1, r1, 45
0423: + JUP    1540, r63
0424:   CMPEQ  r1, 11
0425: + XORI   r1, r1, 10
0426: + JUP    1540, r63
0427:   CMPEQ  r1, 4
0428: + XORI   r1, r1, 25
0429: + JUP    1540, r63
0430:   CMPEQ  r1, 58
0431: + XORI   r1, r1, 53
0432: + JUP    1540, r63
0433:   CMPEQ  r1, 36
0434: + XORI   r1, r1, 52
0435: + JUP    1540, r63
0436:   CMPEQ  r1, 60
0437: + XORI   r1, r1, 48
0438: + JUP    1540, r63
0439:   CMPEQ  r1, 56
0440: + XORI   r1, r1, 56
0441: + JUP    1540, r63
0442:   CMPEQ  r1, 8
0443: + XORI   r1, r1, 34
0444: + JUP    1540, r63
0445:   CMPEQ  r1, 22
0446: + XORI   r1, r1, 24
0447: + JUP    1540, r63
0448:   CMPEQ  r1, 19
0449: + XORI   r1, r1, 17
0450: + JUP    1540, r63
0451:   CMPEQ  r1, 37
0452: + XORI   r1, r1, 55
0453: + JUP    1540, r63
0454:   CMPEQ  r1, 17
0455: + XORI   r1, r1, 5
0456: + JUP    1540, r63
0457:   CMPEQ  r1, 46
0458: + XORI   r1, r1, 13
0459: + JUP    1540, r63
0460:   CMPEQ  r1, 39
0461: + XORI   r1, r1, 22
0462: + JUP    1540, r63
0463:   CMPEQ  r1, 30
0464: + XORI   r1, r1, 15
0465: + JUP    1540, r63
0466:   CMPEQ  r1, 57
0467: + XORI   r1, r1, 31
0468: + JUP    1540, r63
0469:   CMPEQ  r1, 44
0470: + XORI   r1, r1, 30
0471: + JUP    1540, r63
0472:   CMPEQ  r1, 5
0473: + XORI   r1, r1, 30
0474: + JUP    1540, r63
0475:   CMPEQ  r1, 24
0476: + XORI   r1, r1, 43
0477: + JUP    1540, r63
0478:   CMPEQ  r1, 40
0479: + XORI   r1, r1, 16
0480: + JUP    1540, r63
0481:   CMPEQ  r1, 21
0482: + XORI   r1, r1, 31
0483: + JUP    1540, r63
0484:   CMPEQ  r1, 33
0485: + XORI   r1, r1, 13
0486: + JUP    1540, r63
0487:   CMPEQ  r1, 45
0488: + XORI   r1, r1, 51
0489: + JUP    1540, r63
0490:   CMPEQ  r1, 52
0491: + XORI   r1, r1, 19
0492: + JUP    1540, r63
0493:   CMPEQ  r1, 43
0494: + XORI   r1, r1, 22
0495: + JUP    1540, r63
0496:   CMPEQ  r1, 47
0497: + XORI   r1, r1, 51
0498: + JUP    1540, r63
0499:   CMPEQ  r1, 15
0500: + XORI   r1, r1, 42
0501: + JUP    1540, r63
0502:   CMPEQ  r1, 1
0503: + XORI   r1, r1, 44
0504: + JUP    1540, r63
0505:   CMPEQ  r1, 38
0506: + XORI   r1, r1, 7
0507: + JUP    1540, r63
0508:   CMPEQ  r1, 62
0509: + XORI   r1, r1, 33
0510: + JUP    1540, r63
0511:   LBL    1542, 0
0512:   XORI   r40, r40, 58
0513:   XORI   r41, r41, 18
0514:   XORI   r42, r42, 27
0515:   XORI   r43, r43, 11
0516:   XORI   r44, r44, 18
0517:   XORI   r45, r45, 1
0518:   AND    r1, r1, r0
0519:   LBL    1539, 0
0520:   LD     r2, [r1+40]
0521:   IO     r0, SERIAL_WRITE, r2
0522:   ADDI   r1, r1, 1
0523:   CMPNE  r1, 6
0524: + JUP    1539, r0
0525:   JUP    1543, r0

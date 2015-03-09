#!/usr/bin/python3

C1 = [0x50, 0x2b, 0xd2, 0xa4, 0xa4, 0x7f, 0x41]

C2 = [0x44, 0x2b, 0xd2, 0xa0, 0xa2, 0x71, 0x5f]

def xor(xs, ys):
    return [x ^ y for x, y in zip(xs, ys)]

X = xor(C1, C2) # X = M1 xor M2

def breakCode():
    words = open('/usr/share/dict/words', 'r').read().split()
    words = [w.upper().encode() for w in words if len(w) == len(X)] 
    for M1 in words:
        M2 = bytes(xor(M1, X))
        if M2 in words:
            pad = xor(M1, C1)
            print('M1 = %s, M2 = %s, pad = %s' % (M1, M2, pad))

breakCode()

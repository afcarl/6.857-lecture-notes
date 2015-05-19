from Crypto.Cipher import AES

SECRETKEY = 'This is a key...'
SECRETIV = 'This is an IV...'

def encrypt(message):
    cipher = AES.new(SECRETKEY, AES.MODE_CBC, SECRETIV)
    padlen = 16 - (len(message) % 16)
    pad = bytes([padlen]) * padlen
    return cipher.encrypt(message + pad)

def decrypt(ciphertext):
    cipher = AES.new(SECRETKEY, AES.MODE_CBC, SECRETIV)
    message = cipher.decrypt(ciphertext)
    padlen = message[-1]
    return message[:-padlen]

def valid(ciphertext):
    cipher = AES.new(SECRETKEY, AES.MODE_CBC, SECRETIV)
    message = cipher.decrypt(ciphertext)
    padlen = message[-1]
    pad = bytes([padlen]) * padlen
    return message[-padlen:] == pad

TARGET = b'\xf9\xa5\xf0}5\xf7p\x14,\x92\xa6q"\xeb{q\xff\xd0gU|?7\xb6-/\x05|g\x00\xddL'

def guessLastByte(ciphertext):
    c1 = list(ciphertext[0:16])
    for guess in range(256):
        c1[15] = ciphertext[15] ^ guess ^ 0x01
        challenge = bytes(c1) + ciphertext[16:32]
        if guess != 0x01 and valid(challenge):
            return guess

def guessNext(ciphertext, guesses):
    c1 = list(ciphertext[0:16])
    gs = len(guesses)
    padlen = gs + 1
    for j in range(gs):
        c1[15-j] = ciphertext[15-j] ^ guesses[gs-j-1] ^ padlen

    for guess in range(256):
        c1[15-gs] = ciphertext[15-gs] ^ guess ^ padlen
        challenge = bytes(c1) + ciphertext[16:32]
        if valid(challenge):
            return guess

def guessAll(ciphertext):
    gs = [guessLastByte(ciphertext)]
    for block in range(15):
        g = guessNext(ciphertext, gs)
        gs = [g] + gs
    return gs

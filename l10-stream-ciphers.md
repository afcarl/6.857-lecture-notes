Today: Stream Ciphers, Monday. March 9th, 2015
==============================================

 - Stream ciphers
   + Definitions
   + RC4 and Spritz
   + ChaCha
     - Dan Bernstein

PRNGS
-----

If you remember the One-time pad (OTP), we had a message `m` of length 
`n` and a pad `p` of length `n` and we computed the ciphertext `c` by 
computing `c = m \xor p` for all `n` bits.

However, it's very hard to come up with the pad.

**TODO:** transmitting a secert as long as the message is equivalent
to transmitting the message

            pseudo-random generator G

                       ----- 
        key or seed -> | G | -> pad
                       -----
            {0,1}^n             {0,1}^l(n)
                                 l(n) > n

**Definition:** `G` is a _pseudo-random generator (PRG)_ if no adversary can 
distinguish between a string `x` drawn randomly from `{0,1}^l(n)` 
(ideal situation) and the output of the program `G(s)`, 
where `s <- {0,1}^n` with probability better than `1/2 + negl(n)`

 + Remember `negl(n)` is a function that goes to zero faster than any
   inverse polynomial function of `n`


Stream ciphers
--------------

Stream cipher is a PRG
 
 - but has a long-term `K` from short-term key (nonce)

May be counter based:

            -----
            | i | <- + 1
            -----
              |
             \ /
              .
            -----
        k ->| G |
            -----
              |
             \ /
              .
            Output 
             pad

May be state based:

                   <-----------------------\
            ---------                       \
            | state |    next state fn f    |
            ---------                       |
                    \-----------------------/
                |
               \ /          initial state
                .           is the key K
            ---------
            |   G   |
            ---------
                |
               \ /
                .
            output bytes

Spritz - A spongy RC4-like stream cipher
----------------------------------------

### RC4

 - Was a 1987 design.
 - Works for any set of `N` bytes: `Z_n = {0, 1, ..., N-1}`
   (All math is `mod N`). Default `N = 256`
 - State consists of 
   + Two _mod N pointers_ `i` and `j`
   + a permutation `S` of `Z_n`
 - one of the purpose of designing RC4 was for it to have a lot
   of state so that you couldn't build a chip that can store it
 - Key Setup Algorithm initializes `S` from key `K`
 - PRG updates state and generate output

RC4-PRG:

    RC4_PRG():
        i = i + 1               // update state
        j = j + S[i]
        Swap(S[i], S[j])
        z = S[S[i]+S[j]]        // generate output
        return z

 - Heuristically designed
 - No proof of security here
 - Note this is an invertible function, so this is _not good_ because
   given a state, an attacker could trace back and figure out previous
   states, ultimately leading to the key
   + Fortunately, it's hard to get the state

RC4-KSA (key K = `L` values on `N` bits (`|k| = L` bytes when `N = 256`)):

    RC4_KSA(k):
        S[0 ... N-1] = [0 ... N-1]
        j = 0
        for i = 0; to N-1:
            j = j + S[i] + K[i mod L]
            Swap(S[i], S[j])
        i = j = 0

Vulnerabilities:

 - Key-dependent biases of initial output
 - Key collisions (producing same internal state) is possible
 - Key recovery possible from known internal state
 - Related-key attacks (WEP)
 - State recovery from known output (feasible?)
   + i.e. given a million bytes of output, can your recover the
     internal state?
   + so far doesn't seem feasible
 - Output biases `=>` distinguishers

### Spritz

 - Design started after CRYTPO2013 (Really after AlFarden, ..., and 
   Schuldt, USENIX 2013)
 - Design retained the RC4 style (a few registers plus a permutation 
   `S`)
 - Goal is to minimize statistical vulnerabilities
 - Redo key setup entirely
  - Expand API to have "spongy" interface
    + TODO: Absorb entropy?
 - Design for Spritz did a computer-aided search w/ statistic testing
   to find a good function `G`

Code:

    SPRITZ_PRG():
        i = i + w
        j = k + S[j + S[i]]
        k = i + k + S[j]
        Swap(S[i], S[j])
        z = S[j + S[i + S[z+k]]]
        return z

 - `w` is always relatively prime to `N`
 - `z` is used as feedback (see line before `return z`)

Initialization:

 - `S` is the identity permutation
 - `i = j = k = 0`
 - `z = 0`
 - "Number of nibbles absorbed" var. `a` set to 0
 - Step size `w` is initialized to 1

Code:

    SQUEEZE(r):
        if a > 0:
            SHUFFLE()
        P = new array of size r
        for v = 0 to r-1
            p[v] = SPRITZ_PRG
        return p

    ENCRYPT(k, m):
        KEYSETUP(K)
        C = M + SQUEEZE(M.length)
        return C
    KEYSETUP(k):
        InitializeState()
        ABSORB(k)

 - `Absorb` takes an arbitrary sequence of `k` bytes as input 

Spritz can also be used as a hash function!

### ChaCha

 - Recently picked-up by Google as a replacement for RC4 in OpenSSL
 - Nice and simple designs

            --------------
           |512 bit state |
            --------------
                 |
                 | <-----
                 |      |
              ChaCha|   |
                 |      |
                ---     |
               | + |-----
                ---
                 |
                \ /
                 .

State is `4 x 4 x 32 bit` matrix, each cell indexed from `0, ..., 15`

    c | c | c | c  constant 128bit
    -- --- --- --
    k | k | k | k  key 256bit
    -- --- --- -- 
    k | k | k | k
    -- --- --- --
    n | n | n | n  nonce counter 128bit

It's called ChaCha20 because it has 20 rounds, broken up into quarter rounds (QRs).

This is a style of design called ARX design: Additions, Rotations and XOR
    
 - nice to use ARX because operations are constant time and you do not
   tend to be vulnerable to timing or side channel attacks

Code:

    QR(a,b,c,d):
        a += b; d ^= a; d <<<= 16
        c += d; b ^= c; b <<<= 12
        a += b; d ^= a; d <<<= 8
        c += d; b ^= c; b <<<= 7

You can imagine applying this to a column of this matrix.

    Round 1:
    QR(0, 4, 8, 12)   # the first column
    QR(1, 5, 9, 13)   
    QR(2, 6, 10, 14)
    QR(3, 7, 11, 15)

    Round 2
    QR(0, 5, 10, 15)  # the main diagonal
    QR(1, 6, 11, 12)  # just above the main diagonal
    QR(2, 7, 8, 13)
    QR(3, 4, 9, 14)

Round 1 and round 2 are a _double round_

ChaCha20 has 10 double rounds

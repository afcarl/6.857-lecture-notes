Today: Digital signatures, Monday, April 6th
============================================

Digital signature
 
 - Definition
 - Security definition
 - Hash & sign
 - RSA PKCS & PSS
 - ElGamal
 - Digital Signature Algorithm (DSA)

Digital signatures
------------------

An amazing development first due to Diffie and Hellman ("New directions in
public key cryptography" paper)


    Alice           m, s = sig(SK, m)           Bob
        ---------------------------------------->   verify(m, PK, s)

Original Diffie Hellman idea: public key maps a plaintext to a ciphertext, and
secret key unmaps.

    Keygen(1^l) -> PK (verification key), SK (signing key)
    
    Sign(SK, m) -> s_SK(m)
     - this process may be randomized
     - apparently no reason to have deterministic signatures

    Verify(PK, m, s) -> true/false

    \forall m, Verify(PK, m, Sign(SK, m)) -> true
    
### (Weak) existential unforgeability under an adaptive chosen message attack

Game:
 
 1. Challenger generates `(PK, SK)` keypair, sends `PK` to adversary
 2. Adversary can get signatures to messages of his choice
    - `m1, m2, ..., mq`
    - he can repeat messages, no requirements
    - he gets back `s_i = Sign(SK, m)` for each `m_i`
 3. Here `q = poly(l)`, `m_i` may depend on signatures to previous messages
 4. Adversary outputs his attempt at a forgery: a pair `(m, s*)`
 5. Adversary wins if Bob accepts it: `Verify(PK, m, s*) \and m \notin` the set
    of previously queried messages

This scheme is secure if `Prob[Adversary wins] = negl(l)`

The **strong** version, allows the message of the forgery to be one of the
messages the adversary previously asked for as long as the forged signature
is different than the one the adversary received.

Hash & sign
-----------

Early on it became obvious that you should not encrypt or sign full messages,
because public key schemes were slow `=>` sign `h(m)` rather than `m`

As long as the hash function is _collision-resistant_, and it's hard to find `m1
& m2`, s.t. `h(m1) = h(m2)`, a signature for `m1` is guaranteed to be for `m1`
only.

RSA-PKCS (public key cryptography standards)
--------------------------------------------

To sign `M`, compute `m = h(M)`. Need to create a particular message that will
fit into an RSA block.

We can define `pad(m) = 0x 00 01 FF .. FF 00 || hash_name || m`

 - we need a way to specify the hash function, so that Bob will know what
   hash function to use to verify the signature
   + hash functions could be changed because they get broken (like MD5)
 - `hash_name` is in ASN.1 (abstract syntax notation 1) form


Signing:

    RsaSign(SK = (d, n), m) = pad(m)^d (mod n)

No proof of security here... Not that used much anymore, because OAEP has a proof
of security.

Probabilistic signature scheme (PSS), by Bellare and Rogaway, 1996
------------------------------------------------------------------

 - One of the first one that met the security definition
 - RSA based
 - Randomized

Diagram:

        -----------------       ---------
        |       m       |       |   r   |
        -----------------       ---------
            \                       /
             \                     /| 
            -----                 / |
            | h | <--------------/  |
            -----                   |
              |      /----| g1 |--->+ 
             \|     /               |
              w----/                |
              \                    \|
               \                    r*
                \---------------------------> | g2 |
                                                |
                                               \|
        ---------------------------------------------
        0       w                   r*          g2(w)
        ---------------------------------------------
                            |
                            |y
                           \|
                           -----
                          | RSA |
                           -----
                            |
                           \|

                           Sign(m) = y^d (mod n)

Anytime you see a little bit of randomization you have to ask the question of 
what will happen if the users don't have good enough random generators.

Sign, `|w| = k, |r| = k0`:

    r <-R- {0,1}^k_0
    w <- h(M||r)
    r* <- g1(w) \xor r
    y <- 0 || w || r* || g2(w)
    output s(m) = y^d mod n

Verify:

    y <- s(m)^e (mod n)
    parse y as b || w || r* || g2w
    r <- r* \xor g1(w)
    return true if b = 0 && h(m||r) == w && g2(w) == g2w

**Theorem:** PSS is weakly-existentially unforgeable under an adaptive chosen
message attack in the Random Oracle Model if RSA is not invertible on random 
inputs

ElGamal Digital Signatures
--------------------------

    large prime p, generator g of Z_p*
        - public

    h is collision-resistant, outputs value in Z_p-1

    Keygen(1^l):
        x <-R- {0, 1, ..., p-2}
        sk <- x
        pk <- y = g^x (mod p)

    Sign(M):
        m = h(M)
        k <- R - Z_{p-1}*, s.t. gcd(k, p-1) = 1
         - because we will need to compute the multiplicative inverse of k
           in Z_{p-1}*
        r = g^k (mod p)
        s = (m-r*x)/k (mod p-1)
         - sort of shifting domains here

        s(M) = (r, s)

    Verify(M, y = g^x, (r, s)):
        ensure that 0 < r < p
        ensure that y^r * r^s = g^m (mod p)

Why does verification work?

    y^r = g^(rx)
    r^s = (g^k)^s = g^k*((m-rx)/k) = g^(m-r*x)

    y^r * r^s = g^(rx + m - rx) = g^m (mod p)
    
    or alternatively,
    y^r * r^s = g^m (mod p) <=> g^(rx) * g^(sk) = g^m (mod p) <=>
    rx + sk = m (mod p-1) <=> s = (m-rx)/k

Why the p-1? The order of `g` is `p-1`, so things repeat after raising `g^{p-1} = 1`

Can you forge signatures? Yes you can. 

Note that the identity function is CR hash function.

**Theorem:** ElGamal digital signatures are existentially forgeable.  
**Proof:** 

 - Pick `h(x) = x` as the hash function
 - Pick `e <-R- Z_p-1`
 - Pick `r <- g^e * y (mod p)` (`y = g^x` is the PK of the guy whose signature we are forging)
 - Pick `s <- -r (mod p)`
 - Claim that `(r, s)` is a valid signature for `e*s`

Is `y^r * r^s = g^m`? `g^xr * (g^e * y)^-r = g^-er = g^es = g^m`

This is bad. It seems that we need more from our hash function, not just CR.

**Fix:**  
    
    Sign(M):
        k <- R - Z_{p-1}*, s.t. gcd(k, p-1) = 1
         - because we will need to compute the multiplicative inverse of k
           in Z_{p-1}*
        r = g^k (mod p)
        m = h(M||r)
        s = (m-r*x)/k (mod p-1)
         - sort of shifting domains here

        s(M) = (r, s)

**Theorem:** Modified ElGamal is existentially unforgeable against adaptive
chosen message attack in the Random Oracle Model assuming discrete log problem
(DLP) is hard.

Foundation for other schemes, such as the DSA scheme.

Digital Signature Algorithm
---------------------------

Read [DSA FIPS standard here](papers/dsa.pdf).

 - DSA (NIST 1991)
 - based on ElGamal
 - had the same bug as ElGamal
 - assuming DLP is hard

Diagram:

    p = nq+1, p is a large prime
    |q| = 160 bits
    |p| = 1024 bits

    end up with 320-bit signature

    g0 generates Z_p*
    g = g0^n generates subgroup G_q of order q
     - hard to tell appart G_q and Z_p*, given a random element

    x <--R-- Z_q*       // 160 bits, x \in [1, q) (not in G_q)
    y <-- g^x mod p     // 1024 bits

    SK = x, PK = y

    Sign(M):
        k <--R-- Z_q*               // 1 <= k < q
        r <-- ((g^k mod p) mod q)   // |r| = 160 bits

        m <-- h(M)

        s <-- (m+rx)/k mod q        // + instead of -, |s| = 160 bits
        redo if r = 0 or s = 0

        output (r, s)

    Verify(M, r, s):
        m <-- h(M)

        check that 0 < r < q & 0 < s < q 

        check that y^(r/s) g^(m/s) (mod p)(mod q) = r

        [ note that s = (rx + m)/k and r = g^k
          y^(r/s) = g^(rx/s) =>
          y^(r/s) * g^(m/s) = g^(rx + m)/s = g^(m+rx)/((m+rx/k)) = g^k = r ]
          

As before, it's forgeable with certain hash functions. Fix is the same.

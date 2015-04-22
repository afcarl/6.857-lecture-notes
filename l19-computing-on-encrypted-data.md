Today: Computing on Encrypted Data, Wed., April 22nd
====================================================

Guest lecture by Vinod Vaikuntanathan

Intro
-----

Traditional encryption is "all-or-nothing": put the secret message in a locked
box, send it to the person. If he has the key he can decrypt, otherwise he can't
do anything.

Non-malleable encryption: if adversary intercepts ciphertext he cannot do anything
(flip bits, etc) or learn anything from it.

Encryption for cloud computing
------------------------------

You want to compute a function `F` over the encrypted data of an user. But the
user wants its privacy.

Fully homomorphic encryption (FHE), by Rivest, Adleman, Dertouzos (1978):

                    Enc(Data)
                <--------------    
    Cloud                           user
                    Enc(F(Data))
                --------------->

They had no solution for FHE, just an idea that it might be possible.

Classes of computation:

 - fully = any function F
   + for the moment, we think about circuits as the model of computation
     - (boolean, arithmetic, doesn't matter)
     - doesn't support loops whose condition depends on input variables
       + but can get around it by trying a loop for 10 iterations on the FHE
         side, then client-side can tell FHE side that it did not get the 
         correct answer (not clear how it would verify correctness?) => then
         FHE side can retry
 - additive = only additions
 - multiplicative = only multiplications
 - somewhat = circuits of small depth

Gentry, 2009 introduced the first FHE construction.

Outline
-------

 - multiplicative homorphism (ElGamal)
   + `E(x1), E(x2) => E(x1+x2)`
 - additive homomorphisms (Goldwasser Micalli)
   + `E(x1), E(x2) => E(x1*x2)`
 - FHE

If we have addition and multiplication, then we have FHE.

For over 30 years we knew how to do addition and multiplication, but within 
different encryption schemes => no FHE

ElGamal
-------

We've seen it before in class.

    Enc(m1): (g^r1, y^r1*m1)
    Enc(m2): (g^r2, y^r2*m1)
    ------------------------
    Enc(m2*m2): (g^(r2*r1), y^(r2*r1)*m1*m2)

GM
--

Public key: `N = pq, y = non-square mod N`
Secret key: factorization of `N`

In `Z_N*` some numbers can be written as squares and others can't.
 
 + `Z_n*` is the set of all numbers `x, s.t gcd(x,n) = 1`

Encryption:

    Enc(0): r^2 mod N
    Enc(1): y* r^2 mod N

Computationally hard to distinguish between squares and non-squares in `Z_N*`,
unless you know the factorization of `N`

XOR homomorphic, just multiply the ciphertexts:
    
 - square(0) * square(0) = square(0)
 - non-square(1) * square(0)  = non-square(1)
 - square(0) * non-square(1) = square(1)
 - non-square(1) * non-square(1) = square(0)

Other HE schemes
----------------

Additive for numbers larger than 1 bit
 
 - Paillier
 - Damgard-Jurik

Additions + a single multiplication

 - Boneh-Goh-Nissim (based on gap groups)

How to construct an FHE scheme
------------------------------

Step 1: Somewhat homomorphic encryption (SwHE): We know how to do additions and just
one multiplications. Can we extend it to 10 multiplications? Or more?

 - `n` security parameter, SwHE lets you compute circuits of depth `d = \epsilon*log(n)`

Step 2: Bootstrapping theorem (Gentry 2009): Says that "homomorphic-enough" encryption `=>*` FHE

Homomorphic-enough means that the scheme can evaluate a deep enough circuit. Deep
enough means the scheme can evaluate its own decryption circuits (plus some).
Note that decryption circuits are well-defined and don't have unbounded loops.

Step 3: Depth boosting / Modulus reduction: Takes a SwHE scheme that can
compute `log(n)` circuits and boosts it to `O(n)` circuits.

The NTRU encryption scheme
--------------------------

Central characters: ring (add and multiply) of polynomials modulo `q` of bounded
degree (when you multiply two polynomials, the degree grows, but reduction modulo `q` helps reduce it)

Polynomials of degree less than `n`

Example (q = 11):

 - addition is modulo 11 for the coefficients
 - multiplications is modulo (11, x^4 + 1)

Ring: `R_q := Z_q[X] / (x^n + 1)`

    KeyGen():
        sample two "small" polynomials, `f, g \in R_q` with coefficients `<= B` ,
        s.t. `f=1 mod 2`

        secret key = f, public key = h = 2g/f
        (sample again if f has no inverse)
        (multiplying the public key by f, almost "kills" h in the sense
         that the product is small)

    Encryption(m \in {0,1}): 
        sample "small" polynomials s,e \in R_q
        output C = hs + m (mod q, x^n+1)
            (s sort of randomizes the encryption)
        is this semantically secure? you have to add randomness cleverly.
        if m = 0, (hs + m) * h^-1 = s + m*h^-1 = s (small)
        if m = 1, (hs + m) * h^-1 = s + m*h^-1 = s + h^-1 (not small)
          => not semantically secure

        output C = hs + 2e + m (mod q, x^n+1)
            (s sort of randomizes the encryption)
        if m = 0, (hs + 2e + m) * h^-1 = s + 2eh^-1 + m*h^-1 (large)
        if m = 1, (hs + 2e + m) * h^-1 = s + 2eh^-1 + m*h^-1 (large)

    Decryption(C):

        output fC (mod q, X^n+1) mod 2
        fC = f(hs + 2e + m) = 2(gs + fe) + fm (mod q, x^n+1)
        (can't just take the mod 2 of this because ((mod q) mod 2) does not commute)

        this polynomial has small coefficients though, so the mod q has no effect
        if |2(gs+fe) + fm)| < q/2, taking mod 2 gives m

You can show that this scheme is as secure as solving the shortest vector problem
on lattices (SVP)
 
Note that there's no factoring, no discrete logarithm. This relies on the fact
that if I give you a bunch of linear equations for ciphertexts in this scheme,
it is hard to extract the secret or the messages.


    \vecS = (s1, ..., sn) \in Z_2^n

    I can give you:
    \veca1, a1 \cdot s
    ...
    \veca1, am \cdot s

    Your goal is to find s. You can do this with Gaussian elimination.


    However, if I give you noisy equations with e_i, where P(e_i = 1) = p:
    \veca1, a1 \cdot s + e_1
    ...
    \veca1, am \cdot s + e_m
 
    The only solution is to check all possible assignments of \vecS and see
    if the distribution of the e_i's you get out matches P(e_i)
    
Additive homomorphism for NTRU:

    c1 = hs1 + 2e1 + m1
    c2 = hs2 + 2e2 + m2
    ----
    c1+c2 = h(s1+s2) + 2(e1+e2) + m1+m2

Note that you cannot do too many additions because `e` needs to be a small
polynomial => this is a SwHE scheme

What happens when I decrypt these ciphertexts?

    fc1 = 2E1 + fm1
    fc2 = 2E2 + fm2

What about decrypting the sum?

    f(c1+c2) = 2(E1+E2) + f(m1+m2)
    f(c1+c2) = 2(E1+E2) + f(m1+m2)

Multiplication?

    f(c1*c2) = 2(E1m2 + E2m1 + 2E1E2) + f^2(m1*m2)
                 \---------|--------/
                           E
    => I need to use a different secret (f^2) to retrieve m1 * m2

Problem: these errors grow, and they cannot grow beyond a certain amount (`q/2` or
`q/4` or the wraparound will not allow you to decrypt)

Let's look at addition:


    f(c1+c2) = 2(E1+E2) + f(m1+m2)
    the noise is at most 2*B, if E1 < B and E2 < B

    f(c1*c2) = 2(E1m2 + E2m1 + 2E1E2) + f^2(m1*m2)
    norm of E1E2 is at most nB^2 (due to the reduction in R_q)

    after d levels, noise is (nB)^(2^d)

    if noise <= q/2 <= B * 2^(n^\epsilon) we re good
    => d <= log(log q) - log(log nB) <=~ \epsilon log(n) - log(log(n))

The bootstrapping method
------------------------

Theorem: If you can homomorphically evaluate circuits of depth d and the
depth of your decryption circuit < d then you can convert it into an FHE
scheme.

How? What is the best possible noise reduction algorithm that you can think of?
DECRYPTION!!

You encrypt your data, server computes, gets too much noise, now server needs
to decrypt! But that would break security! The next best thing: "homomorphic 
decryption": I have a scheme which can compute circuits of small depths, and
the decryption algorithm is of small depth => Can decrypt "homomorphically" =>
get back a reencrypted plain text. But I would need the secret key to know
the decryption circuit. Maybe the encrypted secret key suffices.

Assume you can use the public key to encrypt the secret key (circular secure).

TODO: kind of weird how the Dec(ctext, sk) is turned into Dec(ctext, enc_pk(sk))

We need the noise we get out of the homomorphic decryption to be independent 
of the noise in the input ciphertext. 

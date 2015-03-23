Today: Message Authentication Codes (MACs), Wed., March 11th
============================================================

 - HMAC
 - CBC-MAC
 - PRF-MAC
 - OTMac
 - AEAD (Authenticated Encryption with Associated Data)
   + EAX mode
   + Encrypt then MAC
 - Finite fields & Number theory

MACs
----

 - Not related to confidentiality
 - Alice wants to send message `m` to Bob
 - would like to ensure only `m` generated by Alice will be accepted by Bob
   + Bob should not accept messages `m'` generated by Eve

Diagram:

                        m, t = MAC(k, m)
        Alice -----------*-------------------------- Bob
          k               \-> Eve                     k  
 
 - both Alice and Bob can compute `t = MAC(k, m)`
 - Eve does not have `k`, so she can't

To verify a message `m'` with tag `t`, Bob can simply compute `t' = MAC(k, m')` and check
that `t'` is equal to `t`. As long as only Alice and Bob have `k`, Bob is sure alice
sent `m'`

 - Eve can successfully guess a new MAC for `m` with probability `2^-l(t)`, where
   `l(t)` is the length of the MAC

Adversarial model:

 - Eve may ask for a MAC on any message `m`
   + `=>` gets a list `(m, MAC(k, m))` for `m`'s chosen by her
 - She wants to forge a message `(m', T)` that Bob will accept
 - The scheme is secure if Eve succeeds with probability `2^-l(t) + negl(l(t))`

### PRF-MAC

    PRF-MAC(k, m) = h(k || m), where h is a random oracle

In practice we don't have a random oracle, and iterative hash functions are
susceptible to _length-extension attacks_ where if you have
`h(k | m)` you can compute `h(k | m | extension)` without knowing `k`

### CBC-MAC

Diagram:

            m1     m2            m3
            \|     \|            \|
        o -> +  |-> +  |-> ... -> +  
            \|  |  \|  |         \|  
        k -> E  |   E  |     k'-> E  
             |  |   |  |          \|  
             ----   ----          tag

        where k' = f(k), f is a constant function

### HMAC

 - designed to fix length extension attacks that `PRF-MAC` is susceptible to
 - `HMAC(k, m) = h(k_1 || h (k_2 || m))`, where
   + `k_1 = k \xor opad`
   + `k_2 = k \xor ipad`
 - this prevents extension attacks
   + **Q:** How?

### OTMac

We saw with encryption that we have information-theoretic secure encryption like the one-time pad.

Can we also have an information-theoretic secure _one-time MAC_?

 - Eve is computationally unbounded
 - Alice and Bob use new key for each MAC computation


                        confidentiality     |    integrity
                       -----------------------------------------     
        unconditional   OTP                 |    OTMac
        conventional    block ciphers       |    MACs
        public-key      PK encryption       |    digital signatures
                    
Authenticated Encryption with Associated Data
---------------------------------------------

 - you may have a situation where parts of the message `m` are confidential
 - and another part of the message `h` (headers?) that need integrity

### Encrypt-then-MAC
 
        Alice computes:
        c = Enc(k_1, m)
        T = MAC(k_2, h || c)

        transmit header h, c, t

        Bob concatenates h || c and computes t' = MAC(k_2, h || c),
        checks that t = t', and if true, decrypt m = Dec(k_1, c)

**Note:** Applying a MAC to the plaintext instead of the ciphertext can be a bad
idea because the MAC could leak plaintext information

 + MACs have no guarantees about the confidentiality of the tag `t`

Notes:
 
 - this seems to require two passes: one for encrypting `m` and one for MACing `c`
   + you can play tricks if you choose the primitives right and make it one pass maybe

### AES-EAX

Nonce `N`:

 - generating randomness is hard, so `N` is pseudo-random

Diagram:

              N          M            H
             \|         \|            |
       k -> MAC1  k -> CTR      k -> MAC2
             |         / |            |
             |    c   /  |            |
             *-------/   |            |
             |          \|            |
             |       ---------        |
             |       | ctext |        |
             |       ---------        |
             |           |            |
             |     k -> MAC3          |
             |           |            |
             |           |            |
             -----------|+|------------
                         |
                        \|
                        tag

Note:
 
 - `MACi(k, m) = MAC(k, i || m)`

Finite fields & number theory
-----------------------------

### Finite fields

**Definition:** `(S, +, *)`, where:
 - `S` is finite,
 - contains some notion of zero and one values (identity for addition and multiplication)
 - `(S, +)` is an abelian (commutative) group with identity zero
   + associativity: `a + (b + c) = (a + b) +c`
   + identity under zero: `a + 0 = 0 + a = a`
   + inverses: `\forall a, \exists b, s.t. a + b = 0`
     - `b = a^-1`
   + commutativity (abelian)
 - `(S*, *)` is an abelian group with identity one
   + `S* = S - {0}`
   + same laws as before
 - distributive law (connecting these two groups)
   + `a*(b+c) = a*b + a*c`
   + `(b+c)*a = b*a + c*a`

`GF(p)` - finite fields (Galois fields) on `p` elements `{0, 1, ..., p-1}`

    ax + b = 0 (mod p) => 
    x = -b * a^-1

    3x + 5 = 6 (mod 7) =>
    3x = 1 (mod 7) => (5 = 3^-1 (mod 7))
    x = 5 

`GF(q)` finite field where `|S| = q`. When do finite fields exists, for what `q's`

**Theorem:** `GF(q)` exists iff `q = p^k` for some prime `p, k >= 1`

How do we create a `GF(p^k)` field, where `k > 1`?

We work with (univariate) polynomials of degree `< k` with coefficients in `GF(p)`

    a_k-1 x^k-1 + a_k-2 x^k-2 + ... + a_1 x + a0

There's `k` coefficients, so there's `p^k` such polynomials, `=> p^k` elements in `S`
 - 

Does it respect the definition of a field?

 - addition: as usual for polynomials
 - multiplication: we do it _modulo an irreducible polynomial of degree `k`_
   + irreducible means the polynomial doesn't factor into a product of two smaller polynomials

Example: `GF(4) = GF(2^2)` has 4 polynomials (4 elements): 

 - `0`
 - `1`
 - `x`
 - `x + 1`

Multiplying them, we work modulo `p(x) = x^2 + x + 1, p(x) = 0 => x^2 = -x-1 => (GF2 -x = x, -1 = 1) => x^2 = x + 1` 

     *  |   0       1      x    x+1
     --------------------------------
     0  |   0       0      0     0
     1  |   0       1      x    x+1
     x  |   0       x     x+1    1
    x+1 |   0      x+1     1     x  


    x * (x + 1) = x^2 + x = (x+1) + x = 1
    (x+1)(x+1) = x^2 + x + x + 1 = x^2 + 1 = (x+1) + 1 = x

How do we choose the modulo `x^2 + x + 1`? Gotta make sure they are irreducible.

 - You only do it once

What about division?

#### Repeated squaring

We want to compute `a^b`, `b` is an integer, `a` is a number in your finite field

    

          {  1,             if b = 0
          {   
    a^b = {  (a^(b/2))^2    if b = even
          { 
          {  a*a^(b-1)      if b = odd

We have to do `<= 2*log_2(b)` multiplications

If `b` is secret, this can be problematic because the runtime is dependent on the value of `b`.

**Fermat's little theorem (FLT):** In `GF(q)` for all `a \in GF(q)*`, we have `a^(q-1) = 1`, where 1 is the multiplicative identity in `GF(q)`

**Corallary:** For all `a \in GF(q)`, we have `a^q = a`

**Corallary:** For all `a \in GF(q)`, we have `a^-1 = a^(q-2)`

Example:

    3^-1 (mod 7) = 3^5 = 27 * 9 = 6 * 2 = 12 = 5
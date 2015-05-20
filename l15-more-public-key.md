Today: Title, Wednesday, April 1st, 2015
=========================================

Today:

 - IND-CCA2
 - Cramer-Shoup
 - RSA
 - making RSA IND-CCA2 secure
 - other aspects of RSA security

IND-CCA2: Indistinguishability under chosen-ciphertext attack
-------------------------------------------------------------

    Phase I: 
        keygen -> (pk, sk)
        adversary can use encryption oracle
        adversary can use decryption oracle
            except on the challenge ctexts

        adversary produces two message of the 
        same length m0, m1 and some state s

    Phase II:
        examiner flips a coin b \in {0,1}
        examiner encrypts one of the messages, computes c* = Enc(m_b)
        examiner sends c* to the advesary
       
        adversary has to figure out in time polynomial in the security
        parameter whether c* is the encryption of m0 or m1

        adversary outputs b* and wins if b = b*
       
This is the strongest notion of security nowadays.

Basic ElGamal does not satisfy this security definition because ciphertexts
can be rerandomized and given to the decryption oracle.

What if the decryption function only decrypts messages that it _knows_ it was
created by the encryption box, as opposed to other things: like playing with bits,
playing with the homomorphic property, etc.

Cramer-Shoup
------------

An extension of ElGamal.

We have `G_q` a group of prime order `q` (remember `g^q = 1`).

**TODO:** Are `g1/g2` generators of `G_q`?

    Keygen(G_q):
        g1, g2           <--R-- G_q
        x1,x2, y1,y2, z  <--R-- Z_q (additive group mod q)
        c <- g1^x1 * g2^x2
        d <- g1^y1 * g2^y2
        h <- g1^z           (ElGamal-like feature)

        pk = (g1, g2,  c,  d, h)
        sk = (x1, x2, y1, y2, z)

Let `H` be a hash function which maps `G_q` triples to `Z_q`

    Enc(m \in G_q):
        r <--R--- Z_q
        u1 <- g1^r          (ElGamal-like)
        u2 <- g2^r          (for the checking portion)
        e  <- m * h^r       (ElGamal-like)
        \alpha <- H(u1, u2, e)
        v  <- c^r * d^(r*\alpha)

        ctext = (u1, u2, e, v)


    Decrypt(ctext = u1, u2, e, v):
        \alpha = H(u1, u2, e)

        [ u1^x1 u2^x2 = g1^rx1 g2^rx2 = c^r ]
        [ u1^y1 u2^y2 = d^r ]
        [ u1^(x1+y1*\alpha) * u2^(x2+y2*\alpha) =
          u1^x1 u2^x2 * u1^(y1*\alpha) * u2^(y2*\alpha) =
          u1^x1 u2^x2 * (u1^y1 * u2^y2)^\alpha = c^r * (d^r)^alpha = v ]

        checks that u1^(x1+y1*\alpha) * u2^(x2+y2*\alpha) == v
            if not equal, then reject

        [ need to divide by (invert) h^r to get m out of e ]
        [ don't have r, have z => have h = g1^z ]
        [ u1 = g1^r, u1^z = (g1^r)^z = h^r ]
        return e/u1^z

**Theorem:** Cramer-Shoup is IND-CCA2 secure, assuming:

 - Decisional Diffie-Hellman (CDH) is hard in `G_q` (Why not CDH? ElGamal needed
   DDH as well so as to maintain indistinguishability under chosen-plaintext `=>`
   Cramer-Shoup, based on ElGamal will need it as well)
 - H is "target collision resistant"
   + **TODO** Is this assuming less than _one-way hash functions_ exist?

This is really cool because at the time it solved an open-problem of whether
IND-CCA2-secure public key encryption schemes exist.

RSA (1977)
----------

    Z_n* = all numbers < n relatively prime to n

    Keygen: 
        find large *random* primes p, q
        let n = pq

        \phi(n) = |Z_n*| = (p-1)(q-1)
            this is unknown to the adversary
            knowing \phi(n) <=> knowing factorization of n 

        e <--R-- Z*_\phi(n)
            just means that gcd(e, \phi(n)) = 1

        d <- e^-1 (mod \phi(n))
            computed using Extended Euclidian Algorithm
        
        pk <- (n, e)
        sk <- (p, q, d)

    Enc(m \in Z_n*):
        c = m^e (mod n)

    Dec(c \in Z_n*):
        m = c^d (mod n)

**Note:** `m` and `c` need to be `\in Z_n* =>` need to be relatively prime to
`n`, so certain messages cannot be encrypted? The only messages that cannot be
encrypted are `p` and `q` and their multiples. Note that if an adversary wanted
to encrypt such messages, he would _literally_ have the factorization of `n`

We can prove using the _Chinese Remainder Theorem_ that RSA works even for 
`m \notin Z_n*`, but `m \in Z_n` (i.e. `m` does not need to be coprime to `n`)

_Chinese Remainder Theorem:_

    n=pq, \forall x,y \in Z_n*, x = y (mod n) <=> x = y (mod p) AND x = y (mod q)

We know, by definition, that `e*d = 1 (mod \phi(n)) => e*d = 1 + t*(p-1)(q-1) =>
e*d = 1 (mod p-1) => d = e^-1 (mod p-1)` 

We want to show that `(m^e)^d = m (mod n), \forall m \in Z_n`

Suffices to show that `(m^e)^d = m (mod p)` and then use the Chinese Remainder
Theorem.

*Case 1:* `m = 0 (mod p) => 0^ed = 0 (mod p)` q.e.d.

*Case 2:* `m != 0 (mod p), m \in Z_p*`

    m^(p-1) = 1 (mod p)     [ element of group raised to group order == identity]
                            [ or Fermat's theorem ]
    m^(ed) = m^(1 + u*(p-1)) = m^1 * (m^(p-1))^u = m * 1^u = m (mod p)

Security of RSA
---------------

Relies on assumption that `n = pq` is hard to factor when `p` and `q` are large
primes.

Best factoring algorithms today have running time `exp(c*(ln(n))^(1/3) * ln(ln(n))^(2/3))`, 
where `n` is the number of bits in the `N = pq` number, subexponential time. (According to Wikipedia, 
it's the number of bits in `n`.)

Q: Why is it important to keep `\phi(n)` secret?  
A: You can factor `n` knowing `\phi(n)`?

        \phi(n) = (p-1)(q-1) => \phi(n) = pq - p - q + 1 =>
        p + q = pq - \phi(n) + 1 => p + q = n - \phi(n) + 1

        We expect p and q to be about the same size, so we can
        guess them easily? Sure, but we can do better

        We have:
        (1) n = pq
        (2) p + q = n - \phi(n) + 1
          => 
        q = (n - \phi(n) + 1) - p
          => (substitute in (1))
        n = p((n - \phi(n) + 1) - p)
          = - p^2 * p((n+1) - \phi(n))
          <=>
        p^2 - p((n+1) - \phi(n)) + n = 0
          <=> (2nd degree equation w/ a,b,c coeff.)
        p = (-b +/- sqrt(b^2 - 4ac))/(2a)
          = ...

Q: If `d` is lost, can you factor `n`?  
A: You can definitely decrypt and sign messages arbitrarily with `d`. The 
[RSA paper](papers/rsa-paper.pdf) in section IX.C says that you can also efficiently factor `n` with
knowledge of `e` and `d`.

OAEP: Optimal Asymmetric Encryption Padding
-------------------------------------------

Assume G and H are random oracles

    
    |       m       |       0^k1    |       |   r   |
    ---------------------------------       ---------
           \------> | <------/                  |
                    / t+k1                      / k0
                    |                           |
                   \|                          \| 
                    + <---------- | G | <-------*
                    |                           |
                   \|                           |
                    +-----------> | H | ------> +
                    |                           |
                   \|                          \|
                |                   |               |
                ------------------------------------- x
                                    |
                                | RSA   |
                                ---------
                                    |
                                x^e (mod n)

Decryption: 

 - invert `RSA`, get `x`
 - invert OAEP Feistel, get `m` and `0^k1`
 - reject if `0^k1` are not present
 - else output `m`

**Theorem:** RSA+OEAP is IND-CCA2 secure assuming

 - RSA is hard to invert on random output
   + **TODO:** What?? Why the _random_ restriction?
 - random oracles exist and we can construct `G` and `H`


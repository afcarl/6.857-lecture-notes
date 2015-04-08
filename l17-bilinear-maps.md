Today: Bilinear maps, April 8th
===============================

 - "Gap groups" & bilinear maps
 - BLS (Boneh, Lynn, Shacham) signatures
   + very simple
   + short signatures
 - [3-way key agreement](http://cgi.di.uoa.gr/~aggelos/crypto/page4/assets/joux-tripartite.pdf) (Joux)
   + Joux brought bilinear maps into the crypto world
 - Identity-based encryption (IBE) (by Boneh, Franklin)
   + Example: encrypt using your email address as your public key

"Gap groups" and bilinear maps
------------------------------

"Gap groups"

 - you've got a pair of groups and can do nice things between them
 - based on elliptic curves

**Definition:** A _gap group_ is a group where Decisional Diffie Hellman (DDH) is _easy_ but where Computational Diffie Hellman is _hard_

How do you construct one? Using this notion of a bilinear map.

Suppose we have a main group `G1` and a shadow group `G2`.

    G1 is a group of prime order q, has generator g (main group)
    G2 is a group of prime order q, has generator h (shadow group)
    
We have a pairing function `e`, or a bilinear map, such that it
takes two elements from `G1` and gives you one in `G2`:

        e : G1 x G1 -> G2
        e(g,g) = h

Picture to illustrate this shadowing operation:

    G1  g   g^a     g^b     g^b     g^ab
        |    |       |       |       |
       \|   \|      \|      \|      \|
    G2  h   h^a     h^b     h^b     h^ab
    (except the mapping function takes two args, not one)

    \forall (a,b), e(g^a, g^b) = h^ab

    The shadowing operation can be implemented as:
    e(g, g) = h
    e(g^a, g) = h^a
    e(g^b, g) = h^b
    e(g^a, g^b) = h^ab

Google for ["pairing-based crypto lounge"](http://www.larc.usp.br/~pbarreto/pblounge.html), to see
applications of bilinear maps.

In practice `G1` is an elliptic curve group and `G2` is a finite field like
`Z_{p^6}`. Won't go into a discussion of what the bilinear map actually is (complicated apparently).

You can compute a pairing function in like 25ms apparently.

**Theorem:** DDH is easy in G1, if you have G2 and a bilinear map from G1 to G2.

To check if `g^a, g^b` and `g^c (could be g^r or g^ab)` are related, we can check if `e(g^a, g^b) = e(g, g^c)` (i.e., if `h^ab = h^c <=> ab = c (mod q)`)

Properties:

    e(g^a,g^b) = e(g^a, g)^b = e(g, g)^ab, = e(g, g^b)^a

**Note:** If DLP is easy in `G2` it is also easy in `G1` (can map `g^a => h^a`, can compute `a` from `h^a => ` have `a` from `g^a`) . 

Q: Why do you need a prime order `q` group?

### How to implement a gap group

`G1` is an elliptic curve group, a _supersingular_ one (terminology?)

    y^2 = x^3 + ax + b (mod p)

To make it supersingular, you need `p = 2 (mod 3), p > 5, a = 0, b \in Z_p*`

    y^2 = x^3 + 1 (mod p)

`G2` is a finite field `F*_{p^k}` for some small `k`

We need groups of prime order `q`, so we use subgroups of prime order `q`, `|q| = 160 bits` from `G1` and `G2`

The bilinear map can be the "Weil pairing" or "Tate pairing"

BLS (Boneh, Lynn, Shacham) signatures
-------------------------------------

We're gonna have a setup sort of like ElGamal. Assume all notation from previous section.

Let `H : messages -> G1` be collision-resistant (CR) hash function that maps messages to our `G1` group.

Secret key is some value `x, 0 < x < q` picked randomly.
Public key is `g^x` (in `G1`)

To sign `M`, output `s_x(M) = (H(M))^x`

How to verify? Let `m = H(M)`, signature will be `m^x`

    g   g^x     m       m^x
    \   \-------/       /
     \-----------------/

Check that `e(g, m^x) = e(g^x, m) <=> e(g, g^tx) = e(g^x, g^t) <=> h^tx = h^tx
<=> tx = tx` (note that since `m \in G1 => m = g^t`, for some `t`, we don't need
to find `t`, we just use it here to show that we should get equality)

A general remark about elliptic curves, is that the DLP problem gets harder faster
relative to the size of the group (compared to `Z_p*`)

For a point on an elliptic curve, you've got two values, the `x` and `y` coords.

    |p| = 160 bits
    point on curve is (x,y), 320 bits

Claim: we can represent a point with only 160 bits. Given `(x, y)` can represent
it as `x`, and for `y`, I can just compute it (there are only two possible, for
this particular curve) and give you a + or - bit to distinguish which `y` is 
the good one

Isn't taking square roots hard? Depends on what the prime `p` is congruent to `1
(mod 4)` then it's easy, if it's congruent to `3 (mod 4)` then it's a little
harder, but still fast using some randomization.

**Theorem:** BLS signatures are secure against existential forgery under chosen
message attack in the random-oracle model (ROM) and assuming CDH is hard in `G1`

3-way key agreement (Joux)
--------------------------

We saw the original Diffie-Hellman problem where Alice and Bob can agree on a key.

Alice, Bob and Charles want to agree on a key. We can do this with DH but with
a lot of message passing: gotta send `g^ab, g^ac, g^bc` to each other and compute
`g^abc` as the shared key.

Faster using bilinear maps

    A   g^a     
    B   g^b     
    C   g^c     

Can take `e(g^a, g^b)^c = h^abc`
Can take `e(g^b, g^c)^a = h^abc`
Can take `e(g^c, g^a)^b = h^abc`

If we want 4-way agreement, maybe a _trilinear map_ could be of use.

Identity-based encryption, Boneh and Franklin, 2001
---------------------------------------------------

Suppose I want to send you a message, and all I have is your email address. Is
there a way for me to use that as a public key?

**Note:** If there's a public key => there needs to be secret key => who computes 
it? Clearly it can't be you, because if you can simply compute it, then so can
anyone else => Seems like we need a trusted third party (TTP) to compute the
secret keys.

TTP has a secret `s` and a public key `y = g^s \in G1`. Everybody knows the TTP's
public key.

We have:

    H1 : names -> G1* (CR hash fn)
    H2 : G2 -> {0,1}^* (an element in G2 can be used to generate a keystream)

You want to encrypt a message `M` to `name` using `y` as the public key of the
TTP.

    encrypt(M, name, y):
        r <-R- Z_q*
        Q_A <- H1(name), Q_A \in G1
        g_A <- e(Q_A, y), g_A \in G2

        ctext <- (g^r, M \xor H2(g_A^r))
    
    my secret is sk = d_A = Q_A^s
        gotta get it from the TTP, because I don't know s

    decrypt(d_A = Q_A^s, (u = g^r, v = M \xor H2(g_A^r))):
        I have g, g^r, Q_A^s
        
        v \xor H2(e(d_A, u)) = v \xor H2(e(Q_A^s, g^r))

        e(Q_A^s, g^r) = e(Q_A, g)^rs = e(Q_A, g^s)^r = g_A^r

        can now do v \xor g_A^r and get the message back

**Note:** You can encrypt to me, before I even have my secret...

Can be shown to be semantically secure in the ROM

Today: Secret sharing and block ciphers
=======================================

 - Shamir's secret sharing
 - Block ciphers (DES, AES, modes of operation)

Shamir's secret sharing
-----------------------

**Problem:** Don't want to put trust in a single person.

If you have`N = 3`, then `t = 2` parties are sufficient to sign a document,
spend money, etc.

Notion: _Threshold capability_

Say Alice has a secret `S` and a number of friends she wants to distribute
_shares of the secret `S`_ to `t` friends, `1 <= t <= n`

 - she gives each friend a share `s_i` of `S` 
 - **Goal:** any `t` of the friends can reconstruct `S` from their `s_i`'s
   + any fewer than `t` have negligible chance of reconstructing `S`
 - _Valid criticism:_ at some point _you have to_ reconstruct `S`, so it'll be
   vulnerable

For `t=1` the problem is trivial: `s_i = S, \forall i`.

For `t=n` the problem is trivial: `s_i = ith chunk of S`
 + would not be that secure, because `n-1` people can guess the last chunk more
   easily (not negligible probability.
 + `S = s_1 \xor s_2 \xor ... \xor s_{n-1} \xor s_{n}`
   - result is random if you don't have all `s_i`'s
   - need all people to generate `S`

For other `t`'s, use _polynomials_.

 - `t=2` points determine a line
 - `t=3` points determine a quadratic polynomial
 - `t=k` points determine a `t-1` degree polynomial
 - `f(x) = a_{t-1}x^{t-1} + a_{t-2}x^{t-2} + ... + a_1*x + a_0 (mod p)`
 - we define `f` over a finite field (because we're using computers which have limits)
 - you can go efficiently between the two representations of `f`
   + the coefficient repr. `a_{t-1}, a_{t-2}, ..., a_1, a_0`
   + the set of (point, value) pairs: `{(x_i, y_i)}, \forall 1 <= i <= t`
 - _Evaluation:_ given an `x`, compute `f(x)`
   + easy to do
 - _Interpolation:_ give a set of `t` points find a unique curve that runs
   through these points
   + easy to do
 
To share a secret `S (0 <= s < p)`
 
 - let `a_0 = S`
 - pick `a_1, a_2, ..., a_{t-1}` at random from `Z_p`
   + this defines our `f` polynomial of degree `t`
 - let `s_i = (i, y_i)`, where `y_i = f(i), \forall 1 <= i <= n`
   + note that `s_0 = (0, y_0) = f(0) = a_0 = S`
   + but you never send `s_0`, you send `s_1, ..., s_n`
   + note that `s_i, i >= 1` are completely uncorrelated to the secret `S`
     - they are picked randomly
     - leak no info about `S`

Now, let's see how `t` out of the `n` friends can reconstruct `S`.

 - Given `(x_i, y_i)` for `1 <= i <= t`
 - `f(x) = \sum_{i = 1, t} {y_i * f_i(x)}`, where
   + `f_i(x) = { 1 at x = x_i || 0 at x = x_j, where j != i}`
 - `f_i(x) = \prod_{j != i}{x - x_j}/\prod{j != i}{x_i - x_j}`
   + the numerator will be a degree `t-1` polynomial
   + note this will satisfy the constraints above
 - `s = f(0) = \sum{i = 1, t} {y_i * f_i(x)} = replace `

**TODO:** Why does this work?

Why having fewer than `t` shares doesn't allow you to reconstruct the secret?
 
 - just try determining a line with 1 point
   + or a quadratic graph with 2 points
   + and so on...
 - A degree `t-1` curve can be defined to go through the adversary's `t-1` points
   and through the point `(0,s)` for any `s`
 - This is information-theoretically secure because the adversary cannot
   "compute" his way into finding `s`. `s` could be any point in `Z_p` and no
   information is leaked about `s` through those `t-1` points

Block ciphers
-------------

                c = Enc(K, M)
        Alice -------------*---------------------------> Bob
                            \
                             \-> Eve

**Problem:** Message could be arbitrarily long. How do you build an encryption
method to handle arbitrarily large messages?
 
 + for starters, we build block ciphers for fixed-length messages
 + then we chain the together wisely and handle arbitrarily long messages


                            p
                            |
                           \ /
                            *
                        -----------
             Key K ---> |   Enc   |
                        -----------
                            |
                           \ /
                            .
                            C

Fixed length `P, C, K`:
 
 - DES: `|P| = |C| = 64 bits`, `|K| = 56 bits` (8 of the 64 bits were used for
   parity)
 - AES: `|P| = |C| = 128 bits`, `|K| = 128, 192, 256`

DES (Data Encryption Standard)
------------------------------

Call put out for commercially usable data ciphers. DES came from IBM.

`m = L_0|R_0`

                   L_0                  R_0
            -----------------     ------------------
            |               |     |                |
            -----------------     ------------------
                   |                      |
                   |                      |
     round 1       +----------|f|----------
                   |            \----------------- k_i round key 48 bits
                    \                    /       
                     \                  /
                      \                /
                        swap for next 
                           round
                             \   /
                              \ /
                              / \ 
                             /   \
                            /     \
                           /       \ 
                          /         \
     round 16
                   L_15                  R_15
            -----------------     ------------------
            |               |     |                |
            -----------------     ------------------

`f` can be anything, and won't affect the _invertibility_ of the cipher if you
have the key.

How do you design a _good `f` box_ that doesn't leak `K` and `P`?

 - Round key `k_i` is split into eight 6-bit chunks.
 - Each chunk goes through a substitution box (S-box) and results in a 4-bit value
 - Results are permuted

Differential attacks: 2^47 attack
---------------------------------

 - You might assume the adversary has access to encryption/decryption oracle (CCA security) with a fixed but unknown key
 - Brute force attack on 56-bit key, would take a while
   + `2^56` different keys
 - Here's an attack that gets us down to `2^48` tries in the CPA security model (i.e. with an encryption model)

You can try tweaking the input plaintext and see what tweaks are caused on the output ciphertext.

`M' = M \xor \delta`, ask oracle to encrypt `M -> C` and `M' -> C' = C + \gamma`.

At a high level: The differences between `delta` and `gamma` give you some information about the last round key.

This requires about `2^47` chosen pairs

[Biham's PhD thesis](https://en.wikipedia.org/wiki/Differential_cryptanalysis),
advised by Adi Shamir

2^43 attack (Matsui)
--------------------

                            p
                            |
                           \ /
                            *
                        -----------
             Key K ---> |   Enc   |
                        -----------
                            |
                           \ /
                            .
                            C

Could be that DES has attacks like: `M_3 \xor M_15 \xor C_2 \xor C_11 \xor K_7
\xor K_19 = 0`. This relates two bits of the key because you know the message
and ciphertext bits.

In practice, these kind of equations are not always true. Maybe they're true
like half the time: `p = 1/2 + \epsilon`

Need `1/\epsilon^2` data points to solve equations like these.

AES (Advanced Encryption Standard), 1997-1999
---------------------------------------------

Open public contest to design a cipher. Submit designs, attack them. Let the
best win. International too, anyone in the world could submit.

 - 15 algorithms were submitted (after bad submissions were scrapped)
   + RC6 (Ron's favorite, lol)
   + Mars
   - Twofish
   - Rijndael
     + designed by Belgian academics
   - ...

Specs:

 - 128 bit plaintext/ciphertext blocks
 - supported key sizes should be 128, 192, 256 bits
 - 10, 12 or 14 rounds
   + as you iterate you tend to get more strength
   + longer key will let you do more rounds (more bits for a round)
 - byte oriented design
 - some `GF(2^8)` math used
   + `GF(2^8)` means the finite field with 256 elements

Basic structure is a 4 by 4 array/matrix of bytes, where each entry is 1 bytes
=> 16 bytes => 128 bits

### AES description
 
 1. Derive 11 _round keys_ of 128 bits from 128 bit key (`k_i`'s)
 2. Given M to encrypt represent it as `4x4x8` matrix
 3. Collection of rounds: for each round `r = 1, 2, ..., 10`
    - take message `m`, XOR in the round key (`m = m XOR k_i`)
    - substitute bytes (as told by S-box)
      + derived using `GF(2^8)` table, modular inverses, etc.
      + each byte `x = S-box(x)`
    - rotate row `i` left by `i` positions
      + `a, b, c, d -> b, c, d, a`
      + columns become diagonals
    - mix each column with matrix
      + if `x` is a column, `x = Ax`, where `A` is a `4x4` matrix
 4. Final round replaces mixed column operation by another round key operation
    - as in, XOR the round key in
    - because anyone can undo the mix (public operation, `A` is known)

**Note:** side channel attacks on S-box

                       L_0                   R_0
                -----------------     ------------------
                |               |     |                |
                -----------------     ------------------
                       |                      |
                       |                      |
         round 1       +----------|f|----------
                       |            \----------------- k_i round key 48 bits
                        \                    /       
                         \                  /
                          \                /
                            swap for next 
                               round
                                 \   /
                                  \ /
                                  / \ 
                                 /   \
                                /     \
                               /       \ 
                              /         \
         round 16
                       L_15                  R_15
                -----------------     ------------------
                |               |     |                |
                -----------------     ------------------



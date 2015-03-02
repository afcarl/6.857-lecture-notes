Cryptographic hash functions II
===============================

One value: `h(x) = y`, y "represents" x

Puzzles
-------

    h : {0,1}^* -> {0,1}^d
        
Given `y = h(x)` find `x` such that `h(x) = y` tends to take `O(2^d)` time, assuming `h` models a _random oracle_ (each trial is correct with prob. `2^-d`)

If `d` is small like 32, then it's feasible for adversary to invert.

Easy to create many puzzles with _keyed hash functions_: `h_k(x) = h(k || x)`

Puzzle spec: `(k, d, y)`, find `x` s.t. `h(x) = y`

Hashcash (Adam Back, 97')
-------------------------

Fight spam. Make people "pay" for sending an email.

Solve for `r`: `h(k || r), where k = sender|receiver|date|time`

Verifier checks the date/time match current time and verifies hash checks out.

Spammers have botnets nowadays that can compute these hashes, so "proof-of-work" mechanisms don't really work that well anymore.

Merkle's idea for public key crypto using puzzles
-------------------------------------------------

How can Alice and Bob establish a secret here, if Eve can listen in?

    Alice *-----------------------------*---------------------------------* Bob
                                         \
                                          \-> Eve (passive, listens)

Use puzzles to solve this problem.

 1. Bob could make `n` puzzles (1 million/billion) of difficulty `D` controlled by Bob.

 2. Bob sends puzzles to Alice. Eve sees all of them.

 3. Alice picks one at random and solves it (let it be puzzle `i`). Neither Bob nor Eve knows which puzzle Alice picked.

 4. Alice lets Bob know which one she solved (careful with the details: can't let Eve know)

 5. So now they have a shared secret.

Notes:

 - work for Alice and Bob: `O(n)` to make the puzzles, plus `O(D)` for Alice to solve the puzzles.
   + `D` and `n` tend to be the same, so total work is `O(n)`
 - work for Eve
   + she hears all the puzzles
   + she hears some secret indication about which puzzle was solved
     - how does she attack this?
     - we're aiming at `O(nD) = O(n^2)` work for Eve
       + if we make `n` 1 billion (feasible nowadays), then the gap between `O(n)` and `O(n^2)` could be good enough
       

Details:

Puzzle `i` can be `P_i = (y_i, E_x_i(k_i), h(i, || x_i) = y_i)`, where `k_i` is a random 256bit key, encrypted under `x_i` which is what Alice needs to get by inverting `y_i = h(i || x_i)`.

Let `x_i` be `\in {0,1}^d` and `y_i \in {0,1}^2d` (apparently for some collision reasons)

How does Alice tell Bob which one she solved? She can send `h(k_i)` to Bob.

How do you build a good hash function?
--------------------------------------

### The Merkle-Damgaard construction

Trying to build `h:{0,1}^* -> {0,1}^d` that is collision-resistant (CR), one-way (OW), etc.

Very long message, break it into blocks:

`c` = "chaining variable", `|c| = 512 bits`
`b` = message block size (maybe 512 bits)

Let `f : {0,1}^c \times {0,1}^b -> {0, 1}^c` (a compression function) be a nice CR, OW primitive that can deal with _fixed-length inputs_

Padding a message `M` to a multiple of `b` bits. Important that padding is invertible: otherwise multiple messages can pad to the same value and you'll easily be able to find collisions apparently.

    | |M| bits              |        | 64 bits
    ----------------------------------------
    | M                     | 100000 | |M| |
    ----------------------------------------

We have our compression function `f`

       m_1      *-*    m_2       *-*         m_1       *-*   
        |       |  \    |        |  \         |        |  \ 
        |-----> |   \   |----->  |   \        |----->  |   \
          c_0   | f |     c_1    | f |         c_{n-1} | f |   c_n
     IV  -----> |   |    ----->  |   |  ....   ----->  |   |  ----->
                *---*            *---*                 *---*

Then, `h(m) = c_n`

### Why is this a good method?

 `f(c_i, m_{i+1}) = c_{i+1}`

**Theorem:** If `f` is collision resistant, then so is `h`.

**Proof by contradiction:** Assume that the big box is not CR, then prove that `f` is not CR and get a contradiction.

Assume we have two messages `m` and `m'` that give us a collision.

If `c_n == c'_n` then since `f` is collision resistant that implies we've found a collision on `f` when we computed `f(m_n, c_n-1)` and `f(m'_n, c'_n-1)` OR when we computed something earlier.

### Davies-Meyer construction

Assuming you have a good block cipher: `f(c_{i-1}, M_i) = C_{i-1} \XOR E(M_i, C_{i-1})`

 
                         |---------------------|
                         |    |----------|    \|/
            C_{i-1}  -------->|    E     |------->
                              |----------|
                                   /|\
                                    |
                                    M_i (key)


### MD5

Incomplete diagram, see notes.

                -----       -----       -----        -----
                | A |       | B |       | C |        | D |      128 = c = d
                -----       -----       -----        -----
                  |           |           |            |
                           <---------------------------|
           m_i  | + | <- g <---------------------------|
                           <---------------------------|

                  |
    const  k_i  | + |
                  |

    rotation    |   |


What is g?

               {  x*y \or \not{x}*z    in pass 1
    g(x,y,z) = {  xz  \or y*\not{z}    in pass 2
               {  x \xor \y \xor \z    in pass 3
               {  y \xor x*\not{z}

Why is it 64 rounds? Seemed like enough at the time, but should be more actually.

Ron: This is sort of an ad-hoc construction, cause you're at the bottom of the food chain. No proofs here anymore. Can't do a reduction. So it becomes a bit of an art form. You ask people to break it and get confidence when they can't.

Ron: Maybe it would've been safe w/ 80 rounds. Even so, it has 128bit output and the birthday problem gives us `O(2^64)` tries to find a collision.



Today: Cryptographic hash functions
===================================

Today:

 - definition
 - random oracle model (ROM)
 - desirable properties (CR, OW, ...)
 - application
 - construction

Hash functions
--------------

**Definition:** A cryptographic hash function `h` maps bit-strings of arbitrary
length to a fixed-length output in an efficient, deterministic, public,
"random", manner

    h : {0,1}* -> {0,1}^d
          /\        /\
           \         \
            \         \--------- all strings of length d
             \
              \---- all strings of any length >= 0

 - Sometimes they are called _message digest_ functions.
 - Typical output lengths are: 128, 160, 256, 512 bits.
 - **No** secret key. Anyone can compute `h`
 - Computation is efficient
 - Examples: 
   + MD4, 128 bits, broken w.r.t. collision resistance
   + MD5, 128 bits, broken w.r.t. collision resistance
   + SHA-1, 160 bits, possibly broken w.r.t to col. resist.?
   + SHA-256, 256 bits,
   + SHA-512, 512 bits,
   + SHA-3 (a.k.a. Keccak), 224/256/384/512 bits

Ideal hash function: Random oracle (RO)
---------------------------------------

Random oracle theoretical model not achievable in practice (some proofs on the
storage requirements I think are out there)

Oracle "in the sky":

 - receives inputs `x` and returns output `h(x)`, for any `x \in {0,1}*` such
   that `|h(x)| = d` bits
 - on input `x`, if `x` is not in the oracle's book:
   + flip a coin `d` times to determine `h(x)`
   + record `(x, h(x))` in the book
 - ...else, return `y` where `(x,y)` is in the book
 - gives a random answer every time, but uses this "book" to record answers so
   it is deterministic & consistent

Many cryptographic schemes are proved secure in the Random Oracle Model (ROM),
which assumes the existence of such an RO. Then, we assumes it is fine (a big
assumption that some cryptographers don't like) to replace the RO with a normal
hash function like SHA in practice.

Hash function properties
------------------------

These properties are expressed informally here:

 1. **One way (OW)** (pre-image resistance)
    + "infeasible," given `y` to find any `x'` such that `h(x') = y`
    + `x` is a _preimage_ of `y`
    + in ROM, an `x'` can be found by brute-force in `\theta(2^d)` time
 2. **(Strong) Collision-resistance (CR)**
    + "infeasible," to find `x, x'` s.t. `x != x` and `h(x) = h(x')`
    + this is known as a _collision_
    + in ROM, requires trying about `2^{d/2} x` values before a pair of two `x` 
      values is found such that `h(x1) = h(x2), x1 != x2`
        - the "birthday paradox"
    + note that collisions are unavoidable (`h` cannot be injective) because
      the domain of the function is infinite while the codomain/image is of
      cardinality `2^d`
 3. **Target (or weak) collision resistance (TCR)** (2nd preimage resistance)
    + "infeasible" given `x` to find `x' != x` such that `h(x) = h(x')`
    + in ROM, an `x'` can be found by brute-force in `\theta(2^d)` time
 4. **Pseudo-randomness (PRF)**
    + "`h` is indistinguishable under black-box access from a random oracle"
    + (to make this notion workable, we need a _family_ of hash functions, one
       of which is picked at random. A single, fixed, public, hash function will
       be easy to distinguish otherwise: just remember what `h(0)` is for
       instance, and with high probability, the RO will output a different value
       on input `0`)
 5. **Non-malleability (NM)**
    + "infeasible," given `h(x)`, to produce `h(x')` where `x` and `x'` are _related_ such as `x' = f(x)`, for some function `f`

**Theorem:** If `h` is CR, then `h` is TCR.  
**Theorem:** `h` is OW does not imply `h` is CR.  
**Theorem:** `h` is CR does not imply `h` is OW.  
**Theorem:** `h` is CR _and_ `h` "compresses" implies `h` is OW.  

See [Phillip Rogaway's paper](papers/rogaway-hashes.pdf) for proofs and for more interesting properties of hash functions.

Applications
------------

### Password storage

 - store `h(password)`, not `password` on server
 - when user logs in, check hash of his password against table of hashed passwords
 - disclosure of `h(password)` should not reveal `password` (or any equivalent
   preimage)
 - Need `h` to be **one-way (OW)**: guarantees (1) adversary doesn't learn anything about password and (2) adversary cannot come up with a `p'` such that `h(p') = h(password)`

### File modification detector

 - for each file `f` store `h(f)` securely
 - can check if `f` has been modified by recomputing `h(f)`
   + need to be sure this is the same `h(f)` as the one I stored, otherwise
     attacker can modify `f -> f'` and `h(f) -> h(f')`
 - need **target collision resistance (TCR)**
   + prevents adversary from coming up with an `f'` such that `h(f') = h(f)`

### Digital signatures

 - signing large `M` is done by signing `m = H(M)` instead (_hash & sign_)
   + some signature `s` is computed as `s = sign(M, secret_key)`
 - verifier computes `h(M)` from  `M` then verifies signature `s`
   + verifier calls `verify(M, s, public_key)`
 - need **collision resistance (CR)**
   + otherwise, if Alice finds a collision `x, x'` with `h(x) = h(x')`, then
     Alice can ask Bob to sign `x` and claim (or prove to Charlie) that Bob
     signed `x'`
   + don't need one-way because `h(x) = x` is still correct (just not as 
     space efficient as we might want)

### Commitments

 - Alice wants to commit to a value `x` to Bob and then reveal it later to Bob
 - Alice has value `x` (e.g. auction bid)
 - Alice commits to her value `x` by computing `C(x)`
 - Alice submits `C(x)` as her sealed commitment (i.e. sealed bit)
 - Alice can _open_ `C(x)` later and reveal `x` to whomever she committed to

Properties:

 - **Binding:** Alice should not be able to open `C(x)` in more than one way (she
   is committed to just one `x`)
 - **Secrecy (hiding):** No one seeing `C(x)` learns anything about `x`
 - **Non-malleability:** Given `C(x)`, it shouldn't be possible to produce 
   `C(f(x))` for some function `f`
 
How can we build a commitment scheme?

Let the commitment be equal to `C(x)`, where `C(x) = h(r||x), r <--R-- {0,1}^256`

 - To commit, we send `C(x)` to Bob but **not** `r`
 - To reveal it, we just send `r` to Bob
 - The randomization using `r` allows us to maintain the _secrecy_ property

Need: 

 - **OW** so that Bob cannot learn possible values for `x` 
   + need more for secrecy though, because if `h(r||x)` leaks info about `x`
     that could be good enough for Bob
   + seems like we need pseudo-randomness (PRF) as well
 - **CR** so that Alice cannot come up with `x, x'` where `h(x) = h(x')`, commit
   to `x` and then reveal `x'` instead of `x`
   B
   + CR implies TCR
 - **NM** so that Bob, or Mallory sitting between Alice and Bob, cannot change
   Alice's commitment in any way


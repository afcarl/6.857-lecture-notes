Today: Crypto math, Monday, March 3rd 
=====================================

 - finding primes
 - one time MAC
 - divisors, GCD, extended GCD, inverses
 - order of elements
 - generators

Finding primes
--------------

Generate & test:

    do 
        p <- k-bit integer
    until p is prime

What we need:

 - Are there a lot of `k`-bit primes?
 - Do we have a fast enough test to see if `p` is prime?

**Prime number theorem:** about `2^k/log(2^k)` k-bit primes. One out of 0.69k k-bit integers is a prime.

**Primality test:** if `p` is a prime, then `2^(p-1) = 1 (mod p)`. The other way is not necessarily true, but we can be fairly confident that if `2^(p-1) = 1 (mod p)` and `p` was chosen randomly then `p` is prime. (Why? How confident?) 

Other primality algorithms:

 - Miller-Rabin
 - AKS deterministic polytime

One-time MAC
------------

    A           m, t=MAC(t)            B
        ---------------------------->

            T
                    key = (slope,y-intercept) coordinates of the line?
            |     / 
        tag |----*
            |   /|
            |  / |
            | /  |
            |/   |
            ------------------ M
                msg


 - p large prime 128-bits
 - key `(a,b), 1 <= a,b <= p-1`
   + `a = slope`
   + `b = y-intercept`
 - `T = MAC_k(m) = am+b (mod p)` 

**Security:** If Eve learns `(M,T)` on the line and replaces with `(M', T')` then `Pr[ Bob accepts M', T' ] = 1/p`

**Proof:**

For fixed `m, m', t` s.t. `t = am + b (mod p)` (Equation 1)

For each `T', \exists` exactly one key `(a,b)` that satisfies Eq. 1 and `T' = aM' + b (mod p)`

**Note:** If you MAC two messages with the same `a,b,p` then you break the security

Divisors
--------

Notation: `d` divides `a` or `d` is a divisor of `a` -> `d | a <=> \exists k, s.t. a = dk`

 - `\forall d, d | 0`
 - `\forall a, 1 | 0`
 - if `d` divisor of `a` and `b` then `d` is a _common divisor_
 - greatest common divisor (gcd)
   + `gcd(0,0) = 0` by definition
   + `gcd(5,0) = 5`
   + `gcd(24,30) = 6`
   + `gcd(33,12) = 3`
 - `gcd(a, b) = 1 <=> a` and `b` are _relatively prime_

How can we find the gcd of two numbers?
---------------------------------------

### Euclid's algorithm


                  a, if b = 0
    gcd(a, b) = {
                  gcd(b, a mod b), otherwise


Example:

    gcd(7,5) = gcd(5, 2) = gcd(2,1) = gcd(1,0) = 1

Running time:

    lg(b)lg(a) bit operations

### Extended Euclidian algorithm

`\forall (a,b), \exists (x,y)` s.t. `ax + by = gcd(a,b)`

When a=7, b=5, what is x,y?

    7 = 7*1 + 5*0
    5 = 7*0 + 5*1

    2 = 7*1 + 5*-1 
    1 = 7*-2 + 5*3

    => (x,y)=(-2,3)

In previous lecture we said, that if `a \in Z*_p`, then `a^-1 = a^(p-2) mod p`

What if `a \in Z*_n = {x | 1 <= x <= n-1, gcd(x,n) = 1}`, where `n` is not prime?

 - this is called a multiplicative group `mod n`

How to find `a^-1`:

    a^-1 = ?
    \exists x,y s.t ax + ny = 1 ax = 1 (mod n) => a^-1 = x (mod n)

Order of elements
-----------------

Notion: The order of an element in a group like `Z*_p` or `Z*_n`

**Definition:** `order_n(a) = smallest t s.t. a^t = 1 (mod n)`, if `a \in Z*_n`

If `n=p` prime, then `t=p-1`

In general, Euler's theorem: `\forall n, \forall a \in Z*_n, a^\phi(n) = 1 (mod n)`, 
where `\phi(n)` is the _totient function_, `\phi(n) = # of elements relatively prime to n = | Z*_n |`

Example:
    
    Z*_10 = {1, 3, 7, 9}

    \phi(10) = 4

    3^4 = 7^4 = 9^4 = 1 (mod n)

Order:

    a, t, and a^t, n = 7

    a\t    1   2   3   4   5   6
    1      1   1   1   1   1   1    order_7(1) = 1
    2      2   4   1   2   4   1    order_7(2) = 3
    3      3   2   6   4   5   1    order_7(3) = 6
    4      4   2   1   4   2   1    order_7(4) = 3
    5      5   4   6   2   3   1    order_7(5) = 6
    6      6   1   6   1   6   1    order_7(6) = 2

Definition: `<a> = { a^t : t >= 0 }`

`<a>` is a subgroup of `Z*_n`, `<a> \included Z*_n` 

Example:

    <2> = {2, 4, 1}

Theorem: `|<a>| = order_n(a)`

Theorem: `|<a>| divides | Z*_n | <=> order_n(a) | \phi(n)`

Theorem: If `p` prime, then `|<a>| divides p-1` because `\phi(p) = p-1`

Generators
----------

Def: If `p` prime and `order_p(g) = p-1`, then `g` is a generator of `Z*_p`

Notation: `<g> = Z*_p`

Theorem: If `p` is prime, `g` is generator `mod p`, then `g^x = y (mod p) \forall y` has unique solution `x`

 - the discrete logarithm using the generator `g` base `p` of `y`
 - `x = dlog_p,g(y)`

Theorem: `Z*_n` has generator iff `n` is 2, 4, `p^m`, `2*p^m`, where `p` is an odd prime & `m >= 1`
 
 - we call such groups which have generators _cyclic groups_

Theorem: If `p` prim, then # of generators = `\phi(p-1)`

 - `p=7 => \phi(6) = |{1,5}| = 2`
 - `p=11 => \phi(10) = |{1,3,7,9}| = 4`

### How to find generators

Factor `\phi(p) = p-1`.

Definition: If `p,q` primes, `p=2q+1` then `p` is a _sage prime_ and `q` is a _Sophie Germain prime_

 - `\phi(p) = p-1 = 2q`

Emipirically, prime `p` is safe with probability `~= 1/ln(p)`

Examples:

    p = 23, q = 11
    p = 11, q = 5
    p = 59, q = 29
    ...

We said that the order of all the subgroups divides the order of the group (earlier)

    order_p(a) = {1, 2, q, 2q}, a \in Z*_p

Generating generators of `Z*_p` (p safe):

    do
        g <- Z*_p
    until |<g>| = p-1

Test (TODO: what's going on here?)

    g != 1 (mod p)
    g^2 != 1 (mod p)
    g^q != 1 (mod p)
    g^2q = 1 (mod p) (Fermat's little theorem)

Theorem: If `p` safe, then # generators is `\phi(p-1) = q-1`

General theorem: If `p` prime, then # of generators is `\phi(p-1) >= (p-1)/(6*ln(ln(p-1)))`

Common public-key setup
-----------------------

Public parameters: 

 - `p` large prime (2048 bit)
 - `g` generator of `Z*_p`

Alice's secret key is `x \in Z*_p, 1 <= x <= p-1`, the public key is `g^x = y (mod p)`
 
 - given `y` there is a unique solution `x` for the equation
 - given `y` it is assumed to be very hard to find `x`



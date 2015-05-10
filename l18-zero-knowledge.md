Today: Zero-knowledge proofs, Monday, April 13th 
================================================

Today:

 - zero-knowledge proofs
 - interactive proofs, ZK
 - **Examples:** Sudoku, 3-colorability, graph iso, hamiltonian cycle (HC), 
   discrete log (DL)
 - any problem in NP has a ZK proof

Zero-knowledge proof
--------------------

We have a _prover_ (Peggy) and a _verifier_ (Victor) and some common input 
`x` which is the statement to be proved.

It's going to be an interactive proof, where Peggy and Victor are exchanging
messages over multiple rounds. At the end, the Victor can accept the proof
or reject it.

    P   ---------------->   V
        <----------------
         
        ----------------> 
        <----------------
         
        ----------------> 
        <----------------
                        
                            (P,V)(x) = True/False

The prover may be powerful (large computation power, or more commonly he knows
something about why the statement `x` is true and he can use that).

### Basic properties

 - Completeness, if `x` is a true statement, then `V` accepts
 - Soundness, if `x` is false, then `V` rejects with prob `> 0`
 - Zero-knowledge, `V` learns nothing beyond fact of whether `x` is true or not 

### "Quality control"

 - widget factory
 - either widgets are perfect (A) _or_ 1 in `k` of them are bad (B)
 - pick `t*k` widgets to test
 - probability that you find no defective widgets given that 1 in `k` of them are
   bad is `(1 - 1/k)^tk ~= (e^(-1/k))^tk = e^-t`
   + `P(no bad widgets | B)`

### Commitments

    c = commit(v, r)
    open(c) -> (v, r)

We wanted two properties out of a commitment scheme

 - _Hiding:_ seeing `c` should reveal no information about `v`
 - _Binding:_ sender can only open the commitment up in one way
 - we saw Pedersen commitments
   + `c = g^v * h^r`, `g,h` generators, `r` random 
   + it was perfectly hiding and computationally binding

Sudoku example
--------------
    
    *---*---*---*
    |   |   |   |
    *---*---*---*
    |   |   |   |
    *---*---*---*
    |   |   |   |
    *---*---*---*

How can I convince you I know a solution to a Sudoku puzzle, without telling you
anything about the solution?

Suppose we make up codes for the numbers, s.t. each number is a letter

    1 2 3 4 5 6 7 8 9 
    O B F H I E G C A

But this is a one to one mapping, so if we just translated our solution to this
the verifier can just extract the solution and learn it.

If we use commitments for each letter, then we can hide the solution.

A challenge can be "open a commitment to a row/column/block". Note that know 
the verifier will learn some mappings. So now the verifier will want to ask again,
which means you'd better remap so that he does not start learning the actual
numbers.

The prover can't cheat because he commits himself to a certain "ciphertext" of
the Sudoku so he has to make sure that his commitment is an actual solution, because
the verifier could query it anywhere (block, row, column) and since the prover
is committed he won't be able "change" or "tune" his answer.

Stages:

 - commit to random table mapping numbers to letters
 - commit to the 9x9 table, each square is a commitment to a letter
 - send all these commitments to the verifier along with the Sudoku problem
 - verifier wants to check that all letters in a block/row/column
   are different and that the letters match the numbers in the original
   Sudoku problem
   + verifier can only do only one check in this round
   + he can do another in the next round, where you remap the numbers to letters
     to prevent him from learning anything

Note: seems like you need to make sure a unique set of 9 letters are used, otherwise
the prover might use extra letters to cheat

Graph 3-colorability
--------------------

Prover has a graph and knows a 3-coloring of the graph, where each vertex is
assigned a color out of 3 colors s.t. no two adjacent vertices have the same color.

The prover's solution is the mapping from vertex to color.

Phase I:

 - prover commits to all colors and sends it to the verifier
 - verifier picks an edge and asks prover to open the two commitments
   and the commitments of the colors
 - note that the verifier could learn the vertex colors if we just repeat this
 - we permute the colors (B -> G, R -> B, G -> R)
 - now verifier has no idea if the "red" in round 1 was also a "red" in some
   later round

If the prover does not know a coloring, then whatever I commit to has to be 
bad on some edge `=>` verifier will discover it at some point

Note that the transcript of the zero-knowledge exchange looks random. It'll have a 
list of random vertices and random colors, so it seems no one should be able to
learn anything from it.

Graph ismorphism
----------------

Hard to solve for two big graphs `G` and `H`.

The solution is a mapping from the vertex #s of the first graph to the vertex #s 
of the second graph: `(1->c, 2->d, 4->a, 3->b)`

As a prover, if I know the isomorphism, I can come up with a third graph `J` that is
isomorphic to both of them (by just reordering the vertices randomly).

    1 -> c -> u
    2 -> d -> t
    4 -> a -> r
    3 -> b -> s

Verifier can now ask you to reveal the isomorphism from `G` to `J` or from
`H` to `J`, but not both.

ZK is complete 

ZK is sound. Suppose G and H are not isomorphic, or you don't know the isomorphism.
You will have to pick one of G or H to derive J from. Suppose you pick G and H. 
If the verifier asks you for the isomorphism between J and H, you do not know
it and sending a fake one will not pass the verifier's check.

Hamiltonian cycle
-----------------

Prover and verifier have a graph G and prover knows a hamiltonian cycle in it.

 - generate a random isomorphic copy H of G
 - verifier asks for either the Hamiltonian cycle in H or the isomorphism between
   G and H
 - repeat

Discrete log
------------

Schnorr protocol for showing knowledge of the discrete log of `y = g^x`.

 - `p` is a prime, `p = 2q+1`, `q` is prime, `g` generates `Z_q`
 - secret key `x` (in `Z_p` or `Z_q`?)
 - public key `y = g^x` (`\in Z_q` because `g` generates `Z_q`?)

Schnorr protocol:

        P                                   V

    k <--R-- Z_q
    a = g^k                 a
                ------------------------>
                            c
                <------------------------ c <--R-- Z_q
    r = cx + k              r
                ------------------------> checks if
                                            y^c * a = g^r <=>
                                            (g^x)^c * g^k = g^(cx + k) <=>
                                            g^(cx+k) = g^(cx+k)

If I don't know `x` what are your chances of catching me? 

Equivalent:

 - I don't know `x =>` I can't play the game
 - I can play game `=>` I know `x`

If can play the game, I know `x`:

**Attack:** If the prover uses the same `k` twice, then the verifier can extract `x`.

    a = g^k

    r = cx + k
    r' = c'x + k
    -------------
    x = (r-r')/(c-c')

**Theorem:** Protocol is zero-knowledge.

**Proof:** After a round is over, verifier has `a, c, r` and they are all
random elements of `Z_q`. Prover hasn't given verifier any info because
the verifier could compute `a` given `c` and `r`.

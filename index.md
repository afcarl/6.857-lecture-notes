Computer and Network Security (6.857, Spring 2015)
==================================================

Lectures
--------
Lecture notes from 6.857, taught by [Prof. Ronald L. Rivest](http://people.csail.mit.edu/rivest/). Some lecture notes are exactly the ones posted on the 6.857 [course website](https://courses.csail.mit.edu/6.857/2015/)

 * Lecture 1: [Introduction](lec-slides/L01-course-introduction.pdf)
 * Lecture 2: (Cancelled):
 * Lecture 3: [Security principles](lec-slides/L03-security-principles.pdf) and
   [Growth of crypto](lec-slides/L03-growth-of-crypto.pdf)
 * Lecture 4: [One-time pad](lec-slides/L04-one-time-pad.pdf)
 * Lecture 5: [Hash functions I](l05-hash-1.html): random oracle model (ROM),
   one-way, collision-resistance, target collision resistance, preimage attack,
   second preimage attack, pseudo-randomness, non-malleability, hashed passwords,
   digital signatures, commitment schemes
 * Lecture 6: [Hash functions II](l06-hash-2.html): puzzles, Hashcash ('97), 
   Merkle's public-key crypto using puzzles, Merkle-Damgaard construction, 
   Davies-Meyer construction, MD5
 * Lecture 7: [Cryptocurrencies](l07-bitcoin.html): atoms vs. bits, Bitcoin,
   public ledger, multiple-in multiple out (MIMO) transactions, 
 * Lecture 8: [Ciphers I](l08-ciphers-1.html): Shamir's secret sharing, block
   ciphers, DES, AES
 * Lecture 9: [Ciphers II](l09-ciphers-2.html): ideal block cipher, modes of 
   operation, electronic codebook mode (ECB), counter mode (CTR), cipher-block 
   chaining mode (CBC), cipher feedback mode (CFB), indistinguishability under
   chosen-ciphertext attack (IND-CCA), unbalanced feistel encryption
 * Lecture 10: [Stream ciphers](l10-stream-ciphers.html): RC4, Spritz, ChaCha
 * Lecture 11: [Message authentication codes](l11-macs.html): HMAC, CBC-MAC,
   PRF-MAC, One-time MAC (OTMac), authenticated encryption with associated data
   (AEAD), EAX mode, encrypt-then-MAC, finite fields and number theory
 * Lecture 12: [Crypto math I](l12-crypto-math-1.html): primality testing, one-time
   MAC, the Totient function (phi), divisors, greatest common divisor (GCD),
   (Extended) Euclid's algorithm, order of group elements, generators, Fermat's
   little theorem, Lagrange's theorem, why we pick safe primes
 * Lecture 13: [Crypto math II](l13-crypto-math-2.pdf): group theory review,
   Diffie-Hellman key-exchange, Zp*, Zn*, Qp, Qn
 * Lecture 14: [Public key crypto I](l14-public-key.html): commitment schemes,
   Pedersen commitments, ElGamal, Decisional Diffie-Hellman (DDH) problem
 * Lecture 15: [Public key crypto II](l15-more-public-key.html): IND-CCA2 security
   Cramer-Shoup, RSA, making RSA IND-CCA2-secure, other RSA security aspects
 * Lecture 16: [Digital signatures](l16-digital-sign.html): hash and sign, RSA
   PKCS, RSA PSS, ElGamal, Digital Signature Algorithm (DSA)
 * Lecture 17: [Bilinear maps](l17-bilinear-maps.html): gap groups, bilinear maps,
   Boneh-Lynn-Shacham (BLS) signatures, 3-way key agreement (Joux), identity-based encryption (IBE)
 * Lecture 18: [Zero knowledge proofs](l18-zero-knowledge.html): zero-knowledge
   proofs (ZKPs), interactive proofs, Sudoku, 3-colorability, graph isomorphism,
   Hamiltonian cycle, discrete log
 * Lecture 19: **Computing on encrypted data** _[guest lecture](l19-computing-on-encrypted-data.html)_ by Vinod Vaikuntanathan: 
 * Lecture 20: [Electronic voting](l20-electronic-voting.html): public voting,
   paper ballots, lever machines, punch cards, optical scan, Direct Recording by
   Electronics (DRE), Voter Verified Paper Audit Trail (VVPAT), DRE+VVPAT, vote 
   by mail, internet voting (oh dear God), voting requirements, security threats,
   end-to-end voting security, Twin (Rivest and Smith), Scantegrity (Chaum et al)

Papers
------

Papers we read in 6.857 ([directory here](papers/)):

 * [Bitcoin](papers/bitcoin.pdf), Satoshi Nakamoto
 * [Research Perspectives and Challenges for Bitcoin and Cryptocurrencies](papers/princeton-bitcoin-overview.pdf), Princeton University
 * [AES Proposal: Rijndael](papers/rijndael.pdf)
 * [How to share a secret](papers/shamir-secret-sharing.pdf), Adi Shamir
 * [The EAX mode of operation](papers/eax.pdf)
 * [New paradigms for constructing symmetric encryption schemes secure under CCA](papers/desai.pdf), via Unbalanced Feistel Encryption
 * [Unlinkable serial transactions: Protocol and applications](papers/unlinkable-serial-transactions.pdf)
 * [A method for obtaining digital signatures and public-key cryptosystems](papers/rsa-paper.pdf), Rivest, Shamir, Adleman
 * [Twenty years of attacks on the RSA cryptosystem](papers/rsa-attacks.pdf), Dan Boneh
 * [New directions in cryptography](papers/diffie-hellman.pdf), Diffie-Hellman
 * [Cramer-Shoup cryptosystem](papers/cramer-shoup.pdf)
 * [ElGamal cryptosystem](papers/elgamal.pdf)
 * [FIPS PUB 186-4: Digital Signature Standard (DSS)](papers/dsa.pdf)
 * [Sequences of Games: A Tool for Taming Complexity in Security Proofs](papers/games.pdf)

Slides, articles
----------------
 
 * [Spritz](papers/spritz-slides.pdf) slides
 * [How to choose an authenticated encryption mode](papers/how-to-choose-an-ae-mode.pdf), Matthew Green
 * [Intro to Bilinear Maps](papers/bilinear-maps.pdf)

TODOs
-----

 * Lecture 6: MD5 drawing

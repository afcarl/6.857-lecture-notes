Today: Ciphers II, Wed. March 4th, 
=================

 - Ideal block cipher: what might this be?
 - Modes of operation
   + ECB, CTR, CBC (Cipher Block Chaining), CFB (Cipher Feedback Mode)
   + Ideal (IND-CCA defn)
   + Desai's "UFE" mode (Unbalanced Feistel Encryption)
 - Project idea: "Program Obfuscation"

Today's project idea: "Program obfuscation"

 - How do you take a program $P$ and give it to $A$ so that $A$ can execute it but not reverse engineer it

Ideal block cipher
------------------

What should an ideal block cipher look like?

Remember an ideal hash function was the "random oracle."

$$
    Enc(k, m): {0,1}^b \times {0,1}^b -> {0,1}^b
$$

What we want: for each key $k$: $Enc(K, \cdot)$ is a random permutation of the message space ${0,1}^b$

Just like we assumed random oracles for hash functions, we also assume random block ciphers that are ideal!

Modes of operation
------------------

Better term would be _domain extension_.

What definition can we give for security of a _mode of operation?_

We'll see that all these modes are hopefully bad under current definition of security.

We assume a _fixed input length_ block cipher that we want to transform into a variable input length encryption mode!

### Electronic Code Book (ECB) mode

Let $m = m_1, m_2, \dots, \m_n$ after we divide it into $n$ equal sized chunks. 

In ECB, $c = E(m) = E(m_1), E(m_2), \dots, E(m_n)$

If message length is not a multiple of cipher block size $b$ we can pad it out.
 
 - Add $1$ and as many zeros as needed to get to multiple of $b$ bits.
 - What if message actually finishes like this?
   + We always add the padding!

TODO: Look into padding oracle attacks!

 - ECB reveals $m_i = m_j$ because $c_i$ will equal $c_j$
 - ECB doesn't hide the patterns across message blocks very well

#### Ciphertext stealing

 - $m = m_1, m_2, |m_2| \lt b$
 - Encrypt the first block $c_1 = E(m_1)$ and steal part of it $p$ and include it in $c_2$
 - $c_2 = E(m_2 | c_2)$
 - Let $c_1'$ be $c_1$ without $p$ You output $c_2 | c_1'$ (you switch them)

### Counter mode (CTR)

 - Let $i$ be our counter
 - $c_i = E(i) \xor m_i$
 - No padding issues because we can just XOR as many bits as we have in the last block
 - $i$ value can be sent in the clear to allow people who have the key to decrypt
 - You shouldn't reuse the $E(i), E(i+1), ...$ pad (just like in OTR)
   + This means use different $i$'s for different messages
   + **Important:** If you encrypt $n$ blocks with IV $i$, then your next IV should 
     be $\gt i + n$
 - Note that since AES is a PRP, you will never see repetitions among
   the $E(i)$ pads
 - If AES was a PRF, you would start seeing repeated $E(i)$'s after $\approx 2^64$ 
   encryptions

### Cipher Block Chaining (CBC) mode

To encrypt:

 - pick a random IV $i$
 - $c_1 = E(m_1 \xor i)$
 - $c_2 = E(m_2 \xor c_1)$
 - $c_3 = E(m_3 \xor c_2)$
 - ...

Note: You need padding if your last block is $\lt b$, where $b$ is the cipher's block size.

To decrypt:
 
 - note that we can parallelize

IVs:

 - $i = Enc(k, nonce)$
   + TODO: not clear this is a good idea, look into requirements for CBC IVs

Cipher block chaining can be used for Message Authentication Codes (MACs).

 - integrity and authentication of message can be a goal sometimes
 - we want Bob to only accept a message if it was sent by Alice

Example:

                    m, MAC(k, m)                    k
        Alice -----------------------------------> Bob 
          k              
                                    Bob checks if MAC is correct for k and m

What can we use a MAC? We sort of need a complicated function of every block
of the message and the key $k$

 - We can use the last block in CBC mode
   + Note: IV has to be set to zero!
     - TODO: lookup attack from SBU
 - If you deal with variable length messages, you have to further tweak
   this by making the key for the last block different
   + TODO: why? prevents a certain class of attacks

#### Authentication and confidentiality

What can you do to get both? Encrypt plaintext $p$ into $c$. Then compute MAC over $c$.

 - TODO: explain why MACing $p$ can be bad

### Cipher Feedback (CFB) mode

 - $c_1 = m_1 \xor E(i)$
 - $c_2 = m_2 \xor E(c_2)$
 - ...
 - One advantage over CBC is that you don't need padding for CFB
   + It uses XOR to compute the ciphertext

Are these modes any good?
-------------------------

### Chosen ciphertext attack (IND-CCA)

IND-CCA2 game: 

 - key $k$ picked at random (adversary does not see it0
   + define $E, D$ operations for encrypting and decrypting under $k$
     - variable input length encryption
 - **Phase I:** Let the adversary play around w/ encryption, decryption boxes
   + will decrypt or encrypt or both anything the adversary wants
   + at the end, adversary output two message $m_0$ and $m_1$ of the same length
 - **Phase II:**
   + Examiner picks $d \leftarrow {0,1}$ randomly
   + examiner outputs $y = E(m_d)$ as the _challenge ciphertext_
   + adversary is given $y$ and access to $E$ and $D$
     - examiner will not let adversary decrypt $y$
     - adversary should not be able to tell which message ($m_0$ or $m_1$) was encrypted
   + adversary picks $d\hat when he's sure and outputs it
     - he wins if $d = d\hat$ or loses otherwise

Note: The encryption scheme better be randomized or _stateful_ if it's gonna satisfy this

 + randomized encryption will not let adversary to just encrypt $m_0$ and $m_1$ and do a simple
   equality test on $y$
 + or it could be stateful and remember it encrypted $m$ before and output a different ciphertext the 2nd time


LOL: We can do exams the same way: Have all students come up with a question and then let them take the exam.
One student mentioned they can share questions and win the game. Ron said "yes, but you'd still have to solve them 
so I would win because you would learn the material"

**Definition:** Encryption scheme is IND-CCA secure if adversary wins with probability $1/2 + \epsilon$ where 
$\epsilon$ is negligible

Which modes satisfy IND-CCA2?

 - ECB mode is deterministic, so won't win
 - CTR mode is bad because in Phase II adversary can take $y$, flip a bit and ask the examiner to decrypt it
   + examiner will do it
   + adversary can see clearly whether result is $m_0$ and $m_1$
 - CBC mode is bad because can flip bits in $c_1$ and encryptions of $c_2, c_3,  ...$ will stay the same
 - Another attack is to take a prefix of the ciphertext and ask the decryption box to decrypt it
   + you can the tell between results
   + Bad property that these modes have w.r.t/ IND-CCA2: decrypt prefix of ciphertext $\Rightarrow$ you get the prefix of message

#### How do we fix these modes?

 - Better be randomized

Unbalanced Feistel Encryption
-----------------------------

We take an arbitrarily long message $m$ and we encrypt it by XORing it with a pad, that we obtain
by running a block cipher in counter mode under some key $k_i$ and encrypting a random value $r$.
 
 - TODO: Is the CTR mode box that generates the pad, is fixed input and variable output? Whaaaat?

The problem with CTR mode was that the initial value for the counter was transmitted in the clear
over the wire.
 - TODO: what?

We take a random value $r$ in ${0,1}^b$

$c$ is CBC MAC'd under $k_2, k_3$ and XORs result with $r$ and obtains $\sigma$

Ctext is $(c, \sigma)$

How does he decrypt?



Atoms vs. Bits
--------------

 - Possessing value means what?
 - How to transfer value?

Bit-based system: bits can be copied (double spending)

**Token-based representation:** like actual coins

**Account-based representation:** like banks that store your value for you, you have to trust them

Bit-coin is _still an account-based system_, but it's distributed and less trust
needs to be put in. No central authority.

Let's think of what an electronic system would look like

 - User `u` has some public key `pk_u` and some secret key `sk_u`.
 - The bank (one global bank) would have its own public key `pk_b` and secret
   key `sk_b` and can certify user `u`
    + it signs a certificate `cert(u, pk_u) = sign_{sk_b}(u | pk_u)`
 - What is a check?
    + `sign_{sk_u}("Pay Bob $100, date, ser #")`
       - serial number is used to prevent a merchant from charging user `u`
         multiple times using the same check

Properties that a currency or monetary system might have that the check system
above does not? Or properties in general!

 - No trusted third party (like the bank above)
 - anonymity (a check would reveals payer and payee)
 - unique coins (not sure what difference they are pointing at here between this
   currency and the electronic system above)
 - no single point of failure
 - fast transactions
 - control of money supply
   + interesting topic in itself
 - no double spending
 - cheap transactions
 - scalable (handle millions of transactions a day)
 - hard to forge (can't make new money, or new payments)
 - need a way to reverse transactions (like chargeback)
 - fraud management/detection
 - variable denominations ($1, $2, $5, $10, $20)
 - divisibility
 - backup value (in Bitcoin losing your SK is disastrous) 
 - exchange w/ other systems
 - DDOS resistance
 - taxation/regulation?
 - compelling for people to use?
 - good for micropayments

Can be hard to prevent system rollback, which can lead to double spending. Can
you detect it?

What would an electronic coin look like?

 - TTP: bank
 - Payer: Alice
 - Payee: Bob
 - Need authorization protocol for withdrawal
 - Need protocol for payment

Diagram:
        
                    TTP (bank accounts)
                 /       *
                /         \
    withdrawal /           \ deposit
              /             \
             *               \
          Alice   ------->   Bob
                  payment

Coin:
 
 - some random number `R` that is the coin's ID with a digital signature from
   the bank `s = sign_{sk_bank}(R)`
   + the coin is `c = R,s` 
 - bank has to keep an _unspent coins DB_ `{r1, r2, ...,}` to prevent double spending
 - when Alice wants to pay Bob, she can just give the coin `c = R, s`
   + Bob cannot verify whether coin `c` is unspent, until it's too late
   + Bank can tell if someone is double spending `c` but the bank cannot
     identify *who* is double spending the coin
     - it could be that Bob is double spending the coin `c` he got from Alice

Bitcoin
-------

Mixes a few ideas: 

 - electronic checks
 - HashCash
 - public ledger (blockchain) probably the most innovative idea

The history of all transactions is public! Not maintained by trusted party, but
via a broadcast system.

How do you identify parties? What are the identities?

 - Bitcoin uses public key crypto to identify people. 
 - Note one person can have multiple key pairs.
 - The account name is the public key and has a value associated with it on the public ledger

Public ledger: for each account, how much value is there in it?
 
 - really it stores all transactions, so you can infer the value in each account

Money is created by those maintaining the public ledger (miners)
 
 - miners add new transactions to the ledger
   + they get rewarded some bitcoins when they solve the puzzle required for this
   + no other way to create value in bitcoin (other than transaction fees?)

Transaction details:

 - Bitcoin transactions allow multiple input accounts (payers) and multiple output accounts (payees)
   - this is sometimes used to give change to yourself by setting one of the output accounts as your account
     + in practice people create new accounts and put their change in it, to preserve their anonymity
 - you don't wanna make it to easy adding to the ledger, otherwise people add too much junk
   + HashCash scheme solves this

Diagram:

TODO: reorder these
    
    head node (just added)

             |---------------------|               |------------------------|
    -------> | Block n-1           | ------------> | Block n                |
             | ---------           |               | -------                |
             | h_{n-2}, nonce      |               | h_{n-1}, nonce'        |
             | T1, T2, ..., Ti     |               | T1', T2', ..., Ti'     |
             |---------------------|               |------------------------|

             h_{n-1} = H(block_{n-1})              h_{n} = H(block_{n})
             must have k leading 0's               must also have k leading 0's
                                                   and note that block_{n}
                                                   includes the previous h_{n-1}

                                                   miner has to adjust nonce'
                                                   until h_{n} has k leading 0's


Diagram for forking:

                  |------------------------|                 |---------------------|
    ------------> | Block n-1              | --------------> | Block n             |
                  | ---------              |                 | -------             |
                  | h_{n-2}, nonce         | ---\            | h_{n-1}, nonce      |
                  | T1, T2, ..., Ti        |     \           | T1, T2, ..., Ti     |
                  |------------------------|      \          |---------------------|
                                                   \
                                                    \                                 
                                                     \       |---------------------|
                                                      \----> | Block n'            |
                                                             |                     |
                                                             | prev hash(n), nonce |
                                                             | T1', T2', ..., Ti'  |
                                                             |---------------------|

It can happen that two miners came up with a block at the same time and both add it, forking the chain


    [] -> [] -> [] -> [] ->  [] 
                         \
               A->B       -> []

**Rule of thumb:** wait like 6 blocks to make sure the incorporated blocks are really there and are not part of a fork that died

 - this is not that great though

Scalability:

 - BitCoin does like 7 transactions / second, VISA does like 3000/sec
 - fee that miners are getting halves every year
   + TODO: How is this implemented?
 - after no fees, transaction fees will be used to reward miners
   + but total # of bitcons will remain the same
   + except people lose their wallets, so some bitcoins will be inaccessible => problems
 - it's becoming harder to be a miner
   + monopoly on mining actually (Ghash holds half the supply of bitcoins?)
 - cannot create money by loaning?
 - "Majority is not enough" paper

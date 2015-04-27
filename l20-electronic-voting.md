Today: Security of voting systems, Monday, April 27th
=====================================================

Interesting application of cryptography. Challenging primarily because of the
need for a secret ballot (how individual people voted).

Voting is not just about producing an answer, but also evidence that the
answer is correct: convince losers that they lost fair and square

Voting tech survey
------------------

 - public voting
   + no secrecy of ballot
   + Problem: You can sell your vote, or be coerced
 - paper ballots
   + initially could have different ballots for each vote
   + then "Australian" ballot came in, 1893
   + same ballot, and people had to read the candidate names
     and write down their vote
     - controversial at the time because not all people could read and write
 - lever machines
   + easy to manipulate and increase counts
   + See "Behind the freedom curtain" (1957)
 - punch cards
   - invented in 1960s based on computerized punch card
   - now illegal due to HAVA (Help America Vote Act) of 2002
   - the famous "butterfly ballot"
     + human interface design for voting systems is critical
 - optical scan
 - Direct Recording by Electronics (DRE)
   + first used in 1970s
   + essentially a standalone computer
   + no state other than counts, produces no evidence

 - DRE + Voter-verified Paper Audit Trail (VVPAT)
   + "really terrible technology"
 - Vote by mail
   + Often used for absentee voting, but some states use it as default
   + Typically uses opscan ballots
   + suffers from retail fraud
     - voters can be coerced by boss/wife/etc
   + chain of custody
     - maybe vote gets lost
     - can confirm vote got there using a code, but not that your vote stayed
       the same
 - internet voting
   + doesn't seem like we have the technology for this
   + risks combining the worst features of vote-by-mail (coercion) with the
     problems of DRE's (software security) and then adding new vulnerabilities
     (DDOS, foreign power attacks)
   + Why?
     - Because we can?
     - More people will show up?
         + Political scientists say this is actually insignificant: when voting
           methods are changed, turnout stays about the same
   + Helios, Ben Adida
   + Civitas, Clarkson, Chong, Myers
 - etc.

Questions to ask of every voting system:

 - Does it produce the right answer?
 - Does the voter vote in private?
 - Does it produce evidence that the outcome is correct?

Retail fraud vs. wholesale fraud

 - retail fraud: by vote one by one
 - wholesale fraud: get hold of computers and change the counts (1000s of vote
   at the same time)

Voting requirements
-------------------

 - Voter registration: each eligible voter votes at most once
 - Voter privacy: no one can tell how any voter voted, even if voter
   wants it (to discourage selling of votes). no "receipt" for voter
 - Integrity: votes can't be changed, added or deleted; tally is accurate
 - Availability: voting systems is available for use when needed
 - Ease of use
 - Accessibility: for voters with disabilities
 - Assurance: verifiable integrity

Security threads
----------------

Adversaries:

 - Political zealots
 - Voters may wish to sell votes
 - Election officials may be partisan
 - Vendors may have evil insider
 - Foreign powers because result can affect them
 - ...really anybody

Threats:
 
 - dead people voting
 - ballot-box stuffing by election officials with votes from people who did not
   show up
 - coercion/intimidation/buying votes
 - replacing votes or memory cards
 - miscount
 - malicious software
 - viruses

Strategies:

 - can voter have a receipt? that won't work if her receipt has her vote in
   plaintext because voter can sell vote now

Software independence (SI): a voting system is software dependent if an undetected
error in the software can cause an undetectable change in the reported election
outcome

New voting system proposals: "end to end"
-----------------------------------------

 - uses web so voter can check that here ballot was counted as she intended

Properties:

 - votes verifiably cast as intended
 - votes verifiably collected as cast 
 - votes verifiably counted as collected

VVPAT only gets the first: once ballot is cast, "chain of custody" determines 
what happens

### Twin (Rivest and Smith)

 - "academic" proposal
 - each paper ballot has a copy made that is put in mixer bin
 - voter casts original paper ballot (which is scanned and published
   on web) and takes home from mixr bin a copy of some previous voter's ballot
   as a receipt
 - then voter can check that the receipt he got is on the web
 - can detect fraud, but you'd better have a plan for what to do

Twin has all the "end-to-end" properties.

## Scantegrity II (Chaum et al)

 - marries traditional opscan with modern crypto end-to-end methods
 - uses 
   + invisible ink for "confirmation codes"
     - special pens reveal confirmation codes when you mark your candidate
     - voters copy and take home CCs
     - officials post revealed CCs
     - voters can confirm posting (uses ballot serial number for lookup) and
       protest if incorrect
   + web  site
   + crypto in the back end
 - ballots can be scanned by ordinary scanners
 - ballots can be recounted by hand as usual
 


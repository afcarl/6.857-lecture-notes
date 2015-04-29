Today: Project presentations, Wednesday, April 29th
===================================================

Timing attacks
--------------

 - timing attacks, how to protect against them
 - [ctgrind](https://github.com/agl/ctgrind), a valgrind-based tool to check
   for timing attacks
 - timing attacks against individual instructions: `imul` and `idiv` on Intel
   are not constant time apparently
 - their work: patch valgrind to detect when these instructions are executed
   on secret input

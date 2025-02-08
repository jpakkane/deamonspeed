# Compiler daemon timing experiment

A "fake" implementation of [a compiler daemon that prebuilds the
standard
library](https://nibblestew.blogspot.com/2024/12/compiler-daemon-thought-experiment.html). It
performs all the same steps as a real compiler but instead of
compiling it just sleeps. All sleep time intervals are changeable so
people can easily evaluate what sort of a speedup they would get.

Basically:

- Start a background process
- Parse all stdlib headers
- When compiling, pass the file to the daemon process, fork it, compile

`genproject.py` creates a Ninja project that can then be built in the
usual way. Passing`--daemon` to it makes it use the daemon process.

On this laptop with 22 cores, compiling the code regularly takes 26
seconds while the daemon version takes 7 seconds. This is
approximately a 3.7x speedup.

# Compiler daemon timing experiment

Test implementation of [a compiler daemon that prebuilds the standard
library](https://nibblestew.blogspot.com/2024/12/compiler-daemon-thought-experiment.html).

Basically:

- Start a background process
- Parse all stdlib headers
- When compiling, pass the file to the daemon process, fork it, compile

`genproject.py` creates a Ninja project that can then be built in the
usual way. Passing`--daemon` to it makes it use the daemon process.

On this laptop with 22 cores, compiling the code regularly takes 26
seconds and 7 seconds with the daemon. This is approximately a 3.7x
speedup.
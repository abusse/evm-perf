// ID: byte-32b-const
// NAME: TODO
// DESC: TODO
// NOTE: Comparison and Bitwise Logic
// ITER:  50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000
// OVERHEAD: push-32b-const, push-1b-const, pop-prealloc
// #START-ITER
PUSH32 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
PUSH1 0x10
BYTE
POP

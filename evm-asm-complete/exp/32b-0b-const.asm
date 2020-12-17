// ID: exp-32b-0b-const
// NAME: TODO
// DESC: TODO
// NOTE: Arithmetic
// ITER: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000
// OVERHEAD: push-1b-const, push-32b-const, pop-prealloc
// #START-ITER
PUSH1 0x00
PUSH32 0x0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f0f
EXP
POP

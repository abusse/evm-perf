// ID: mulmod-32b-rand-zero
// NAME: TODO
// DESC: TODO
// NOTE: Arithmetic
// ITER: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000
// OVERHEAD: push-32b-const, push-32b-rand, push-32b-rand, pop-prealloc
// #START-ITER
PUSH32 0x0
PUSH32 #RAND,32
PUSH32 #RAND,32
MULMOD
POP

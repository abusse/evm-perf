// ID: exp-32b-1b-rand-f0
// NAME: TODO
// DESC: TODO
// NOTE: Arithmetic
// ITER: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000
// OVERHEAD: push-1b-const, push-32b-rand, pop-prealloc
// #START-ITER
PUSH1 0xF0
PUSH32 #RAND,32
EXP
POP

// ID: exp-32b-2b-rand-ff
// NAME: TODO
// DESC: TODO
// NOTE: Arithmetic
// ITER: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000
// OVERHEAD: push-2b-const, push-32b-rand, pop-prealloc
// #START-ITER
PUSH2 0xFFFF
PUSH32 #RAND,32
EXP
POP

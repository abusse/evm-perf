// ID: exp-32b-8b-rand-f0
// NAME: TODO
// DESC: TODO
// NOTE: Arithmetic
// ITER: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000
// OVERHEAD: push-8b-const, push-32b-rand, pop-prealloc
// #START-ITER
PUSH8 0xF0F0F0F0F0F0F0F0
PUSH32 #RAND,32
EXP
POP

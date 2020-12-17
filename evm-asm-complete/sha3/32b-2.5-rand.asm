// ID: sha3-32b-2.5-rand
// NAME: TODO
// DESC: TODO
// NOTE: SHA3
// ITER: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 4000
// OVERHEAD: push-1b-const, push-1b-rand, pop-prealloc
#MINIT,1024
// #START-ITER
PUSH1 0x50
PUSH1 #RAND,1
SHA3
POP

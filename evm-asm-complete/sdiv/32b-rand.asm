// ID: sdiv-32b-rand
// NAME: TODO
// DESC: TODO
// NOTE: Arithmetic
// ITER:  50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000
// OVERHEAD: push-32b-rand
PUSH32 #RAND,32
// #START-ITER
PUSH32 #RAND,32
SDIV

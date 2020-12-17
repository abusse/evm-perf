// ID: sdiv-32b-const-maxneg
// NAME: TODO
// DESC: Edgecase (-2^255)^-1
// NOTE: Arithmetic
// ITER: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000
// OVERHEAD: push-32b-const, push-32b-const, pop-prealloc
// #START-ITER
PUSH32 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
PUSH32 0xf000000000000000000000000000000000000000000000000000000000000000
SDIV
POP

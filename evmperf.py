#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The Photon main part."""
from __future__ import print_function

import argparse
from datetime import datetime

from core.analyze import analyze
from core.benchmark import benchmark
from core.output import output

#IUT: Final = "/Users/abusse/Documents/repositories/evm-perf/remote-evm.sh"
#ASM_PATH: Final = "../evm-asm-complete"


# Processing command line arguments
parser = argparse.ArgumentParser()
# Options
parser.add_argument('-i', '--iut', help='Path to IUT', dest='iut', required=True)
parser.add_argument('-b', '--benchmarks', help='Path to benchmarks folder', dest='benchmarks', required=True)
parser.add_argument('-r', '--runs', help='Number of runs for each benchmark', dest='runs', type=int, default=10000)
parser.add_argument('-o', '--output', help='Output path', dest='out', required=True)
args = parser.parse_args()

iut = args.iut
benchmarks = args.benchmarks
runs = args.runs
out = args.out

timestamp = datetime.now()

results = benchmark(iut, runs, benchmarks)
analyzed = analyze(results)
output(analyzed, out, timestamp)

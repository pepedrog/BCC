#! /bin/bash

set -o xtrace
make
ITERATIONS=10
SIZE=16
NAME=mandelbrot_seq
for ((i=1; i<=$ITERATIONS; i++)); do
	./$NAME -2.5 1.5 -2.0 2.0 $SIZE >> fullT.log 2>&1
	./$NAME -0.8 -0.7 0.05 0.15 $SIZE>> seahorseT.log 2>&1
	./$NAME 0.175 0.375 -0.1 0.1 $SIZE>> elephantT.log 2>&1
	./$NAME -0.188 -0.012 0.554 0.754 $SIZE>> triple_spiralT.log 2>&1
	SIZE=$(($SIZE * 2))
done

rm output.ppm

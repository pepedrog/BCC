#! /bin/bash

set -o xtrace

MEASUREMENTS=13
ITERATIONS=10
INITIAL_SIZE=16
TH_NUM=('1' '2' '4' '8' '16' '32')
SIZE=$INITIAL_SIZE


NAMES_TH=('mandelbrot_omp' 'mandelbrot_pth') 
make
mkdir results

NAME='mandelbrot_seq'
mkdir results/$NAME

for ((i=1; i<=$ITERATIONS; i++)); do
    perf stat -r $MEASUREMENTS ./$NAME -2.5 1.5 -2.0 2.0 $SIZE>> full.log 2>&1
    perf stat -r $MEASUREMENTS ./$NAME -0.8 -0.7 0.05 0.15 $SIZE>> seahorse.log 2>&1
    perf stat -r $MEASUREMENTS ./$NAME 0.175 0.375 -0.1 0.1 $SIZE>> elephant.log 2>&1
    perf stat -r $MEASUREMENTS ./$NAME -0.188 -0.012 0.554 0.754 $SIZE>> triple_spiral.log 2>&1
    SIZE=$(($SIZE * 2))
done

SIZE=$INITIAL_SIZE

mv *.log results/$NAME

for NAME in ${NAMES_TH[@]}; do
    mkdir results/$NAME
    
    for TH in ${TH_NUM[@]}; do

    	for ((i=1; i<=$ITERATIONS; i++)); do
           	 perf stat -r $MEASUREMENTS ./$NAME -2.5 1.5 -2.0 2.0 $SIZE $TH>> full$TH.log 2>&1
	   	 perf stat -r $MEASUREMENTS ./$NAME -0.8 -0.7 0.05 0.15 $SIZE $TH>> seahorse$TH.log 2>&1
       		 perf stat -r $MEASUREMENTS ./$NAME 0.175 0.375 -0.1 0.1 $SIZE $TH>> elephant$TH.log 2>&1
	         perf stat -r $MEASUREMENTS ./$NAME -0.188 -0.012 0.554 0.754 $SIZE $TH>> triple_spiral$TH.log 2>&1
           	 SIZE=$(($SIZE * 2))
    	 done

         SIZE=$INITIAL_SIZE

    done
    mv *.log results/$NAME
done
rm output.ppm

#! /bin/bash

set -o xtrace

MEASUREMENTS=5
ITERATIONS=1
TH_NUM=('8')
SIZE=1150

NAMES_TH=('mandelbrot_omp' 'mandelbrot_pth') 
NAME='mandelbrot_seq'
make
mkdir results_inter


mkdir results_inter/$NAME

for ((i=1; i<=$ITERATIONS; i++)); do
    perf record -F 60000 ./$NAME -2.5 1.5 -2.0 2.0 $SIZE && perf report>> full.log 2>&1
    perf record -F 60000 ./$NAME -0.8 -0.7 0.05 0.15 $SIZE && perf report>> seahorse.log 2>&1
    perf record -F 60000 ./$NAME 0.175 0.375 -0.1 0.1 $SIZE && perf report>> elephant.log 2>&1
    perf record -F 60000 ./$NAME -0.188 -0.012 0.554 0.754 $SIZE && perf report>> triple_spiral.log 2>&1
done


mv *.log results_inter/$NAME

for NAME in ${NAMES_TH[@]}; do
    mkdir results_inter/$NAME
    
    for TH in ${TH_NUM[@]}; do

    	for ((i=1; i<=$ITERATIONS; i++)); do
           	 perf record -F 60000 ./$NAME -2.5 1.5 -2.0 2.0 $SIZE $TH && perf report>> full$TH.log 2>&1
	   	 perf record -F 60000 ./$NAME -0.8 -0.7 0.05 0.15 $SIZE $TH && perf report>> seahorse$TH.log 2>&1
       		 perf record -F 60000 ./$NAME 0.175 0.375 -0.1 0.1 $SIZE $TH && perf report>> elephant$TH.log 2>&1
	         perf record -F 60000 ./$NAME -0.188 -0.012 0.554 0.754 $SIZE $TH && perf report>> triple_spiral$TH.log 2>&1
    	 done
    done
    mv *.log results_inter/$NAME
done
rm output.ppm
rm perf.data*

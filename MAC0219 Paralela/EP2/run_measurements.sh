#! /bin/bash

set -o xtrace

MEASUREMENTS=15
SIZE=4096

# CUDA parameters
CUDA_BLOCKS=('1' '512' '1024' '2048')
CUDA_RUN="./bin/mandelbrot_cuda"

# OMPI parameters
NUM_TASKS=('4' '8' '16' '32' '64')
MPI_RUN="mpirun -np"
MPI_BIN="./bin/mandelbrot_ompi"

# OMPI+OMP parameters
MPI_OMP_BIN="./bin/mandelbrot_ompi_omp"

MKDIR='mkdir -p'

make
${MKDIR} results
${MKDIR} results/cuda
${MKDIR} results/ompi
${MKDIR} results/ompi_omp

for BLOCKS in ${CUDA_BLOCKS[@]}; do
    for ((THREADS=4; THREADS<=2048; THREADS*=2)); do
        perf stat -r $MEASUREMENTS $CUDA_RUN -0.188 -0.012 0.554 0.754 $SIZE $BLOCKS\
                     $THREADS >> triple_spiral_"$BLOCKS"_"$THREADS".log 2>&1
    done
done

mv *.log results/cuda/

for ((i = 0; i < ${#NUM_TASKS[@]}; i+=1)) do
    perf stat -r $MEASUREMENTS $MPI_RUN ${NUM_TASKS[$i]} $MPI_BIN -0.188 -0.012 0.554 0.754 $SIZE\
    >> triple_spiral_${NUM_TASKS[$i]}.log 2>&1
done
mv *.log results/ompi/

for ((i = 0; i < ${#NUM_TASKS[@]}; i+=1)) do
    for ((THREADS=1; THREADS<=64; THREADS*=2)); do
        perf stat -r $MEASUREMENTS $MPI_RUN ${NUM_TASKS[$i]} $MPI_OMP_BIN -0.188 -0.012 0.554 0.754 \
        $SIZE $THREADS >> triple_spiral_${NUM_TASKS[$i]}_"$THREADS".log 2>&1
    done
done
mv *.log results/ompi_omp/

rm output.ppm

#include <stdio.h>

// For the CUDA runtime routines (prefixed with "cuda_")
#include <cuda_runtime.h>
#include <cuda.h>

// Device global variables
__device__ double c_x_min;
__device__ double c_x_max;
__device__ double c_y_min;
__device__ double c_y_max;

__device__ double pixel_width;
__device__ double pixel_height;

__device__ int iteration_max = 200;

__device__ int image_size;
__device__ int image_buffer_size;

__device__ int num_threads;
__device__ int th_per_block;
__device__ int pixels_per_thread;

__device__ int gradient_size = 16;
__device__ int colors[17][3] = {
    {66, 30, 15},
    {25, 7, 26},
    {9, 1, 47},
    {4, 4, 73},
    {0, 7, 100},
    {12, 44, 138},
    {24, 82, 177},
    {57, 125, 209},
    {134, 181, 229},
    {211, 236, 248},
    {241, 233, 191},
    {248, 201, 95},
    {255, 170, 0},
    {204, 128, 0},
    {153, 87, 0},
    {106, 52, 3},
    {16, 16, 16},
};

// Host global variables
dim3 num_blocks, threads_per_block;
int num_blocks_x, th_per_block_x;
int num_blocks_y, th_per_block_y;
int host_image_buffer_size;
unsigned char* image_buffer_host;

int i_x_max;
int i_y_max;

int check (cudaError_t& err, const char* msg) {
    if (err != cudaSuccess) {
        printf ("%s", msg);
        printf (" | Error: %s\n", cudaGetErrorString(err));
        return 1;
    }
    return 0;
}

void print_bad_arguments () {
    printf("usage: ./mandelbrot_seq c_x_min c_x_max c_y_min c_y_max"
    " image_size NUM_BLOCKS TH_PER_BLOCK \n");
    printf("examples with image_size = 11500:\n");
    printf("    Full Picture:         ./mandelbrot_cuda -2.5 1.5 -2.0 2.0 11500 4 64 \n");
    printf("    Seahorse Valley:      ./mandelbrot_cuda -0.8 -0.7 0.05 0.15 11500 4 64 \n");
    printf("    Elephant Valley:      ./mandelbrot_cuda 0.175 0.375 -0.1 0.1 11500 4 64 \n");
    printf("    Triple Spiral Valley: ./mandelbrot_cuda -0.188 -0.012 0.554 0.754 11500 4 64 \n");
}
// Get global variables from command line args
void init (int argc, char* argv[]) {
    // host variables
    double host_c_x_min, host_c_x_max;
    double host_c_y_min, host_c_y_max;
    int host_image_size;

    if (argc < 8) {
        print_bad_arguments();
        exit(0);
    }
    else {
        num_blocks_y = th_per_block_y = 1;

        sscanf(argv[1], "%lf", &host_c_x_min);
        sscanf(argv[2], "%lf", &host_c_x_max);
        sscanf(argv[3], "%lf", &host_c_y_min);
        sscanf(argv[4], "%lf", &host_c_y_max);
        sscanf(argv[5], "%d", &host_image_size);
        sscanf(argv[6], "%d", &num_blocks_x);
        if (argc == 8) {
            sscanf(argv[7], "%d", &th_per_block_x);
        }
        else if (argc == 10) {
            sscanf(argv[7], "%d", &num_blocks_y);
            sscanf(argv[8], "%d", &th_per_block_x);
            sscanf(argv[9], "%d", &th_per_block_y);
        }
        else {
            print_bad_arguments();
            exit(0);
        }

        host_image_buffer_size = host_image_size * host_image_size;

        int host_th_per_block = th_per_block_x * th_per_block_y;
        int host_num_threads = host_th_per_block * num_blocks_x * num_blocks_y;

        int host_pixels_per_thread = host_image_buffer_size / host_num_threads;

        i_x_max = host_image_size;
        i_y_max = host_image_size;
        double host_pixel_width = (host_c_x_max - host_c_x_min) / i_x_max;
        double host_pixel_height = (host_c_y_max - host_c_y_min) / i_y_max;
        // copy host variables to device
        cudaError_t err = cudaSuccess;
        cudaMemcpyToSymbol(c_x_min, &host_c_x_min, sizeof(double));
        cudaMemcpyToSymbol(c_x_max, &host_c_x_max, sizeof(double));
        cudaMemcpyToSymbol(c_y_min, &host_c_y_min, sizeof(double));
        cudaMemcpyToSymbol(c_y_max, &host_c_y_max, sizeof(double));
        cudaMemcpyToSymbol(image_size, &host_image_size, sizeof(int));
        cudaMemcpyToSymbol(num_threads, &host_num_threads, sizeof(int));
        cudaMemcpyToSymbol(th_per_block, &host_th_per_block, sizeof(int));
        cudaMemcpyToSymbol(pixel_width, &host_pixel_width, sizeof(double));
        cudaMemcpyToSymbol(pixel_height, &host_pixel_height, sizeof(double));
        cudaMemcpyToSymbol(pixels_per_thread, &host_pixels_per_thread, sizeof(int));
        cudaMemcpyToSymbol(image_buffer_size, &host_image_buffer_size, sizeof(int));
        err = cudaGetLastError();
        if (check(err, "Failed to copy command line args to device"))
            exit(EXIT_FAILURE);
    };
};

__device__
void update_rgb_buffer(unsigned char* image_buffer_device, int iteration, int pix) {
    int color;

    if (iteration == iteration_max) {
        image_buffer_device[pix * 3 + 0] = colors[gradient_size][0];
        image_buffer_device[pix * 3 + 1] = colors[gradient_size][1];
        image_buffer_device[pix * 3 + 2] = colors[gradient_size][2];
    } else {
        color = iteration % gradient_size;
        image_buffer_device[pix * 3 + 0] = colors[color][0];
        image_buffer_device[pix * 3 + 1] = colors[color][1];
        image_buffer_device[pix * 3 + 2] = colors[color][2];
    };
};

__global__
void compute_mandelbrot(unsigned char* image_buffer_device) {

    double z_x;
    double z_y;
    double z_x_squared;
    double z_y_squared;
    double escape_radius_squared = 4;

    int iteration;
    int i_x;
    int i_y;

    double c_x;
    double c_y;

    // Calculates pixel where current thread will start its work
    int my_block = blockIdx.x + gridDim.x * blockIdx.y;
    int my_thread_in_block = threadIdx.x + blockDim.x * threadIdx.y;

    int my_thread = my_block * th_per_block + my_thread_in_block;

    /* what thread will process each pixel ?
     *
     * Example: image 5x5 -> buffer_size = 25
     * 3 blocks of 3 threads -> 9 threads
     *
     * 2 4 7 - -
     * 1 4 6 - -
     * 1 3 6 8 -
     * 0 3 5 8 -
     * 0 2 5 7 -
     *
     * and the remaining pixels we process separetedly,
     * each thread process its remaining pixel in the end
     *
     * 2 4 7 5 0
     * 1 4 6 6 1
     * 1 3 6 8 2
     * 0 3 5 8 3
     * 0 2 5 7 4
     */

     // Its easier to process by pixels instead of by row-collunm
    int pix = my_thread * pixels_per_thread;
    int end_pixel = pix + pixels_per_thread;
    int my_rem_pixel = image_buffer_size - my_thread - 1;

    while (pix <= my_rem_pixel) {
        i_y = pix / image_size;
        i_x = pix % image_size;

        c_y = c_y_min + i_y * pixel_height;
        if (fabs(c_y) < pixel_height / 2) {
            c_y = 0.0;
        };

        c_x = c_x_min + i_x * pixel_width;

        z_x = 0.0;
        z_y = 0.0;

        z_x_squared = 0.0;
        z_y_squared = 0.0;

        for (iteration = 0;
            iteration < iteration_max && \
            ((z_x_squared + z_y_squared) < escape_radius_squared);
            iteration++) {
            z_y = 2 * z_x * z_y + c_y;
            z_x = z_x_squared - z_y_squared + c_x;
            z_x_squared = z_x * z_x;
            z_y_squared = z_y * z_y;
        };
        
        update_rgb_buffer(image_buffer_device, iteration, pix);

        pix++;

        // Treat remaining pixel
        if (pix == end_pixel) {
            if (my_rem_pixel >= pix) pix = my_rem_pixel;
            else break;
        }
    }
}

void allocate_image_buffer(unsigned char** image_buffer_device, size_t size) {
    // Our buffer, instead of a matrix, will be a continuous array

    // Allocate host memory
    image_buffer_host = (unsigned char*)malloc(sizeof(unsigned char) * size);

    // Allocate device memory
    cudaError_t err = cudaSuccess;
    err = cudaMalloc((void**)(image_buffer_device), size);

    // Test alloc success
    if (image_buffer_host == NULL) {
        fprintf(stderr, "Failed to allocate host vectors!\n");
        exit(EXIT_FAILURE);
    }
    if (check(err, "Failed to allocate device image buffer"))
        exit(EXIT_FAILURE);
};

void write_to_file() {
    FILE* file;
    const char* filename = "output.ppm";
    const char* comment = "# ";
    int max_color_component_value = 255;

    file = fopen(filename, "wb");

    fprintf(file, "P6\n %s\n %d\n %d\n %d\n", comment,
        i_x_max, i_y_max, max_color_component_value);

    for (int i = 0; i < host_image_buffer_size; i++) {
        fwrite(image_buffer_host + 3*i, 1, 3, file);
    };
    fclose(file);
};

int main(int argc, char* argv[]) {
    init(argc, argv);

    cudaError_t err;
    int rgb_size = 3;
    size_t size = host_image_buffer_size * rgb_size;

    unsigned char* image_buffer_device;
    allocate_image_buffer(&image_buffer_device, size);

    // Launch compute_mandelbrot CUDA Kernel
    num_blocks = dim3(num_blocks_x, num_blocks_y);
    threads_per_block = dim3(th_per_block_x, th_per_block_y);
    compute_mandelbrot<<<num_blocks, threads_per_block>>>(image_buffer_device);
    cudaDeviceSynchronize();
    err = cudaGetLastError();
    if (check(err, "Failed to launch compute_mandelbrot kernel"))
        exit(EXIT_FAILURE);

    // Copy the device result vector in device memory to the host result vector
    // in host memory.
    err = cudaMemcpy(image_buffer_host, image_buffer_device, size,
        cudaMemcpyDeviceToHost);
    if (check(err, "Failed to copy vector from device to host"))
        exit(EXIT_FAILURE);

    // Free device global memory
    err = cudaFree(image_buffer_device);
    if (check(err, "Failed to free device vector"))
        exit(EXIT_FAILURE);

    write_to_file();
    // Free host memory
    free(image_buffer_host);

    return 0;
}
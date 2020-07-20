#include "mpi.h"
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define  MASTER    0

double c_x_min, c_x_max;
double c_y_min, c_y_max;

double pixel_width, pixel_height;

int iteration_max = 200;
int image_size;
unsigned char *image_buffer;

const int rgb_size = 3;

int i_x_max, i_y_max;
int image_buffer_size;
int n_threads;

int gradient_size = 16;
int colors[17][3] = {
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

int get_index (int row, int col) {
    return row * rgb_size + col;
}

void allocate_image_buffer(){
    image_buffer = (unsigned char *) malloc(sizeof(unsigned char)
                        * image_buffer_size * rgb_size);
};

void free_image_buffer () {
    free(image_buffer);
};

void init(int argc, char *argv[]){
    if(argc < 6){
        printf("usage: mpirun mandelbrot_ompi_omp c_x_min c_x_max c_y_min c_y_max image_size n_threads\n");
        printf("Or...: mpirun mandelbrot_ompi_omp c_x_min c_x_max c_y_min c_y_max image_size\n");
        printf("(Default values to n_threads)\n");
        printf("examples with image_size = 4096:\n");
        printf("    Full Picture:         mpirun mandelbrot_ompi -2.5 1.5 -2.0 2.0 4096 4\n");
        printf("    Seahorse Valley:      mpirun mandelbrot_ompi -0.8 -0.7 0.05 0.15 4096 4\n");
        printf("    Elephant Valley:      mpirun mandelbrot_ompi 0.175 0.375 -0.1 0.1 4096 4\n");
        printf("    Triple Spiral Valley: mpirun mandelbrot_ompi -0.188 -0.012 0.554 0.754 4096 4\n");
        exit(0);
    }
    else{
        sscanf(argv[1], "%lf", &c_x_min);
        sscanf(argv[2], "%lf", &c_x_max);
        sscanf(argv[3], "%lf", &c_y_min);
        sscanf(argv[4], "%lf", &c_y_max);
        sscanf(argv[5], "%d", &image_size);
        if (argc > 6) sscanf(argv[6], "%d", &n_threads);
        else n_threads = 0;

        i_x_max           = image_size;
        i_y_max           = image_size;
        image_buffer_size = image_size * image_size; 

        pixel_width       = (c_x_max - c_x_min) / i_x_max;
        pixel_height      = (c_y_max - c_y_min) / i_y_max;

    };
};

void init_worker (char *argv[], int chunksize) {
    sscanf(argv[1], "%lf", &c_x_min);
    sscanf(argv[2], "%lf", &c_x_max);
    sscanf(argv[3], "%lf", &c_y_min);
    sscanf(argv[4], "%lf", &c_y_max);
    sscanf(argv[5], "%d", &image_size);

    i_x_max           = image_size;
    i_y_max           = image_size;
    image_buffer_size = chunksize;

    pixel_width       = (c_x_max - c_x_min) / i_x_max;
    pixel_height      = (c_y_max - c_y_min) / i_y_max;
}

void update_rgb_buffer (int iteration, int x, int y){
    int color;
    int ind = (i_y_max * y) + x;
    if(iteration == iteration_max){
        image_buffer[get_index(ind, 0)] = colors[gradient_size][0];
        image_buffer[get_index(ind, 1)] = colors[gradient_size][1];
        image_buffer[get_index(ind, 2)] = colors[gradient_size][2];
    }
    else{
        color = iteration % gradient_size;

        image_buffer[get_index(ind, 0)] = colors[color][0];
        image_buffer[get_index(ind, 1)] = colors[color][1];
        image_buffer[get_index(ind, 2)] = colors[color][2];
    };
};

void update_rgb_buffer_worker (int iteration, int x, int y, int begin_y){
    int color, offset, ind;

    offset = begin_y * i_y_max;

    ind = y * i_y_max + x - offset;

    if(iteration == iteration_max){
        image_buffer[get_index(ind, 0)] = colors[gradient_size][0];
        image_buffer[get_index(ind, 1)] = colors[gradient_size][1];
        image_buffer[get_index(ind, 2)] = colors[gradient_size][2];
    }
    else{
        color = iteration % gradient_size;
        image_buffer[get_index(ind, 0)] = colors[color][0];
        image_buffer[get_index(ind, 1)] = colors[color][1];
        image_buffer[get_index(ind, 2)] = colors[color][2];
    };
};

void write_to_file () {
    FILE * file;
    char * filename               = "output.ppm";
    char * comment                = "# ";

    int max_color_component_value = 255;

    file = fopen(filename,"wb");

    fprintf(file, "P6\n %s\n %d\n %d\n %d\n", comment,
            i_x_max, i_y_max, max_color_component_value);

    for (int i = 0; i < image_buffer_size*rgb_size; i+=rgb_size) {
        fwrite(&image_buffer[i], 1 , 3, file);
    };
    fclose(file);
};


void compute_mandelbrot (int begin_y, int end_y) {

    int iteration;
    int i_x, i_y;

    int rank;
    MPI_Comm_rank (MPI_COMM_WORLD, &rank);

    double c_x, c_y;
    double z_x, z_y;
    double z_x_squared, z_y_squared;
    double escape_radius_squared = 4;


    /************************OMP**********************************/
    if (n_threads > 0) omp_set_num_threads(n_threads);
    #pragma omp parallel for \
        shared (n_threads)\
        private(i_x, z_x, z_y, z_x_squared, z_y_squared, c_y, c_x, iteration)    

        for (i_y = begin_y; i_y < end_y; i_y++) {
            // printf ("Thread: %d\n", omp_get_thread_num ());
            c_y = c_y_min + i_y * pixel_height;

            if(fabs(c_y) < pixel_height / 2)
                c_y = 0.0;

            for(i_x = 0; i_x < i_x_max; i_x++) {
                c_x         = c_x_min + i_x * pixel_width;
                z_x         = 0.0;
                z_y         = 0.0;
                z_x_squared = 0.0;
                z_y_squared = 0.0;
 
                for(iteration = 0; iteration < iteration_max && \
                    ((z_x_squared + z_y_squared) < escape_radius_squared);
                    iteration++){
                    z_y         = 2 * z_x * z_y + c_y;
                    z_x         = z_x_squared - z_y_squared + c_x;
                    z_x_squared = z_x * z_x;
                    z_y_squared = z_y * z_y;
                }
                if (rank == MASTER)
                    update_rgb_buffer (iteration, i_x, i_y);
                else 
                    update_rgb_buffer_worker (iteration, i_x, i_y, begin_y);
            }
        }
    
}

int main(int argc, char *argv[]){
    int size, rank, rows, chunksize, leftover, n, begin_y, end_y, tag1, tag2, source, dest;
    MPI_Status status;

    init (argc, argv);

    /*Start MPI */

    MPI_Init (&argc, &argv);

    MPI_Comm_size (MPI_COMM_WORLD, &size);
    MPI_Comm_rank (MPI_COMM_WORLD, &rank);

    rows = image_size / size;
    chunksize = image_buffer_size / size;
    leftover  = image_buffer_size % size; //cant be distributed equally if > 0

    //send and receive tags
    tag1 = 1; //ints
    tag2 = 2; //matrix

    // MASTER TASK
    if (rank == MASTER) {
        allocate_image_buffer();
        //printf("mpi_mm has started with %d tasks.\n", size);
        /* Send each task its portion of the work, some more than others (+1) */
        begin_y = rows;
        end_y = begin_y + rows;
        for (dest = 1; dest < size; dest++) {
            if (dest <= leftover) end_y++;
            chunksize = (end_y - begin_y) * 3 * image_size;

            MPI_Send  (&begin_y,    1, MPI_INT, dest, tag1, MPI_COMM_WORLD);
            MPI_Send  (&end_y,      1, MPI_INT, dest, tag1, MPI_COMM_WORLD);
            MPI_Send  (&image_size, 1, MPI_INT, dest, tag1, MPI_COMM_WORLD);
            //printf ("Sent %d elements to task %d. To start: %d\n", chunksize, dest, begin_y * i_x_max);
            begin_y = end_y;
            end_y += rows;
        }

        /* Master does its part of the work */
        compute_mandelbrot (0, rows);

        /* Wait to receive results from each task */
        for (int i = 1; i < size; i++) {
            source = i;
            MPI_Recv (&begin_y, 1, MPI_INT, source, tag1, MPI_COMM_WORLD, &status);
            MPI_Recv ( &end_y , 1, MPI_INT, source, tag1, MPI_COMM_WORLD, &status);
            chunksize = (end_y - begin_y) * image_size;
            int start_index = get_index(begin_y * i_x_max, 0);
            MPI_Recv (&image_buffer[start_index], chunksize * 3, MPI_UNSIGNED_CHAR, source, tag2, MPI_COMM_WORLD, &status);
        }

        //printf ("Writing to file........ \n");

        write_to_file();

        free_image_buffer ();
    }  /* end of master section */

    //WORKER TASK
    if (rank > MASTER) {  
        /* Receive my portion of matrix from the master task */
        source = MASTER;
        
        MPI_Recv (&begin_y,    1, MPI_INT, source, tag1, MPI_COMM_WORLD, &status);
        MPI_Recv (&end_y,      1, MPI_INT, source, tag1, MPI_COMM_WORLD, &status);
        MPI_Recv (&image_size, 1, MPI_INT, source, tag1, MPI_COMM_WORLD, &status);

        int chunksize = (end_y - begin_y) * image_size;

        init_worker (argv, chunksize);

        allocate_image_buffer ();

        /* Do my part of the work */

        compute_mandelbrot (begin_y, end_y);
        
        /* Send my results back to the master task */
        dest = MASTER;
        MPI_Send (&begin_y, 1, MPI_INT, dest, tag1, MPI_COMM_WORLD);
        MPI_Send (&end_y  , 1, MPI_INT, dest, tag1, MPI_COMM_WORLD);
        MPI_Send (image_buffer, chunksize * 3, MPI_UNSIGNED_CHAR, MASTER, tag2, MPI_COMM_WORLD);

        free_image_buffer ();
        
    } /* end of non-master */

    MPI_Finalize();

    return 0;
};

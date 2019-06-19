#include <iostream>
#include <stdio.h>
#include <cmath>
#include <GL/glew.h>
#include <GL/glut.h>
#include <cuda_runtime_api.h>
#include <cuda_gl_interop.h>

#define N 10
#define T 27

using namespace std;

__global__ void alpha(cudaPitchedPtr devicePitchedPointer)
{   int ix =  blockIdx.x*blockDim.x+threadIdx.x;
    int iy =  blockIdx.y*blockDim.y+threadIdx.y;
    int iz =  blockIdx.z*blockDim.z+threadIdx.z;

    // Get attributes from device pitched pointer
    char     *devicePointer  =   (char *)devicePitchedPointer.ptr;
    size_t    pitch          =   devicePitchedPointer.pitch;
    size_t    slicePitch     =   pitch * 3; //dimension y

    char *current_slice = devicePointer + iz * slicePitch;
    float *current_row = (float*)(current_slice + iy * pitch);
    current_row[ix] = current_row[ix] + 1;
}

int main(void)
{
    // Set up test data
    float image_data[3][3][3] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26};
    // Allocate 3D memory on the device
    cudaExtent volumeSizeBytes = make_cudaExtent(sizeof(float) * N, N, N);
    cudaPitchedPtr devicePitchedPointer;
    cudaMalloc3D(&devicePitchedPointer, volumeSizeBytes);

    cudaMemcpy3DParms p0 = { 0 }; 
    p0.srcPtr.ptr = image_data;
    p0.srcPtr.pitch = 3 * sizeof(float);
    p0.srcPtr.xsize = 3;
    p0.srcPtr.ysize = 3;
    p0.dstPtr.ptr = devicePitchedPointer.ptr;
    p0.dstPtr.pitch = devicePitchedPointer.pitch;
    p0.dstPtr.xsize = 3;
    p0.dstPtr.ysize = 3;
    p0.extent.width = 3 * sizeof(float);
    p0.extent.height = 3;
    p0.extent.depth = 3;
    p0.kind = cudaMemcpyHostToDevice;
    cudaMemcpy3D(&p0);

    // Kernel Launch Configuration
    dim3 threads_per_block = dim3(3, 3, 3);
    dim3 blocks_per_grid = dim3(1, 1, 1);
    alpha<<<blocks_per_grid, threads_per_block>>>(devicePitchedPointer);

    p0.srcPtr.ptr = devicePitchedPointer.ptr;
    p0.srcPtr.pitch = devicePitchedPointer.pitch;
    p0.dstPtr.ptr = image_data;
    p0.dstPtr.pitch = 3 * sizeof(float); 
    p0.kind = cudaMemcpyDeviceToHost;
    cudaMemcpy3D(&p0);
    
    for(int i=0; i < 3; i++){
        for(int j=0; j < 3; j++){
            for(int k=0; k < 3; k++){
                cout << image_data[i][j][k] << endl;
            }
        }
    }
    cudaFree(&devicePitchedPointer.ptr);
}
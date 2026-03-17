# tilelang.contrib.cutedsl.grid_syncÂ¶

Grid-level synchronization for CuTeDSL backend.

Implements a software grid barrier using atomic operations on a device-global counter declared via llvm.mlir.global. Requires cooperative kernel launch (cuLaunchCooperativeKernel) to guarantee all thread blocks are resident.

The barrier: 1\. __syncthreads() within each block 2\. Thread 0 atomically increments global counter, spin-waits until all blocks arrive 3\. Thread 0 resets counter 4\. __syncthreads() within each block

## FunctionsÂ¶

`sync_grid`() | Synchronize all thread blocks in a grid.  
---|---  
  
## Module ContentsÂ¶

tilelang.contrib.cutedsl.grid_sync.sync_grid()Â¶
    

Synchronize all thread blocks in a grid.

NOTE: This requires the kernel to be launched with cuLaunchCooperativeKernel to guarantee all blocks are resident simultaneously. The CuTeDSL wrapper handles this automatically when the kernel uses sync_grid().

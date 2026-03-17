# tilelang.language.kernelÂ¶

Kernel launching language interface in TileLang.

## ClassesÂ¶

`FrameStack` | A simple stack-like wrapper around a deque that provides  
---|---  
`KernelLaunchFrame` | KernelLaunchFrame is a custom TIRFrame that manages block/thread indices  
  
## FunctionsÂ¶

`Kernel`(*blocks[, threads, cluster_dims, is_cpu, prelude]) | Tools to quickly construct a GPU kernel launch frame.  
---|---  
`get_thread_binding`([dim]) | Returns the thread binding for the given dimension.  
`get_thread_bindings`() | Returns all three thread bindings.  
`get_block_binding`([dim]) | Returns the block binding for the given dimension.  
`get_block_bindings`() | Returns all three block bindings.  
`get_thread_extent`([dim]) | Returns the thread extent for the given dimension.  
`get_thread_extents`() | Returns all three thread extents.  
`get_block_extent`([dim]) | Returns the block extent for the given dimension.  
`get_block_extents`() | Returns all three block extents.  
  
## Module ContentsÂ¶

_class _tilelang.language.kernel.FrameStackÂ¶
    

A simple stack-like wrapper around a deque that provides push, pop, and top methods for convenience.

push(_item_)Â¶
    

Pushes an item onto the top of the stack.

pop()Â¶
    

Pops and returns the top of the stack, or returns None if the stack is empty.

top()Â¶
    

Returns the item on the top of the stack without removing it, or None if the stack is empty.

size()Â¶
    

Returns the number of items in the stack.

__len__()Â¶
    

Returns the number of items in the stack.

__bool__()Â¶
    

Allows truthy checks on the stack object itself, e.g., âif stack: â¦â

_class _tilelang.language.kernel.KernelLaunchFrameÂ¶
    

Bases: `tvm.script.ir_builder.tir.frame.TIRFrame`

KernelLaunchFrame is a custom TIRFrame that manages block/thread indices and handles the entry and exit of the kernel launch scope.

__enter__()Â¶
    

Enters the KernelLaunchFrame scope and pushes this frame onto the stack. Returns one Var if we detect exactly 5 frames (meaning there is a single block dimension), or a list of Vars otherwise.

Return type:
    

tvm.tir.Var | list[tvm.tir.Var]

__exit__(_ptype_ , _value_ , _trace_)Â¶
    

Exits the KernelLaunchFrame scope and pops this frame from the stack, but only if itâs indeed the topmost frame.

_classmethod _Current()Â¶
    

Returns the topmost (current) KernelLaunchFrame from the stack if it exists, or None if the stack is empty.

Return type:
    

KernelLaunchFrame | None

get_block_extent(_dim_)Â¶
    

Returns the block extent for the given dimension. dim=0 corresponds to blockIdx.x, dim=1 to blockIdx.y, and dim=2 to blockIdx.z.

Parameters:
    

**dim** (_int_)

Return type:
    

int

get_block_extents()Â¶
    

Returns the block extents for all three dimensions.

Return type:
    

list[int]

get_thread_extent(_dim_)Â¶
    

Returns the thread extent for the given dimension. dim=0 corresponds to threadIdx.x, dim=1 to threadIdx.y, and dim=2 to threadIdx.z.

Parameters:
    

**dim** (_int_)

Return type:
    

int

get_thread_extents()Â¶
    

Returns the thread extents for all three dimensions.

Return type:
    

list[int]

get_thread_binding(_dim =0_)Â¶
    

Returns the thread binding for the given dimension. dim=0 corresponds to threadIdx.x, dim=1 to threadIdx.y, and dim=2 to threadIdx.z.

Parameters:
    

**dim** (_int_)

Return type:
    

tvm.tir.Var

get_thread_bindings()Â¶
    

Returns the thread binding for the given dimension. dim=0 corresponds to threadIdx.x, dim=1 to threadIdx.y, and dim=2 to threadIdx.z.

Return type:
    

list[tvm.tir.Var]

get_num_threads()Â¶
    

Returns the thread indices from the topmost frame.

Return type:
    

int

get_block_binding(_dim =0_)Â¶
    

Returns the block binding for the given dimension. dim=0 corresponds to blockIdx.x, dim=1 to blockIdx.y, and dim=2 to blockIdx.z.

Parameters:
    

**dim** (_int_)

Return type:
    

tvm.tir.Var

get_block_bindings()Â¶
    

Returns all three block bindings.

Return type:
    

list[tvm.tir.Var]

_property _blocks _: list[tvm.tir.Var]_Â¶
    

Returns the block indices from the topmost frame.

Return type:
    

list[tvm.tir.Var]

_property _threads _: list[tvm.tir.Var]_Â¶
    

Returns the thread indices from the topmost frame.

Return type:
    

list[tvm.tir.Var]

_property _num_threads _: int_Â¶
    

Returns the total number of threads.

Return type:
    

int

tilelang.language.kernel.Kernel(_* blocks_, _threads =None_, _cluster_dims =None_, _is_cpu =False_, _prelude =None_)Â¶
    

Tools to quickly construct a GPU kernel launch frame.

Parameters:
    

  * **blocks** (_int_) â A list of extent, can be 1-3 dimension, representing gridDim.(x|y|z)

  * **threads** (_int_) â A integer representing blockDim.x Or a list of integers representing blockDim.(x|y|z) if the value is -1, we skip the threadIdx.x binding.

  * **cluster_dims** (_int_ _|__tuple_ _[__int_ _,__int_ _,__int_ _]__|__list_ _[__int_ _]__|__None_) â The cluster dimensions for SM90+ cluster launch. For example, use 2 or (2, 1, 1) to create 2-CTA clusters. When specified, the kernel will be launched using cudaLaunchKernelEx with cudaLaunchAttributeClusterDimension.

  * **is_cpu** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether the kernel is running on CPU. Thus we will not bind threadIdx.x, threadIdx.y, threadIdx.z. and blockIdx.x, blockIdx.y, blockIdx.z.

  * **prelude** (_str_) â The import c code of the kernel, will be injected before the generated kernel code.



Returns:
    

**res** â The result LaunchThreadFrame.

Return type:
    

Tuple[frame.LaunchThreadFrame]

Examples

Create a 1-D CUDA kernel launch and unpack the single block index:
    
    
    with T.Kernel(T.ceildiv(N, 128), threads=128) as bx:
        # bx is the blockIdx.x binding (also iterable as (bx,))
        ...
    

Launch a 2-D grid while requesting two thread dimensions:
    
    
    with T.Kernel(grid_x, grid_y, threads=(64, 2)) as (bx, by):
        tx, ty = T.get_thread_bindings()
        ...
    

Emit a CPU kernel where thread bindings are skipped:
    
    
    with T.Kernel(loop_extent, is_cpu=True) as (i,):
        ...
    

tilelang.language.kernel.get_thread_binding(_dim =0_)Â¶
    

Returns the thread binding for the given dimension.

Parameters:
    

**dim** (_int_)

Return type:
    

tvm.tir.Var

tilelang.language.kernel.get_thread_bindings()Â¶
    

Returns all three thread bindings.

Return type:
    

list[tvm.tir.Var]

tilelang.language.kernel.get_block_binding(_dim =0_)Â¶
    

Returns the block binding for the given dimension.

Parameters:
    

**dim** (_int_)

Return type:
    

tvm.tir.Var

tilelang.language.kernel.get_block_bindings()Â¶
    

Returns all three block bindings.

Return type:
    

list[tvm.tir.Var]

tilelang.language.kernel.get_thread_extent(_dim =0_)Â¶
    

Returns the thread extent for the given dimension.

Parameters:
    

**dim** (_int_)

Return type:
    

int

tilelang.language.kernel.get_thread_extents()Â¶
    

Returns all three thread extents.

Return type:
    

list[int]

tilelang.language.kernel.get_block_extent(_dim =0_)Â¶
    

Returns the block extent for the given dimension.

Parameters:
    

**dim** (_int_)

Return type:
    

int

tilelang.language.kernel.get_block_extents()Â¶
    

Returns all three block extents.

Return type:
    

list[int]

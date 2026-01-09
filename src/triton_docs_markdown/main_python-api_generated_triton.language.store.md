# triton.language.store¶

triton.language.store(_pointer_ , _value_ , _mask =None_, _boundary_check =()_, _cache_modifier =''_, _eviction_policy =''_, __semantic =None_)¶
    

Store a tensor of data into memory locations defined by pointer.

>   1. If pointer is a single element pointer, a scalar is stored. In this case:
> 
>      * mask must also be scalar, and
> 
>      * boundary_check and padding_option must be empty.
> 
>   2. If pointer is an N-dimensional tensor of pointers, an N-dimensional block is stored. In this case:
> 
>      * mask is implicitly broadcast to pointer.shape, and
> 
>      * boundary_check must be empty.
> 
>   3. If pointer is a block pointer defined by make_block_ptr, a block of data is stored. In this case:
> 
>      * mask must be None, and
> 
>      * boundary_check can be specified to control the behavior of out-of-bound access.
> 
> 


value is implicitly broadcast to pointer.shape and typecast to pointer.dtype.element_ty.

Parameters:
    

  * **pointer** (triton.PointerType, or block of dtype=triton.PointerType) – The memory location where the elements of value are stored

  * **value** (_Block_) – The tensor of elements to be stored

  * **mask** (_Block_ _of_ _triton.int1_ _,__optional_) – If mask[idx] is false, do not store value[idx] at pointer[idx]

  * **boundary_check** (_tuple_ _of_ _ints_ _,__optional_) – tuple of integers, indicating the dimensions which should do the boundary check

  * **cache_modifier** (str, optional, should be one of {“”, “.wb”, “.cg”, “.cs”, “.wt”}, where “.wb” stands for cache write-back all coherent levels, “.cg” stands for cache global, “.cs” stands for cache streaming, “.wt” stands for cache write-through, see [cache operator](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#cache-operators) for more details.) – changes cache option in NVIDIA PTX

  * **eviction_policy** (_str_ _,__optional_ _,__should be one_ _of_ _{""__,__"evict_first"__,__"evict_last"}_) – changes eviction policy in NVIDIA PTX




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.store(...)` instead of `store(x, ...)`.

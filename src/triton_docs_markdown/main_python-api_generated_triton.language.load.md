# triton.language.load¶

triton.language.load(_pointer_ , _mask =None_, _other =None_, _boundary_check =()_, _padding_option =''_, _cache_modifier =''_, _eviction_policy =''_, _volatile =False_, __semantic =None_)¶
    

Return a tensor of data whose values are loaded from memory at location defined by pointer:

>   1. If pointer is a single element pointer, a scalar is be loaded. In this case:
> 
>      * mask and other must also be scalars,
> 
>      * other is implicitly typecast to pointer.dtype.element_ty, and
> 
>      * boundary_check and padding_option must be empty.
> 
>   2. If pointer is an N-dimensional tensor of pointers, an N-dimensional tensor is loaded. In this case:
> 
>      * mask and other are implicitly broadcast to pointer.shape,
> 
>      * other is implicitly typecast to pointer.dtype.element_ty, and
> 
>      * boundary_check and padding_option must be empty.
> 
>   3. If pointer is a block pointer defined by make_block_ptr, a tensor is loaded. In this case:
> 
>      * mask and other must be None, and
> 
>      * boundary_check and padding_option can be specified to control the behavior of out-of-bound access.
> 
> 


Parameters:
    

  * **pointer** (triton.PointerType, or block of dtype=triton.PointerType) – Pointer to the data to be loaded

  * **mask** (Block of triton.int1, optional) – if mask[idx] is false, do not load the data at address pointer[idx] (must be None with block pointers)

  * **other** (_Block_ _,__optional_) – if mask[idx] is false, return other[idx]

  * **boundary_check** (_tuple_ _of_ _ints_ _,__optional_) – tuple of integers, indicating the dimensions which should do the boundary check

  * **padding_option** – should be one of {“”, “zero”, “nan”}, the padding value to use while out of bounds. “” means an undefined value.

  * **cache_modifier** (str, optional, should be one of {“”, “.ca”, “.cg”, “.cv”}, where “.ca” stands for cache at all levels, “.cg” stands for cache at global level (cache in L2 and below, not L1), and “.cv” means don’t cache and fetch again. see [cache operator](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#cache-operators) for more details.) – changes cache option in NVIDIA PTX

  * **eviction_policy** (_str_ _,__optional_) – changes eviction policy in NVIDIA PTX

  * **volatile** (_bool_ _,__optional_) – changes volatile option in NVIDIA PTX




# triton.language.make_tensor_descriptor¶

triton.language.make_tensor_descriptor(_base : [tensor](triton.language.tensor.html#triton.language.tensor "triton.language.core.tensor")_, _shape : List[[tensor](triton.language.tensor.html#triton.language.tensor "triton.language.core.tensor")]_, _strides : List[[tensor](triton.language.tensor.html#triton.language.tensor "triton.language.core.tensor")]_, _block_shape : List[constexpr]_, _padding_option ='zero'_, __semantic =None_) → [tensor_descriptor](triton.language.tensor_descriptor.html#triton.language.tensor_descriptor "triton.language.core.tensor_descriptor")¶
    

Make a tensor descriptor object

Parameters:
    

  * **base** – the base pointer of the tensor, must be 16-byte aligned

  * **shape** – A list of non-negative integers representing the tensor shape

  * **strides** – A list of tensor strides. Leading dimensions must be multiples of 16-byte strides and the last dimension must be contiguous.

  * **block_shape** – The shape of block to be loaded/stored from global memory




Notes

On NVIDIA GPUs with TMA support, this will result in a TMA descriptor object and loads and stores from the descriptor will be backed by the TMA hardware.

Currently only 2-5 dimensional tensors are supported.

Example
    
    
    @triton.jit
    def inplace_abs(in_out_ptr, M, N, M_BLOCK: tl.constexpr, N_BLOCK: tl.constexpr):
        desc = tl.make_tensor_descriptor(
            in_out_ptr,
            shape=[M, N],
            strides=[N, 1],
            block_shape=[M_BLOCK, N_BLOCK],
        )
    
        moffset = tl.program_id(0) * M_BLOCK
        noffset = tl.program_id(1) * N_BLOCK
    
        value = desc.load([moffset, noffset])
        desc.store([moffset, noffset], tl.abs(value))
    
    # TMA descriptors require a global memory allocation
    def alloc_fn(size: int, alignment: int, stream: Optional[int]):
        return torch.empty(size, device="cuda", dtype=torch.int8)
    
    triton.set_allocator(alloc_fn)
    
    M, N = 256, 256
    x = torch.randn(M, N, device="cuda")
    M_BLOCK, N_BLOCK = 32, 32
    grid = (M / M_BLOCK, N / N_BLOCK)
    inplace_abs[grid](x, M, N, M_BLOCK, N_BLOCK)
    

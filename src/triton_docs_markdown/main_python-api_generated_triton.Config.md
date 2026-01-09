# triton.Config¶

_class _triton.Config(_self_ , _kwargs_ , _num_warps =4_, _num_stages =3_, _num_ctas =1_, _maxnreg =None_, _pre_hook =None_, _ir_override =None_)¶
    

An object that represents a possible kernel configuration for the auto-tuner to try.

Variables:
    

  * **kwargs** – a dictionary of meta-parameters to pass to the kernel as keyword arguments.

  * **num_warps** – the number of warps to use for the kernel when compiled for GPUs. For example, if num_warps=8, then each kernel instance will be automatically parallelized to cooperatively execute using 8 * 32 = 256 threads.

  * **num_stages** – the number of stages that the compiler should use when software-pipelining loops. Mostly useful for matrix multiplication workloads on SM80+ GPUs.

  * **num_ctas** – number of blocks in a block cluster. SM90+ only.

  * **maxnreg** – maximum number of registers one thread can use. Corresponds to ptx .maxnreg directive. Not supported on all platforms.

  * **pre_hook** – a function that will be called before the kernel is called. Parameters of this function are args.

  * **ir_override** – filename of a user-defined IR (*.{ttgir|llir|ptx|amdgcn}).




__init__(_self_ , _kwargs_ , _num_warps =4_, _num_stages =3_, _num_ctas =1_, _maxnreg =None_, _pre_hook =None_, _ir_override =None_)¶
    

Methods

`__init__`(self, kwargs[, num_warps, ...]) |   
---|---  
`all_kwargs`(self) | 

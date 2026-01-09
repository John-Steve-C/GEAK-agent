# triton.language.range¶

_class _triton.language.range(_self_ , _arg1_ , _arg2 =None_, _step =None_, _num_stages =None_, _loop_unroll_factor =None_, _disallow_acc_multi_buffer =False_, _flatten =False_, _warp_specialize =False_, _disable_licm =False_)¶
    

Iterator that counts upward forever.
    
    
    @triton.jit
    def kernel(...):
        for i in tl.range(10, num_stages=3):
            ...
    

Note:
    

This is a special iterator used to implement similar semantics to Python’s `range` in the context of `triton.jit` functions. In addition, it allows user to pass extra attributes to the compiler.

Parameters:
    

  * **arg1** – the start value.

  * **arg2** – the end value.

  * **step** – the step value.

  * **num_stages** – 

pipeline the loop into this many stages (so there are `num_stages` iterations of the loop in flight at once).

Note this is subtly different than passing `num_stages` as a kernel argument. The kernel argument only pipelines loads that feed into `dot` operations, while this attribute tries to pipeline most (though not all) loads in this loop.

  * **loop_unroll_factor** – Tells the Triton IR level loop unroller how many times to unroll a for loop that this range is used with. Less than 2 for this value implies no unrolling.

  * **disallow_acc_multi_buffer** – If true, prevent the accumulator of the dot operation in the loop to be multi-buffered, if applicable.

  * **flatten** – automatically flatten the loop nest starting at this loop to create a single flattened loop. The compiler will try to pipeline the flattened loop which can avoid stage stalling.

  * **warp_specialize** – Enable automatic warp specialization on the loop. The compiler will attempt to partition memory, MMA, and vector operations in the loop into separate async partitions. This will increase the total number of warps required by the kernel.

  * **disable_licm** – 

Tells the compiler it shouldn’t hoist loop invariant code outside the loop. This is often useful to avoid creating long liveranges within a loop.

Note that warp specialization is only supported on Blackwell GPUs and only works on simple matmul loops. Support for arbitrary loops will be expanded over time.




__init__(_self_ , _arg1_ , _arg2 =None_, _step =None_, _num_stages =None_, _loop_unroll_factor =None_, _disallow_acc_multi_buffer =False_, _flatten =False_, _warp_specialize =False_, _disable_licm =False_)¶
    

Methods

`__init__`(self, arg1[, arg2, step, ...]) |   
---|---  
  
Attributes

`type` |   
---|---

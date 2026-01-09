# triton.language.atomic_xor¶

triton.language.atomic_xor(_pointer_ , _val_ , _mask =None_, _sem =None_, _scope =None_, __semantic =None_)¶
    

Performs an atomic logical xor at the memory location specified by `pointer`.

Return the data stored at `pointer` before the atomic operation.

Parameters:
    

  * **pointer** (_Block_ _of_ _dtype=triton.PointerDType_) – The memory locations to operate on

  * **val** (_Block_ _of_ _dtype=pointer.dtype.element_ty_) – The values with which to perform the atomic operation

  * **sem** (_str_ _,__optional_) – Specifies the memory semantics for the operation. Acceptable values are “acquire”, “release”, “acq_rel” (stands for “ACQUIRE_RELEASE”), and “relaxed”. If not provided, the function defaults to using “acq_rel” semantics.

  * **scope** (_str_ _,__optional_) – Defines the scope of threads that observe the synchronizing effect of the atomic operation. Acceptable values are “gpu” (default), “cta” (cooperative thread array, thread block), or “sys” (stands for “SYSTEM”). The default value is “gpu”.




This function can also be called as a member function on [`tensor`](triton.language.tensor.html#triton.language.tensor "triton.language.tensor"), as `x.atomic_xor(...)` instead of `atomic_xor(x, ...)`.

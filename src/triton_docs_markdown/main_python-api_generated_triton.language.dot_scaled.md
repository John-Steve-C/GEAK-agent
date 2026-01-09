# triton.language.dot_scaled¶

triton.language.dot_scaled(_lhs_ , _lhs_scale_ , _lhs_format_ , _rhs_ , _rhs_scale_ , _rhs_format_ , _acc =None_, _fast_math =False_, _lhs_k_pack =True_, _rhs_k_pack =True_, _out_dtype =triton.language.float32_, __semantic =None_)¶
    

Returns the matrix product of two blocks in microscaling format.

lhs and rhs use microscaling formats described here: <https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf>

Software emulation enables targeting hardware architectures without native microscaling operation support. Right now for such case, microscaled lhs/rhs are upcasted to `bf16` element type beforehand for dot computation, with one exception: for AMD CDNA3 specifically, if one of the inputs is of `fp16` element type, the other input is also upcasted to `fp16` element type instead. This behavior is experimental and may be subject to change in the future.

Parameters:
    

  * **lhs** (_2D tensor representing fp4_ _,__fp8_ _or_ _bf16 elements. Fp4 elements are packed into uint8 inputs with the first element in lower bits. Fp8 are stored as uint8_ _or_ _the corresponding fp8 type._) – The first tensor to be multiplied.

  * **lhs_scale** (_e8m0 type represented as an uint8 tensor_ _, or_ _None._) – Scale factor for lhs tensor. Shape should be [M, K//group_size] when lhs is [M, K], where group_size is 32 if scales type are e8m0.

  * **lhs_format** (_str_) – format of the lhs tensor. Available formats: {`e2m1`, `e4m3`, `e5m2`, `bf16`, `fp16`}.

  * **rhs** (_2D tensor representing fp4_ _,__fp8_ _or_ _bf16 elements. Fp4 elements are packed into uint8 inputs with the first element in lower bits. Fp8 are stored as uint8_ _or_ _the corresponding fp8 type._) – The second tensor to be multiplied.

  * **rhs_scale** (_e8m0 type represented as an uint8 tensor_ _, or_ _None._) – Scale factor for rhs tensor. Shape should be [N, K//group_size] where rhs is [K, N]. Important: Do NOT transpose rhs_scale

  * **rhs_format** (_str_) – format of the rhs tensor. Available formats: {`e2m1`, `e4m3`, `e5m2`, `bf16`, `fp16`}.

  * **acc** – The accumulator tensor. If not None, the result is added to this tensor.

  * **lhs_k_pack** (_bool_ _,__optional_) – If false, the lhs tensor is packed into uint8 along M dimension.

  * **rhs_k_pack** (_bool_ _,__optional_) – If false, the rhs tensor is packed into uint8 along N dimension.




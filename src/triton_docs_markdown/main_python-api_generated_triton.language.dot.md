# triton.language.dot¶

triton.language.dot(_input_ , _other_ , _acc =None_, _input_precision =None_, _allow_tf32 =None_, _max_num_imprecise_acc =None_, _out_dtype =triton.language.float32_, __semantic =None_)¶
    

Returns the matrix product of two blocks.

The two blocks must both be two-dimensional or three-dimensional and have compatible inner dimensions. For three-dimensional blocks, tl.dot performs the batched matrix product, where the first dimension of each block represents the batch dimension.

Parameters:
    

  * **input** (2D or 3D tensor of scalar-type in {`int8`, `float8_e5m2`, `float16`, `bfloat16`, `float32`}) – The first tensor to be multiplied.

  * **other** (2D or 3D tensor of scalar-type in {`int8`, `float8_e5m2`, `float16`, `bfloat16`, `float32`}) – The second tensor to be multiplied.

  * **acc** (2D or 3D tensor of scalar-type in {`float16`, `float32`, `int32`}) – The accumulator tensor. If not None, the result is added to this tensor.

  * **input_precision** (string. Available options for nvidia: `"tf32"`, `"tf32x3"`, `"ieee"`. Default: `"tf32"`. Available options for amd: `"ieee"`, (CDNA3 only) `"tf32"`.) – How to exercise the Tensor Cores for f32 x f32. If the device does not have Tensor Cores or the inputs are not of dtype f32, this option is ignored. For devices that do have tensor cores, the default precision is tf32.

  * **allow_tf32** – _Deprecated._ If true, input_precision is set to “tf32”. Only one of `input_precision` and `allow_tf32` can be specified (i.e. at least one must be `None`).




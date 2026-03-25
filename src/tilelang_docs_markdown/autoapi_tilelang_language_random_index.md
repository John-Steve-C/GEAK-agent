# tilelang.language.randomÂ¶

## FunctionsÂ¶

`rng_init`(seed[, seq, off, generator]) | Initialize CUDA curand random number generator state  
---|---  
`rng_rand`() | Generate a 32-bit unsigned random integer  
`rng_rand_float`([bit, dist]) | Generate a random float  
  
## Module ContentsÂ¶

tilelang.language.random.rng_init(_seed_ , _seq =None_, _off =0_, _generator ='curandStatePhilox4_32_10_t'_)Â¶
    

Initialize CUDA curand random number generator state

Parameters:
    

  * **seed** (_PrimExpr_) â Random seed value.

  * **seq** (_PrimExpr_) â Sequence number for parallel random number generation.

  * **off** (_PrimExpr_) â Offset number for parallel random number generation.

  * **generator** (_StringImm_) â Set random generator. See <https://docs.nvidia.com/cuda/curand/group__DEVICE.html>



Returns:
    

**state** â The random number generator state handle.

Return type:
    

PrimExpr

tilelang.language.random.rng_rand()Â¶
    

Generate a 32-bit unsigned random integer

Returns:
    

**random_value** â A 32-bit unsigned random integer.

Return type:
    

PrimExpr

tilelang.language.random.rng_rand_float(_bit =32_, _dist ='uniform'_)Â¶
    

Generate a random float

Parameters:
    

  * **bit** (_int =__[__32_ _,__64_ _]_) â Bitwidth of random float.

  * **dist** (_StringImm =__[__"uniform"__,__"normal"__]_) â Random distribution.



Returns:
    

**random_value** â A random float.

Return type:
    

PrimExpr

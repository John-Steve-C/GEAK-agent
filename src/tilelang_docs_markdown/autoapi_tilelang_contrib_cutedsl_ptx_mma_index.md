# tilelang.contrib.cutedsl.ptx_mmaÂ¶

PTX MMA operations for CuTeDSL backend. Based on tl_templates/cuda/instruction/mma.h

These functions provide wrappers around PTX mma.sync instructions for performing matrix multiply-accumulate operations using Tensor Cores.

Uses inline PTX assembly for direct MMA instruction generation.

Supported dense configurations (from mma.h): \- FP16: m16n8k16 -> f16/f32 accumulator \- BF16: m16n8k16 -> f32 accumulator \- INT8: m16n8k32 -> i32 accumulator \- UINT8: m16n8k32 -> i32 accumulator \- INT4: m16n8k32 -> i32 accumulator (mapped to m16n8k64 in PTX) \- UINT4: m16n8k32 -> i32 accumulator \- FP8 (e4m3/e5m2): m16n8k32 -> f16/f32 accumulator \- TF32: m16n8k4, m16n8k8 -> f32 accumulator \- FP64: m8n8k4 -> f64 accumulator

Sparse (mma.sp) variants mirror the dense ones with halved A registers, an extra metadata register, and a sparse_selector literal.

## AttributesÂ¶

`ptx_mma_m16n8k16_f16_f16_f32` |   
---|---  
`ptx_mma_m16n8k16_f16_f16_f16` |   
`ptx_mma_m16n8k16_bf16_bf16_f32` |   
`ptx_mma_m16n8k32_s8_s8_s32` |   
`ptx_mma_m16n8k32_u8_u8_s32` |   
`ptx_mma_m16n8k32_s4_s4_s32` |   
`ptx_mma_m16n8k32_u4_u4_s32` |   
`ptx_mma_m16n8k4_tf32_tf32_f32` |   
`ptx_mma_m16n8k8_tf32_tf32_f32` |   
`ptx_mma_m8n8k4_f64_f64_f64` |   
`ptx_mma_m16n8k32_e4m3_e4m3_f32` |   
`ptx_mma_m16n8k32_e4m3_e4m3_f16` |   
`ptx_mma_m16n8k32_e5m2_e5m2_f32` |   
  
## FunctionsÂ¶

`ptx_mma`(shape, a_layout, b_layout, a_dtype, b_dtype, ...) | Generic PTX MMA dispatcher.  
---|---  
`ptx_mma_sp`(shape, a_layout, b_layout, a_dtype, ...[, ...]) | Generic PTX sparse MMA dispatcher.  
  
## Module ContentsÂ¶

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m16n8k16_f16_f16_f32Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m16n8k16_f16_f16_f16Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m16n8k16_bf16_bf16_f32Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m16n8k32_s8_s8_s32Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m16n8k32_u8_u8_s32Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m16n8k32_s4_s4_s32Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m16n8k32_u4_u4_s32Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m16n8k4_tf32_tf32_f32Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m16n8k8_tf32_tf32_f32Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m8n8k4_f64_f64_f64Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m16n8k32_e4m3_e4m3_f32Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m16n8k32_e4m3_e4m3_f16Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma_m16n8k32_e5m2_e5m2_f32Â¶
    

tilelang.contrib.cutedsl.ptx_mma.ptx_mma(_shape_ , _a_layout_ , _b_layout_ , _a_dtype_ , _b_dtype_ , _c_dtype_ , _a_ptr_ , _a_offset_ , _b_ptr_ , _b_offset_ , _c_ptr_ , _c_offset_ , _saturate =False_)Â¶
    

Generic PTX MMA dispatcher.

Dispatches to the appropriate specialized MMA function based on shape and data types.

Parameters:
    

  * **shape** (_str_)

  * **a_layout** (_str_)

  * **b_layout** (_str_)

  * **a_dtype** (_str_)

  * **b_dtype** (_str_)

  * **c_dtype** (_str_)

  * **saturate** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.contrib.cutedsl.ptx_mma.ptx_mma_sp(_shape_ , _a_layout_ , _b_layout_ , _a_dtype_ , _b_dtype_ , _c_dtype_ , _a_ptr_ , _a_offset_ , _b_ptr_ , _b_offset_ , _c_ptr_ , _c_offset_ , _meta_ptr_ , _meta_offset_ , _sparse_selector =0_, _saturate =False_)Â¶
    

Generic PTX sparse MMA dispatcher.

Dispatches to the appropriate specialized sparse MMA function based on shape and data types.

Parameters:
    

  * **shape** (_str_)

  * **a_layout** (_str_)

  * **b_layout** (_str_)

  * **a_dtype** (_str_)

  * **b_dtype** (_str_)

  * **c_dtype** (_str_)

  * **sparse_selector** (_int_)

  * **saturate** ([_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




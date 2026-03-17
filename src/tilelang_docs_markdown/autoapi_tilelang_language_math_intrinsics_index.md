# tilelang.language.math_intrinsicsÂ¶

Common math intrinsics exposed on the TileLang language surface.

## FunctionsÂ¶

`ieee_add`(x, y[, rounding_mode]) | IEEE-compliant addition with specified rounding mode  
---|---  
`ieee_sub`(x, y[, rounding_mode]) | IEEE-compliant subtraction with specified rounding mode  
`ieee_mul`(x, y[, rounding_mode]) | IEEE-compliant multiplication with specified rounding mode  
`ieee_fmaf`(x, y, z[, rounding_mode]) | IEEE-compliant fused multiply-add with specified rounding mode  
`ieee_frcp`(x[, rounding_mode]) | IEEE-compliant reciprocal with specified rounding mode  
`ieee_fsqrt`(x[, rounding_mode]) | IEEE-compliant square root with specified rounding mode  
`ieee_frsqrt`(x) | IEEE-compliant reciprocal square root (round to nearest only)  
`ieee_fdiv`(x, y[, rounding_mode]) | IEEE-compliant division with specified rounding mode  
`fadd2`(x, y) | Packed FP32x2 add.  
`fmul2`(x, y) | Packed FP32x2 multiply.  
`fma2`(x, y, z) | Packed FP32x2 fused multiply-add (x * y + z).  
  
## Module ContentsÂ¶

tilelang.language.math_intrinsics.ieee_add(_x_ , _y_ , _rounding_mode ='rn'_)Â¶
    

IEEE-compliant addition with specified rounding mode

Parameters:
    

  * **x** (_PrimExpr_) â First operand.

  * **y** (_PrimExpr_) â Second operand.

  * **rounding_mode** (_str_ _,__optional_) â Rounding mode: ârnâ (round to nearest), ârzâ (round toward zero), âruâ (round toward positive infinity), ârdâ (round toward negative infinity). Default is ârnâ.



Returns:
    

**result** â The result.

Return type:
    

PrimExpr

tilelang.language.math_intrinsics.ieee_sub(_x_ , _y_ , _rounding_mode ='rn'_)Â¶
    

IEEE-compliant subtraction with specified rounding mode

Parameters:
    

  * **x** (_PrimExpr_) â First operand.

  * **y** (_PrimExpr_) â Second operand.

  * **rounding_mode** (_str_ _,__optional_) â Rounding mode: ârnâ, ârzâ, âruâ, ârdâ. Default is ârnâ.



Returns:
    

**result** â The result.

Return type:
    

PrimExpr

tilelang.language.math_intrinsics.ieee_mul(_x_ , _y_ , _rounding_mode ='rn'_)Â¶
    

IEEE-compliant multiplication with specified rounding mode

Parameters:
    

  * **x** (_PrimExpr_) â First operand.

  * **y** (_PrimExpr_) â Second operand.

  * **rounding_mode** (_str_ _,__optional_) â Rounding mode: ârnâ, ârzâ, âruâ, ârdâ. Default is ârnâ.



Returns:
    

**result** â The result.

Return type:
    

PrimExpr

tilelang.language.math_intrinsics.ieee_fmaf(_x_ , _y_ , _z_ , _rounding_mode ='rn'_)Â¶
    

IEEE-compliant fused multiply-add with specified rounding mode

Parameters:
    

  * **x** (_PrimExpr_) â First operand.

  * **y** (_PrimExpr_) â Second operand.

  * **z** (_PrimExpr_) â Third operand (addend).

  * **rounding_mode** (_str_ _,__optional_) â Rounding mode: ârnâ, ârzâ, âruâ, ârdâ. Default is ârnâ.



Returns:
    

**result** â The result of x * y + z.

Return type:
    

PrimExpr

tilelang.language.math_intrinsics.ieee_frcp(_x_ , _rounding_mode ='rn'_)Â¶
    

IEEE-compliant reciprocal with specified rounding mode

Parameters:
    

  * **x** (_PrimExpr_) â Input operand.

  * **rounding_mode** (_str_ _,__optional_) â Rounding mode: ârnâ, ârzâ, âruâ, ârdâ. Default is ârnâ.



Returns:
    

**result** â The result of 1/x.

Return type:
    

PrimExpr

tilelang.language.math_intrinsics.ieee_fsqrt(_x_ , _rounding_mode ='rn'_)Â¶
    

IEEE-compliant square root with specified rounding mode

Parameters:
    

  * **x** (_PrimExpr_) â Input operand.

  * **rounding_mode** (_str_ _,__optional_) â Rounding mode: ârnâ, ârzâ, âruâ, ârdâ. Default is ârnâ.



Returns:
    

**result** â The result of sqrt(x).

Return type:
    

PrimExpr

tilelang.language.math_intrinsics.ieee_frsqrt(_x_)Â¶
    

IEEE-compliant reciprocal square root (round to nearest only)

Parameters:
    

**x** (_PrimExpr_) â Input operand.

Returns:
    

**result** â The result of 1/sqrt(x).

Return type:
    

PrimExpr

tilelang.language.math_intrinsics.ieee_fdiv(_x_ , _y_ , _rounding_mode ='rn'_)Â¶
    

IEEE-compliant division with specified rounding mode

Parameters:
    

  * **x** (_PrimExpr_) â Dividend.

  * **y** (_PrimExpr_) â Divisor.

  * **rounding_mode** (_str_ _,__optional_) â Rounding mode: ârnâ, ârzâ, âruâ, ârdâ. Default is ârnâ.



Returns:
    

**result** â The result of x/y.

Return type:
    

PrimExpr

tilelang.language.math_intrinsics.fadd2(_x_ , _y_)Â¶
    

Packed FP32x2 add.

Lowers to PTX add.rn.f32x2 on supported NVIDIA architectures/toolchains, and falls back to per-lane scalar operations otherwise.

Parameters:
    

  * **x** (_PrimExpr_) â First operand. Must be dtype `float32x2`.

  * **y** (_PrimExpr_) â Second operand. Must be dtype `float32x2`.



Returns:
    

**result** â A `float32x2` result.

Return type:
    

PrimExpr

tilelang.language.math_intrinsics.fmul2(_x_ , _y_)Â¶
    

Packed FP32x2 multiply.

Lowers to PTX mul.rn.f32x2 on supported NVIDIA architectures/toolchains, and falls back to per-lane scalar operations otherwise.

Parameters:
    

  * **x** (_tvm.tir.PrimExpr_)

  * **y** (_tvm.tir.PrimExpr_)



Return type:
    

tvm.tir.PrimExpr

tilelang.language.math_intrinsics.fma2(_x_ , _y_ , _z_)Â¶
    

Packed FP32x2 fused multiply-add (x * y + z).

Lowers to PTX fma.rn.f32x2 on supported NVIDIA architectures/toolchains, and falls back to per-lane scalar operations otherwise.

Parameters:
    

  * **x** (_tvm.tir.PrimExpr_)

  * **y** (_tvm.tir.PrimExpr_)

  * **z** (_tvm.tir.PrimExpr_)



Return type:
    

tvm.tir.PrimExpr

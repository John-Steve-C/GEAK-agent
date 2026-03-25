# tilelang.contrib.cutedsl.ieee_mathÂ¶

IEEE-754 compliant floating-point operations with explicit rounding modes.

These correspond to CUDA __fadd_rn, __fsub_rz, etc. Implemented via inline PTX to ensure exact rounding mode compliance.

Rounding modes: rn (nearest), rz (toward zero), rm (toward -inf), rp (toward +inf)

## FunctionsÂ¶

`ieee_fadd`(a, b[, rounding]) | IEEE-754 add with explicit rounding mode.  
---|---  
`ieee_fsub`(a, b[, rounding]) | IEEE-754 subtract with explicit rounding mode.  
`ieee_fmul`(a, b[, rounding]) | IEEE-754 multiply with explicit rounding mode.  
`ieee_fmaf`(a, b, c[, rounding]) | IEEE-754 fused multiply-add with explicit rounding mode.  
`ieee_frcp`(a[, rounding]) | IEEE-754 reciprocal with explicit rounding mode.  
`ieee_fsqrt`(a[, rounding]) | IEEE-754 square root with explicit rounding mode.  
`ieee_fdiv`(a, b[, rounding]) | IEEE-754 divide with explicit rounding mode.  
  
## Module ContentsÂ¶

tilelang.contrib.cutedsl.ieee_math.ieee_fadd(_a_ , _b_ , _rounding ='rn'_)Â¶
    

IEEE-754 add with explicit rounding mode.

tilelang.contrib.cutedsl.ieee_math.ieee_fsub(_a_ , _b_ , _rounding ='rn'_)Â¶
    

IEEE-754 subtract with explicit rounding mode.

tilelang.contrib.cutedsl.ieee_math.ieee_fmul(_a_ , _b_ , _rounding ='rn'_)Â¶
    

IEEE-754 multiply with explicit rounding mode.

tilelang.contrib.cutedsl.ieee_math.ieee_fmaf(_a_ , _b_ , _c_ , _rounding ='rn'_)Â¶
    

IEEE-754 fused multiply-add with explicit rounding mode.

tilelang.contrib.cutedsl.ieee_math.ieee_frcp(_a_ , _rounding ='rn'_)Â¶
    

IEEE-754 reciprocal with explicit rounding mode.

tilelang.contrib.cutedsl.ieee_math.ieee_fsqrt(_a_ , _rounding ='rn'_)Â¶
    

IEEE-754 square root with explicit rounding mode.

tilelang.contrib.cutedsl.ieee_math.ieee_fdiv(_a_ , _b_ , _rounding ='rn'_)Â¶
    

IEEE-754 divide with explicit rounding mode.

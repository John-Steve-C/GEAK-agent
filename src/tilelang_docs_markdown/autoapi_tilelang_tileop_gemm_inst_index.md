# tilelang.tileop.gemm.instÂ¶

## ClassesÂ¶

`GemmInst` | Enum where members are also (and must be) ints  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.tileop.gemm.inst.GemmInstÂ¶
    

Bases: `enum.IntEnum`

Enum where members are also (and must be) ints

MMA _ = 0_Â¶
    

WGMMA _ = 1_Â¶
    

TCGEN5MMA _ = 2_Â¶
    

MFMA _ = 3_Â¶
    

Scalar _ = 4_Â¶
    

is_mma()Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_wgmma()Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_tcgen5mma()Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_mfma()Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_scalar()Â¶
    

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

__repr__()Â¶
    

Return repr(self).

Return type:
    

str

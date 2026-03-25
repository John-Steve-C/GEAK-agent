# tilelang.language.warpgroupÂ¶

The language interface for tl programs.

## AttributesÂ¶

`ws` |   
---|---  
  
## ClassesÂ¶

`WarpSpecializeFrame` | WarpSpecializeFrame is a custom TIRFrame that manages warp group indices  
---|---  
  
## FunctionsÂ¶

`WarpSpecialize`(*warp_group_idx) | Tools to construct a warp group frame.  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.language.warpgroup.WarpSpecializeFrameÂ¶
    

Bases: `tvm.script.ir_builder.tir.frame.TIRFrame`

WarpSpecializeFrame is a custom TIRFrame that manages warp group indices and handles the entry and exit of the kernel launch scope.

tilelang.language.warpgroup.WarpSpecialize(_* warp_group_idx_)Â¶
    

Tools to construct a warp group frame.

Parameters:
    

**warp_group_idx** (_int_) â A integer representing warp group index Or a list of integers representing blockDim.(x|y|z) if the value is -1, we skip the threadIdx.x binding.

Returns:
    

  * **res** (_Tuple[frame.LaunchThreadFrame]_) â The result LaunchThreadFrame.

  * _Examples_ â >>> T.ws(0) -> if tx < 128 >>> T.ws(1) -> if tx >= 128 and tx < 256 >>> T.ws(0, 1) -> if tx < 128 or (tx >= 128 and tx < 256)




Return type:
    

WarpSpecializeFrame

tilelang.language.warpgroup.wsÂ¶
    

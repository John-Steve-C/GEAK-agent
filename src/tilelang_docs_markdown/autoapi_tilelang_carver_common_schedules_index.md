# tilelang.carver.common_schedulesÂ¶

Common schedule strategies for TIR.

## FunctionsÂ¶

`get_block`(sch, blocks, name) | Get the target block from a schedule.  
---|---  
`get_output_blocks`(sch, blocks) | Get the output blocks of a schedule.  
`try_inline`(sch, blocks) | Try to inline as many blocks as possible, and return the remaining blocks.  
`try_inline_contiguous_spatial`(sch, block_infos) | Try to inline contiguous spatial blocks in a schedule  
  
## Module ContentsÂ¶

tilelang.carver.common_schedules.get_block(_sch_ , _blocks_ , _name_)Â¶
    

Get the target block from a schedule.

Parameters:
    

  * **sch** (_tir.Schedule_) â The TIR schedule used to get target block.

  * **name** (_str_) â The name of the target block.

  * **blocks** (_list_ _[_[_tilelang.carver.analysis.BlockInfo_](../analysis/index.html#tilelang.carver.analysis.BlockInfo "tilelang.carver.analysis.BlockInfo") _]_)



Returns:
    

**target_block** â The target block.

Return type:
    

BlockRV

tilelang.carver.common_schedules.get_output_blocks(_sch_ , _blocks_)Â¶
    

Get the output blocks of a schedule.

Parameters:
    

  * **sch** (_tir.Schedule_) â The TIR schedule used to get output blocks.

  * **blocks** (_List_ _[_[_BlockInfo_](../analysis/index.html#tilelang.carver.analysis.BlockInfo "tilelang.carver.analysis.BlockInfo") _]_) â The blocks to be analyzed.



Returns:
    

**output_blocks** â The output blocks.

Return type:
    

List[[BlockInfo](../analysis/index.html#tilelang.carver.analysis.BlockInfo "tilelang.carver.analysis.BlockInfo")]

tilelang.carver.common_schedules.try_inline(_sch_ , _blocks_)Â¶
    

Try to inline as many blocks as possible, and return the remaining blocks.

Parameters:
    

  * **sch** (_tir.Schedule_) â The TIR schedule used to inline blocks.

  * **blocks** (_List_ _[_[_BlockInfo_](../analysis/index.html#tilelang.carver.analysis.BlockInfo "tilelang.carver.analysis.BlockInfo") _]_) â The blocks to be inlined.



Returns:
    

**remaining** â The remaining blocks that cannot be inlined.

Return type:
    

List[[BlockInfo](../analysis/index.html#tilelang.carver.analysis.BlockInfo "tilelang.carver.analysis.BlockInfo")]

tilelang.carver.common_schedules.try_inline_contiguous_spatial(_sch_ , _block_infos_)Â¶
    

Try to inline contiguous spatial blocks in a schedule

Parameters:
    

  * **sch** (_tir.Schedule_) â The TIR schedule used to inline blocks.

  * **block_infos** (_List_ _[_[_BlockInfo_](../analysis/index.html#tilelang.carver.analysis.BlockInfo "tilelang.carver.analysis.BlockInfo") _]_) â The blocks to be try.



Returns:
    

**remaining** â The remaining blocks that cannot be inlined.

Return type:
    

List[[BlockInfo](../analysis/index.html#tilelang.carver.analysis.BlockInfo "tilelang.carver.analysis.BlockInfo")]

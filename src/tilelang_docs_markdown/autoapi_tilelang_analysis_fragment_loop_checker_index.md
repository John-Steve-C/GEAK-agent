# tilelang.analysis.fragment_loop_checkerÂ¶

## FunctionsÂ¶

`collect_fragment_accesses`(statement) | Collect fragment accesses in the loop body.  
---|---  
`FragmentLoopChecker`() | When using T.Parallel over a local/fragment buffer, there are several restrictions:  
  
## Module ContentsÂ¶

tilelang.analysis.fragment_loop_checker.collect_fragment_accesses(_statement_)Â¶
    

Collect fragment accesses in the loop body.

Parameters:
    

**statement** â The TIR statement to analyze

Returns:
    

Tuple of buffer accesses in the loop body.

Return type:
    

list[tvm.tir.BufferLoad | tvm.tir.BufferStore]

tilelang.analysis.fragment_loop_checker.FragmentLoopChecker()Â¶
    

When using T.Parallel over a local/fragment buffer, there are several restrictions: to ensure that the parallelization is valid.

  1. The range of loop can not be symbolic.




Returns:
    

A prim_func_pass that applies the transformation

# tilelang.analysis.nested_loop_checkerÂ¶

## FunctionsÂ¶

`is_pipelined_for`(op) | Check if a for loop is pipelined.  
---|---  
`is_tile_op`(op) | Check if a call is a tile-op  
`NestedLoopChecker`() | User-friendly pass which identifies any invalid any nested-loop pattern.  
  
## Module ContentsÂ¶

tilelang.analysis.nested_loop_checker.is_pipelined_for(_op_)Â¶
    

Check if a for loop is pipelined.

Parameters:
    

**op** (_tvm.tir.For_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.analysis.nested_loop_checker.is_tile_op(_op_)Â¶
    

Check if a call is a tile-op

Parameters:
    

**op** (_tvm.tir.Call_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.analysis.nested_loop_checker.NestedLoopChecker()Â¶
    

User-friendly pass which identifies any invalid any nested-loop pattern.

Nested loops is an annoying problem in tilelang or other polyhedral-style compilers. It contains many corner cases and undefined behaviours.

In tilelang, there are four loops:
    

T.serial T.Parallel (T.vectorized) T.Pipelined T.Persistent

T.Persistent is a new feature which we do not consider here.

We define the following rules: \- (Rule 1) T.serial can be nested inside any other loop type without restriction. \- (Rule 2) Consecutive T.Parallel nested loops are not allowed. Including any TileOp (T.copy, etc.) which has

> âparallelâ behaviours is also forbidden.
> 
> Examples: for i in T.Parallel(M):
>
>> stmt for j in T.Parallel(N):
>>
>>> â¦
> 
> for i in T.Parallel(M):
>     
> 
> T.copy(A, B) # forbidden!
> 
> **Only a special case is allowed: strict continuous Parallel loops.** Since we can fuse them into a single T.Parallel loop. Example:
> 
> for i in T.Parallel(M):
>     
> 
> for j in T.Parallel(N):
>     
> 
> â¦ # allowed

  * (Rule 3) T.Pipelined inside a T.Parallel is forbidden.

> Examples:
>     
> 
> for i in T.Parallel(M):
>     
> 
> for j in T.Pipelined(K): # forbidden!
>     
> 
> â¦
> 
> for i in T.Pipelined(K):
>     
> 
> for j in T.Parallel(N): # allowed, ok
>     
> 
> â¦




In summary, the problem mainly lies in the âT.Parallelâ. We highly recommend to use T.Parallel to implement a tiled operator inside a kernel (e.g. T.gemm level) instead of other usages. This guideline can help you avoid most of the issues.

Returns:
    

A prim_func_pass that applies the transformation

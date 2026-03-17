# tilelang.language.loopÂ¶

Loop related language interfaces in TileLang.

## FunctionsÂ¶

`Parallel`(*extents[, coalesced_width, loop_layout, ...]) | Tools to construct nested parallel for loop.  
---|---  
`Persistent`(domain, wave_size, index[, group_size]) | Tools to construct persistent for loop.  
`Pipelined`(start[, stop, num_stages, order, stage, ...]) | Tools to construct pipelined for loop.  
`serial`(start[, stop, step, annotations]) | The serial For statement.  
`unroll`(start[, stop, step, explicit, unroll_factor, ...]) | The unrolled For statement.  
`Serial`(start[, stop, step, annotations]) | Alias of T.serial.  
`Unroll`(start[, stop, step, explicit, unroll_factor, ...]) | Alias of T.unroll.  
`vectorized`(start[, stop, annotations]) | The vectorized For statement.  
`Vectorized`(start[, stop, annotations]) | Alias of T.vectorized.  
  
## Module ContentsÂ¶

tilelang.language.loop.Parallel(_* extents_, _coalesced_width =None_, _loop_layout =None_, _prefer_async =None_, _annotations =None_)Â¶
    

Tools to construct nested parallel for loop.
    

This can be used to create element-wise tensor expression.

Parameters:
    

  * **extents** (_PrimExpr_) â The extents of the iteration.

  * **coalesced_width** (_Optional_ _[__int_ _]_) â The coalesced width of the parallel loop.

  * **loop_layout** (_to the outermost generated loop only. If you omit_) â A layout annotation for the parallel loop nest, expressed as a `T.Fragment`. When provided, it is attached as the `"parallel_loop_layout"` annotation on the outermost parallel loop. For a k-dimensional `T.Parallel(...)` nest, the fragmentâs `InputDim` must equal `k`.

  * **prefer_async** (_Optional_ _[_[_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _]_) â Optional hint for PTX async-copy rewrite in this parallel loop subtree. When set to `True`, it requests cp.async injection even outside pipelined loops. `False`/`None` keeps default behavior. Internally lowered as loop annotation `"parallel_prefer_async"`.

  * **annotations** (_Optional_ _[__Dict_ _[__str_ _,__Any_ _]__]_) â Optional user-provided loop annotations attached to the outermost generated parallel loop. For example: `{"parallel_async_without_async_commit_wait": True}`.

  * **constraints** (_Notes on layout_)

  * **\---------------------------**

  * **during** (_TileLang validates parallel loop layout annotations_)

  * **ParallelLoopLayoutValidator.** (_tl.transform.LayoutInference with_)

  * **are** (_The key constraints_)

  * **after** (_\- Every parallel loop must be covered by a layout annotation_) â layout inference. For a nested parallel nest, this annotation must live on the outermost loop; inner parallel loops must not carry the layout annotation themselves.

  * **k** (_\- For a nest depth of_) â `InputDim == k`.

  * **satisfy** (_the layout must_) â `InputDim == k`.

  * **loop** (_\- Violations_ _(__missing annotation on the outermost_) â inner loops, or mismatched `InputDim`) cause a compilation error.

  * **on** (_outermost loop can manage its inner nest. Therefore the layout is placed_) â inner loops, or mismatched `InputDim`) cause a compilation error.

  * **Rationale** (_inner loops cannot control/annotate their outer loops_ _,__while the_)

  * **on**

  * **region.** (_the outermost loop so lowering passes can rewrite the entire_)

  * **easy** (_To make this_)

  * **loop_layout**

  * **loop_layout**

  * **the** (_compiler will try to infer a valid layout and attach it during_)

  * **the**

  * **pass.** (_LayoutInference_)



Returns:
    

**res** â The ForFrame.

Return type:
    

frame.ForFrame

tilelang.language.loop.Persistent(_domain_ , _wave_size_ , _index_ , _group_size =8_)Â¶
    

Tools to construct persistent for loop.

Parameters:
    

  * **domain** (_List_ _[__tir.PrimExpr_ _]_) â The list of dominators.

  * **wave_size** (_int_) â The wave size.

  * **index** (_int_) â The tile index in one wave.

  * **group_size** (_tir.PrimExpr_) â The group size.



Return type:
    

tvm.script.ir_builder.tir.frame.ForFrame

tilelang.language.loop.Pipelined(_start_ , _stop =None_, _num_stages =0_, _order =None_, _stage =None_, _sync =None_, _group =None_)Â¶
    

Tools to construct pipelined for loop.

Parameters:
    

  * **start** (_PrimExpr_) â The minimum value of iteration.

  * **stop** (_PrimExpr_) â The maximum value of iteration.

  * **num_stages** (_int_) â The max number of buffer used between pipeline producers and consumers. if num_stages is 0, pipeline will not be enabled.

  * **order** (_list_ _[__int_ _]__|__None_)

  * **stage** (_list_ _[__int_ _]__|__None_)

  * **sync** (_list_ _[__list_ _[__int_ _]__]__|__None_)

  * **group** (_list_ _[__list_ _[__int_ _]__]__|__None_)



Returns:
    

**res** â The ForFrame.

Return type:
    

frame.ForFrame

tilelang.language.loop.serial(_start_ , _stop =None_, _step =None_, _*_ , _annotations =None_)Â¶
    

The serial For statement.

Parameters:
    

  * **start** (_PrimExpr_) â The minimum value of iteration.

  * **stop** (_PrimExpr_) â The maximum value of iteration.

  * **step** (_PrimExpr_) â The step size of the iteration.

  * **annotations** (_Dict_ _[__str_ _,__Any_ _]_) â The optional annotations of the For statement.



Returns:
    

**res** â The ForFrame.

Return type:
    

frame.ForFrame

tilelang.language.loop.unroll(_start_ , _stop =None_, _step =None_, _*_ , _explicit =False_, _unroll_factor =None_, _annotations =None_)Â¶
    

The unrolled For statement.

Parameters:
    

  * **start** (_PrimExpr_) â The minimum value of iteration.

  * **stop** (_PrimExpr_) â The maximum value of iteration.

  * **step** (_PrimExpr_) â The step size of the iteration.

  * **explicit** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â Whether to explicitly unroll the loop.

  * **unroll_factor** (_int_) â The unroll factor of the loop.

  * **annotations** (_Dict_ _[__str_ _,__Any_ _]_) â The optional annotations of the For statement.



Returns:
    

**res** â The ForFrame.

Return type:
    

frame.ForFrame

tilelang.language.loop.Serial(_start_ , _stop =None_, _step =None_, _*_ , _annotations =None_)Â¶
    

Alias of T.serial.

Parameters:
    

  * **start** (_tvm.tir.PrimExpr_)

  * **stop** (_tvm.tir.PrimExpr_ _|__None_)

  * **step** (_tvm.tir.PrimExpr_ _|__None_)

  * **annotations** (_dict_ _[__str_ _,__Any_ _]__|__None_)



Return type:
    

tvm.script.ir_builder.tir.frame.ForFrame

tilelang.language.loop.Unroll(_start_ , _stop =None_, _step =None_, _*_ , _explicit =False_, _unroll_factor =None_, _annotations =None_)Â¶
    

Alias of T.unroll.

Parameters:
    

  * **start** (_tvm.tir.PrimExpr_)

  * **stop** (_tvm.tir.PrimExpr_ _|__None_)

  * **step** (_tvm.tir.PrimExpr_ _|__None_)

  * **explicit** ([_bool_](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **unroll_factor** (_int_ _|__None_)

  * **annotations** (_dict_ _[__str_ _,__Any_ _]__|__None_)



Return type:
    

tvm.script.ir_builder.tir.frame.ForFrame

tilelang.language.loop.vectorized(_start_ , _stop =None_, _*_ , _annotations =None_)Â¶
    

The vectorized For statement.

Parameters:
    

  * **start** (_PrimExpr_) â The minimum value of iteration.

  * **stop** (_PrimExpr_) â The maximum value of iteration.

  * **annotations** (_Dict_ _[__str_ _,__Any_ _]_) â The optional annotations of the For statement.



Returns:
    

**res** â The ForFrame.

Return type:
    

frame.ForFrame

tilelang.language.loop.Vectorized(_start_ , _stop =None_, _*_ , _annotations =None_)Â¶
    

Alias of T.vectorized.

Parameters:
    

  * **start** (_tvm.tir.PrimExpr_)

  * **stop** (_tvm.tir.PrimExpr_ _|__None_)

  * **annotations** (_dict_ _[__str_ _,__Any_ _]__|__None_)



Return type:
    

tvm.script.ir_builder.tir.frame.ForFrame

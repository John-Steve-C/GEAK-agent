# tilelang.engine.phaseÂ¶

## FunctionsÂ¶

`allow_warp_specialized`([pass_ctx, target]) |   
---|---  
`allow_tma_and_warp_specialized`([pass_ctx, target]) |   
`allow_tma_lower`([pass_ctx, target]) | Return True when TMA lowering is enabled for the given target.  
`allow_fence_proxy`([target]) |   
`allow_vectorize`([pass_ctx]) |   
`allow_global_thread_synchronization`([pass_ctx]) |   
`should_enable_aggressive_merge`([pass_ctx, target]) |   
`should_force_let_inline`([pass_ctx]) |   
`should_enable_ast_print`([pass_ctx]) |   
`should_enable_layout_visual`([pass_ctx]) |   
`should_enable_race_check`([pass_ctx]) |   
`get_layout_visual_formats`([pass_ctx]) |   
`LayoutVisual`(mod) | Apply layout visualization pass if enabled.  
`PreLowerSemanticCheck`(mod) | Check whether the module is valid before lowering. If not, raise a user-friendly error  
`LowerAndLegalize`(mod, target) | Bind target information and progressively legalize and lower frontend Tile IR into a form suitable for downstream optimization and codegen.  
`OptimizeForTarget`(mod, target) |   
  
## Module ContentsÂ¶

tilelang.engine.phase.allow_warp_specialized(_pass_ctx =None_, _target =None_)Â¶
    

Parameters:
    

  * **pass_ctx** (_tilelang.transform.PassContext_ _|__None_)

  * **target** (_tvm.target.Target_ _|__None_)



Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.engine.phase.allow_tma_and_warp_specialized(_pass_ctx =None_, _target =None_)Â¶
    

Parameters:
    

  * **pass_ctx** (_tilelang.transform.PassContext_ _|__None_)

  * **target** (_tvm.target.Target_ _|__None_)



Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.engine.phase.allow_tma_lower(_pass_ctx =None_, _target =None_)Â¶
    

Return True when TMA lowering is enabled for the given target.

This is intentionally decoupled from warp specialization so Hopper TMA can be used in a non-warp-specialized pipeline (e.g., no-WS kernels still need mbarrier allocation/init and expect_tx injection).

Parameters:
    

  * **pass_ctx** (_tilelang.transform.PassContext_ _|__None_)

  * **target** (_tvm.target.Target_ _|__None_)



Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.engine.phase.allow_fence_proxy(_target =None_)Â¶
    

Parameters:
    

**target** (_tvm.target.Target_ _|__None_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.engine.phase.allow_vectorize(_pass_ctx =None_)Â¶
    

Parameters:
    

**pass_ctx** (_tilelang.transform.PassContext_ _|__None_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.engine.phase.allow_global_thread_synchronization(_pass_ctx =None_)Â¶
    

Parameters:
    

**pass_ctx** (_tilelang.transform.PassContext_ _|__None_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.engine.phase.should_enable_aggressive_merge(_pass_ctx =None_, _target =None_)Â¶
    

Parameters:
    

  * **pass_ctx** (_tilelang.transform.PassContext_ _|__None_)

  * **target** (_tvm.target.Target_ _|__None_)



Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.engine.phase.should_force_let_inline(_pass_ctx =None_)Â¶
    

Parameters:
    

**pass_ctx** (_tilelang.transform.PassContext_ _|__None_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.engine.phase.should_enable_ast_print(_pass_ctx =None_)Â¶
    

Parameters:
    

**pass_ctx** (_tilelang.transform.PassContext_ _|__None_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.engine.phase.should_enable_layout_visual(_pass_ctx =None_)Â¶
    

Parameters:
    

**pass_ctx** (_tilelang.transform.PassContext_ _|__None_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.engine.phase.should_enable_race_check(_pass_ctx =None_)Â¶
    

Parameters:
    

**pass_ctx** (_tilelang.transform.PassContext_ _|__None_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.engine.phase.get_layout_visual_formats(_pass_ctx =None_)Â¶
    

Parameters:
    

**pass_ctx** (_tilelang.transform.PassContext_ _|__None_)

Return type:
    

list[str]

tilelang.engine.phase.LayoutVisual(_mod_)Â¶
    

Apply layout visualization pass if enabled.

Parameters:
    

**mod** (_tvm.IRModule_)

Return type:
    

None

tilelang.engine.phase.PreLowerSemanticCheck(_mod_)Â¶
    

Check whether the module is valid before lowering. If not, raise a user-friendly error in Python side instead of letting the error dive into the complicated TVM/C++ stack. Note: This is a validation-only pipeline of passes and does not modify or return the module.

Parameters:
    

**mod** (_tvm.IRModule_)

Return type:
    

None

tilelang.engine.phase.LowerAndLegalize(_mod_ , _target_)Â¶
    

Bind target information and progressively legalize and lower frontend Tile IR into a form suitable for downstream optimization and codegen.

This pass pipeline: \- Binds the provided target to the module. \- Legalizes frontend Tile IR into TVM-compatible constructs. \- Simplifies expressions. \- Configures reducer layouts and performs layout inference for fragments and shared memory. \- Lowers high-level tile operations and L2 persistent maps. \- Legalizes vectorized loops and inserts safety checks for memory accesses. \- Re-simplifies to remove redundancies introduced by safety checks. \- Attempts loop vectorization for dynamic-shaped loops.

Parameters:
    

  * **mod** (_IRModule_) â The input IR module containing frontend Tile IR.

  * **target** (_Target_) â Target device information to bind into the module.



Returns:
    

The transformed module, ready for target-specific optimization passes.

Return type:
    

IRModule

tilelang.engine.phase.OptimizeForTarget(_mod_ , _target_)Â¶
    

Parameters:
    

  * **mod** (_tvm.IRModule_)

  * **target** (_tvm.target.Target_)



Return type:
    

tvm.IRModule

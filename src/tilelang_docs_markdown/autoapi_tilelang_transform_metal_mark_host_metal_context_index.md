# tilelang.transform.metal.mark_host_metal_contextÂ¶

## AttributesÂ¶

`tvm_call_packed_lowered` |   
---|---  
  
## ClassesÂ¶

`MarkHostMetalContextMutator` |   
---|---  
  
## FunctionsÂ¶

`MarkHostMetalContext`() |   
---|---  
  
## Module ContentsÂ¶

tilelang.transform.metal.mark_host_metal_context.tvm_call_packed_loweredÂ¶
    

_class _tilelang.transform.metal.mark_host_metal_context.MarkHostMetalContextMutator(_* args_, _** kwargs_)Â¶
    

Bases: `tvm.tir.PyStmtExprMutator`

is_in_compute_scope _ = False_Â¶
    

visit_attr_stmt_(_stmt_)Â¶
    

visit_evaluate_(_op_)Â¶
    

Parameters:
    

**op** (_tvm.tir.Evaluate_)

tilelang.transform.metal.mark_host_metal_context.MarkHostMetalContext()Â¶
    

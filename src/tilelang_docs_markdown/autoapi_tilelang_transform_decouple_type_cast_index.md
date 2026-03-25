# tilelang.transform.decouple_type_castÂ¶

Decouple type cast vectorization constraints.

When a vectorized loop has mixed-precision operations between local and memory buffers, the vectorization length would be constrained by the GCD of all involved dtypes.

This pass decouples the constraints by inserting a local buffer as an intermediate stage, allowing optimal vectorization for both computation and memory access.

Two cases are handled:

## Case 1: local â memory (store to memory with mixed types)Â¶

Before:
    

for vec in T.vectorized(16):
    

b[vec] = T.cast(a_frag[vec], âfloat4_e2m1fnâ)

After:
    

for vec in T.vectorized(16):
    

cast_buf[vec] = T.cast(a_frag[vec], âfloat4_e2m1fnâ) # compute

for vec_copy in T.vectorized(16):
    

b[vec_copy] = cast_buf[vec_copy] # copy to memory

## Case 2: memory â local (load from memory with different dtype)Â¶

Before:
    

for vec in T.vectorized(16):
    

a_frag[vec] = T.cast(b[vec], âfloat32â)

After:
    

for vec_copy in T.vectorized(16):
    

cast_buf[vec_copy] = b[vec_copy] # copy from memory

for vec in T.vectorized(16):
    

a_frag[vec] = T.cast(cast_buf[vec], âfloat32â) # compute

## AttributesÂ¶

`CastBufferMap` |   
---|---  
  
## ClassesÂ¶

`MixedTypeChecker` | Check if expression contains BufferLoads with different dtypes, skipping indices.  
---|---  
`GlobalSharedBufferLoadCollector` | Collect BufferLoads from global/shared buffers, skipping if_then_else conditions.  
`StoreCollector` | Collect BufferStore nodes that need transformation, skipping indices traversal.  
`DecoupleTypeCastMutator` | Mutator that decouples type cast vectorization constraints.  
`StoreReplacer` | Mutator to replace memory BufferStores with cast buffer BufferStores.  
`LoadReplacer` | Mutator to replace memory BufferLoads with cast buffer BufferLoads.  
  
## FunctionsÂ¶

`is_local_buffer`(buffer) | Check if a buffer is local (register-level), including local.var.  
---|---  
`is_global_or_shared_buffer`(buffer) | Check if a buffer is a global or shared buffer.  
`validate_buffer_scope`(buffer) | Validate that buffer has a known scope.  
`has_mixed_types`(expr, target_dtype) | Check if expression contains BufferLoads with different dtypes than target.  
`get_global_or_shared_buffer_loads`(expr[, ...]) | Get BufferLoads from global/shared buffers in the expression.  
`has_global_or_shared_load_with_different_dtype`(expr, ...) | Check if expression has global/shared BufferLoad with different dtype than target.  
`contains_seq_stmt`(stmt) | Check if statement contains SeqStmt (multiple statements).  
`extract_if_condition`(stmt) | Extract IfThenElse condition from statement if present.  
`DecoupleTypeCast`() | Create a TVM pass that decouples type cast vectorization constraints.  
  
## Module ContentsÂ¶

tilelang.transform.decouple_type_cast.is_local_buffer(_buffer_)Â¶
    

Check if a buffer is local (register-level), including local.var.

Parameters:
    

**buffer** (_tvm.tir.Buffer_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.transform.decouple_type_cast.is_global_or_shared_buffer(_buffer_)Â¶
    

Check if a buffer is a global or shared buffer.

Parameters:
    

**buffer** (_tvm.tir.Buffer_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.transform.decouple_type_cast.validate_buffer_scope(_buffer_)Â¶
    

Validate that buffer has a known scope.

Raises:
    

**ValueError** â If buffer scope is unknown or empty.

Parameters:
    

**buffer** (_tvm.tir.Buffer_)

Return type:
    

None

_class _tilelang.transform.decouple_type_cast.MixedTypeChecker(_target_dtype_)Â¶
    

Bases: `tvm.tir.PyStmtExprVisitor`

Check if expression contains BufferLoads with different dtypes, skipping indices.

Parameters:
    

**target_dtype** (_str_)

target_dtype _ = ''_Â¶
    

found_different _ = False_Â¶
    

visit_buffer_load_(_op_)Â¶
    

Parameters:
    

**op** (_tvm.tir.BufferLoad_)

Return type:
    

None

tilelang.transform.decouple_type_cast.has_mixed_types(_expr_ , _target_dtype_)Â¶
    

Check if expression contains BufferLoads with different dtypes than target.

If any BufferLoad in the expression has a different dtype than the target (store bufferâs dtype), vectorization may be constrained by GCD of all dtypes.

Parameters:
    

  * **expr** (_tvm.tir.PrimExpr_)

  * **target_dtype** (_str_)



Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_class _tilelang.transform.decouple_type_cast.GlobalSharedBufferLoadCollector(_skip_if_then_else_cond =False_)Â¶
    

Bases: `tvm.tir.PyStmtExprVisitor`

Collect BufferLoads from global/shared buffers, skipping if_then_else conditions.

The condition part of if_then_else doesnât participate in type casting, so we skip collecting BufferLoads from there.

Parameters:
    

**skip_if_then_else_cond** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

result _: list[tvm.tir.BufferLoad]__ = []_Â¶
    

skip_if_then_else_cond _ = False_Â¶
    

visit_buffer_load_(_op_)Â¶
    

Parameters:
    

**op** (_tvm.tir.BufferLoad_)

Return type:
    

None

visit_call_(_op_)Â¶
    

Parameters:
    

**op** (_tvm.tir.Call_)

Return type:
    

None

tilelang.transform.decouple_type_cast.get_global_or_shared_buffer_loads(_expr_ , _skip_if_then_else_cond =False_)Â¶
    

Get BufferLoads from global/shared buffers in the expression.

Parameters:
    

  * **expr** (_tvm.tir.PrimExpr_) â The expression to search.

  * **skip_if_then_else_cond** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â If True, skip BufferLoads in if_then_else conditions, since they donât participate in type casting.



Return type:
    

list[tvm.tir.BufferLoad]

tilelang.transform.decouple_type_cast.has_global_or_shared_load_with_different_dtype(_expr_ , _target_dtype_)Â¶
    

Check if expression has global/shared BufferLoad with different dtype than target.

Used to detect memoryâlocal cases where we need to insert cast buffer. Skips if_then_else condition since it doesnât participate in type casting.

Parameters:
    

  * **expr** (_tvm.tir.PrimExpr_)

  * **target_dtype** (_str_)



Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_class _tilelang.transform.decouple_type_cast.StoreCollectorÂ¶
    

Bases: `tvm.tir.PyStmtExprVisitor`

Collect BufferStore nodes that need transformation, skipping indices traversal.

This avoids visiting BufferLoad/BufferStore nodes inside indices, which donât participate in the type casting transformation.

local_to_memory _: list[tvm.tir.BufferStore]__ = []_Â¶
    

memory_to_local _: list[tvm.tir.BufferStore]__ = []_Â¶
    

visit_buffer_store_(_op_)Â¶
    

Parameters:
    

**op** (_tvm.tir.BufferStore_)

Return type:
    

None

visit_buffer_load_(_op_)Â¶
    

Parameters:
    

**op** (_tvm.tir.BufferLoad_)

Return type:
    

None

tilelang.transform.decouple_type_cast.contains_seq_stmt(_stmt_)Â¶
    

Check if statement contains SeqStmt (multiple statements).

When the For body has SeqStmt, the transformation is more complex and we skip the optimization for now.

Parameters:
    

**stmt** (_tvm.tir.Stmt_)

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.transform.decouple_type_cast.extract_if_condition(_stmt_)Â¶
    

Extract IfThenElse condition from statement if present.

Returns:
    

A tuple of (condition, inner_body). If no IfThenElse, returns (None, stmt).

Parameters:
    

**stmt** (_tvm.tir.Stmt_)

Return type:
    

tuple[tvm.tir.PrimExpr | None, tvm.tir.Stmt]

tilelang.transform.decouple_type_cast.CastBufferMapÂ¶
    

_class _tilelang.transform.decouple_type_cast.DecoupleTypeCastMutatorÂ¶
    

Bases: `tvm.tir.PyStmtExprMutator`

Mutator that decouples type cast vectorization constraints.

This mutator transforms vectorized loops that store to memory buffers (global/shared) with mixed-precision expressions by inserting local cache buffers as intermediate stages.

visit_for_(_op_)Â¶
    

Visit For nodes, transforming vectorized loops with mixed-type stores.

Parameters:
    

**op** (_tvm.tir.For_)

Return type:
    

tvm.tir.Stmt

_class _tilelang.transform.decouple_type_cast.StoreReplacer(_cast_buffers_ , _loop_var_)Â¶
    

Bases: `tvm.tir.PyStmtExprMutator`

Mutator to replace memory BufferStores with cast buffer BufferStores.

Parameters:
    

  * **cast_buffers** (_CastBufferMap_)

  * **loop_var** (_tvm.tir.Var_)




cast_buffersÂ¶
    

loop_varÂ¶
    

visit_buffer_store_(_op_)Â¶
    

Parameters:
    

**op** (_tvm.tir.BufferStore_)

Return type:
    

tvm.tir.Stmt

_class _tilelang.transform.decouple_type_cast.LoadReplacer(_cast_buffers_ , _loop_var_)Â¶
    

Bases: `tvm.tir.PyStmtExprMutator`

Mutator to replace memory BufferLoads with cast buffer BufferLoads.

Parameters:
    

  * **cast_buffers** (_CastBufferMap_)

  * **loop_var** (_tvm.tir.Var_)




cast_buffersÂ¶
    

loop_varÂ¶
    

visit_buffer_load_(_op_)Â¶
    

Parameters:
    

**op** (_tvm.tir.BufferLoad_)

Return type:
    

tvm.tir.PrimExpr

tilelang.transform.decouple_type_cast.DecoupleTypeCast()Â¶
    

Create a TVM pass that decouples type cast vectorization constraints.

This pass inserts a local buffer as an intermediate stage for vectorized stores to non-local buffers (global/shared) where the store value contains expressions with different dtypes.

This allows optimal vectorization for both computation and memory access.

Note

This pass must be applied before VectorizeLoop and StorageRewrite passes, while the IR still uses BufferLoad/BufferStore (not tvm_access_ptr).

Returns:
    

A TVM PrimFunc pass.

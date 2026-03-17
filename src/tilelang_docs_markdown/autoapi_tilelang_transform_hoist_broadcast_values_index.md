# tilelang.transform.hoist_broadcast_valuesÂ¶

## ClassesÂ¶

`HoistBroadcastValuesMutator` |   
---|---  
  
## FunctionsÂ¶

`HoistBroadcastValues`() | TVM Pass: HoistBroadcastValues.  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.transform.hoist_broadcast_values.HoistBroadcastValuesMutatorÂ¶
    

Bases: `tvm.tir.PyStmtExprMutator`

pending_defs _ = []_Â¶
    

hoist_enabled _ = False_Â¶
    

visit_broadcast_(_op_)Â¶
    

visit_buffer_store_(_op_)Â¶
    

Parameters:
    

**op** (_tvm.tir.BufferStore_)

visit_let_stmt_(_op_)Â¶
    

Parameters:
    

**op** (_tvm.tir.LetStmt_)

tilelang.transform.hoist_broadcast_values.HoistBroadcastValues()Â¶
    

TVM Pass: HoistBroadcastValues.

This pass scans the TIR for Broadcast operations involving immediate constants (IntImm, FloatImm). It extracts these constants into variables defined via LetStmt immediately surrounding the statement where the broadcast occurs.

### Example Transformation:Â¶

Before:
    

A[i] = B[i] + T.Broadcast(3.14, 4) + T.Broadcast(3.14, 4)

After:
    

bv_3_14 = 3.14 bv_3_14_1 = 3.14 A[i] = B[i] + T.Broadcast(bv_3_14, 4) + T.Broadcast(bv_3_14_1, 4)

# tilelang.language.print_opÂ¶

This module provides macros and utilities for debugging TileLang (tl) programs. It includes functionality to print variables, print values in buffers, conditionally execute debug prints and assert.

## FunctionsÂ¶

`print_var`(var[, msg]) | Prints the value of a TIR primitive expression (PrimExpr) for debugging purposes.  
---|---  
`print_var_with_condition`(condition, var[, msg]) | Conditionally prints a TIR primitive expression (PrimExpr) if a given condition is True.  
`print_global_buffer_with_condition`(condition, buffer, ...) | Conditionally prints the values of a flattened TIR buffer if the condition is True.  
`print_shared_buffer_with_condition`(condition, buffer, ...) | Conditionally prints the values of a flattened TIR buffer if the condition is True.  
`print_fragment_buffer_with_condition`(condition, ...[, msg]) | Conditionally prints the values of a flattened TIR buffer if the condition is True.  
`print_msg`(msg) | Prints a message string.  
`print_local_buffer_with_condition`(condition, buffer, elems) | Conditionally prints the values of a flattened TIR buffer if the condition is True.  
`get_stack_str`(msg[, stacklevel]) |   
`device_assert`(condition[, msg, no_stack_info]) | Device-side assert emulation.  
`print`([obj, msg, warp_group_id, warp_id]) | A generic print function that handles both TIR buffers and primitive expressions.  
  
## Module ContentsÂ¶

tilelang.language.print_op.print_var(_var_ , _msg =''_)Â¶
    

Prints the value of a TIR primitive expression (PrimExpr) for debugging purposes.

Parameters:
    

  * **var** (_tir.PrimExpr_) â The variable or expression to be printed.

  * **msg** (_str_)



Returns:
    

The TIR expression for the debug print operation.

Return type:
    

tir.PrimExpr

tilelang.language.print_op.print_var_with_condition(_condition_ , _var_ , _msg =''_)Â¶
    

Conditionally prints a TIR primitive expression (PrimExpr) if a given condition is True.

Parameters:
    

  * **condition** (_tir.PrimExpr_) â A TIR expression representing the condition to check.

  * **var** (_tir.PrimExpr_) â The variable or expression to be printed.

  * **msg** (_str_)



Returns:
    

The TIR expression for the debug print operation, if the condition is True.

Return type:
    

tir.PrimExpr

tilelang.language.print_op.print_global_buffer_with_condition(_condition_ , _buffer_ , _elems_ , _msg =''_)Â¶
    

Conditionally prints the values of a flattened TIR buffer if the condition is True.

Parameters:
    

  * **condition** (_tvm.tir.PrimExpr_)

  * **buffer** (_tvm.tir.Buffer_)

  * **elems** (_int_)

  * **msg** (_str_)



Return type:
    

tvm.tir.PrimExpr

tilelang.language.print_op.print_shared_buffer_with_condition(_condition_ , _buffer_ , _elems_ , _msg =''_)Â¶
    

Conditionally prints the values of a flattened TIR buffer if the condition is True.

Parameters:
    

  * **condition** (_tir.PrimExpr_) â A TIR expression representing the condition to check.

  * **buffer** (_tir.Buffer_) â The buffer whose values need to be printed.

  * **elems** (_int_) â The number of elements in the buffer to print.

  * **msg** (_str_)



Returns:
    

The TIR expression for the debug print operation.

Return type:
    

tir.PrimExpr

tilelang.language.print_op.print_fragment_buffer_with_condition(_condition_ , _buffer_ , _elems_ , _msg =''_)Â¶
    

Conditionally prints the values of a flattened TIR buffer if the condition is True.

Parameters:
    

  * **condition** (_tir.PrimExpr_) â A TIR expression representing the condition to check.

  * **buffer** (_tir.Buffer_) â The buffer whose values need to be printed.

  * **elems** (_int_) â The number of elements in the buffer to print.

  * **msg** (_str_)



Returns:
    

The TIR expression for the debug print operation.

Return type:
    

tir.PrimExpr

tilelang.language.print_op.print_msg(_msg_)Â¶
    

Prints a message string.

Parameters:
    

**msg** (_str_)

Return type:
    

None

tilelang.language.print_op.print_local_buffer_with_condition(_condition_ , _buffer_ , _elems_ , _msg =''_)Â¶
    

Conditionally prints the values of a flattened TIR buffer if the condition is True.

Parameters:
    

  * **condition** (_tir.PrimExpr_) â A TIR expression representing the condition to check.

  * **buffer** (_tir.Buffer_) â The buffer whose values need to be printed.

  * **elems** (_int_) â The number of elements in the buffer to print.

  * **msg** (_str_)



Return type:
    

None

tilelang.language.print_op.get_stack_str(_msg_ , _stacklevel =1_)Â¶
    

tilelang.language.print_op.device_assert(_condition_ , _msg =''_, _no_stack_info =False_)Â¶
    

Device-side assert emulation. Emits a device-side assert call on CUDA targets when CUDA is available. The assert is always enabled and cannot be disabled at runtime.

Parameters:
    

  * **condition** (_tvm.tir.PrimExpr_)

  * **msg** (_str_)




tilelang.language.print_op.print(_obj =None_, _msg =''_, _warp_group_id =0_, _warp_id =0_)Â¶
    

A generic print function that handles both TIR buffers and primitive expressions.

  * If the input is a TIR buffer, it prints its values, but only on the first thread (tx=0, ty=0, tz=0).

  * If the input is a TIR primitive expression, it prints its value directly.




Parameters:
    

  * **obj** (_Any_) â The object to print. It can be either a tir.Buffer, tir.PrimExpr, or None (for msg-only print).

  * **msg** (_str_) â An optional message to include in the print statement.

  * **warp_group_id** (_int_) â The warp group id to print.

  * **warp_id** (_print thread will be warp_group_id * warp_group_size +_) â The warp id to print.

  * **warp_id**



Raises:
    

**ValueError** â If the input object type is unsupported.

Return type:
    

None

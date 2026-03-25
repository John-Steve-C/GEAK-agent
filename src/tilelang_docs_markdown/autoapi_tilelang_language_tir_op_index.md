# tilelang.language.tir.opÂ¶

## AttributesÂ¶

`sum` |   
---|---  
`min` |   
`max` |   
  
## FunctionsÂ¶

`call_packed`(*args[, span]) | Build expression by call an external packed function.  
---|---  
`call_cpacked`(*args[, span]) | Build expression by call an external packed function.  
`call_packed_lowered`(*args[, span]) | Lowered version of call packed.  
`call_cpacked_lowered`(*args[, span]) | Lowered version of call c-packed.  
`call_intrin`(dtype, func_name, *args[, annotations, span]) | Build expression by calling an intrinsic function.  
`call_pure_extern`(dtype, func_name, *args[, span]) | Build expression by calling a pure extern function.  
`call_extern`(dtype, func_name, *args[, span]) | Build expression by calling a extern function.  
`call_llvm_intrin`(dtype, name, *args[, span]) | Build expression by calling a llvm intrinsic function  
`call_llvm_pure_intrin`(dtype, name, *args[, span]) | Build expression by calling a pure llvm intrinsic function  
`tvm_check_return`(expected, return_unexpected, nested_call) | Return new on stack dtype[num]  
`tvm_stack_alloca`(dtype_str, num) | Return new on stack dtype[num]  
`tvm_stack_make_shape`(*args) | Allocate a shape tuple on stack, return the handle  
`tvm_stack_make_array`(data, shape, strides, ndim, ...) | Allocate a NDArray(DLTensor) on stack, return the handle  
`assume`([cond]) | Provide a true statement that can be used for simplifications  
`undef`() | Returns an initialized but arbitrary value  
`call_tir`(global_var, *args) | Performs a call into another PrimFunc in the same IRModule  
`start_profile_intrinsic`(id) | Start profile intrinsic.  
`end_profile_intrinsic`(id) | End profile intrinsic.  
`tvm_tuple`(*value) | Create a tuple structure in value field of AttrStmt  
`tvm_struct_get`(arr, index, field, dtype) | Get struct field value in array  
`tvm_struct_set`(arr, index, field, value) | Set value in struct field in array  
`address_of`(buffer_load[, span]) | Returns the address of an element in the buffer  
`lookup_param`(param_name[, span]) | Returns the param by name  
`tvm_thread_allreduce`(*freduce_args) | Perform allreduce inside threadblock.  
`tvm_thread_invariant`(cond) | Mark condition as thread invariant.  
`tvm_storage_sync`(storage_scope) | Perform synchronization in specified scope.  
`tvm_warp_shuffle`(mask, value, warp_id, width, warp_size) | Exchange value between threads inside a warp.  
`tvm_warp_shuffle_up`(mask, value, offset, width, warp_size) | Copy value from a lane with lower (by offset) index relative to caller.  
`tvm_warp_shuffle_down`(mask, value, offset, width, ...) | Copy value from a lane with higher (by offset) index relative to caller.  
`tvm_warp_activemask`() | Return a 32-bit mask indicates currently active threads in a calling warp.  
`type_annotation`(dtype) | Create a type annotation expression  
`tvm_access_ptr`(ptype, data, offset, extent, rw_mask) | Get head access address with memory access pattern info  
`tvm_throw_last_error`() | Throw TVMGetLastError()  
`tvm_load_matrix_sync`(fragment, m, n, k, index, ...) | TVM intrinsic for tensor core load operators  
`tvm_mma_sync`(fragment_d, index_d, fragment_a, index_a, ...) | TVM intrinsic for tensor core mma_sync operators  
`tvm_bmma_sync`(fragment_d, index_d, fragment_a, ...) | TVM intrinsic for tensor core bmma_sync operators  
`tvm_fill_fragment`(fragment, m, n, k, index, value) | TVM intrinsic for tensor core fill_fragment operators  
`tvm_store_matrix_sync`(fragment, m, n, k, index, ...) | TVM intrinsic for tensor core store operators  
`ptx_mma`(dtype, shape, A_layout, B_layout, A_dtype, ...) | TVM intrinsic for ptx tensor core mma instructions  
`ptx_mma_sp`(dtype, shape, A_layout, B_layout, A_dtype, ...) | TVM intrinsic for sparse tensor core ptx instructions  
`ptx_wgmma_ss`(dtype, wgmma_prefix, a_is_k_major, ...) | TVM intrinsic for ptx tensor core wmma instructions  
`ptx_wgmma_rs`(dtype, wgmma_prefix, b_is_k_major, ...) |   
`ptx_tcgen05_mma_ss`(kind_dtype, desc_a, A_offset, ...) | TVM intrinsic for tcgen05.mma shared-memory Ã shared-memory instructions.  
`ptx_tcgen05_mma_ts`(kind_dtype, A_ptr, A_offset, ...) | TVM intrinsic for tcgen05.mma tensor-memory Ã shared-memory instructions.  
`mma_store`(dtype, m, n, dst_ptr, src_ptr, src_offset, ...) | TVM intrinsic for storing the result of PTX MMA into a destination pointer  
`mma_fill`(dtype, local_size, local_ptr, offset) | TVM intrinsic for zero-initalizing an MMA accumulation register  
`ptx_ldmatrix`(dtype, trans, num, type, local_ptr, ...) | TVM intrinsic for ptx load matrix from shared memory  
`ptx_cp_async`(dst_access_ptr, src_access_ptr, bytes[, ...]) | TVM intrinsic for ptx async copy from global to shared memory using cp.async  
`ptx_cp_async_bulk`(dtype, shared_ptr, shared_offset, ...) | TVM intrinsic for ptx async copy from global to shared memory using cp.async.bulk  
`ptx_commit_group`() | TVM intrinsic for ptx async copy commit  
`ptx_wait_group`(num) | TVM intrinsic for ptx async copy wait  
`tvm_mfma`(dtype, shape, A_layout, B_layout, A_dtype, ...) | TVM intrinsic for amd matrix core mfma instructions  
`tvm_mfma_store`(dtype, m, n, dst_ptr, src_ptr, ...) | TVM intrinsic for storing the result of PTX MMA into a destination pointer  
`tvm_rdna_wmma`(dtype, shape, A_layout, B_layout, ...) | TVM intrinsic for amd matrix core mfma instructions  
`tvm_rdna_wmma_store`(dtype, m, n, dst_ptr, src_ptr, ...) | TVM intrinsic for storing the result of PTX MMA into a destination pointer  
`ptx_cp_async_barrier`(barrier_id) | TVM intrinsic for ptx async copy barrier using cp.async.mbarrier.arrive  
`ptx_init_barrier_thread_count`(barrier_id, thread_count) | TVM intrinsic for ptx barrier initialization of thread count using mbarrier.init  
`ptx_fence_barrier_init`() | TVM intrinsic for ptx fence barrier initialization.  
`ptx_arrive_barrier`(barrier_id) | TVM intrinsic for ptx barrier arrival using mbarrier.arrive  
`ptx_arrive_barrier_expect_tx`(barrier_id, byte_count) | TVM intrinsic for ptx barrier arrival with expect tx using mbarrier.arrive.expect_tx  
`ptx_wait_barrier`(barrier_id) | TVM intrinsic for ptx barrier wait using mbarrier.try_wait  
`create_barriers`(barrier_count) | TVM intrinsic to create N barriers  
`vectorlow`(dtype, vec) | Get the low level half of the vector  
`vectorhigh`(dtype, vec) | Get the high level half of the vector  
`vectorcombine`(dtype, vec1, vec2) | Concat two vectors  
`ret`(val) | Create a tir return expression  
`any`(*args[, span]) | Create a new expression of the union of all conditions in the arguments  
`all`(*args[, span]) | Create a new expression of the intersection of all conditions in the  
`trace`(args[, trace_action]) | Trace tensor data at the runtime.  
`min_value`(dtype[, span]) | minimum value of dtype  
`max_value`(dtype[, span]) | maximum value of dtype  
`infinity`(dtype[, span]) | infinity value of dtype  
`reinterpret`(value, dtype[, span]) | Reinterpret cast a value to dtype.  
`exp`(x) | Take exponential of input x.  
`exp2`(x) | Calculate 2**x  
`exp10`(x) | Calculate 10**x  
`erf`(x) | Take gauss error function of the input x.  
`tanh`(x) | Take hyperbolic tanh of input x.  
`sigmoid`(x) | Quick function to get sigmoid  
`log`(x) | Take log of input x.  
`log2`(x) | Take log2 of input x.  
`log10`(x) | Take log10 of input x.  
`log1p`(x) | Take log(x + 1) with respect to input x.  
`tan`(x) | Take tan of input x.  
`cos`(x) | Take cos of input x.  
`cosh`(x) | Take cosh of input x.  
`acos`(x) | Take acos of input x.  
`acosh`(x) | Take acos of input x.  
`sin`(x) | Take sin of input x.  
`sinh`(x) | Take sinh of input x.  
`asin`(x) | Take asin of input x.  
`asinh`(x) | Take asinh of input x.  
`atan`(x) | Take atan of input x.  
`atanh`(x) | Take atanh of input x.  
`atan2`(x1, x2) | Take arctan2(x1, x2).  
`sqrt`(x) | Take square root of input x.  
`rsqrt`(x) | Take reciprocal of square root of input x.  
`clz`(x) | Count leading zero bits of an integer x.  
`floor`(x[, span]) | Take floor of float input x.  
`ceil`(x[, span]) | Take ceil of float input x.  
`trunc`(x[, span]) | Get truncated value of the input.  
`abs`(x[, span]) | Get absolute value of the input element-wise.  
`bitwise_and`(x, y[, span]) | Take bitwise and of two values  
`bitwise_not`(x[, span]) | Take bitwise not of input value  
`bitwise_or`(x, y[, span]) | Take bitwise or of two values  
`bitwise_xor`(x, y[, span]) | Take bitwise xor of two values  
`round`(x[, span]) | Round elements of the array to the nearest integer.  
`nearbyint`(x[, span]) | Round elements of the array to the nearest integer.  
`nextafter`(x1, x2) | Return the next floating-point value after x1 towards x2.  
`hypot`(x1, x2) | Equivalent to sqrt(x1**2 + x2**2), element-wise.  
`copysign`(x1, x2) | Change the sign of x1 to that of x2, element-wise.  
`ldexp`(x1, x2) | Returns x1 * (2 ** x2).  
`likely`(cond[, span]) | Mark condition as likely.  
`isnan`(x[, span]) | Check if input value is Nan.  
`isnullptr`(x[, span]) | Check if input value is nullptr.  
`isfinite`(x[, span]) | Check if input value is finite.  
`isinf`(x[, span]) | Check if input value is infinite.  
`pow_of_int`(x, y) | Fast power operation than pow(float, float).  
`power`(x, y[, span]) | x power y  
`pow`(x, y[, span]) | x power y  
`popcount`(x) | Count the number of set bits in input x.  
`q_multiply_shift`(x, y, q, s) | Execute a multiplication between two Q-numbers x and y  
`q_multiply_shift_per_axis`(x, y, ls, rs, q, ...) | Execute a multiplication between two Q-numbers x and y  
`shift_left`(x, y[, span]) | Return the result of x left shifted by y bits.  
`shift_right`(x, y[, span]) | Return the result of x right shifted by y bits.  
`fmod`(x, y) | Return the remainder of x divided by y with the same sign as x.  
`if_then_else`(cond, t, f[, span]) | Conditional selection expression.  
`div`(a, b[, span]) | Compute a / b as in C/C++ semantics.  
`indexdiv`(a, b[, span]) | Compute floor(a / b) where a and b are non-negative.  
`indexmod`(a, b[, span]) | Compute the remainder of indexdiv. a and b are non-negative.  
`truncdiv`(a, b[, span]) | Compute the truncdiv of two expressions.  
`truncmod`(a, b[, span]) | Compute the truncmod of two expressions.  
`floordiv`(a, b[, span]) | Compute the floordiv of two expressions.  
`floormod`(a, b[, span]) | Compute the floormod of two expressions.  
`ceildiv`(lhs, rhs[, span]) | Generic ceildiv operator.  
`comm_reducer`(fcombine, fidentity[, name]) | Create a commutative reducer for reduction.  
`TVMBackendAllocWorkspace`(device_type, device_id, ...) | Backend function to allocate temporal workspace  
`TVMBackendFreeWorkspace`(device_type, device_id, ptr) | Backend function to free temporal workspace.  
`anylist_getitem`(list_handle, index) | Returns an item from any list.  
`anylist_resetitem`(list_handle, index) | Reset an item from any list.  
`anylist_setitem_call_packed`(list_handle, index, ...) | Set anylist item by result of packed call.  
`anylist_setitem_call_cpacked`(list_handle, index, ...) | Set anylist item by result of packed call.  
`vscale`() | Get the target's vscale value. It will be lowered to llvm.vscale intrinsic  
  
## Module ContentsÂ¶

tilelang.language.tir.op.call_packed(_* args_, _span =None_)Â¶
    

Build expression by call an external packed function.

The argument to packed function can be Expr or Buffer. The argument is the corresponding POD type when Expr is presented.

When the argument is Buffer, the corresponding PackedFunc will receive an TVMArrayHandle whose content is valid during the callback period. If the PackedFunc is a python callback, then the corresponding argument is NDArray.

Parameters:
    

  * **args** (_list_ _of_ _Expr_ _or_ _Buffer._) â Positional arguments.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

See also

`te.extern`
    

Create tensor with extern function call.

tilelang.language.tir.op.call_cpacked(_* args_, _span =None_)Â¶
    

Build expression by call an external packed function.

Same as call_packed, except that the first argument is the function name (as in call_extern), and the last argument is the resource handle.

Parameters:
    

  * **args** (_list_ _of_ _Expr_ _or_ _Buffer._) â Positional arguments.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

See also

`te.extern`
    

Create tensor with extern function call.

tilelang.language.tir.op.call_packed_lowered(_* args_, _span =None_)Â¶
    

Lowered version of call packed. The argument to packed function can be Expr or Buffer. The argument is the corresponding POD type when Expr is presented. When the argument is Buffer, the corresponding PackedFunc will receive an TVMArrayHandle whose content is valid during the callback period. If the PackedFunc is a python callback, then the corresponding argument is NDArray.

Parameters:
    

  * **args** (_list_ _of_ _Expr_ _or_ _Buffer._) â Positional arguments.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

See also

`te.extern`
    

Create tensor with extern function call.

tilelang.language.tir.op.call_cpacked_lowered(_* args_, _span =None_)Â¶
    

Lowered version of call c-packed. Same as call_packed, except that the first argument is the function name (as in call_extern), and the last argument is the resource handle.

Parameters:
    

  * **args** (_list_ _of_ _Expr_ _or_ _Buffer._) â Positional arguments.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

See also

`te.extern`
    

Create tensor with extern function call.

tilelang.language.tir.op.call_intrin(_dtype_ , _func_name_ , _* args_, _annotations =None_, _span =None_)Â¶
    

Build expression by calling an intrinsic function.

Intrinsics can be overloaded with multiple data types via the intrinsic translation rule.

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **func_name** (_str_) â The intrinsic function name.

  * **args** (_list_) â Positional arguments.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.call_pure_extern(_dtype_ , _func_name_ , _* args_, _span =None_)Â¶
    

Build expression by calling a pure extern function.

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **func_name** (_str_) â The extern function name.

  * **args** (_list_) â Positional arguments.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.call_extern(_dtype_ , _func_name_ , _* args_, _span =None_)Â¶
    

Build expression by calling a extern function.

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **func_name** (_str_) â The extern function name.

  * **args** (_list_) â Positional arguments.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.call_llvm_intrin(_dtype_ , _name_ , _* args_, _span =None_)Â¶
    

Build expression by calling a llvm intrinsic function

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **name** (_str_) â The name of the llvm intrinsic function.

  * **args** (_list_) â Positional arguments.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.call_llvm_pure_intrin(_dtype_ , _name_ , _* args_, _span =None_)Â¶
    

Build expression by calling a pure llvm intrinsic function

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **name** (_str_) â The name of the llvm intrinsic function.

  * **args** (_list_) â Positional arguments.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_check_return(_expected_ , _return_unexpected_ , _nested_call_)Â¶
    

Return new on stack dtype[num] :param expected: The expected return code. :type expected: int :param return_unexpected: The unexpected return code. :type return_unexpected: int :param nested_call: The call expression to check return. :type nested_call: PrimExpr

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_stack_alloca(_dtype_str_ , _num_)Â¶
    

Return new on stack dtype[num]

Parameters:
    

  * **dtype_str** (_str_) â The data type of array.

  * **num** (_int_) â The size of array.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_stack_make_shape(_* args_)Â¶
    

Allocate a shape tuple on stack, return the handle

Parameters:
    

**args** (_int_) â The tuple shape.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_stack_make_array(_data_ , _shape_ , _strides_ , _ndim_ , _arr_dtype_ , _elem_offset_)Â¶
    

Allocate a NDArray(DLTensor) on stack, return the handle

Parameters:
    

  * **data** (_Expr_) â The data of array.

  * **shape** (_Expr_) â The shape of array.

  * **strides** (_Expr_) â The strides of array.

  * **ndim** (_Expr_) â The dimensions of array.

  * **arr_dtype** (_Expr_) â The data type of array.

  * **elem_offse** (_Expr_) â The element offset of array.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.assume(_cond =None_)Â¶
    

Provide a true statement that can be used for simplifications

Parameters:
    

**cond** (_Expr_) â The constraint condition.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.undef()Â¶
    

Returns an initialized but arbitrary value

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.call_tir(_global_var_ , _* args_)Â¶
    

Performs a call into another PrimFunc in the same IRModule

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

Parameters:
    

**global_var** (_tvm.ir.GlobalVar_)

tilelang.language.tir.op.start_profile_intrinsic(_id_)Â¶
    

Start profile intrinsic. :param id: The intrinsic id. :type id: int

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.end_profile_intrinsic(_id_)Â¶
    

End profile intrinsic. :param id: The intrinsic id. :type id: int

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_tuple(_* value_)Â¶
    

Create a tuple structure in value field of AttrStmt

Parameters:
    

**value** (_Expr_) â The value in tuple.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_struct_get(_arr_ , _index_ , _field_ , _dtype_)Â¶
    

Get struct field value in array

Parameters:
    

  * **dtype** (_str_) â The date type of the result.

  * **arr** (_StructType*_) â The array of struct.

  * **index** (_int_) â The index of struct.

  * **field** (_int_) â The field of struct.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_struct_set(_arr_ , _index_ , _field_ , _value_)Â¶
    

Set value in struct field in array

Parameters:
    

  * **arr** (_StructType*_) â The array of struct.

  * **index** (_int_) â The index of struct.

  * **field** (_int_) â The field of struct.

  * **value** (_Expr_) â The value to be set in field.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.address_of(_buffer_load_ , _span =None_)Â¶
    

Returns the address of an element in the buffer

Parameters:
    

  * **buffer_load** (_BufferLoad_) â The buffer load.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.lookup_param(_param_name_ , _span =None_)Â¶
    

Returns the param by name

Parameters:
    

  * **param_name** (_str_) â The name of param.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_thread_allreduce(_* freduce_args_)Â¶
    

Perform allreduce inside threadblock.

Parameters:
    

**freduce_args** (_Expr_) â The args.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_thread_invariant(_cond_)Â¶
    

Mark condition as thread invariant.

Parameters:
    

**cond** (_Expr_) â The condition.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_storage_sync(_storage_scope_)Â¶
    

Perform synchronization in specified scope.

Parameters:
    

**storage_scope** (_str_) â The storage scope to perform synchronization.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_warp_shuffle(_mask_ , _value_ , _warp_id_ , _width_ , _warp_size_)Â¶
    

Exchange value between threads inside a warp.

Parameters:
    

  * **mask** (_PrimExpr_) â The warp mask indicates active threads inside warp.

  * **value** (_PrimExpr_) â The value to exchange.

  * **warp_id** (_PrimExpr_) â The source lane index to fetch value.

  * **width** (_PrimExpr_) â The width of sub-sections to perform warp shuffle.

  * **warp_size** (_PrimExpr_) â The warp size.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_warp_shuffle_up(_mask_ , _value_ , _offset_ , _width_ , _warp_size_)Â¶
    

Copy value from a lane with lower (by offset) index relative to caller.

Parameters:
    

  * **mask** (_PrimExpr_) â The warp mask indicates active threads inside warp.

  * **value** (_PrimExpr_) â The value to exchange.

  * **offset** (_PrimExpr_) â The difference between source lane index and destination lane index: offset = dst_lane_idx - src_lane_idx

  * **width** (_PrimExpr_) â The width of sub-sections to perform warp shuffle.

  * **warp_size** (_PrimExpr_) â The warp size.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_warp_shuffle_down(_mask_ , _value_ , _offset_ , _width_ , _warp_size_)Â¶
    

Copy value from a lane with higher (by offset) index relative to caller.

Parameters:
    

  * **mask** (_PrimExpr_) â The warp mask indicates active threads inside warp.

  * **value** (_PrimExpr_) â The value to exchange.

  * **offset** (_PrimExpr_) â The difference between source lane index and destination lane index: offset = src_lane_idx - dst_lane_idx

  * **width** (_PrimExpr_) â The width of sub-sections to perform warp shuffle.

  * **warp_size** (_PrimExpr_) â The warp size.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_warp_activemask()Â¶
    

Return a 32-bit mask indicates currently active threads in a calling warp.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.type_annotation(_dtype_)Â¶
    

Create a type annotation expression

Parameters:
    

**dtype** (_Expr_) â The data type.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_access_ptr(_ptype_ , _data_ , _offset_ , _extent_ , _rw_mask_)Â¶
    

Get head access address with memory access pattern info

Parameters:
    

  * **ptype** (_Expr_) â The data type of pointer.

  * **data** (_DType*_) â The data of pointer.

  * **offset** (_int_) â The offset of pointer.

  * **extent** (_int_) â The extent of pointer.

  * **rw_mask** (_int_) â The read write mask.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_throw_last_error()Â¶
    

Throw TVMGetLastError()

Returns:
    

**ret** â The return expression

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_load_matrix_sync(_fragment_ , _m_ , _n_ , _k_ , _index_ , _buffer_ptr_ , _stride_ , _layout_)Â¶
    

TVM intrinsic for tensor core load operators

Parameters:
    

  * **fragment** (_Var_) â The wmma fragment.

  * **m** (_UIntImm_) â The shape of wmma fragment.

  * **n** (_UIntImm_) â The shape of wmma fragment.

  * **k** (_UIntImm_) â The shape of wmma fragment.

  * **index** (_Expr_) â The fragment index.

  * **buffer_ptr** (_Expr_) â The fragment buffer pointer.

  * **stride** (_Expr_) â The fragment stride.

  * **layout** (_Literal_ _[__"row_major"__,__"column_major"__]_) â The fragment layout.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_mma_sync(_fragment_d_ , _index_d_ , _fragment_a_ , _index_a_ , _fragment_b_ , _index_b_ , _fragment_c_ , _index_c_)Â¶
    

TVM intrinsic for tensor core mma_sync operators

Parameters:
    

  * **fragment_d** (_Var_) â The wmma fragment_d.

  * **index_d** (_Expr_) â The fragment_d index.

  * **fragment_a** (_Var_) â The wmma fragment_a.

  * **index_a** (_Expr_) â The fragment_a index.

  * **fragment_b** (_Var_) â The wmma fragment_b.

  * **index_b** (_Expr_) â The fragment_b index.

  * **fragment_c** (_Var_) â The wmma fragment_c.

  * **index_c** (_Expr_) â The fragment_c index.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_bmma_sync(_fragment_d_ , _index_d_ , _fragment_a_ , _index_a_ , _fragment_b_ , _index_b_ , _fragment_c_ , _index_c_)Â¶
    

TVM intrinsic for tensor core bmma_sync operators

Parameters:
    

  * **fragment_d** (_Var_) â The bwmma fragment_d.

  * **index_d** (_Expr_) â The fragment_d index.

  * **fragment_a** (_Var_) â The bwmma fragment_a.

  * **index_a** (_Expr_) â The fragment_a index.

  * **fragment_b** (_Var_) â The bwmma fragment_b.

  * **index_b** (_Expr_) â The fragment_b index.

  * **fragment_c** (_Var_) â The bwmma fragment_c.

  * **index_c** (_Expr_) â The fragment_c index.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_fill_fragment(_fragment_ , _m_ , _n_ , _k_ , _index_ , _value_)Â¶
    

TVM intrinsic for tensor core fill_fragment operators

Parameters:
    

  * **fragment** (_Var_) â The wmma fragment

  * **m** (_UIntImm_) â The shape of wmma fragment.

  * **n** (_UIntImm_) â The shape of wmma fragment.

  * **k** (_UIntImm_) â The shape of wmma fragment.

  * **index** (_Expr_) â The fragment index.

  * **value** (_Expr_) â The value to be filled in fragment.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_store_matrix_sync(_fragment_ , _m_ , _n_ , _k_ , _index_ , _buffer_ptr_ , _stride_ , _layout_)Â¶
    

TVM intrinsic for tensor core store operators

Parameters:
    

  * **fragment** (_Var_) â The wmma fragment.

  * **m** (_UIntImm_) â The shape of wmma fragment.

  * **n** (_UIntImm_) â The shape of wmma fragment.

  * **k** (_UIntImm_) â The shape of wmma fragment.

  * **index** (_Expr_) â The fragment index.

  * **buffer_ptr** (_Expr_) â The fragment buffer pointer.

  * **stride** (_Expr_) â The fragment stride.

  * **layout** (_Literal_ _[__"row_major"__,__"column_major"__]_) â The fragment layout.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_mma(_dtype_ , _shape_ , _A_layout_ , _B_layout_ , _A_dtype_ , _B_dtype_ , _C_dtype_ , _multiplicand_a_ , _a_index_ , _multiplicand_b_ , _b_index_ , _accumulator_ , _c_index_ , _saturate_ , _operator =None_)Â¶
    

TVM intrinsic for ptx tensor core mma instructions <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#warp-level-matrix-instructions-for-mma>

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **shape** (_str_) â The shape of mma fragment.

  * **A_layout** (_Literal_ _[__"row"__,__"col"__]_) â The layout of multiplicand fragment A.

  * **B_layout** (_Literal_ _[__"row"__,__"col"__]_) â The layout of multiplicand fragment B.

  * **A_dtype** (_str_) â The data type of multiplicand fragment A.

  * **B_dtype** (_str_) â The data type of multiplicand fragment B.

  * **C_dtype** (_str_) â The data type of accumulator fragment C.

  * **multiplicand_a** (_Var_) â The multiplicand fragment A variable.

  * **a_index** (_Expr_) â The index of multiplicand fragment A.

  * **multiplicand_b** (_Var_) â The multiplicand fragment B variable.

  * **b_index** (_Expr_) â The index of multiplicand fragment A.

  * **accumulator** (_Var_) â The accumulator fragment C variable.

  * **c_index** (_Expr_) â The index of accumulator fragment C.

  * **saturate** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â The optional saturation at the output.

  * **operator** (_Optional_ _[__Literal_ _[__"xor"__,__"and"__]__]_) â The 1-bit operator.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_mma_sp(_dtype_ , _shape_ , _A_layout_ , _B_layout_ , _A_dtype_ , _B_dtype_ , _C_dtype_ , _multiplicand_a_ , _a_index_ , _multiplicand_b_ , _b_index_ , _accumulator_ , _c_index_ , _metadata_ , _meta_index_ , _sparse_selector_ , _saturate_)Â¶
    

TVM intrinsic for sparse tensor core ptx instructions <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#warp-level-matrix-instructions-for-sparse-mma>

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **shape** (_str_) â The shape of mma fragment.

  * **A_layout** (_Literal_ _[__"row"__,__"col"__]_) â The layout of multiplicand fragment A.

  * **B_layout** (_Literal_ _[__"row"__,__"col"__]_) â The layout of multiplicand fragment B.

  * **A_dtype** (_str_) â The data type of multiplicand fragment A.

  * **B_dtype** (_str_) â The data type of multiplicand fragment B.

  * **C_dtype** (_str_) â The data type of accumulator fragment C.

  * **multiplicand_a** (_Var_) â The multiplicand fragment A variable.

  * **a_index** (_Expr_) â The index of multiplicand fragment A.

  * **multiplicand_b** (_Var_) â The multiplicand fragment B variable.

  * **b_index** (_Expr_) â The index of multiplicand fragment B.

  * **accumulator** (_Var_) â The accumulator fragment C variable.

  * **c_index** (_Expr_) â The index of accumulator fragment C.

  * **metadata** (_Expr_) â The metadata of operand.

  * **meta_index** (_Expr_) â The metadata index of operand.

  * **sparse_selector** (_Expr_) â The sparse selector indicating the thread that stores the metadata.

  * **saturate** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â The optional saturation at the output.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_wgmma_ss(_dtype_ , _wgmma_prefix_ , _a_is_k_major_ , _b_is_k_major_ , _a_dtype_abbrv_ , _b_dtype_abbrv_ , _accum_dtype_abbrv_ , _A_desc_ , _A_offset_ , _B_desc_ , _B_offset_ , _C_data_ , _C_offset_ , _scale_out_ , _scale_in_a_ , _scale_in_b_)Â¶
    

TVM intrinsic for ptx tensor core wmma instructions <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#warp-level-matrix-instructions-for-wmma>

tilelang.language.tir.op.ptx_wgmma_rs(_dtype_ , _wgmma_prefix_ , _b_is_k_major_ , _a_dtype_abbrv_ , _b_dtype_abbrv_ , _accum_dtype_abbrv_ , _A_buf_ , _A_offset_ , _B_desc_ , _B_offset_ , _C_data_ , _C_offset_ , _scale_out_ , _scale_in_a_ , _scale_in_b_)Â¶
    

tilelang.language.tir.op.ptx_tcgen05_mma_ss(_kind_dtype_ , _desc_a_ , _A_offset_ , _desc_b_ , _B_offset_ , _C_ptr_ , _C_offset_ , _desc_val_ , _scale_out_ , _mask0_ , _mask1_ , _mask2_ , _mask3_ , _enable_ws =False_, _ws =None_, _warp_specialized =None_, _variant =None_)Â¶
    

TVM intrinsic for tcgen05.mma shared-memory Ã shared-memory instructions.

Expects 13 or 14 positional arguments: (kind_dtype, desc_a, A_offset, desc_b, B_offset, C_ptr, C_offset,

> desc_val, scale_out, mask0, mask1, mask2, mask3[, enable_ws]).

Aliases: you can also pass ws or warp_specialized (booleans) instead of enable_ws. Alternatively, use variant=âwsâ (or âdefaultâ). \- kind_dtype: instruction kind selector (e.g., T.float16 for kind::f16,

> âtf32â for kind::tf32, âint8â for kind::i8, âfloat8_e4m3â for kind::f8f6f4).

tilelang.language.tir.op.ptx_tcgen05_mma_ts(_kind_dtype_ , _A_ptr_ , _A_offset_ , _desc_b_ , _B_offset_ , _C_ptr_ , _C_offset_ , _desc_val_ , _scale_out_ , _mask0_ , _mask1_ , _mask2_ , _mask3_)Â¶
    

TVM intrinsic for tcgen05.mma tensor-memory Ã shared-memory instructions.

Expects 13 positional arguments: (kind_dtype, A_ptr, A_offset, desc_b, B_offset, C_ptr, C_offset,

> desc_val, scale_out, mask0, mask1, mask2, mask3).

  * kind_dtype: instruction kind selector (e.g., T.float16 for kind::f16, âtf32â for kind::tf32, âint8â for kind::i8, âfloat8_e4m3â for kind::f8f6f4).




tilelang.language.tir.op.mma_store(_dtype_ , _m_ , _n_ , _dst_ptr_ , _src_ptr_ , _src_offset_ , _dst_stride_)Â¶
    

TVM intrinsic for storing the result of PTX MMA into a destination pointer

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **m** (_IntImm_) â The shape of mma fragment.

  * **n** (_IntImm_) â The shape of mma fragment.

  * **dst_ptr** (_Var_) â The destination pointer variable.

  * **src_ptr** (_Var_) â The source pointer variable.

  * **src_offset** (_Expr_) â The source offset.

  * **dst_stride** (_Var_) â The destination stride.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.mma_fill(_dtype_ , _local_size_ , _local_ptr_ , _offset_)Â¶
    

TVM intrinsic for zero-initalizing an MMA accumulation register

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **local_size** (_IntImm_) â The number of elements.

  * **local_ptr** (_Var_) â The destination pointer variable.

  * **offset** (_Expr_) â The destination offset.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_ldmatrix(_dtype_ , _trans_ , _num_ , _type_ , _local_ptr_ , _local_offset_ , _smem_ptr_ , _smem_offset_)Â¶
    

TVM intrinsic for ptx load matrix from shared memory <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#warp-level-matrix-instructions-ldmatrix>

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **trans** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")) â The matrix is loaded in column-major format.

  * **num** (_IntImm_) â The number of matrices.

  * **type** (_Literal_ _[__".b16"__]_) â The data type of the matrices.

  * **local_ptr** (_Var_) â The local pointer variable.

  * **local_offset** (_Expr_) â The offset of local pointer.

  * **smem_ptr** (_Var_) â The shared memory pointer variable.

  * **smem_offset** (_Expr_) â The offset of shared memort pointer.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_cp_async(_dst_access_ptr_ , _src_access_ptr_ , _bytes_ , _predicate =None_)Â¶
    

TVM intrinsic for ptx async copy from global to shared memory using cp.async <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#data-movement-and-conversion-instructions-cp-async>

Parameters:
    

  * **dst_access_ptr** (_PrimExpr_) â The destination (shared memory) access pointer created by tvm_access_ptr. Should include pointer, offset, extent, and write access flag (rw_mask=2).

  * **src_access_ptr** (_PrimExpr_) â The source (global memory) access pointer created by tvm_access_ptr. Should include pointer, offset, extent, and read access flag (rw_mask=1).

  * **bytes** (_int_ _or_ _PrimExpr_) â The number of bytes to copy (must be 4, 8, or 16).

  * **predicate** (_PrimExpr_ _,__optional_) â Optional predicate condition for conditional cp.async. When provided, the copy will only be performed if the predicate evaluates to true. Otherwise, the destination will be filled with zeros (default behavior of cp.async).



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

Examples
    
    
    >>> # Copy 16 bytes from global to shared memory
    >>> T.ptx_cp_async(
    ...     T.tvm_access_ptr(T.type_annotation(T.uint8), A_shared.data, 0, 16, 2),  # dst
    ...     T.tvm_access_ptr(T.type_annotation(T.uint8), B_global.data, 0, 16, 1),  # src
    ...     16  # bytes
    ... )
    >>>
    >>> # Predicated cp.async (only copy if condition is true)
    >>> T.ptx_cp_async(
    ...     T.tvm_access_ptr(T.type_annotation(T.uint8), A_shared.data, 0, 16, 2),
    ...     T.tvm_access_ptr(T.type_annotation(T.uint8), B_global.data, 0, 16, 1),
    ...     16,
    ...     predicate=guard  # only copy if guard is true
    ... )
    

tilelang.language.tir.op.ptx_cp_async_bulk(_dtype_ , _shared_ptr_ , _shared_offset_ , _global_ptr_ , _global_offset_ , _bytes_ , _barrier_id_)Â¶
    

TVM intrinsic for ptx async copy from global to shared memory using cp.async.bulk <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#data-movement-and-conversion-instructions-cp-async-bulk>

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **shared_ptr** (_Var_) â The shared memory pointer variable.

  * **shared_offset** (_Expr_) â The offset of shared memory pointer.

  * **global_ptr** (_Var_) â The global memory pointer variable.

  * **global_offset** (_Expr_) â The offset of global memory pointer.

  * **bytes** (_int_) â The data size to copy.

  * **barrier_id** (_int_) â The ID of the barrier shared memory pointer.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_commit_group()Â¶
    

TVM intrinsic for ptx async copy commit <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#data-movement-and-conversion-instructions-cp-async-commit-group>

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_wait_group(_num_)Â¶
    

TVM intrinsic for ptx async copy wait <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#data-movement-and-conversion-instructions-cp-async-wait-group>

Parameters:
    

**num** (_int_) â The number of the most recent uncommitted pending cp.async groups to wait.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_mfma(_dtype_ , _shape_ , _A_layout_ , _B_layout_ , _A_dtype_ , _B_dtype_ , _C_dtype_ , _multiplicand_a_ , _a_index_ , _multiplicand_b_ , _b_index_ , _accumulator_ , _c_index_)Â¶
    

TVM intrinsic for amd matrix core mfma instructions <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#warp-level-matrix-instructions-for-mma>

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **shape** (_str_) â The shape of mma fragment.

  * **A_layout** (_Literal_ _[__"row"__,__"col"__]_) â The layout of multiplicand fragment A.

  * **B_layout** (_Literal_ _[__"row"__,__"col"__]_) â The layout of multiplicand fragment B.

  * **A_dtype** (_str_) â The data type of multiplicand fragment A.

  * **B_dtype** (_str_) â The data type of multiplicand fragment B.

  * **C_dtype** (_str_) â The data type of accumulator fragment C.

  * **multiplicand_a** (_Var_) â The multiplicand fragment A variable.

  * **a_index** (_Expr_) â The index of multiplicand fragment A.

  * **multiplicand_b** (_Var_) â The multiplicand fragment B variable.

  * **b_index** (_Expr_) â The index of multiplicand fragment A.

  * **accumulator** (_Var_) â The accumulator fragment C variable.

  * **c_index** (_Expr_) â The index of accumulator fragment C.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_mfma_store(_dtype_ , _m_ , _n_ , _dst_ptr_ , _src_ptr_ , _src_offset_ , _dst_stride_)Â¶
    

TVM intrinsic for storing the result of PTX MMA into a destination pointer

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **m** (_IntImm_) â The shape of mma fragment.

  * **n** (_IntImm_) â The shape of mma fragment.

  * **dst_ptr** (_Var_) â The destination pointer variable.

  * **src_ptr** (_Var_) â The source pointer variable.

  * **src_offset** (_Expr_) â The source offset.

  * **dst_stride** (_Var_) â The destination stride.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_rdna_wmma(_dtype_ , _shape_ , _A_layout_ , _B_layout_ , _A_dtype_ , _B_dtype_ , _C_dtype_ , _multiplicand_a_ , _a_index_ , _multiplicand_b_ , _b_index_ , _accumulator_ , _c_index_)Â¶
    

TVM intrinsic for amd matrix core mfma instructions <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#warp-level-matrix-instructions-for-mma>

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **shape** (_str_) â The shape of mma fragment.

  * **A_layout** (_Literal_ _[__"row"__,__"col"__]_) â The layout of multiplicand fragment A.

  * **B_layout** (_Literal_ _[__"row"__,__"col"__]_) â The layout of multiplicand fragment B.

  * **A_dtype** (_str_) â The data type of multiplicand fragment A.

  * **B_dtype** (_str_) â The data type of multiplicand fragment B.

  * **C_dtype** (_str_) â The data type of accumulator fragment C.

  * **multiplicand_a** (_Var_) â The multiplicand fragment A variable.

  * **a_index** (_Expr_) â The index of multiplicand fragment A.

  * **multiplicand_b** (_Var_) â The multiplicand fragment B variable.

  * **b_index** (_Expr_) â The index of multiplicand fragment A.

  * **accumulator** (_Var_) â The accumulator fragment C variable.

  * **c_index** (_Expr_) â The index of accumulator fragment C.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.tvm_rdna_wmma_store(_dtype_ , _m_ , _n_ , _dst_ptr_ , _src_ptr_ , _src_offset_ , _dst_stride_)Â¶
    

TVM intrinsic for storing the result of PTX MMA into a destination pointer

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **m** (_IntImm_) â The shape of mma fragment.

  * **n** (_IntImm_) â The shape of mma fragment.

  * **dst_ptr** (_Var_) â The destination pointer variable.

  * **src_ptr** (_Var_) â The source pointer variable.

  * **src_offset** (_Expr_) â The source offset.

  * **dst_stride** (_Var_) â The destination stride.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_cp_async_barrier(_barrier_id_)Â¶
    

TVM intrinsic for ptx async copy barrier using cp.async.mbarrier.arrive <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#parallel-synchronization-and-communication-instructions-cp-async-mbarrier-arrive>

Parameters:
    

**barrier_id** (_int_) â The ID of the barrier shared memory pointer.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_init_barrier_thread_count(_barrier_id_ , _thread_count_)Â¶
    

TVM intrinsic for ptx barrier initialization of thread count using mbarrier.init <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#parallel-synchronization-and-communication-instructions-mbarrier-init>

Parameters:
    

  * **barrier_id** (_int_) â The ID of the barrier shared memory pointer.

  * **thread_count** (_int_) â Number of threads expected to arrive at the barrier.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_fence_barrier_init()Â¶
    

TVM intrinsic for ptx fence barrier initialization.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_arrive_barrier(_barrier_id_)Â¶
    

TVM intrinsic for ptx barrier arrival using mbarrier.arrive <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#parallel-synchronization-and-communication-instructions-mbarrier-arrive>

Parameters:
    

**barrier_id** (_int_) â The ID of the barrier shared memory pointer.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_arrive_barrier_expect_tx(_barrier_id_ , _byte_count_)Â¶
    

TVM intrinsic for ptx barrier arrival with expect tx using mbarrier.arrive.expect_tx <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#parallel-synchronization-and-communication-instructions-mbarrier-arrive> <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#parallel-synchronization-and-communication-instructions-mbarrier-expect-tx-operation>

Parameters:
    

  * **barrier_id** (_int_) â The ID of the barrier shared memory pointer.

  * **byte_count** (_int_) â Increases the tx count of the mbarrier object to track completion of additional async transactions.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ptx_wait_barrier(_barrier_id_)Â¶
    

TVM intrinsic for ptx barrier wait using mbarrier.try_wait <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#parallel-synchronization-and-communication-instructions-mbarrier-test-wait-mbarrier-try-wait>

Parameters:
    

**barrier_id** (_int_) â The ID of the barrier shared memory pointer.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.create_barriers(_barrier_count_)Â¶
    

TVM intrinsic to create N barriers

Parameters:
    

**barrier_count** (_int_) â The number of barriers to create.

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.vectorlow(_dtype_ , _vec_)Â¶
    

Get the low level half of the vector

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **vec** (_list_) â The input vector.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.vectorhigh(_dtype_ , _vec_)Â¶
    

Get the high level half of the vector

Parameters:
    

  * **dtype** (_str_) â The data type of the result.

  * **vec** (_list_) â The input vector.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.vectorcombine(_dtype_ , _vec1_ , _vec2_)Â¶
    

Concat two vectors

Parameters:
    

  * **vec1** (_list_) â The input vector.

  * **vec2** (_list_) â The input vector.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ret(_val_)Â¶
    

Create a tir return expression

Parameters:
    

**val** (_Expr_) â The returned tir expression, whose data type is int, float or void pointer.

Returns:
    

**ret** â The return expression

Return type:
    

PrimExpr

tilelang.language.tir.op.any(_* args_, _span =None_)Â¶
    

Create a new expression of the union of all conditions in the arguments

Parameters:
    

  * **args** (_list_) â List of symbolic boolean expressions

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**expr** â Expression

Return type:
    

Expr

tilelang.language.tir.op.all(_* args_, _span =None_)Â¶
    

Create a new expression of the intersection of all conditions in the
    

arguments

Parameters:
    

  * **args** (_list_) â List of symbolic boolean expressions

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**expr** â Expression

Return type:
    

Expr

tilelang.language.tir.op.trace(_args_ , _trace_action ='tvm.default_trace_action'_)Â¶
    

Trace tensor data at the runtime.

The trace function allows to trace specific tensor at the runtime. The tracing value should come as last argument. The trace action should be specified, by default tvm.default_trace_action is used.

Parameters:
    

  * **args** (_list_ _of_ _Expr_ _or_ _Buffers._) â Positional arguments.

  * **trace_action** (_str._) â The name of the trace action.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

See also

`tvm.tir.call_packed`
    

Creates packed function.

tilelang.language.tir.op.min_value(_dtype_ , _span =None_)Â¶
    

minimum value of dtype

Parameters:
    

  * **dtype** (_str_) â The data type.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**value** â The minimum value of dtype.

Return type:
    

tvm.Expr

tilelang.language.tir.op.max_value(_dtype_ , _span =None_)Â¶
    

maximum value of dtype

Parameters:
    

  * **dtype** (_str_) â The data type.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**value** â The maximum value of dtype.

Return type:
    

tvm.Expr

tilelang.language.tir.op.infinity(_dtype_ , _span =None_)Â¶
    

infinity value of dtype

Parameters:
    

  * **dtype** (_str_) â The data type.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**value** â The infinity value of dtype.

Return type:
    

tvm.Expr

tilelang.language.tir.op.reinterpret(_value_ , _dtype_ , _span =None_)Â¶
    

Reinterpret cast a value to dtype.

Parameters:
    

  * **value** (_PrimExpr_) â The input value.

  * **dtype** (_str_) â The data type.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**value** â The reinterpret cast value of dtype.

Return type:
    

tvm.Expr

tilelang.language.tir.op.exp(_x_)Â¶
    

Take exponential of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.exp2(_x_)Â¶
    

Calculate 2**x

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.exp10(_x_)Â¶
    

Calculate 10**x

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.erf(_x_)Â¶
    

Take gauss error function of the input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.tanh(_x_)Â¶
    

Take hyperbolic tanh of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.sigmoid(_x_)Â¶
    

Quick function to get sigmoid

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.log(_x_)Â¶
    

Take log of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.log2(_x_)Â¶
    

Take log2 of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.log10(_x_)Â¶
    

Take log10 of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.log1p(_x_)Â¶
    

Take log(x + 1) with respect to input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.tan(_x_)Â¶
    

Take tan of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.cos(_x_)Â¶
    

Take cos of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.cosh(_x_)Â¶
    

Take cosh of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.acos(_x_)Â¶
    

Take acos of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.acosh(_x_)Â¶
    

Take acos of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.sin(_x_)Â¶
    

Take sin of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.sinh(_x_)Â¶
    

Take sinh of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.asin(_x_)Â¶
    

Take asin of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.asinh(_x_)Â¶
    

Take asinh of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.atan(_x_)Â¶
    

Take atan of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.atanh(_x_)Â¶
    

Take atanh of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.atan2(_x1_ , _x2_)Â¶
    

Take arctan2(x1, x2).

Parameters:
    

  * **x1** (_PrimExpr_) â Input argument.

  * **x2** (_PrimExpr_) â Input argument.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.sqrt(_x_)Â¶
    

Take square root of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.rsqrt(_x_)Â¶
    

Take reciprocal of square root of input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.clz(_x_)Â¶
    

Count leading zero bits of an integer x.

Parameters:
    

**x** (_PrimExpr_) â Input 32 or 64 bit integer. The result is undefined if the input is 0.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.floor(_x_ , _span =None_)Â¶
    

Take floor of float input x.

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.ceil(_x_ , _span =None_)Â¶
    

Take ceil of float input x.

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.trunc(_x_ , _span =None_)Â¶
    

Get truncated value of the input.

The truncated value of the scalar x is the nearest integer i which is closer to zero than x is.

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.abs(_x_ , _span =None_)Â¶
    

Get absolute value of the input element-wise.

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.bitwise_and(_x_ , _y_ , _span =None_)Â¶
    

Take bitwise and of two values

Parameters:
    

  * **x** (_PrimExpr_) â Left operand

  * **y** (_PrimExpr_) â Right operand

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**res** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.bitwise_not(_x_ , _span =None_)Â¶
    

Take bitwise not of input value

Parameters:
    

  * **x** (_PrimExpr_) â Input operand

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**res** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.bitwise_or(_x_ , _y_ , _span =None_)Â¶
    

Take bitwise or of two values

Parameters:
    

  * **x** (_PrimExpr_) â Left operand

  * **y** (_PrimExpr_) â Right operand

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**res** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.bitwise_xor(_x_ , _y_ , _span =None_)Â¶
    

Take bitwise xor of two values

Parameters:
    

  * **x** (_PrimExpr_) â Left operand

  * **y** (_PrimExpr_) â Right operand

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**res** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.round(_x_ , _span =None_)Â¶
    

Round elements of the array to the nearest integer.

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.nearbyint(_x_ , _span =None_)Â¶
    

Round elements of the array to the nearest integer. This intrinsic uses llvm.nearbyint instead of llvm.round which is faster but will results different from te.round. Notably nearbyint rounds according to the rounding mode, whereas te.round (llvm.round) ignores that. For differences between the two see: <https://en.cppreference.com/w/cpp/numeric/math/round> <https://en.cppreference.com/w/cpp/numeric/math/nearbyint>

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.nextafter(_x1_ , _x2_)Â¶
    

Return the next floating-point value after x1 towards x2.

Parameters:
    

  * **x1** (_PrimExpr_) â Input argument.

  * **x2** (_PrimExpr_) â Input argument.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.hypot(_x1_ , _x2_)Â¶
    

Equivalent to sqrt(x1**2 + x2**2), element-wise.

Parameters:
    

  * **x1** (_PrimExpr_) â Input argument.

  * **x2** (_PrimExpr_) â Input argument.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.copysign(_x1_ , _x2_)Â¶
    

Change the sign of x1 to that of x2, element-wise.

Parameters:
    

  * **x1** (_PrimExpr_) â Input argument.

  * **x2** (_PrimExpr_) â Input argument.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.ldexp(_x1_ , _x2_)Â¶
    

Returns x1 * (2 ** x2).

Parameters:
    

  * **x1** (_PrimExpr_) â Input argument.

  * **x2** (_PrimExpr_) â Input argument.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.likely(_cond_ , _span =None_)Â¶
    

Mark condition as likely.

Parameters:
    

  * **cond** (_PrimExpr_) â Input argument.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**y** â The marked expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.isnan(_x_ , _span =None_)Â¶
    

Check if input value is Nan.

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.isnullptr(_x_ , _span =None_)Â¶
    

Check if input value is nullptr.

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.isfinite(_x_ , _span =None_)Â¶
    

Check if input value is finite.

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.isinf(_x_ , _span =None_)Â¶
    

Check if input value is infinite.

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.pow_of_int(_x_ , _y_)Â¶
    

Fast power operation than pow(float, float).

Parameters:
    

  * **x** (_PrimExpr_) â Base value

  * **y** (_int_) â Exponent value



Return type:
    

tvm.ir.PrimExpr

tilelang.language.tir.op.power(_x_ , _y_ , _span =None_)Â¶
    

x power y

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **y** (_PrimExpr_) â The exponent

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**z** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.pow(_x_ , _y_ , _span =None_)Â¶
    

x power y

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **y** (_PrimExpr_) â The exponent

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source code.



Returns:
    

**z** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.popcount(_x_)Â¶
    

Count the number of set bits in input x.

Parameters:
    

**x** (_PrimExpr_) â Input argument.

Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.q_multiply_shift(_x_ , _y_ , _q_ , _s_)Â¶
    

Execute a multiplication between two Q-numbers x and y followed by a right shift s. The mathematical expression is:

> out = round(x*y*2^-s)

More about Q-numbers here: <https://en.wikipedia.org/wiki/Q_(number_format>) The rounding rule is to the nearest value, rounding half up (i.e., round(x.1) = x and round (x.5) = x+1)

Parameters:
    

  * **x** (_PrimExpr_) â First Q-number

  * **y** (_PrimExpr_) â Second Q-number

  * **q** (_PrimExpr_) â Number of fractional bits in x and y. Needs to be > 0

  * **s** (_PrimExpr_) â Integer shift



Returns:
    

**y** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.q_multiply_shift_per_axis(_x_ , _y_ , _ls_ , _rs_ , _q_ , _is_lshift_required_ , _is_rshift_required_)Â¶
    

Execute a multiplication between two Q-numbers x and y

Parameters:
    

  * **x** (_PrimExpr_) â First Q-number.

  * **y** (_PrimExpr_) â Second Q-number.

  * **ls** (_PrimExpr_) â Integer left shift.

  * **rs** (_PrimExpr_) â Integer right shift.

  * **q** (_IntImm_) â Number of fractional bits in x and y. Needs to be > 0.

  * **is_lshift_required** (_IntImm_) â Whether we need to do left shift or not.

  * **is_rshift_required** (_IntImm_) â Whether we need to do right shift or not.



Returns:
    

**z** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.shift_left(_x_ , _y_ , _span =None_)Â¶
    

Return the result of x left shifted by y bits.

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **y** (_PrimExpr_) â Input argument.



Returns:
    

**z** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.shift_right(_x_ , _y_ , _span =None_)Â¶
    

Return the result of x right shifted by y bits.

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **y** (_PrimExpr_) â Input argument.



Returns:
    

**z** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.fmod(_x_ , _y_)Â¶
    

Return the remainder of x divided by y with the same sign as x.

Parameters:
    

  * **x** (_PrimExpr_) â Input argument.

  * **y** (_PrimExpr_) â Input argument.



Returns:
    

**z** â The result.

Return type:
    

PrimExpr

tilelang.language.tir.op.if_then_else(_cond_ , _t_ , _f_ , _span =None_)Â¶
    

Conditional selection expression.

Parameters:
    

  * **cond** (_PrimExpr_) â The condition

  * **t** (_PrimExpr_) â The result expression if cond is true.

  * **f** (_PrimExpr_) â The result expression if cond is false.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source.



Returns:
    

**result** â The result of conditional expression.

Return type:
    

[Node](../../../carver/roller/node/index.html#tilelang.carver.roller.node.Node "tilelang.carver.roller.node.Node")

Note

Unlike Select, if_then_else will not execute the branch that does not satisfy the condition. You can use it to guard against out of bound access. Unlike Select, if_then_else cannot be vectorized if some lanes in the vector have different conditions.

tilelang.language.tir.op.div(_a_ , _b_ , _span =None_)Â¶
    

Compute a / b as in C/C++ semantics.

Parameters:
    

  * **a** (_PrimExpr_) â The left hand operand, known to be non-negative.

  * **b** (_PrimExpr_) â The right hand operand, known to be non-negative.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source.



Returns:
    

**res** â The result expression.

Return type:
    

PrimExpr

Note

When operands are integers, returns truncdiv(a, b, span).

tilelang.language.tir.op.indexdiv(_a_ , _b_ , _span =None_)Â¶
    

Compute floor(a / b) where a and b are non-negative.

Parameters:
    

  * **a** (_PrimExpr_) â The left hand operand, known to be non-negative.

  * **b** (_PrimExpr_) â The right hand operand, known to be non-negative.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source.



Returns:
    

**res** â The result expression.

Return type:
    

PrimExpr

Note

Use this function to split non-negative indices. This function may take advantage of operandsâ non-negativeness.

tilelang.language.tir.op.indexmod(_a_ , _b_ , _span =None_)Â¶
    

Compute the remainder of indexdiv. a and b are non-negative.

Parameters:
    

  * **a** (_PrimExpr_) â The left hand operand, known to be non-negative.

  * **b** (_PrimExpr_) â The right hand operand, known to be non-negative.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source.



Returns:
    

**res** â The result expression.

Return type:
    

PrimExpr

Note

Use this function to split non-negative indices. This function may take advantage of operandsâ non-negativeness.

tilelang.language.tir.op.truncdiv(_a_ , _b_ , _span =None_)Â¶
    

Compute the truncdiv of two expressions.

Parameters:
    

  * **a** (_PrimExpr_) â The left hand operand

  * **b** (_PrimExpr_) â The right hand operand

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source.



Returns:
    

**res** â The result expression.

Return type:
    

PrimExpr

Note

This is the default integer division behavior in C.

tilelang.language.tir.op.truncmod(_a_ , _b_ , _span =None_)Â¶
    

Compute the truncmod of two expressions.

Parameters:
    

  * **a** (_PrimExpr_) â The left hand operand

  * **b** (_PrimExpr_) â The right hand operand

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source.



Returns:
    

**res** â The result expression.

Return type:
    

PrimExpr

Note

This is the default integer division behavior in C.

tilelang.language.tir.op.floordiv(_a_ , _b_ , _span =None_)Â¶
    

Compute the floordiv of two expressions.

Parameters:
    

  * **a** (_PrimExpr_) â The left hand operand

  * **b** (_PrimExpr_) â The right hand operand

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source.



Returns:
    

**res** â The result expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.floormod(_a_ , _b_ , _span =None_)Â¶
    

Compute the floormod of two expressions.

Parameters:
    

  * **a** (_PrimExpr_) â The left hand operand

  * **b** (_PrimExpr_) â The right hand operand

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source.



Returns:
    

**res** â The result expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.ceildiv(_lhs_ , _rhs_ , _span =None_)Â¶
    

Generic ceildiv operator.

Parameters:
    

  * **lhs** (_object_) â The left operand.

  * **rhs** (_object_) â The right operand.

  * **span** (_Optional_ _[__Span_ _]_) â The location of this operator in the source.



Returns:
    

**op** â The result Expr of ceildiv operation.

Return type:
    

tvm.Expr

tilelang.language.tir.op.comm_reducer(_fcombine_ , _fidentity_ , _name ='reduce'_)Â¶
    

Create a commutative reducer for reduction.

Parameters:
    

  * **fcombine** (_function_ _(__Expr - > Expr -> Expr_ _)_) â A binary function which takes two Expr as input to return a Expr.

  * **fidentity** (_function_ _(__str - > Expr_ _)_) â A function which takes a type string as input to return a const Expr.



Returns:
    

**reducer** â A function which creates a reduce expression over axis. There are two ways to use it:

  1. accept (expr, axis, where) to produce an Reduce Expr on specified axis;

  2. simply use it with multiple Exprs.




Return type:
    

function

Example
    
    
    n = te.var("n")
    m = te.var("m")
    mysum = te.comm_reducer(lambda x, y: x+y,
        lambda t: tvm.tir.const(0, dtype=t), name="mysum")
    A = te.placeholder((n, m), name="A")
    k = te.reduce_axis((0, m), name="k")
    B = te.compute((n,), lambda i: mysum(A[i, k], axis=k), name="B")
    

tilelang.language.tir.op.TVMBackendAllocWorkspace(_device_type_ , _device_id_ , _nbytes_ , _dtype_code_hint_ , _dtype_bits_hint_)Â¶
    

Backend function to allocate temporal workspace

Parameters:
    

  * **device_type** (_int_) â The device type which the space will be allocated.

  * **device_id** (_int_) â The device id which the space will be allocated.

  * **nbytes** (_int_) â The size of the space requested.

  * **dtype_code_hint** (_int_) â The type code of the array elements. Only used in certain backends such as OpenGL.

  * **dtype_bits_hint** (_int_) â The type bits of the array elements. Only used in certain backends such as OpenGL.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.TVMBackendFreeWorkspace(_device_type_ , _device_id_ , _ptr_)Â¶
    

Backend function to free temporal workspace.

Parameters:
    

  * **device_type** (_int_) â The device type which the space will be allocated.

  * **device_id** (_int_) â The device id which the space will be allocated.

  * **ptr** (_Var_) â The result allocated space pointer.



Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.anylist_getitem(_list_handle_ , _index_)Â¶
    

Returns an item from any list. list_handle: Var

> The handle to anylist

indexint
    

The index

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.anylist_resetitem(_list_handle_ , _index_)Â¶
    

Reset an item from any list. list_handle: Var

> The handle to anylist

indexint
    

The index

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.anylist_setitem_call_packed(_list_handle_ , _index_ , _func_name_ , _* args_)Â¶
    

Set anylist item by result of packed call. list_handle: Var

> The handle to anylist

indexint
    

The index

func_name: str
    

The name of the function to be called.

Parameters:
    

**arguments** (_Extra_)

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.anylist_setitem_call_cpacked(_list_handle_ , _index_ , _func_name_ , _* args_)Â¶
    

Set anylist item by result of packed call. list_handle: Var

> The handle to anylist

indexint
    

The index

func_name: str
    

The name of the function to be called.

Parameters:
    

**arguments** (_Extra_)

Returns:
    

**call** â The call expression.

Return type:
    

PrimExpr

tilelang.language.tir.op.vscale()Â¶
    

Get the targetâs vscale value. It will be lowered to llvm.vscale intrinsic (<https://llvm.org/docs/LangRef.html#llvm-vscale-intrinsic>) :returns: **call** â Call to the vscale intrinsic :rtype: PrimExpr

tilelang.language.tir.op.sumÂ¶
    

tilelang.language.tir.op.minÂ¶
    

tilelang.language.tir.op.maxÂ¶
    

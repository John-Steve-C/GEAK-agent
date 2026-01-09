# triton.language¶  
  
## Programming Model¶

[`tensor`](generated/triton.language.tensor.html#triton.language.tensor "triton.language.tensor") | Represents an N-dimensional array of values or pointers.  
---|---  
[`tensor_descriptor`](generated/triton.language.tensor_descriptor.html#triton.language.tensor_descriptor "triton.language.tensor_descriptor") | A descriptor representing a tensor in global memory.  
[`program_id`](generated/triton.language.program_id.html#triton.language.program_id "triton.language.program_id") | Returns the id of the current program instance along the given `axis`.  
[`num_programs`](generated/triton.language.num_programs.html#triton.language.num_programs "triton.language.num_programs") | Returns the number of program instances launched along the given `axis`.  
  
## Creation Ops¶

[`arange`](generated/triton.language.arange.html#triton.language.arange "triton.language.arange") | Returns contiguous values within the half-open interval `[start, end)`.  
---|---  
[`cat`](generated/triton.language.cat.html#triton.language.cat "triton.language.cat") | Concatenate the given blocks  
[`full`](generated/triton.language.full.html#triton.language.full "triton.language.full") | Returns a tensor filled with the scalar value for the given `shape` and `dtype`.  
[`zeros`](generated/triton.language.zeros.html#triton.language.zeros "triton.language.zeros") | Returns a tensor filled with the scalar value 0 for the given `shape` and `dtype`.  
[`zeros_like`](generated/triton.language.zeros_like.html#triton.language.zeros_like "triton.language.zeros_like") | Returns a tensor of zeros with the same shape and type as a given tensor.  
[`cast`](generated/triton.language.cast.html#triton.language.cast "triton.language.cast") | Casts a tensor to the given `dtype`.  
  
## Shape Manipulation Ops¶

[`broadcast`](generated/triton.language.broadcast.html#triton.language.broadcast "triton.language.broadcast") | Tries to broadcast the two given blocks to a common compatible shape.  
---|---  
[`broadcast_to`](generated/triton.language.broadcast_to.html#triton.language.broadcast_to "triton.language.broadcast_to") | Tries to broadcast the given tensor to a new `shape`.  
[`expand_dims`](generated/triton.language.expand_dims.html#triton.language.expand_dims "triton.language.expand_dims") | Expand the shape of a tensor, by inserting new length-1 dimensions.  
[`interleave`](generated/triton.language.interleave.html#triton.language.interleave "triton.language.interleave") | Interleaves the values of two tensors along their last dimension.  
[`join`](generated/triton.language.join.html#triton.language.join "triton.language.join") | Join the given tensors in a new, minor dimension.  
[`permute`](generated/triton.language.permute.html#triton.language.permute "triton.language.permute") | Permutes the dimensions of a tensor.  
[`ravel`](generated/triton.language.ravel.html#triton.language.ravel "triton.language.ravel") | Returns a contiguous flattened view of `x`.  
[`reshape`](generated/triton.language.reshape.html#triton.language.reshape "triton.language.reshape") | Returns a tensor with the same number of elements as input but with the provided shape.  
[`split`](generated/triton.language.split.html#triton.language.split "triton.language.split") | Split a tensor in two along its last dim, which must have size 2.  
[`trans`](generated/triton.language.trans.html#triton.language.trans "triton.language.trans") | Permutes the dimensions of a tensor.  
[`view`](generated/triton.language.view.html#triton.language.view "triton.language.view") | Returns a tensor with the same elements as input but a different shape.  
  
## Linear Algebra Ops¶

[`dot`](generated/triton.language.dot.html#triton.language.dot "triton.language.dot") | Returns the matrix product of two blocks.  
---|---  
[`dot_scaled`](generated/triton.language.dot_scaled.html#triton.language.dot_scaled "triton.language.dot_scaled") | Returns the matrix product of two blocks in microscaling format.  
  
## Memory/Pointer Ops¶

[`load`](generated/triton.language.load.html#triton.language.load "triton.language.load") | Return a tensor of data whose values are loaded from memory at location defined by pointer:  
---|---  
[`store`](generated/triton.language.store.html#triton.language.store "triton.language.store") | Store a tensor of data into memory locations defined by pointer.  
[`make_tensor_descriptor`](generated/triton.language.make_tensor_descriptor.html#triton.language.make_tensor_descriptor "triton.language.make_tensor_descriptor") | Make a tensor descriptor object  
[`load_tensor_descriptor`](generated/triton.language.load_tensor_descriptor.html#triton.language.load_tensor_descriptor "triton.language.load_tensor_descriptor") | Load a block of data from a tensor descriptor.  
[`store_tensor_descriptor`](generated/triton.language.store_tensor_descriptor.html#triton.language.store_tensor_descriptor "triton.language.store_tensor_descriptor") | Store a block of data to a tensor descriptor.  
[`make_block_ptr`](generated/triton.language.make_block_ptr.html#triton.language.make_block_ptr "triton.language.make_block_ptr") | Returns a pointer to a block in a parent tensor  
[`advance`](generated/triton.language.advance.html#triton.language.advance "triton.language.advance") | Advance a block pointer  
  
## Indexing Ops¶

[`flip`](generated/triton.language.flip.html#triton.language.flip "triton.language.flip") | Flips a tensor x along the dimension dim.  
---|---  
[`where`](generated/triton.language.where.html#triton.language.where "triton.language.where") | Returns a tensor of elements from either `x` or `y`, depending on `condition`.  
[`swizzle2d`](generated/triton.language.swizzle2d.html#triton.language.swizzle2d "triton.language.swizzle2d") | Transforms the indices of a row-major size_i * size_j matrix into the indices of a column-major matrix for each group of size_g rows.  
  
## Math Ops¶

[`abs`](generated/triton.language.abs.html#triton.language.abs "triton.language.abs") | Computes the element-wise absolute value of `x`.  
---|---  
[`cdiv`](generated/triton.language.cdiv.html#triton.language.cdiv "triton.language.cdiv") | Computes the ceiling division of `x` by `div`  
[`ceil`](generated/triton.language.ceil.html#triton.language.ceil "triton.language.ceil") | Computes the element-wise ceil of `x`.  
[`clamp`](generated/triton.language.clamp.html#triton.language.clamp "triton.language.clamp") | Clamps the input tensor `x` within the range [min, max].  
[`cos`](generated/triton.language.cos.html#triton.language.cos "triton.language.cos") | Computes the element-wise cosine of `x`.  
[`div_rn`](generated/triton.language.div_rn.html#triton.language.div_rn "triton.language.div_rn") | Computes the element-wise precise division (rounding to nearest wrt the IEEE standard) of `x` and `y`.  
[`erf`](generated/triton.language.erf.html#triton.language.erf "triton.language.erf") | Computes the element-wise error function of `x`.  
[`exp`](generated/triton.language.exp.html#triton.language.exp "triton.language.exp") | Computes the element-wise exponential of `x`.  
[`exp2`](generated/triton.language.exp2.html#triton.language.exp2 "triton.language.exp2") | Computes the element-wise exponential (base 2) of `x`.  
[`fdiv`](generated/triton.language.fdiv.html#triton.language.fdiv "triton.language.fdiv") | Computes the element-wise fast division of `x` and `y`.  
[`floor`](generated/triton.language.floor.html#triton.language.floor "triton.language.floor") | Computes the element-wise floor of `x`.  
[`fma`](generated/triton.language.fma.html#triton.language.fma "triton.language.fma") | Computes the element-wise fused multiply-add of `x`, `y`, and `z`.  
[`log`](generated/triton.language.log.html#triton.language.log "triton.language.log") | Computes the element-wise natural logarithm of `x`.  
[`log2`](generated/triton.language.log2.html#triton.language.log2 "triton.language.log2") | Computes the element-wise logarithm (base 2) of `x`.  
[`maximum`](generated/triton.language.maximum.html#triton.language.maximum "triton.language.maximum") | Computes the element-wise maximum of `x` and `y`.  
[`minimum`](generated/triton.language.minimum.html#triton.language.minimum "triton.language.minimum") | Computes the element-wise minimum of `x` and `y`.  
[`rsqrt`](generated/triton.language.rsqrt.html#triton.language.rsqrt "triton.language.rsqrt") | Computes the element-wise inverse square root of `x`.  
[`sigmoid`](generated/triton.language.sigmoid.html#triton.language.sigmoid "triton.language.sigmoid") | Computes the element-wise sigmoid of `x`.  
[`sin`](generated/triton.language.sin.html#triton.language.sin "triton.language.sin") | Computes the element-wise sine of `x`.  
[`softmax`](generated/triton.language.softmax.html#triton.language.softmax "triton.language.softmax") | Computes the element-wise softmax of `x`.  
[`sqrt`](generated/triton.language.sqrt.html#triton.language.sqrt "triton.language.sqrt") | Computes the element-wise fast square root of `x`.  
[`sqrt_rn`](generated/triton.language.sqrt_rn.html#triton.language.sqrt_rn "triton.language.sqrt_rn") | Computes the element-wise precise square root (rounding to nearest wrt the IEEE standard) of `x`.  
[`umulhi`](generated/triton.language.umulhi.html#triton.language.umulhi "triton.language.umulhi") | Computes the element-wise most significant N bits of the 2N-bit product of `x` and `y`.  
  
## Reduction Ops¶

[`argmax`](generated/triton.language.argmax.html#triton.language.argmax "triton.language.argmax") | Returns the maximum index of all elements in the `input` tensor along the provided `axis`  
---|---  
[`argmin`](generated/triton.language.argmin.html#triton.language.argmin "triton.language.argmin") | Returns the minimum index of all elements in the `input` tensor along the provided `axis`  
[`max`](generated/triton.language.max.html#triton.language.max "triton.language.max") | Returns the maximum of all elements in the `input` tensor along the provided `axis`  
[`min`](generated/triton.language.min.html#triton.language.min "triton.language.min") | Returns the minimum of all elements in the `input` tensor along the provided `axis`  
[`reduce`](generated/triton.language.reduce.html#triton.language.reduce "triton.language.reduce") | Applies the combine_fn to all elements in `input` tensors along the provided `axis`  
[`sum`](generated/triton.language.sum.html#triton.language.sum "triton.language.sum") | Returns the sum of all elements in the `input` tensor along the provided `axis`  
[`xor_sum`](generated/triton.language.xor_sum.html#triton.language.xor_sum "triton.language.xor_sum") | Returns the xor sum of all elements in the `input` tensor along the provided `axis`  
  
## Scan/Sort Ops¶

[`associative_scan`](generated/triton.language.associative_scan.html#triton.language.associative_scan "triton.language.associative_scan") | Applies the combine_fn to each elements with a carry in `input` tensors along the provided `axis` and update the carry  
---|---  
[`cumprod`](generated/triton.language.cumprod.html#triton.language.cumprod "triton.language.cumprod") | Returns the cumprod of all elements in the `input` tensor along the provided `axis`  
[`cumsum`](generated/triton.language.cumsum.html#triton.language.cumsum "triton.language.cumsum") | Returns the cumsum of all elements in the `input` tensor along the provided `axis`  
[`histogram`](generated/triton.language.histogram.html#triton.language.histogram "triton.language.histogram") | computes an histogram based on input tensor with num_bins bins, the bins have a width of 1 and start at 0.  
[`sort`](generated/triton.language.sort.html#triton.language.sort "triton.language.sort") |   
[`gather`](generated/triton.language.gather.html#triton.language.gather "triton.language.gather") | Gather from a tensor along a given dimension.  
  
## Atomic Ops¶

[`atomic_add`](generated/triton.language.atomic_add.html#triton.language.atomic_add "triton.language.atomic_add") | Performs an atomic add at the memory location specified by `pointer`.  
---|---  
[`atomic_and`](generated/triton.language.atomic_and.html#triton.language.atomic_and "triton.language.atomic_and") | Performs an atomic logical and at the memory location specified by `pointer`.  
[`atomic_cas`](generated/triton.language.atomic_cas.html#triton.language.atomic_cas "triton.language.atomic_cas") | Performs an atomic compare-and-swap at the memory location specified by `pointer`.  
[`atomic_max`](generated/triton.language.atomic_max.html#triton.language.atomic_max "triton.language.atomic_max") | Performs an atomic max at the memory location specified by `pointer`.  
[`atomic_min`](generated/triton.language.atomic_min.html#triton.language.atomic_min "triton.language.atomic_min") | Performs an atomic min at the memory location specified by `pointer`.  
[`atomic_or`](generated/triton.language.atomic_or.html#triton.language.atomic_or "triton.language.atomic_or") | Performs an atomic logical or at the memory location specified by `pointer`.  
[`atomic_xchg`](generated/triton.language.atomic_xchg.html#triton.language.atomic_xchg "triton.language.atomic_xchg") | Performs an atomic exchange at the memory location specified by `pointer`.  
[`atomic_xor`](generated/triton.language.atomic_xor.html#triton.language.atomic_xor "triton.language.atomic_xor") | Performs an atomic logical xor at the memory location specified by `pointer`.  
  
## Random Number Generation¶

[`randint4x`](generated/triton.language.randint4x.html#triton.language.randint4x "triton.language.randint4x") | Given a `seed` scalar and an `offset` block, returns four blocks of random `int32`.  
---|---  
[`randint`](generated/triton.language.randint.html#triton.language.randint "triton.language.randint") | Given a `seed` scalar and an `offset` block, returns a single block of random `int32`.  
[`rand`](generated/triton.language.rand.html#triton.language.rand "triton.language.rand") | Given a `seed` scalar and an `offset` block, returns a block of random `float32` in \\(U(0, 1)\\).  
[`randn`](generated/triton.language.randn.html#triton.language.randn "triton.language.randn") | Given a `seed` scalar and an `offset` block, returns a block of random `float32` in \\(\mathcal{N}(0, 1)\\).  
  
## Iterators¶

[`range`](generated/triton.language.range.html#triton.language.range "triton.language.range") | Iterator that counts upward forever.  
---|---  
[`static_range`](generated/triton.language.static_range.html#triton.language.static_range "triton.language.static_range") | Iterator that counts upward forever.  
  
## Inline Assembly¶

[`inline_asm_elementwise`](generated/triton.language.inline_asm_elementwise.html#triton.language.inline_asm_elementwise "triton.language.inline_asm_elementwise") | Execute inline assembly over a tensor.  
---|---  
  
## Compiler Hint Ops¶

[`assume`](generated/triton.language.assume.html#triton.language.assume "triton.language.assume") | Allow compiler to assume the `cond` is True.  
---|---  
[`debug_barrier`](generated/triton.language.debug_barrier.html#triton.language.debug_barrier "triton.language.debug_barrier") | Insert a barrier to synchronize all threads in a block.  
[`max_constancy`](generated/triton.language.max_constancy.html#triton.language.max_constancy "triton.language.max_constancy") | Let the compiler know that the value first values in `input` are constant.  
[`max_contiguous`](generated/triton.language.max_contiguous.html#triton.language.max_contiguous "triton.language.max_contiguous") | Let the compiler know that the value first values in `input` are contiguous.  
[`multiple_of`](generated/triton.language.multiple_of.html#triton.language.multiple_of "triton.language.multiple_of") | Let the compiler know that the values in `input` are all multiples of `value`.  
  
## Debug Ops¶

[`static_print`](generated/triton.language.static_print.html#triton.language.static_print "triton.language.static_print") | Print the values at compile time.  
---|---  
[`static_assert`](generated/triton.language.static_assert.html#triton.language.static_assert "triton.language.static_assert") | Assert the condition at compile time.  
[`device_print`](generated/triton.language.device_print.html#triton.language.device_print "triton.language.device_print") | Print the values at runtime from the device.  
[`device_assert`](generated/triton.language.device_assert.html#triton.language.device_assert "triton.language.device_assert") | Assert the condition at runtime from the device.

# triton.language.tensor¶

_class _triton.language.tensor(_self_ , _handle_ , _type : dtype_)¶
    

Represents an N-dimensional array of values or pointers.

`tensor` is the fundamental data structure in Triton programs. Most functions in `triton.language` operate on and return tensors.

Most of the named member functions here are duplicates of the free functions in `triton.language`. For example, `triton.language.sqrt(x)` is equivalent to `x.sqrt()`.

`tensor` also defines most of the magic/dunder methods, so you can write `x+y`, `x << 2`, etc.

Constructors

__init__(_self_ , _handle_ , _type : dtype_)¶
    

Not called by user code.

Methods

`__init__`(self, handle, type) | Not called by user code.  
---|---  
`abs`(self[, _semantic]) | Forwards to [`abs()`](triton.language.abs.html#triton.language.abs "triton.language.abs") free function  
`advance`(self, offsets[, _semantic]) | Forwards to [`advance()`](triton.language.advance.html#triton.language.advance "triton.language.advance") free function  
`argmax`(input, axis[, tie_break_left, keep_dims]) | Returns the maximum index of all elements in the `input` tensor along the provided `axis`  
`argmin`(input, axis[, tie_break_left, keep_dims]) | Returns the minimum index of all elements in the `input` tensor along the provided `axis`  
`associative_scan`(self, axis, combine_fn[, ...]) | Forwards to [`associative_scan()`](triton.language.associative_scan.html#triton.language.associative_scan "triton.language.associative_scan") free function  
`atomic_add`(self, val[, mask, sem, scope, ...]) | Forwards to [`atomic_add()`](triton.language.atomic_add.html#triton.language.atomic_add "triton.language.atomic_add") free function  
`atomic_and`(self, val[, mask, sem, scope, ...]) | Forwards to [`atomic_and()`](triton.language.atomic_and.html#triton.language.atomic_and "triton.language.atomic_and") free function  
`atomic_cas`(self, cmp, val[, sem, scope, ...]) | Forwards to [`atomic_cas()`](triton.language.atomic_cas.html#triton.language.atomic_cas "triton.language.atomic_cas") free function  
`atomic_max`(self, val[, mask, sem, scope, ...]) | Forwards to [`atomic_max()`](triton.language.atomic_max.html#triton.language.atomic_max "triton.language.atomic_max") free function  
`atomic_min`(self, val[, mask, sem, scope, ...]) | Forwards to [`atomic_min()`](triton.language.atomic_min.html#triton.language.atomic_min "triton.language.atomic_min") free function  
`atomic_or`(self, val[, mask, sem, scope, ...]) | Forwards to [`atomic_or()`](triton.language.atomic_or.html#triton.language.atomic_or "triton.language.atomic_or") free function  
`atomic_xchg`(self, val[, mask, sem, scope, ...]) | Forwards to [`atomic_xchg()`](triton.language.atomic_xchg.html#triton.language.atomic_xchg "triton.language.atomic_xchg") free function  
`atomic_xor`(self, val[, mask, sem, scope, ...]) | Forwards to [`atomic_xor()`](triton.language.atomic_xor.html#triton.language.atomic_xor "triton.language.atomic_xor") free function  
`broadcast_to`(self, *shape[, _semantic]) | Forwards to [`broadcast_to()`](triton.language.broadcast_to.html#triton.language.broadcast_to "triton.language.broadcast_to") free function  
`cast`(self, dtype[, fp_downcast_rounding, ...]) | Forwards to [`cast()`](triton.language.cast.html#triton.language.cast "triton.language.cast") free function  
`cdiv`(x, div) | Computes the ceiling division of `x` by `div`  
`ceil`(self[, _semantic]) | Forwards to [`ceil()`](triton.language.ceil.html#triton.language.ceil "triton.language.ceil") free function  
`cos`(self[, _semantic]) | Forwards to [`cos()`](triton.language.cos.html#triton.language.cos "triton.language.cos") free function  
`cumprod`(input[, axis, reverse]) | Returns the cumprod of all elements in the `input` tensor along the provided `axis`  
`cumsum`(input[, axis, reverse, dtype]) | Returns the cumsum of all elements in the `input` tensor along the provided `axis`  
`erf`(self[, _semantic]) | Forwards to [`erf()`](triton.language.erf.html#triton.language.erf "triton.language.erf") free function  
`exp`(self[, _semantic]) | Forwards to [`exp()`](triton.language.exp.html#triton.language.exp "triton.language.exp") free function  
`exp2`(self[, _semantic]) | Forwards to [`exp2()`](triton.language.exp2.html#triton.language.exp2 "triton.language.exp2") free function  
`expand_dims`(self, axis[, _semantic]) | Forwards to [`expand_dims()`](triton.language.expand_dims.html#triton.language.expand_dims "triton.language.expand_dims") free function  
`flip`(x[, dim]) | Flips a tensor x along the dimension dim.  
`floor`(self[, _semantic]) | Forwards to [`floor()`](triton.language.floor.html#triton.language.floor "triton.language.floor") free function  
`gather`(self, index, axis[, _semantic]) | Forwards to [`gather()`](triton.language.gather.html#triton.language.gather "triton.language.gather") free function  
`histogram`(self, num_bins[, mask, _semantic, ...]) | Forwards to [`histogram()`](triton.language.histogram.html#triton.language.histogram "triton.language.histogram") free function  
`item`(self[, _semantic, _generator]) | Forwards to `item()` free function  
`log`(self[, _semantic]) | Forwards to [`log()`](triton.language.log.html#triton.language.log "triton.language.log") free function  
`log2`(self[, _semantic]) | Forwards to [`log2()`](triton.language.log2.html#triton.language.log2 "triton.language.log2") free function  
`logical_and`(self, other[, _semantic]) |   
`logical_or`(self, other[, _semantic]) |   
`max`(input[, axis, return_indices, ...]) | Returns the maximum of all elements in the `input` tensor along the provided `axis`  
`min`(input[, axis, return_indices, ...]) | Returns the minimum of all elements in the `input` tensor along the provided `axis`  
`permute`(self, *dims[, _semantic]) | Forwards to [`permute()`](triton.language.permute.html#triton.language.permute "triton.language.permute") free function  
`ravel`(x[, can_reorder]) | Returns a contiguous flattened view of `x`.  
`reduce`(self, axis, combine_fn[, keep_dims, ...]) | Forwards to [`reduce()`](triton.language.reduce.html#triton.language.reduce "triton.language.reduce") free function  
`reduce_or`(input, axis[, keep_dims]) | Returns the reduce_or of all elements in the `input` tensor along the provided `axis`  
`reshape`(self, *shape[, can_reorder, ...]) | Forwards to [`reshape()`](triton.language.reshape.html#triton.language.reshape "triton.language.reshape") free function  
`rsqrt`(self[, _semantic]) | Forwards to [`rsqrt()`](triton.language.rsqrt.html#triton.language.rsqrt "triton.language.rsqrt") free function  
`sigmoid`(x) | Computes the element-wise sigmoid of `x`.  
`sin`(self[, _semantic]) | Forwards to [`sin()`](triton.language.sin.html#triton.language.sin "triton.language.sin") free function  
`softmax`(x[, dim, keep_dims, ieee_rounding]) | Computes the element-wise softmax of `x`.  
`sort`(self[, dim, descending]) |   
`split`(self[, _semantic, _generator]) | Forwards to [`split()`](triton.language.split.html#triton.language.split "triton.language.split") free function  
`sqrt`(self[, _semantic]) | Forwards to [`sqrt()`](triton.language.sqrt.html#triton.language.sqrt "triton.language.sqrt") free function  
`sqrt_rn`(self[, _semantic]) | Forwards to [`sqrt_rn()`](triton.language.sqrt_rn.html#triton.language.sqrt_rn "triton.language.sqrt_rn") free function  
`store`(self, value[, mask, boundary_check, ...]) | Forwards to [`store()`](triton.language.store.html#triton.language.store "triton.language.store") free function  
`sum`(input[, axis, keep_dims, dtype]) | Returns the sum of all elements in the `input` tensor along the provided `axis`  
`to`(self, dtype[, fp_downcast_rounding, ...]) | Alias for `tensor.cast()`.  
`trans`(self, *dims[, _semantic]) | Forwards to [`trans()`](triton.language.trans.html#triton.language.trans "triton.language.trans") free function  
`view`(self, *shape[, _semantic]) | Forwards to [`view()`](triton.language.view.html#triton.language.view "triton.language.view") free function  
`xor_sum`(input[, axis, keep_dims]) | Returns the xor sum of all elements in the `input` tensor along the provided `axis`  
  
Attributes

`T` | Transposes a 2D tensor.  
---|---  
`type` | 

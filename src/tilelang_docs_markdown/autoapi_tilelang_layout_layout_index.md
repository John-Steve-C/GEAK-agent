# tilelang.layout.layoutÂ¶

Wrapping Layouts.

## ClassesÂ¶

`Layout` |   
---|---  
  
## Module ContentsÂ¶

_class _tilelang.layout.layout.Layout(_shape_ , _forward_fn_)Â¶
    

Bases: `tvm.ir.Node`

_property _indexÂ¶
    

Property to retrieve the forward index of the layout.

Returns:
    

The computed forward index expression(s).

Return type:
    

PrimExpr or List[PrimExpr]

get_input_shape()Â¶
    

Get the input shape of the layout.

Returns:
    

The shape of the input layout.

Return type:
    

List[int]

get_output_shape()Â¶
    

Get the output shape of the layout.

Returns:
    

The shape of the output layout.

Return type:
    

List[int]

get_forward_vars()Â¶
    

Retrieve the iteration variables associated with the layout.

Returns:
    

A list of iteration variables that define the layout transformation.

Return type:
    

List[IterVar]

get_forward_index()Â¶
    

map_forward_index(_indices_)Â¶
    

Compute the forward index mapping for a given set of input indices.

Parameters:
    

**indices** (_list_ _of_ _PrimExpr_) â The input indices to be mapped to their corresponding output indices.

Returns:
    

The mapped index expression for the provided input indices.

Return type:
    

PrimExpr

repeat(_dim_ , _factor_)Â¶
    

Repeat a layout along a single input dimension.

This is useful for building a larger layout by tiling an âatomâ layout. Conceptually, repeating on dimension `dim` with `factor` constructs a new layout `L'` such that:
    
    
    L'(*idx) = [idx[dim] // extent_dim] + L(idx with idx[dim] % extent_dim)
    

where `extent_dim` is the original extent of the repeated dimension.

Parameters:
    

  * **dim** (_int_) â The input dimension to repeat (0-based, supports negative indexing).

  * **factor** (_int_) â The repeat factor. Must be a positive integer.



Returns:
    

A new Layout with the repeated input shape and an extra leading output dimension representing the repeat-group index.

Return type:
    

Layout

expand(_leading_shape_)Â¶
    

Expand (lift) this layout by prepending new leading input dimensions.

The new leading dimensions are forwarded unchanged to the output, and the original layout is applied to the remaining trailing dimensions.

Example

Given a 2D layout `L` over `[J, K]`, you can lift it to a 3D layout over `[I, J, K]` by:
    
    
    L3 = L.expand([I])
    # [i, j, k] -> [i, *L(j, k)]
    

Parameters:
    

**leading_shape** (_int_ _or_ _Sequence_ _[__int_ _or_ _PrimExpr_ _]_) â The shape of the new leading dimensions to prepend. Use an empty list/tuple for a no-op.

Returns:
    

A new Layout with input shape `leading_shape + input_shape` and output indices `[leading_dims] + old_forward_index`.

Return type:
    

Layout

inverse()Â¶
    

Compute the inverse of the current layout transformation.

Returns:
    

A new Layout object representing the inverse transformation.

Return type:
    

Layout

reshape(_shape_ , _rescale_num =1_, _rescale_den =1_)Â¶
    

Reshape the input shape of the layout.

Parameters:
    

  * **shape** (_list_ _[__PrimExpr_ _] or_ _list_ _[__int_ _]_) â The new input shape.

  * **rescale_num** (_int_) â Rescale numerator for element size changes.

  * **rescale_den** (_int_) â Rescale denominator for element size changes.



Return type:
    

Layout

is_equal(_other_)Â¶
    

Check if the current layout is equal to another layout.

Parameters:
    

**other** (_Layout_) â The layout to compare with.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

__call__(_* args_)Â¶
    

Parameters:
    

**args** (_list_ _[__tvm.tir.PrimExpr_ _]_)

Return type:
    

tvm.tir.PrimExpr

__repr__()Â¶
    

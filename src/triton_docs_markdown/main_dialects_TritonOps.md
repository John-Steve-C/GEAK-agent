# TritonOps¶

## `tt.call` (triton::CallOp)¶

_Call operation_

Syntax:
    
    
    operation ::= `tt.call` $callee `(` $operands `)` attr-dict `:` functional-type($operands, results)
    

The `tt.call` operation represents a direct call to a function that is within the same symbol scope as the call. The operands and result types of the call must match the specified function type. The callee is encoded as a symbol reference attribute named “callee”.

Example:
    
    
    %2 = tt.call @my_add(%0, %1) : (f32, f32) -> f32
    

Traits: `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ArgAndResultAttrsOpInterface`, `CallOpInterface`, `SymbolUserOpInterface`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`callee`| ::mlir::FlatSymbolRefAttr| flat symbol reference attribute  
`arg_attrs`| ::mlir::ArrayAttr| Array of dictionary attributes  
`res_attrs`| ::mlir::ArrayAttr| Array of dictionary attributes  
  
### Operands:¶

Operand | Description  
---|---  
`operands` | variadic of any type  
  
### Results:¶

Result | Description  
---|---  
«unnamed» | variadic of any type  
  
## `tt.func` (triton::FuncOp)¶

_An operation with a name containing a single` SSACFG` region_

Operations within the function cannot implicitly capture values defined outside of the function, i.e. Functions are `IsolatedFromAbove`. All external references must use function arguments or attributes that establish a symbolic connection (e.g. symbols referenced by name via a string attribute like SymbolRefAttr). An external function declaration (used when referring to a function declared in some other module) has no body. While the MLIR textual form provides a nice inline syntax for function arguments, they are internally represented as “block arguments” to the first block in the region.

Only dialect attribute names may be specified in the attribute dictionaries for function arguments, results, or the function itself.

Example:
    
    
    // External function definitions.
    tt.func @abort()
    tt.func @scribble(i32, i64, memref<? x 128 x f32, #layout_map0>) -> f64
    
    // A function that returns its argument twice:
    tt.func @count(%x: i64) -> (i64, i64)
      attributes {fruit: "banana"} {
      return %x, %x: i64, i64
    }
    
    // A function with an argument attribute
    tt.func @example_fn_arg(%x: i32 {swift.self = unit})
    
    // A function with a result attribute
    tt.func @example_fn_result() -> (f64 {dialectName.attrName = 0 : i64})
    
    // A function with an attribute
    tt.func @example_fn_attr() attributes {dialectName.attrName = false}
    

Traits: `AffineScope`, `AutomaticAllocationScope`, `HasParent<ModuleOp>`, `IsolatedFromAbove`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ArgAndResultAttrsOpInterface`, `CallableOpInterface`, `FunctionOpInterface`, `OpAsmOpInterface`, `Symbol`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`sym_name`| ::mlir::StringAttr| string attribute  
`function_type`| ::mlir::TypeAttr| type attribute of function type  
`sym_visibility`| ::mlir::StringAttr| string attribute  
`arg_attrs`| ::mlir::ArrayAttr| Array of dictionary attributes  
`res_attrs`| ::mlir::ArrayAttr| Array of dictionary attributes  
  
## `tt.return` (triton::ReturnOp)¶

_Function return operation_

Syntax:
    
    
    operation ::= `tt.return` attr-dict ($srcs^ `:` type($srcs))?
    

The `tt.return` operation represents a return operation within a function. The operation takes variable number of operands and produces no results. The operand number and types must match the signature of the function that contains the operation.

Example:
    
    
    tt.func @foo() : (i32, f8) {
      ...
      tt.return %0, %1 : i32, f8
    }
    

Traits: `AlwaysSpeculatableImplTrait`, `HasParent<FuncOp>`, `ReturnLike`, `TensorSizeTrait`, `Terminator`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`, `RegionBranchTerminatorOpInterface`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`srcs` | variadic of any type  
  
## `tt.addptr` (triton::AddPtrOp)¶

Syntax:
    
    
    operation ::= `tt.addptr` $ptr `,` $offset attr-dict `:` type($result) `,` type($offset)
    

Traits: `AlwaysSpeculatableImplTrait`, `Elementwise`, `SameOperandsAndResultEncoding`, `SameOperandsAndResultShape`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`ptr` | ptr or ranked tensor of ptr values  
`offset` | integer or ranked tensor of integer values  
  
### Results:¶

Result | Description  
---|---  
`result` | ptr or ranked tensor of ptr values  
  
## `tt.advance` (triton::AdvanceOp)¶

_Advance a tensor pointer by offsets_

Syntax:
    
    
    operation ::= `tt.advance` $ptr `,` `[` $offsets `]` attr-dict `:` type($result)
    

Traits: `AlwaysSpeculatableImplTrait`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`ptr` | ptr  
`offsets` | variadic of 32-bit signless integer  
  
### Results:¶

Result | Description  
---|---  
`result` | ptr  
  
## `tt.assert` (triton::AssertOp)¶

_Device-side assert, as in CUDA for correctness checking_

Syntax:
    
    
    operation ::= `tt.assert` $condition `,` $message attr-dict `:` type($condition)
    

`tt.assert` takes a condition tensor and a message string. If the condition is false, the message is printed, and the program is aborted.

Traits: `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `MemoryEffectOpInterface (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{MemoryEffects::Write on ::mlir::triton::GlobalMemory}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`message`| ::mlir::StringAttr| string attribute  
  
### Operands:¶

Operand | Description  
---|---  
`condition` | 1-bit signless integer or tensor of 1-bit signless integer values  
  
## `tt.atomic_cas` (triton::AtomicCASOp)¶

_Atomic cas_

Syntax:
    
    
    operation ::= `tt.atomic_cas` $sem `,` $scope `,` $ptr `,` $cmp `,` $val attr-dict `:`
                  functional-type(operands, $result)
    

compare $cmp with data $old at location $ptr,

if $old == $cmp, store $val to $ptr,

else store $old to $ptr,

return $old

Traits: `SameOperandsAndResultEncoding`, `SameOperandsAndResultShape`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`sem`| ::mlir::triton::MemSemanticAttr| allowed 32-bit signless integer cases: 1, 2, 3, 4  
`scope`| ::mlir::triton::MemSyncScopeAttr| allowed 32-bit signless integer cases: 1, 2, 3  
  
### Operands:¶

Operand | Description  
---|---  
`ptr` | ptr or ranked tensor of ptr values  
`cmp` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
`val` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
### Results:¶

Result | Description  
---|---  
`result` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
## `tt.atomic_rmw` (triton::AtomicRMWOp)¶

_Atomic rmw_

Syntax:
    
    
    operation ::= `tt.atomic_rmw` $atomic_rmw_op `,` $sem `,` $scope `,` $ptr `,` $val (`,` $mask^)?  attr-dict `:`
                  functional-type(operands, $result)
    

load data at $ptr, do $rmw_op with $val, and store result to $ptr.

return old value at $ptr

Traits: `SameOperandsAndResultEncoding`, `SameOperandsAndResultShape`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`atomic_rmw_op`| ::mlir::triton::RMWOpAttr| allowed 32-bit signless integer cases: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10  
`sem`| ::mlir::triton::MemSemanticAttr| allowed 32-bit signless integer cases: 1, 2, 3, 4  
`scope`| ::mlir::triton::MemSyncScopeAttr| allowed 32-bit signless integer cases: 1, 2, 3  
  
### Operands:¶

Operand | Description  
---|---  
`ptr` | ptr or ranked tensor of ptr values  
`val` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
`mask` | 1-bit signless integer or ranked tensor of 1-bit signless integer values  
  
### Results:¶

Result | Description  
---|---  
`result` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
## `tt.bitcast` (triton::BitcastOp)¶

_Cast between types of the same bitwidth_

Syntax:
    
    
    operation ::= `tt.bitcast` $src attr-dict `:` type($src) `->` type($result)
    

Traits: `AlwaysSpeculatableImplTrait`, `Elementwise`, `SameOperandsAndResultEncoding`, `SameOperandsAndResultShape`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`src` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
### Results:¶

Result | Description  
---|---  
`result` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
## `tt.broadcast` (triton::BroadcastOp)¶

_Broadcast a tensor_

Syntax:
    
    
    operation ::= `tt.broadcast` $src attr-dict `:` type($src) `->` type($result)
    

For a given tensor, broadcast changes one or more dimensions with size 1 to a new size, e.g. tensor<1x32x1xf32> -> tensor<2x32x4xf32>. You cannot change the size of a non-1 dimension.

Traits: `AlwaysSpeculatableImplTrait`, `SameOperandsAndResultElementType`, `SameOperandsAndResultEncoding`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`src` | ranked tensor of floating-point or integer or ptr values  
  
### Results:¶

Result | Description  
---|---  
`result` | ranked tensor of floating-point or integer or ptr values  
  
## `tt.cat` (triton::CatOp)¶

_Concatenate 2 tensors_

Syntax:
    
    
    operation ::= `tt.cat` $lhs `,` $rhs attr-dict `:` type($lhs) `->` type($result)
    

Traits: `SameOperandsAndResultElementType`, `SameTypeOperands`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`lhs` | ranked tensor of floating-point or integer or ptr values  
`rhs` | ranked tensor of floating-point or integer or ptr values  
  
### Results:¶

Result | Description  
---|---  
`result` | ranked tensor of floating-point or integer or ptr values  
  
## `tt.clampf` (triton::ClampFOp)¶

_Clamp operation for floating point types_

Syntax:
    
    
    operation ::= `tt.clampf` $x `,` $min `,` $max `,` `propagateNan` `=` $propagateNan attr-dict `:` type($result)
    

Clamp operation for floating point types.

The operation takes three arguments: x, min, and max. It returns a tensor of the same shape as x with its values clamped to the range [min, max].

Traits: `AlwaysSpeculatableImplTrait`, `Elementwise`, `SameOperandsAndResultType`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`propagateNan`| ::mlir::triton::PropagateNanAttr| allowed 32-bit signless integer cases: 0, 65535  
  
### Operands:¶

Operand | Description  
---|---  
`x` | floating-point or ranked tensor of floating-point values  
`min` | floating-point or ranked tensor of floating-point values  
`max` | floating-point or ranked tensor of floating-point values  
  
### Results:¶

Result | Description  
---|---  
`result` | floating-point or ranked tensor of floating-point values  
  
## `tt.descriptor_gather` (triton::DescriptorGatherOp)¶

_Gather multiple rows from a descriptor into a single tensor_

Syntax:
    
    
    operation ::= `tt.descriptor_gather` $desc `[` $x_offsets `,` $y_offset `]`
                  attr-dict `:` functional-type(operands, results)
    

The `tt.descriptor_gather` op will be lowered to NVIDIA TMA gather operations on targets that support it.

`desc_ptr` is a pointer to the TMA descriptor allocated in global memory. The descriptor block must have 1 row and the indices must be a 1D tensor. Accordingly, the result is a 2D tensor multiple rows.

Traits: `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `TT_DescriptorOpInterface`

### Operands:¶

Operand | Description  
---|---  
`desc` | Tensor descriptor type (`::mlir::triton::TensorDescType`) in Triton IR type system  
`x_offsets` | ranked tensor of 32-bit signless integer values  
`y_offset` | 32-bit signless integer  
  
### Results:¶

Result | Description  
---|---  
`result` | ranked tensor of floating-point or integer or ptr values  
  
## `tt.descriptor_load` (triton::DescriptorLoadOp)¶

_Load from descriptor_

Syntax:
    
    
    operation ::= `tt.descriptor_load` $desc `[` $indices `]`
                  oilist(
                  `cacheModifier` `=` $cache |
                  `evictionPolicy` `=` $evict
                  )
                  attr-dict `:` qualified(type($desc)) `->` type($result)
    

This operation will be lowered to Nvidia TMA load operation on targets supporting it. `desc` is a tensor descriptor object. The destination tensor type and shape must match the descriptor otherwise the result is undefined.

Traits: `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `TT_DescriptorOpInterface`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`cache`| ::mlir::triton::CacheModifierAttr| allowed 32-bit signless integer cases: 1, 2, 3, 4, 5, 6, 7  
`evict`| ::mlir::triton::EvictionPolicyAttr| allowed 32-bit signless integer cases: 1, 2, 3  
  
### Operands:¶

Operand | Description  
---|---  
`desc` | Tensor descriptor type (`::mlir::triton::TensorDescType`) in Triton IR type system  
`indices` | variadic of 32-bit signless integer  
  
### Results:¶

Result | Description  
---|---  
`result` | ranked tensor of floating-point or integer or ptr values  
  
## `tt.descriptor_reduce` (triton::DescriptorReduceOp)¶

_Performs a reducing store operation based on a descriptor_

Syntax:
    
    
    operation ::= `tt.descriptor_reduce` $kind `,` $desc `[` $indices `]` `,` $src
                  attr-dict `:` qualified(type($desc)) `,` type($src)
    

This operation will be lowered to Nvidia TMA store operation on targets supporting it. `desc` is a tensor descriptor object. The shape and types of `src` must match the descriptor otherwise the result is undefined.

Traits: `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `TT_DescriptorOpInterface`, `TT_DescriptorStoreLikeOpInterface`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`kind`| ::mlir::triton::DescriptorReduceKindAttr| allowed 32-bit signless integer cases: 1, 2, 3, 4, 5, 6, 7, 8  
  
### Operands:¶

Operand | Description  
---|---  
`desc` | Tensor descriptor type (`::mlir::triton::TensorDescType`) in Triton IR type system  
`src` | ranked tensor of floating-point or integer or ptr values  
`indices` | variadic of 32-bit signless integer  
  
## `tt.descriptor_scatter` (triton::DescriptorScatterOp)¶

_Scatter multiple rows to a descriptor from a single tensor_

Syntax:
    
    
    operation ::= `tt.descriptor_scatter` $desc `[` $x_offsets `,` $y_offset `]` `,` $src
                  attr-dict `:` type(operands)
    

The `tt.descriptor_scatter` op will be lowered to NVIDIA TMA scatter operations on targets that support it.

`desc_ptr` is a pointer to the TMA descriptor allocated in global memory. The descriptor block must have 1 row and the indices must be a 1D tensor. Accordingly, the result is a 2D tensor multiple rows.

Traits: `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `TT_DescriptorOpInterface`, `TT_DescriptorStoreLikeOpInterface`

### Operands:¶

Operand | Description  
---|---  
`desc` | Tensor descriptor type (`::mlir::triton::TensorDescType`) in Triton IR type system  
`x_offsets` | ranked tensor of 32-bit signless integer values  
`y_offset` | 32-bit signless integer  
`src` | ranked tensor of floating-point or integer or ptr values  
  
## `tt.descriptor_store` (triton::DescriptorStoreOp)¶

_Store value based on descriptor_

Syntax:
    
    
    operation ::= `tt.descriptor_store` $desc `[` $indices `]` `,` $src
                  attr-dict `:` qualified(type($desc)) `,` type($src)
    

This operation will be lowered to Nvidia TMA store operation on targets supporting it. `desc` is a tensor descriptor object. The shape and types of `src` must match the descriptor otherwise the result is undefined.

Traits: `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `TT_DescriptorOpInterface`, `TT_DescriptorStoreLikeOpInterface`

### Operands:¶

Operand | Description  
---|---  
`desc` | Tensor descriptor type (`::mlir::triton::TensorDescType`) in Triton IR type system  
`src` | ranked tensor of floating-point or integer or ptr values  
`indices` | variadic of 32-bit signless integer  
  
## `tt.dot` (triton::DotOp)¶

_Dot_

Syntax:
    
    
    operation ::= `tt.dot` $a`,` $b`,` $c (`,` `inputPrecision` `=` $inputPrecision^)? attr-dict `:`
                  type($a) `*` type($b) `->` type($d)
    

$d = matrix_multiply($a, $b) + $c. $inputPrecision describes how to exercise the TC when the inputs are f32. It can be one of: tf32, tf32x3, ieee, bf16x3, bf16x6. tf32: use TC with tf32 ops. tf32x3: implement the 3xTF32 trick. For more info see the pass in F32DotTC.cpp bf16x3: implement the 3xBF16 trick. For more info see the pass in F32DotTC.cpp bf16x6: implement the 6xBF16 trick. For more info see the pass in F32DotTC.cpp ieee: don’t use TC, implement dot in software. If the GPU does not have Tensor cores or the inputs are not f32, this flag is ignored.

Traits: `AlwaysSpeculatableImplTrait`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `DotOpInterface`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`inputPrecision`| ::mlir::triton::InputPrecisionAttr| allowed 32-bit signless integer cases: 0, 1, 2, 3, 4  
`maxNumImpreciseAcc`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
  
### Operands:¶

Operand | Description  
---|---  
`a` | ranked tensor of floating-point or integer values  
`b` | ranked tensor of floating-point or integer values  
`c` | ranked tensor of floating-point or integer values  
  
### Results:¶

Result | Description  
---|---  
`d` | ranked tensor of floating-point or integer values  
  
## `tt.dot_scaled` (triton::DotScaledOp)¶

_Dot_scaled_

Syntax:
    
    
    operation ::= `tt.dot_scaled` $a (`scale` $a_scale^)? `,` $b (`scale` $b_scale^)? `,` $c
                  `lhs` `=` $a_elem_type `rhs` `=` $b_elem_type attr-dict
                  `:` type($a) (`,` type($a_scale)^)? `*` type($b) (`,` type($b_scale)^)? `->` type($d)
    

$d = matrix_multiply(scale($a, $a_scale), scale($b, $b_scale)) + $c. Where scale(x, s) is a function that applies the scale per block following microscaling spec.

Traits: `AlwaysSpeculatableImplTrait`, `AttrSizedOperandSegments`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `DotOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`a_elem_type`| ::mlir::triton::ScaleDotElemTypeAttr| allowed 32-bit signless integer cases: 0, 1, 2, 3, 4, 5, 6  
`b_elem_type`| ::mlir::triton::ScaleDotElemTypeAttr| allowed 32-bit signless integer cases: 0, 1, 2, 3, 4, 5, 6  
`fastMath`| ::mlir::BoolAttr| bool attribute  
`lhs_k_pack`| ::mlir::BoolAttr| bool attribute  
`rhs_k_pack`| ::mlir::BoolAttr| bool attribute  
  
### Operands:¶

Operand | Description  
---|---  
`a` | ranked tensor of floating-point or 8-bit signless integer values  
`b` | ranked tensor of floating-point or 8-bit signless integer values  
`c` | ranked tensor of floating-point values  
`a_scale` | ranked tensor of floating-point or 8-bit signless integer values  
`b_scale` | ranked tensor of floating-point or 8-bit signless integer values  
  
### Results:¶

Result | Description  
---|---  
`d` | ranked tensor of floating-point values  
  
## `tt.elementwise_inline_asm` (triton::ElementwiseInlineAsmOp)¶

_Inline assembly applying an elementwise operation to a group of packed elements._

Syntax:
    
    
    operation ::= `tt.elementwise_inline_asm` $asm_string attr-dict ($args^ `:` type($args))? `->` type($result)
    

Runs an inline asm block to generate one or more tensors.

The asm block is given `packed_element` elements at a time. Exactly which elems it receives is unspecified.

Traits: `Elementwise`, `SameOperandsAndResultEncoding`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `MemoryEffectOpInterface`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`asm_string`| ::mlir::StringAttr| string attribute  
`constraints`| ::mlir::StringAttr| string attribute  
`pure`| ::mlir::BoolAttr| bool attribute  
`packed_element`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
  
### Operands:¶

Operand | Description  
---|---  
`args` | variadic of floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
### Results:¶

Result | Description  
---|---  
`result` | variadic of floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
## `tt.expand_dims` (triton::ExpandDimsOp)¶

_Expand_dims_

Syntax:
    
    
    operation ::= `tt.expand_dims` $src attr-dict `:` type($src) `->` type($result)
    

Traits: `AlwaysSpeculatableImplTrait`, `SameOperandsAndResultElementType`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`axis`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
  
### Operands:¶

Operand | Description  
---|---  
`src` | ranked tensor of floating-point or integer or ptr values  
  
### Results:¶

Result | Description  
---|---  
`result` | ranked tensor of floating-point or integer or ptr values  
  
## `tt.extern_elementwise` (triton::ExternElementwiseOp)¶

Syntax:
    
    
    operation ::= `tt.extern_elementwise` operands attr-dict `:` functional-type(operands, $result)
    

call an external function $symbol implemented in $libpath/$libname with $args return $libpath/$libname:$symbol($args…)

Traits: `Elementwise`, `SameOperandsAndResultEncoding`, `SameVariadicOperandSize`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `MemoryEffectOpInterface`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`libname`| ::mlir::StringAttr| string attribute  
`libpath`| ::mlir::StringAttr| string attribute  
`symbol`| ::mlir::StringAttr| string attribute  
`pure`| ::mlir::BoolAttr| bool attribute  
  
### Operands:¶

Operand | Description  
---|---  
`srcs` | variadic of floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
### Results:¶

Result | Description  
---|---  
`result` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
## `tt.fp_to_fp` (triton::FpToFpOp)¶

_Floating point casting for custom types_

Syntax:
    
    
    operation ::= `tt.fp_to_fp` $src attr-dict  (`,` `rounding` `=` $rounding^)? `:` type($src) `->` type($result)
    

Floating point casting for custom types (F8), and non-default rounding modes.

F8 <-> FP16, BF16, FP32, FP64

Traits: `AlwaysSpeculatableImplTrait`, `Elementwise`, `SameOperandsAndResultEncoding`, `SameOperandsAndResultShape`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`rounding`| ::mlir::triton::RoundingModeAttr| allowed 32-bit signless integer cases: 0, 1  
  
### Operands:¶

Operand | Description  
---|---  
`src` | floating-point or ranked tensor of floating-point values  
  
### Results:¶

Result | Description  
---|---  
`result` | floating-point or ranked tensor of floating-point values  
  
## `tt.gather` (triton::GatherOp)¶

_Local gather operation_

Syntax:
    
    
    operation ::= `tt.gather` $src `[` $indices `]` attr-dict `:`
                  functional-type(operands, results)
    

Gather elements from the input tensor using the indices tensor along a single specified axis. The output tensor has the same shape as the indices tensor. The input and indices tensors must have the same number of dimension, and each dimension of the indices tensor that is not the gather dimension cannot be greater than the corresponding dimension in the input tensor.

The `efficient_layout` attribute is set when the compiler has determined an optimized layout for the operation, indicating that it should not be changed.

Traits: `AlwaysSpeculatableImplTrait`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`axis`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
`efficient_layout`| ::mlir::UnitAttr| unit attribute  
  
### Operands:¶

Operand | Description  
---|---  
`src` | ranked tensor of floating-point or integer or ptr values  
`indices` | ranked tensor of integer values  
  
### Results:¶

Result | Description  
---|---  
`result` | ranked tensor of floating-point or integer or ptr values  
  
## `tt.get_num_programs` (triton::GetNumProgramsOp)¶

Syntax:
    
    
    operation ::= `tt.get_num_programs` $axis attr-dict `:` type($result)
    

Traits: `AlwaysSpeculatableImplTrait`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`axis`| ::mlir::triton::ProgramIDDimAttr| allowed 32-bit signless integer cases: 0, 1, 2  
  
### Results:¶

Result | Description  
---|---  
`result` | 32-bit signless integer  
  
## `tt.get_program_id` (triton::GetProgramIdOp)¶

Syntax:
    
    
    operation ::= `tt.get_program_id` $axis attr-dict `:` type($result)
    

Traits: `AlwaysSpeculatableImplTrait`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`axis`| ::mlir::triton::ProgramIDDimAttr| allowed 32-bit signless integer cases: 0, 1, 2  
  
### Results:¶

Result | Description  
---|---  
`result` | 32-bit signless integer  
  
## `tt.histogram` (triton::HistogramOp)¶

_Return a histogram of the inputs._

Syntax:
    
    
    operation ::= `tt.histogram` $src (`,` $mask^)? attr-dict `:` type($src) `->` type($result)
    

Return the histogram of the input tensor. The number of bins is equal to the dimension of the output tensor. Each bins has a width of 1 and bins start at 0.

Traits: `AlwaysSpeculatableImplTrait`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`src` | ranked tensor of integer values  
`mask` | 1-bit signless integer or ranked tensor of 1-bit signless integer values  
  
### Results:¶

Result | Description  
---|---  
`result` | ranked tensor of integer values  
  
## `tt.int_to_ptr` (triton::IntToPtrOp)¶

_Cast int64 to pointer_

Syntax:
    
    
    operation ::= `tt.int_to_ptr` $src attr-dict `:` type($src) `->` type($result)
    

Traits: `AlwaysSpeculatableImplTrait`, `Elementwise`, `SameOperandsAndResultEncoding`, `SameOperandsAndResultShape`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`src` | 64-bit signless integer or tensor of 64-bit signless integer values  
  
### Results:¶

Result | Description  
---|---  
`result` | ptr or ranked tensor of ptr values  
  
## `tt.join` (triton::JoinOp)¶

_Join two tensors along a new, minor dimension_

Syntax:
    
    
    operation ::= `tt.join` $lhs `,` $rhs attr-dict `:` type($lhs) `->` type($result)
    

For example, if the two input tensors are 4x8xf32, returns a tensor of shape 4x8x2xf32.

Because Triton tensors always have a power-of-two number of elements, the two input tensors must have the same shape.

Traits: `AlwaysSpeculatableImplTrait`, `SameTypeOperands`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`lhs` | ranked tensor of floating-point or integer or ptr values  
`rhs` | ranked tensor of floating-point or integer or ptr values  
  
### Results:¶

Result | Description  
---|---  
`result` | ranked tensor of floating-point or integer or ptr values  
  
## `tt.load` (triton::LoadOp)¶

_Load from a tensor of pointers or from a tensor pointer_

Syntax:
    
    
    operation ::= `tt.load` $ptr (`,` $mask^)? (`,` $other^)?
                  oilist(
                  `cacheModifier` `=` $cache |
                  `evictionPolicy` `=` $evict
                  )
                  attr-dict `:` type($ptr)
    

Traits: `AttrSizedOperandSegments`, `SameLoadStoreOperandsAndResultEncoding`, `SameLoadStoreOperandsAndResultShape`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `InferTypeOpInterface`, `MemoryEffectOpInterface`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`boundaryCheck`| ::mlir::DenseI32ArrayAttr| i32 dense array attribute  
`padding`| ::mlir::triton::PaddingOptionAttr| allowed 32-bit signless integer cases: 1, 2  
`cache`| ::mlir::triton::CacheModifierAttr| allowed 32-bit signless integer cases: 1, 2, 3, 4, 5, 6, 7  
`evict`| ::mlir::triton::EvictionPolicyAttr| allowed 32-bit signless integer cases: 1, 2, 3  
`isVolatile`| ::mlir::BoolAttr| bool attribute  
  
### Operands:¶

Operand | Description  
---|---  
`ptr` | ptr or ranked tensor of ptr values or ptr  
`mask` | 1-bit signless integer or ranked tensor of 1-bit signless integer values  
`other` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
### Results:¶

Result | Description  
---|---  
`result` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
## `tt.make_range` (triton::MakeRangeOp)¶

_Make range_

Syntax:
    
    
    operation ::= `tt.make_range` attr-dict `:` type($result)
    

Returns an 1D int32 tensor.

Values span from $start to $end (exclusive), with step = 1

Traits: `AlwaysSpeculatableImplTrait`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`start`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
`end`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
  
### Results:¶

Result | Description  
---|---  
`result` | ranked tensor of integer values  
  
## `tt.make_tensor_descriptor` (triton::MakeTensorDescOp)¶

_Make a tensor descriptor type with meta information of the parent tensor and block size_

Syntax:
    
    
    operation ::= `tt.make_tensor_descriptor` $base `,` `[` $shape `]` `,` `[` $strides `]` attr-dict `:` type($base) `,` type($result)
    

`tt.make_tensor_descriptor` takes both meta information of the parent tensor and the block size, and returns a descriptor object which can be used to load/store from the tensor in global memory.

Traits: `AlwaysSpeculatableImplTrait`, `SameVariadicOperandSize`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`padding`| ::mlir::triton::PaddingOptionAttr| allowed 32-bit signless integer cases: 1, 2  
  
### Operands:¶

Operand | Description  
---|---  
`base` | ptr  
`shape` | variadic of 32-bit signless integer  
`strides` | variadic of 64-bit signless integer  
  
### Results:¶

Result | Description  
---|---  
`result` | Tensor descriptor type (`::mlir::triton::TensorDescType`) in Triton IR type system  
  
## `tt.make_tensor_ptr` (triton::MakeTensorPtrOp)¶

_Make a tensor pointer type with meta information of the parent tensor and the block specified_

Syntax:
    
    
    operation ::= `tt.make_tensor_ptr` $base `,` `[` $shape `]` `,` `[` $strides `]` `,` `[` $offsets `]` attr-dict `:` type($result)
    

`tt.make_tensor_ptr` takes both meta information of the parent tensor and the block tensor, then it returns a pointer to the block tensor, e.g. returns a type of `tt.ptr<tensor<8x8xf16>>`.

Traits: `AlwaysSpeculatableImplTrait`, `SameVariadicOperandSize`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`order`| ::mlir::DenseI32ArrayAttr| i32 dense array attribute  
  
### Operands:¶

Operand | Description  
---|---  
`base` | ptr  
`shape` | variadic of 64-bit signless integer  
`strides` | variadic of 64-bit signless integer  
`offsets` | variadic of 32-bit signless integer  
  
### Results:¶

Result | Description  
---|---  
`result` | ptr  
  
## `tt.map_elementwise` (triton::MapElementwiseOp)¶

_Map a scalar subregion over a tensor_

Traits: `RecursiveMemoryEffects`, `SameOperandsAndResultEncoding`, `SameOperandsAndResultShape`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`pack`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
  
### Operands:¶

Operand | Description  
---|---  
`srcs` | variadic of ranked tensor of floating-point or integer or ptr values  
  
### Results:¶

Result | Description  
---|---  
`result` | variadic of ranked tensor of floating-point or integer or ptr values  
  
## `tt.map_elementwise.return` (triton::MapElementwiseReturnOp)¶

_Terminator for map elementwise operator_

Syntax:
    
    
    operation ::= `tt.map_elementwise.return` attr-dict ($result^ `:` type($result))?
    

Traits: `AlwaysSpeculatableImplTrait`, `HasParent<MapElementwiseOp>`, `ReturnLike`, `TensorSizeTrait`, `Terminator`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`, `RegionBranchTerminatorOpInterface`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`result` | variadic of any type  
  
## `tt.mulhiui` (triton::MulhiUIOp)¶

_Most significant N bits of the 2N-bit product of two integers_

Syntax:
    
    
    operation ::= `tt.mulhiui` $x `,` $y attr-dict `:` type($x)
    

Most significant N bits of the 2N-bit product of two integers.

Traits: `AlwaysSpeculatableImplTrait`, `Elementwise`, `SameOperandsAndResultType`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`x` | integer or ranked tensor of integer values  
`y` | integer or ranked tensor of integer values  
  
### Results:¶

Result | Description  
---|---  
`result` | integer or ranked tensor of integer values  
  
## `tt.precise_divf` (triton::PreciseDivFOp)¶

_Precise div for floating point types_

Syntax:
    
    
    operation ::= `tt.precise_divf` $x `,` $y attr-dict `:` type($x)
    

Precise div for floating point types.

Traits: `AlwaysSpeculatableImplTrait`, `Elementwise`, `SameOperandsAndResultType`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`x` | floating-point or ranked tensor of floating-point values  
`y` | floating-point or ranked tensor of floating-point values  
  
### Results:¶

Result | Description  
---|---  
`result` | floating-point or ranked tensor of floating-point values  
  
## `tt.precise_sqrt` (triton::PreciseSqrtOp)¶

_Precise sqrt for floating point types_

Syntax:
    
    
    operation ::= `tt.precise_sqrt` $x attr-dict `:` type($x)
    

Precise sqrt for floating point types.

Traits: `AlwaysSpeculatableImplTrait`, `Elementwise`, `SameOperandsAndResultType`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`x` | floating-point or ranked tensor of floating-point values  
  
### Results:¶

Result | Description  
---|---  
`result` | floating-point or ranked tensor of floating-point values  
  
## `tt.print` (triton::PrintOp)¶

_Device-side print, as in CUDA for debugging_

Syntax:
    
    
    operation ::= `tt.print` $prefix attr-dict (`:` $args^ `:` type($args))?
    

`tt.print` takes a literal string prefix and an arbitrary number of scalar or tensor arguments that should be printed. format are generated automatically from the arguments.

Traits: `SameVariadicOperandSize`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `MemoryEffectOpInterface (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{MemoryEffects::Write on ::mlir::triton::GlobalMemory}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`prefix`| ::mlir::StringAttr| string attribute  
`hex`| ::mlir::BoolAttr| bool attribute  
`isSigned`| ::mlir::DenseI32ArrayAttr| i32 dense array attribute  
  
### Operands:¶

Operand | Description  
---|---  
`args` | variadic of floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
## `tt.ptr_to_int` (triton::PtrToIntOp)¶

_Cast pointer to int64_

Syntax:
    
    
    operation ::= `tt.ptr_to_int` $src attr-dict `:` type($src) `->` type($result)
    

Traits: `AlwaysSpeculatableImplTrait`, `Elementwise`, `SameOperandsAndResultEncoding`, `SameOperandsAndResultShape`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`src` | ptr or ranked tensor of ptr values  
  
### Results:¶

Result | Description  
---|---  
`result` | 64-bit signless integer or tensor of 64-bit signless integer values  
  
## `tt.reduce` (triton::ReduceOp)¶

_Reduction using generic combination algorithm_

Traits: `AlwaysSpeculatableImplTrait`, `SameOperandsEncoding`, `SameOperandsShape`, `SingleBlock`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`axis`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
  
### Operands:¶

Operand | Description  
---|---  
`srcs` | variadic of ranked tensor of floating-point or integer or ptr values  
  
### Results:¶

Result | Description  
---|---  
`result` | variadic of floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
## `tt.reduce.return` (triton::ReduceReturnOp)¶

_Terminator for reduce operator_

Syntax:
    
    
    operation ::= `tt.reduce.return` $result attr-dict `:` type($result)
    

Traits: `AlwaysSpeculatableImplTrait`, `HasParent<ReduceOp>`, `ReturnLike`, `TensorSizeTrait`, `Terminator`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`, `RegionBranchTerminatorOpInterface`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`result` | variadic of any type  
  
## `tt.reshape` (triton::ReshapeOp)¶

_Reinterpret a tensor to a different shape. It may change elements order if the attribute is set._

Syntax:
    
    
    operation ::= `tt.reshape` $src (`allow_reorder` $allow_reorder^)? (`efficient_layout` $efficient_layout^)? attr-dict `:` type($src) `->` type($result)
    

reinterpret a tensor to a different shape.

If allow_reorder is set the compiler is free to change the order of elements to generate more efficient code.

If efficient_layout is set, this is a hint that the destination layout should be kept for performance reason. The compiler is still free to change it for better performance.

Traits: `AlwaysSpeculatableImplTrait`, `SameOperandsAndResultElementType`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`allow_reorder`| ::mlir::UnitAttr| unit attribute  
`efficient_layout`| ::mlir::UnitAttr| unit attribute  
  
### Operands:¶

Operand | Description  
---|---  
`src` | ranked tensor of floating-point or integer or ptr values  
  
### Results:¶

Result | Description  
---|---  
`result` | ranked tensor of floating-point or integer or ptr values  
  
## `tt.scan` (triton::ScanOp)¶

_Associative scan using generic combination algorithm_

Traits: `AlwaysSpeculatableImplTrait`, `SameOperandsAndResultEncoding`, `SameOperandsAndResultShape`, `SingleBlock`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`axis`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
`reverse`| ::mlir::BoolAttr| bool attribute  
  
### Operands:¶

Operand | Description  
---|---  
`srcs` | variadic of ranked tensor of floating-point or integer or ptr values  
  
### Results:¶

Result | Description  
---|---  
`result` | variadic of ranked tensor of floating-point or integer or ptr values  
  
## `tt.scan.return` (triton::ScanReturnOp)¶

_Terminator for scan operator_

Syntax:
    
    
    operation ::= `tt.scan.return` $result attr-dict `:` type($result)
    

Traits: `AlwaysSpeculatableImplTrait`, `HasParent<ScanOp>`, `ReturnLike`, `TensorSizeTrait`, `Terminator`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`, `RegionBranchTerminatorOpInterface`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`result` | variadic of any type  
  
## `tt.splat` (triton::SplatOp)¶

_Splat_

Syntax:
    
    
    operation ::= `tt.splat` $src attr-dict `:` type($src) `->` type($result)
    

Traits: `AlwaysSpeculatableImplTrait`, `SameOperandsAndResultElementType`, `SameOperandsAndResultEncoding`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`src` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
  
### Results:¶

Result | Description  
---|---  
`result` | ranked tensor of floating-point or integer or ptr values  
  
## `tt.split` (triton::SplitOp)¶

_Splits a tensor into two, along its last dimension_

Syntax:
    
    
    operation ::= `tt.split` $src attr-dict `:` type($src) `->` type($outLHS)
    

The input must be a tensor whose last dimension has size 2. Returns two tensors, src[…, 0] and src[…, 1].

For example, if the input shape is 4x8x2xf32, returns two tensors of shape 4x8xf32.

Traits: `AlwaysSpeculatableImplTrait`, `InferTypeOpAdaptor`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Operands:¶

Operand | Description  
---|---  
`src` | ranked tensor of floating-point or integer or ptr values  
  
### Results:¶

Result | Description  
---|---  
`outLHS` | ranked tensor of floating-point or integer or ptr values  
`outRHS` | ranked tensor of floating-point or integer or ptr values  
  
## `tt.store` (triton::StoreOp)¶

_Store by a tensor of pointers or by a tensor pointer_

Syntax:
    
    
    operation ::= `tt.store` $ptr `,` $value (`,` $mask^)?
                  oilist(`cacheModifier` `=` $cache | `evictionPolicy` `=` $evict)
                  attr-dict `:` type($ptr)
    

Traits: `SameLoadStoreOperandsEncoding`, `SameLoadStoreOperandsShape`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`boundaryCheck`| ::mlir::DenseI32ArrayAttr| i32 dense array attribute  
`cache`| ::mlir::triton::CacheModifierAttr| allowed 32-bit signless integer cases: 1, 2, 3, 4, 5, 6, 7  
`evict`| ::mlir::triton::EvictionPolicyAttr| allowed 32-bit signless integer cases: 1, 2, 3  
  
### Operands:¶

Operand | Description  
---|---  
`ptr` | ptr or ranked tensor of ptr values or ptr  
`value` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr  
`mask` | 1-bit signless integer or ranked tensor of 1-bit signless integer values  
  
## `tt.trans` (triton::TransOp)¶

_Rearrange the dimensions of a tensor_

Syntax:
    
    
    operation ::= `tt.trans` $src attr-dict `:` type($src) `->` type($result)
    

For example, given a tensor x with shape [1,2,4], transpose(x) with order=[2,0,1] rearranges the tensor to have shape [4,1,2].

Although this op is called “trans”, it implements both tl.trans() and tl.permute(). (“permute” might be a better name, but it’s called “trans” because originally it only supported 2D tensors.)

## Implementation note on encodings:¶

In the TritonGPU dialect (and probably others), an encoding is chosen for this op’s output so it’s a nop from the perspective of code generation.

For example, suppose tensor x has an encoding such that GPU thread [i,j,k] has a register containing element [i,j,k] of the tensor. Now we transpose x with order [2,1,0], i.e. we reverse the order of its dimensions. In TritonGPU, we will choose a layout for the output of the transpose so that GPU thread [i,j,k] has element [k,j,i] of transpose(x). But this is the same element it had before! All we’ve done is “rename” the element that thread [i,j,k] has.

The “real” transpose – i.e. moving data between GPU threads – occurs in convertLayout ops that appear before and/or after the operation.

We do this so that you can chain multiple data-movement ops (e.g. transpose+reshape+concat) without going to shared memory after each one.

Traits: `AlwaysSpeculatableImplTrait`, `InferTypeOpAdaptor`, `SameOperandsAndResultElementType`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`, `TransposeOpInterface`

Effects: `MemoryEffects::Effect{}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`order`| ::mlir::DenseI32ArrayAttr| i32 dense array attribute  
  
### Operands:¶

Operand | Description  
---|---  
`src` | ranked tensor of floating-point or integer or ptr values  
  
### Results:¶

Result | Description  
---|---  
`result` | ranked tensor of floating-point or integer or ptr values  
  
### `tt.unsplat` (triton::UnsplatOp)¶

_Convert a tensor with a single element to a scalar_

Syntax:
    
    
    operation ::= `tt.unsplat` $src attr-dict `:` type($src)
    

Traits: `AlwaysSpeculatableImplTrait`, `TensorSizeTrait`, `VerifyTensorLayoutsTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

#### Operands:¶

Operand | Description  
---|---  
`src` | ranked tensor of floating-point or integer or ptr values  
  
#### Results:¶

Result | Description  
---|---  
`result` | floating-point or ranked tensor of floating-point values or integer or ranked tensor of integer values or ptr or ranked tensor of ptr values or ptr

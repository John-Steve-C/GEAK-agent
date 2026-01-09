# NVGPUOps¶

## `nvg.cluster_id` (triton::nvgpu::ClusterCTAIdOp)¶

Syntax:
    
    
    operation ::= `nvg.cluster_id` attr-dict
    

Traits: `AlwaysSpeculatableImplTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Results:¶

Result | Description  
---|---  
`result` | 32-bit signless integer  
  
## `nvg.ld_acquire` (triton::nvgpu::LoadAcquireOp)¶

Syntax:
    
    
    operation ::= `nvg.ld_acquire` $sem `,` $scope `,` $addr (`,` $mask^)? attr-dict `:` functional-type($addr, $result)
    

Interfaces: `MemoryEffectOpInterface (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{MemoryEffects::Read on ::mlir::SideEffects::DefaultResource}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`sem`| ::mlir::triton::nvgpu::MemSemanticAttr| allowed 32-bit signless integer cases: 1, 2, 3, 4  
`scope`| ::mlir::triton::nvgpu::MemSyncScopeAttr| allowed 32-bit signless integer cases: 1, 2, 3  
  
### Operands:¶

Operand | Description  
---|---  
`addr` | LLVM pointer in address space 1  
`mask` | 1-bit signless integer  
  
### Results:¶

Result | Description  
---|---  
`result` | floating-point or integer  
  
## `nvg.tensor_memory_base` (triton::nvgpu::TensorMemoryBaseAddress)¶

Syntax:
    
    
    operation ::= `nvg.tensor_memory_base` attr-dict
    

Op to represent base address of tensor memory in a kernel. This is used to simplify lowering from TritonGPU to LLVM.

Traits: `AlwaysSpeculatableImplTrait`

Interfaces: `ConditionallySpeculatable`, `InferTypeOpInterface`, `NoMemoryEffect (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{}`

### Results:¶

Result | Description  
---|---  
`result` | LLVM pointer in address space 6  
  
## `nvg.wgmma` (triton::nvgpu::WGMMAOp)¶

Syntax:
    
    
    operation ::= `nvg.wgmma` $opA `,` $opB `,` $useC (`,` $opC^)? attr-dict `:` functional-type(operands, $res)
    

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`m`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
`n`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
`k`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
`eltTypeC`| ::mlir::triton::nvgpu::WGMMAEltTypeAttr| wgmma operand type, either 's8', 's32', 'e4m3', 'e5m2', 'f16', 'bf16', 'tf32', or 'f32'  
`eltTypeA`| ::mlir::triton::nvgpu::WGMMAEltTypeAttr| wgmma operand type, either 's8', 's32', 'e4m3', 'e5m2', 'f16', 'bf16', 'tf32', or 'f32'  
`eltTypeB`| ::mlir::triton::nvgpu::WGMMAEltTypeAttr| wgmma operand type, either 's8', 's32', 'e4m3', 'e5m2', 'f16', 'bf16', 'tf32', or 'f32'  
`layoutA`| ::mlir::triton::nvgpu::WGMMALayoutAttr| wgmma layout, either 'row' or 'col'  
`layoutB`| ::mlir::triton::nvgpu::WGMMALayoutAttr| wgmma layout, either 'row' or 'col'  
  
### Operands:¶

Operand | Description  
---|---  
`opA` | wgmma operand A/B type  
`opB` | wgmma operand A/B type  
`useC` | 1-bit signless integer  
`opC` | LLVM structure type  
  
### Results:¶

Result | Description  
---|---  
`res` | LLVM structure type  
  
## `nvg.wgmma_wait_group` (triton::nvgpu::WGMMAWaitGroupOp)¶

Syntax:
    
    
    operation ::= `nvg.wgmma_wait_group` $input attr-dict `:` type($input)
    

Interfaces: `InferTypeOpInterface`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`pendings`| ::mlir::IntegerAttr| 32-bit signless integer attribute  
  
### Operands:¶

Operand | Description  
---|---  
`input` | LLVM structure type  
  
### Results:¶

Result | Description  
---|---  
`output` | LLVM structure type

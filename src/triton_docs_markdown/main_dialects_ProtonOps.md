# ProtonOps¶

## `proton.record` (triton::proton::RecordOp)¶

_Record an event_

Syntax:
    
    
    operation ::= `proton.record` (`start` $isStart^):(`end`)? $name attr-dict
    

This operation annotates a region of IR where events are recorded. Events can be classified as hardware or software events. Hardware events are provided by the hardware performance counters obtained in later passes that convert Triton to target-specific IR. Software events are provided by the user or the compiler.

Example:
    
    
    proton.record start "name0"
    ...
    proton.record end "name0"
    

Scope names cannot be reused within the same function.

Interfaces: `MemoryEffectOpInterface (MemoryEffectOpInterface)`

Effects: `MemoryEffects::Effect{MemoryEffects::Read on ::mlir::SideEffects::DefaultResource, MemoryEffects::Write on ::mlir::SideEffects::DefaultResource}`

### Attributes:¶

Attribute| MLIR Type| Description  
---|---|---  
`isStart`| ::mlir::UnitAttr| unit attribute  
`name`| ::mlir::StringAttr| string attribute

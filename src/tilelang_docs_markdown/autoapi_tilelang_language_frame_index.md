# tilelang.language.frameÂ¶

Override the LetFrame to print a message when entering the frame.

## ClassesÂ¶

`FrameStack` | A stack-like container for managing TIR frame objects and their variable bindings.  
---|---  
`LetFrame` | A TIR frame for let bindings that manages variable scope and value tracking.  
  
## FunctionsÂ¶

`has_let_value`(var) | Check if a variable has a binding in the current let frame stack.  
---|---  
`get_let_value`(var) | Get the value bound to a variable in the current let frame stack.  
  
## Module ContentsÂ¶

_class _tilelang.language.frame.FrameStackÂ¶
    

A stack-like container for managing TIR frame objects and their variable bindings.

This class implements a stack data structure using a deque and maintains a mapping of variables to their values. It provides methods for stack operations and variable value lookups.

push(_item_)Â¶
    

Push an item onto the stack and update variable mapping if applicable.

Parameters:
    

**item** â The frame object to push onto the stack

pop()Â¶
    

Remove and return the top item from the stack.

Returns:
    

The top frame object from the stack

Raises:
    

**IndexError** â If the stack is empty

get_value(_var_)Â¶
    

Retrieve the value associated with a variable.

Parameters:
    

**var** â The variable to look up

Returns:
    

The value associated with the variable, or None if not found

has_value(_var_)Â¶
    

Check if a variable has an associated value.

Parameters:
    

**var** â The variable to check

Returns:
    

True if the variable has an associated value, False otherwise

Return type:
    

[bool](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

top()Â¶
    

Return the top item of the stack without removing it.

Returns:
    

The top frame object from the stack

Raises:
    

**IndexError** â If the stack is empty

__len__()Â¶
    

Returns the number of items in the stack.

__bool__()Â¶
    

Allows truthy checks on the stack object itself, e.g., âif stack: â¦â

_class _tilelang.language.frame.LetFrameÂ¶
    

Bases: `tvm.script.ir_builder.tir.frame.TIRFrame`

A TIR frame for let bindings that manages variable scope and value tracking.

This frame type extends TIRFrame to provide variable binding functionality and maintains a global stack of active bindings.

__enter__()Â¶
    

Enter the let frame scope and process buffer loads.

Returns:
    

The variable bound in this frame

Return type:
    

Var

__exit__(_ptype_ , _value_ , _trace_)Â¶
    

Exit the let frame scope and clean up the stack.

Parameters:
    

  * **ptype** â Exception type if an exception occurred

  * **value** â Exception value if an exception occurred

  * **trace** â Exception traceback if an exception occurred




_classmethod _Current()Â¶
    

Get the current (topmost) let frame.

Returns:
    

The current let frame

Return type:
    

LetFrame

Raises:
    

**IndexError** â If there are no active let frames

_static _get_value(_var_)Â¶
    

Get the value bound to a variable in any active frame.

Parameters:
    

**var** (_Var_) â The variable to look up

Returns:
    

The value bound to the variable, or None if not found

_static _has_value(_var_)Â¶
    

Check if a variable has a binding in any active frame.

Parameters:
    

**var** (_Var_) â The variable to check

Returns:
    

True if the variable has a binding, False otherwise

Return type:
    

[bool](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.language.frame.has_let_value(_var_)Â¶
    

Check if a variable has a binding in the current let frame stack.

Parameters:
    

**var** (_Var_) â The variable to check

Returns:
    

True if the variable has a binding, False otherwise

Return type:
    

[bool](../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.language.frame.get_let_value(_var_)Â¶
    

Get the value bound to a variable in the current let frame stack.

Parameters:
    

**var** (_Var_) â The variable to look up

Returns:
    

The bound value if found, None otherwise

Return type:
    

Optional[PrimExpr]

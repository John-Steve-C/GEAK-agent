# tilelang.autotuner.captureÂ¶

## ClassesÂ¶

`CaptureStack` | A simple stack implementation for capturing items in a thread-local context.  
---|---  
`AutotuneInputsCapture` |   
  
## FunctionsÂ¶

`set_autotune_inputs`(*args) | Set input tensors for auto-tuning.  
---|---  
`get_autotune_inputs`() | Get the current autotune inputs from the stack.  
  
## Module ContentsÂ¶

_class _tilelang.autotuner.capture.CaptureStackÂ¶
    

A simple stack implementation for capturing items in a thread-local context. Used to manage a stack of items (e.g., input tensors) for auto-tuning capture.

stack _ = []_Â¶
    

push(_item_)Â¶
    

Push an item onto the top of the stack.

Parameters:
    

**item** â The item to be pushed onto the stack.

pop()Â¶
    

Pop and return the top item from the stack.

Returns:
    

The item at the top of the stack.

Raises:
    

**IndexError** â If the stack is empty.

top()Â¶
    

Return the item at the top of the stack without removing it.

Returns:
    

The item at the top of the stack.

Raises:
    

**IndexError** â If the stack is empty.

size()Â¶
    

Return the number of items in the stack.

Returns:
    

The size of the stack.

Return type:
    

int

__len__()Â¶
    

Return the number of items in the stack (len operator support).

Returns:
    

The size of the stack.

Return type:
    

int

__bool__()Â¶
    

Return True if the stack is not empty, False otherwise.

Returns:
    

Whether the stack contains any items.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_class _tilelang.autotuner.capture.AutotuneInputsCapture(_tensors_)Â¶
    

Parameters:
    

**tensors** (_list_ _[__Any_ _]_)

__slots___ = 'tensors'_Â¶
    

tensorsÂ¶
    

__enter__()Â¶
    

Return type:
    

None

__exit__(_exc_type_ , _exc_val_ , _exc_tb_)Â¶
    

tilelang.autotuner.capture.set_autotune_inputs(_* args_)Â¶
    

Set input tensors for auto-tuning.

This function creates a context manager for capturing input tensors during the auto-tuning process. It supports both:

> set_autotune_inputs(a, b, c) set_autotune_inputs([a, b, c])

Parameters:
    

***args** â Either a single list/tuple of tensors, or multiple tensor arguments.

Returns:
    

A context manager for auto-tuning inputs.

Return type:
    

AutotuneInputsCapture

tilelang.autotuner.capture.get_autotune_inputs()Â¶
    

Get the current autotune inputs from the stack.

Return type:
    

list[Any] | None

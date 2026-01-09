# triton.language.static_range¶

_class _triton.language.static_range(_self_ , _arg1_ , _arg2 =None_, _step =None_)¶
    

Iterator that counts upward forever.
    
    
    @triton.jit
    def kernel(...):
        for i in tl.static_range(10):
            ...
    

Note:
    

This is a special iterator used to implement similar semantics to Python’s `range` in the context of `triton.jit` functions. In addition, it also guides the compiler to unroll the loop aggressively.

Parameters:
    

  * **arg1** – the start value.

  * **arg2** – the end value.

  * **step** – the step value.




__init__(_self_ , _arg1_ , _arg2 =None_, _step =None_)¶
    

Methods

`__init__`(self, arg1[, arg2, step]) |   
---|---  
  
Attributes

`type` |   
---|---

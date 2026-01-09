# triton.language.cat¶

triton.language.cat(_input_ , _other_ , _can_reorder =False_, __semantic =None_)¶
    

Concatenate the given blocks

Parameters:
    

  * **input** (_Tensor_) – The first input tensor.

  * **other** (_Tensor_) – The second input tensor.

  * **reorder** – Compiler hint. If true, the compiler is allowed to reorder elements while concatenating inputs. Only use if the order does not matter (e.g., result is only used in reduction ops). Current implementation of cat supports only can_reorder=True.




# triton.language.make_block_ptr¶

triton.language.make_block_ptr(_base : [tensor](triton.language.tensor.html#triton.language.tensor "triton.language.core.tensor")_, _shape_ , _strides_ , _offsets_ , _block_shape_ , _order_ , __semantic =None_)¶
    

Returns a pointer to a block in a parent tensor

Parameters:
    

  * **base** – The base pointer to the parent tensor

  * **shape** – The shape of the parent tensor

  * **strides** – The strides of the parent tensor

  * **offsets** – The offsets to the block

  * **block_shape** – The shape of the block

  * **order** – The order of the original data format




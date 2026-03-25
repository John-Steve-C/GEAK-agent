# tilelang.utils.sparseÂ¶

## AttributesÂ¶

`compress_util` |   
---|---  
  
## FunctionsÂ¶

`compress_sm90`(A, block_k, transposed) |   
---|---  
`compress_sm80`(A, transposed) |   
`compress`(A, transposed[, arch]) | Compress a tensor using the appropriate method based on the CUDA architecture.  
`randn_semi_sparse`(M, K[, dtype, device, transposed]) | Generate a random semi-sparse tensor. The generated tensor will have 2:4 sparsity along the K dimension.  
`randint_semi_sparse`(M, K, low, high[, dtype, device, ...]) | Generate a random semi-sparse integer tensor. The generated tensor will have 2:4 sparsity along the K dimension.  
`arange_semi_sparse`(M, K[, dtype, device, transposed]) | Generate a semi-sparse tensor with values from 0 to M*K-1. The generated tensor will have 2:4 sparsity along the K dimension.  
  
## Module ContentsÂ¶

tilelang.utils.sparse.compress_utilÂ¶
    

tilelang.utils.sparse.compress_sm90(_A_ , _block_k_ , _transposed_)Â¶
    

Parameters:
    

  * **A** (_torch.Tensor_)

  * **block_k** (_int_)

  * **transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

tuple[torch.Tensor, torch.Tensor]

tilelang.utils.sparse.compress_sm80(_A_ , _transposed_)Â¶
    

Parameters:
    

  * **A** (_torch.Tensor_)

  * **transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

tuple[torch.Tensor, torch.Tensor]

tilelang.utils.sparse.compress(_A_ , _transposed_ , _arch =None_, _** kwargs_)Â¶
    

Compress a tensor using the appropriate method based on the CUDA architecture.

Parameters:
    

  * **A** (_torch.Tensor_)

  * **transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **arch** (_str_ _|__None_)



Return type:
    

tuple[torch.Tensor, torch.Tensor]

tilelang.utils.sparse.randn_semi_sparse(_M_ , _K_ , _dtype =torch.float16_, _device ='cuda'_, _transposed =False_)Â¶
    

Generate a random semi-sparse tensor. The generated tensor will have 2:4 sparsity along the K dimension. :param M: Number of rows :type M: int :param K: Number of columns :type K: int :param dtype: Data type of the tensor :param device: Device to create the tensor on :param transposed: If True, returns a transposed tensor of shape (K, M) :type transposed: bool

Parameters:
    

  * **M** (_int_)

  * **K** (_int_)

  * **transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.utils.sparse.randint_semi_sparse(_M_ , _K_ , _low_ , _high_ , _dtype =torch.int32_, _device ='cuda'_, _transposed =False_)Â¶
    

Generate a random semi-sparse integer tensor. The generated tensor will have 2:4 sparsity along the K dimension. :param M: Number of rows :type M: int :param K: Number of columns :type K: int :param low: Lower bound of the random integers :type low: int :param high: Upper bound of the random integers :type high: int :param dtype: Data type of the tensor :param device: Device to create the tensor on :param transposed: If True, returns a transposed tensor of shape (K, M) :type transposed: bool

Parameters:
    

  * **M** (_int_)

  * **K** (_int_)

  * **low** (_int_)

  * **high** (_int_)

  * **transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.utils.sparse.arange_semi_sparse(_M_ , _K_ , _dtype =torch.float16_, _device ='cuda'_, _transposed =False_)Â¶
    

Generate a semi-sparse tensor with values from 0 to M*K-1. The generated tensor will have 2:4 sparsity along the K dimension. :param M: Number of rows :type M: int :param K: Number of columns :type K: int :param dtype: Data type of the tensor :param device: Device to create the tensor on :param transposed: If True, returns a transposed tensor of shape (K, M) :type transposed: bool

Parameters:
    

  * **M** (_int_)

  * **K** (_int_)

  * **transposed** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




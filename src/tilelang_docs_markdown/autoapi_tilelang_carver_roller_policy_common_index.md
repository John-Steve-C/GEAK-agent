# tilelang.carver.roller.policy.commonÂ¶

## FunctionsÂ¶

`get_all_factors`(n) |   
---|---  
`factorize`(n) |   
`coalesced_factor`(subtensor, tensor) |   
`coalesced_tensor_shape`(subtensor, tensor, transaction_size) |   
  
## Module ContentsÂ¶

tilelang.carver.roller.policy.common.get_all_factors(_n_)Â¶
    

Parameters:
    

**n** (_int_)

Return type:
    

list[int]

tilelang.carver.roller.policy.common.factorize(_n_)Â¶
    

Parameters:
    

**n** (_int_)

Return type:
    

list[int]

tilelang.carver.roller.policy.common.coalesced_factor(_subtensor_ , _tensor_)Â¶
    

Parameters:
    

  * **subtensor** (_list_ _[__int_ _]_)

  * **tensor** (_list_ _[__int_ _]_)



Return type:
    

int

tilelang.carver.roller.policy.common.coalesced_tensor_shape(_subtensor_ , _tensor_ , _transaction_size_)Â¶
    

Parameters:
    

  * **subtensor** (_list_ _[__int_ _]_)

  * **tensor** (_list_ _[__int_ _]_)

  * **transaction_size** (_int_)



Return type:
    

int

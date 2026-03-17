# tilelang.quantize.utilsÂ¶

## FunctionsÂ¶

`gen_quant4`(k, n[, groupsize]) |   
---|---  
`general_compress`(lowprecision_weight[, source_bits, ...]) |   
`interleave_weight`(qweight[, nbits, target_dtype]) | Interleave the weight to the target data type.  
  
## Module ContentsÂ¶

tilelang.quantize.utils.gen_quant4(_k_ , _n_ , _groupsize =-1_)Â¶
    

tilelang.quantize.utils.general_compress(_lowprecision_weight_ , _source_bits =4_, _storage_dtype =None_)Â¶
    

tilelang.quantize.utils.interleave_weight(_qweight_ , _nbits =4_, _target_dtype ='float16'_)Â¶
    

Interleave the weight to the target data type.

Parameters:
    

  * **qweight** (__type__) â _description_

  * **nbits** (_int_ _,__optional_) â _description_. Defaults to 4.

  * **target_dtype** (_str_ _,__optional_) â _description_. Defaults to âfloat16â.



Returns:
    

_description_

Return type:
    

_type_

Example

qweight = torch.randint(0, 127, (10, 10), dtype=torch.int8).cuda() interleave_weight(qweight, 4, âfloat16â)

# tilelang.testingÂ¶

## SubmodulesÂ¶

  * [tilelang.testing.perf_regression](perf_regression/index.html)



## AttributesÂ¶

`__all__` |   
---|---  
  
## FunctionsÂ¶

`main`() |   
---|---  
`set_random_seed`([seed]) |   
`requires_cuda_compute_version`(major_version[, ...]) | Mark a test as requiring at least a compute architecture  
`requires_cuda_compute_version_ge`(major_version[, ...]) |   
`requires_cuda_compute_version_gt`(major_version[, ...]) |   
`requires_cuda_compute_version_eq`(major_version[, ...]) |   
`requires_cuda_compute_version_lt`(major_version[, ...]) |   
`requires_cuda_compute_version_le`(major_version[, ...]) |   
  
## Package ContentsÂ¶

tilelang.testing.__all__Â¶
    

tilelang.testing.main()Â¶
    

tilelang.testing.set_random_seed(_seed =42_)Â¶
    

Parameters:
    

**seed** (_int_)

Return type:
    

None

tilelang.testing.requires_cuda_compute_version(_major_version_ , _minor_version =0_, _mode ='ge'_)Â¶
    

Mark a test as requiring at least a compute architecture

Unit test marked with this decorator will run only if the CUDA compute architecture of the GPU is at least (major_version, minor_version).

This also marks the test as requiring a cuda support.

Parameters:
    

  * **major_version** (_int_) â The major version of the (major,minor) version tuple.

  * **minor_version** (_int_) â The minor version of the (major,minor) version tuple.

  * **mode** (_str_) â The mode of the comparison. \- âgeâ: greater than or equal to \- âgtâ: greater than \- âleâ: less than or equal to \- âltâ: less than




tilelang.testing.requires_cuda_compute_version_ge(_major_version_ , _minor_version =0_)Â¶
    

tilelang.testing.requires_cuda_compute_version_gt(_major_version_ , _minor_version =0_)Â¶
    

tilelang.testing.requires_cuda_compute_version_eq(_major_version_ , _minor_version =0_)Â¶
    

tilelang.testing.requires_cuda_compute_version_lt(_major_version_ , _minor_version =0_)Â¶
    

tilelang.testing.requires_cuda_compute_version_le(_major_version_ , _minor_version =0_)Â¶
    

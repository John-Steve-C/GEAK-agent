# tilelang.carver.arch.driver.cuda_driverÂ¶

## ClassesÂ¶

`cudaDeviceAttrNames` | refer to <https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__TYPES.html#group__CUDART__TYPES_1g49e2f8c2c0bd6fe264f2fc970912e5cd>  
---|---  
  
## FunctionsÂ¶

`get_cuda_device_properties`([device_id]) |   
---|---  
`get_device_name`([device_id]) |   
`get_shared_memory_per_block`([device_id, format]) |   
`get_device_attribute`(attr[, device_id]) |   
`get_max_dynamic_shared_size_bytes`([device_id, format]) | Get the maximum dynamic shared memory size in bytes, kilobytes, or megabytes.  
`get_persisting_l2_cache_max_size`([device_id]) |   
`get_num_sms`([device_id]) | Get the number of streaming multiprocessors (SMs) on the CUDA device.  
`get_registers_per_block`([device_id]) | Get the maximum number of 32-bit registers available per block.  
  
## Module ContentsÂ¶

_class _tilelang.carver.arch.driver.cuda_driver.cudaDeviceAttrNamesÂ¶
    

refer to <https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__TYPES.html#group__CUDART__TYPES_1g49e2f8c2c0bd6fe264f2fc970912e5cd>

cudaDevAttrMaxThreadsPerBlock _: int_ _ = 1_Â¶
    

cudaDevAttrMaxRegistersPerBlock _: int_ _ = 12_Â¶
    

cudaDevAttrMaxSharedMemoryPerMultiprocessor _: int_ _ = 81_Â¶
    

cudaDevAttrMaxPersistingL2CacheSize _: int_ _ = 108_Â¶
    

tilelang.carver.arch.driver.cuda_driver.get_cuda_device_properties(_device_id =0_)Â¶
    

Parameters:
    

**device_id** (_int_)

Return type:
    

torch.cuda._CudaDeviceProperties | None

tilelang.carver.arch.driver.cuda_driver.get_device_name(_device_id =0_)Â¶
    

Parameters:
    

**device_id** (_int_)

Return type:
    

str | None

tilelang.carver.arch.driver.cuda_driver.get_shared_memory_per_block(_device_id =0_, _format ='bytes'_)Â¶
    

Parameters:
    

  * **device_id** (_int_)

  * **format** (_str_)



Return type:
    

int | None

tilelang.carver.arch.driver.cuda_driver.get_device_attribute(_attr_ , _device_id =0_)Â¶
    

Parameters:
    

  * **attr** (_int_)

  * **device_id** (_int_)



Return type:
    

int

tilelang.carver.arch.driver.cuda_driver.get_max_dynamic_shared_size_bytes(_device_id =0_, _format ='bytes'_)Â¶
    

Get the maximum dynamic shared memory size in bytes, kilobytes, or megabytes.

Parameters:
    

  * **device_id** (_int_)

  * **format** (_str_)



Return type:
    

int | None

tilelang.carver.arch.driver.cuda_driver.get_persisting_l2_cache_max_size(_device_id =0_)Â¶
    

Parameters:
    

**device_id** (_int_)

Return type:
    

int

tilelang.carver.arch.driver.cuda_driver.get_num_sms(_device_id =0_)Â¶
    

Get the number of streaming multiprocessors (SMs) on the CUDA device.

Parameters:
    

**device_id** (_int_ _,__optional_) â The CUDA device ID. Defaults to 0.

Returns:
    

The number of SMs on the device.

Return type:
    

int

Raises:
    

**RuntimeError** â If unable to get the device properties.

tilelang.carver.arch.driver.cuda_driver.get_registers_per_block(_device_id =0_)Â¶
    

Get the maximum number of 32-bit registers available per block.

Parameters:
    

**device_id** (_int_)

Return type:
    

int

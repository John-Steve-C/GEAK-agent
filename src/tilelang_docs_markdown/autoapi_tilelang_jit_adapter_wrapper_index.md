# tilelang.jit.adapter.wrapperÂ¶

## AttributesÂ¶

`PREDEF_ATTRIBUTE_SET_DYNAMIC_MEMORY` |   
---|---  
`PREDEF_ATTRIBUTE_SET_DYNAMIC_MEMORY_HIP` |   
`PREDEF_INIT_FUNC` |   
`PREDEF_HOST_FUNC` |   
`L2_PERSISTENT_MAP_CREATE_HANDLE` |   
`L2_PERSISTENT_MAP_INIT_FUNC` |   
`L2_PERSISTENT_MAP_RESET_HANDLE` |   
`TMA_DESC_INIT_FUNC` |   
`TMA_IM2COL_DESC_INIT_FUNC` |   
`KERNEL_LAUNCH_FUNC_CODE` |   
`KERNEL_CLUSTER_LAUNCH_FUNC_CODE` |   
`logger` |   
  
## ClassesÂ¶

`BaseWrapper` | Helper class that provides a standard way to create an ABC using  
---|---  
`TLCUDASourceWrapper` |   
`TLHIPSourceWrapper` | A wrapper class for the TileLang HIP backend.  
`TLCPUSourceWrapper` |   
`TLMetalSourceWrapper` |   
`TLWrapper` | A wrapper class for the TileLang backend.  
`TLPyWrapper` | A wrapper class for the TileLang backend.  
  
## Module ContentsÂ¶

tilelang.jit.adapter.wrapper.PREDEF_ATTRIBUTE_SET_DYNAMIC_MEMORY _ = Multiline-String_Â¶
    Show Value
    
    
    """
        cudaError_t result_{0} = cudaFuncSetAttribute({0}, cudaFuncAttributeMaxDynamicSharedMemorySize, {1});
        if (result_{0} != cudaSuccess) {{
            snprintf(error_buf, ERROR_BUF_SIZE, "Failed to set the allowed dynamic shared memory size to %d with error: %s", {1}, cudaGetErrorString(result_{0}));
            return -1;
        }}
    """
    

tilelang.jit.adapter.wrapper.PREDEF_ATTRIBUTE_SET_DYNAMIC_MEMORY_HIP _ = Multiline-String_Â¶
    Show Value
    
    
    """
        int device_{0} = 0;
        hipError_t dev_res_{0} = hipGetDevice(&device_{0});
        if (dev_res_{0} != hipSuccess) {{
            snprintf(error_buf, ERROR_BUF_SIZE, "Failed to get HIP device for {0}: %s", hipGetErrorString(dev_res_{0}));
            return -1;
        }}
        int max_smem_{0} = 0;
        hipError_t attr_res_{0} = hipDeviceGetAttribute(&max_smem_{0}, hipDeviceAttributeMaxSharedMemoryPerBlock, device_{0});
        if (attr_res_{0} != hipSuccess || max_smem_{0} <= 0) {{
            snprintf(error_buf, ERROR_BUF_SIZE, "Failed to query HIP max shared memory for {0}: %s", hipGetErrorString(attr_res_{0}));
            return -1;
        }}
        if ({1} > max_smem_{0}) {{
            snprintf(
                error_buf,
                ERROR_BUF_SIZE,
                "Requested dynamic shared memory %d exceeds device limit %d for {0}",
                {1},
                max_smem_{0}
            );
            return -1;
        }}
        return 0;
    """
    

tilelang.jit.adapter.wrapper.PREDEF_INIT_FUNC _ = Multiline-String_Â¶
    Show Value
    
    
    """
    #define ERROR_BUF_SIZE 1024
    static char error_buf[ERROR_BUF_SIZE];
    
    extern "C" const char* get_last_error() {{
        return error_buf;
    }}
    
    extern "C" int init() {{
        error_buf[0] = '\0';
        {0}
        return 0;
    }}
    """
    

tilelang.jit.adapter.wrapper.PREDEF_HOST_FUNC _ = Multiline-String_Â¶
    Show Value
    
    
    """
    extern "C" int call({}) {{
    {}
      return 0;
    }}
    """
    

tilelang.jit.adapter.wrapper.L2_PERSISTENT_MAP_CREATE_HANDLE _ = Multiline-String_Â¶
    Show Value
    
    
    """
      cudaStreamAttrValue stream_attribute;
      size_t init_persisting_l2_cache_size;
      cudaDeviceGetLimit(&init_persisting_l2_cache_size, cudaLimitPersistingL2CacheSize);
    """
    

tilelang.jit.adapter.wrapper.L2_PERSISTENT_MAP_INIT_FUNC _ = Multiline-String_Â¶
    Show Value
    
    
    """
      stream_attribute.accessPolicyWindow.hitRatio = {1};
      stream_attribute.accessPolicyWindow.hitProp = cudaAccessPropertyPersisting;
      stream_attribute.accessPolicyWindow.missProp = cudaAccessPropertyStreaming;
      cudaDeviceSetLimit(cudaLimitPersistingL2CacheSize, {2});
      stream_attribute.accessPolicyWindow.base_ptr = (void*)({0});
      stream_attribute.accessPolicyWindow.num_bytes = {2};
      cudaStreamSetAttribute(stream, cudaStreamAttributeAccessPolicyWindow, &stream_attribute);
    """
    

tilelang.jit.adapter.wrapper.L2_PERSISTENT_MAP_RESET_HANDLE _ = Multiline-String_Â¶
    Show Value
    
    
    """
      stream_attribute.accessPolicyWindow.num_bytes = 0;
      cudaStreamSetAttribute(stream, cudaStreamAttributeAccessPolicyWindow, &stream_attribute);
      cudaCtxResetPersistingL2Cache();
      cudaDeviceSetLimit(cudaLimitPersistingL2CacheSize, init_persisting_l2_cache_size);
    """
    

tilelang.jit.adapter.wrapper.TMA_DESC_INIT_FUNC _ = Multiline-String_Â¶
    Show Value
    
    
    """
      CUtensorMap {0};
      CUtensorMapDataType {0}_type= (CUtensorMapDataType){1};
      cuuint32_t {0}_tensorRank= {2};
      void *{0}_globalAddress= {3};
      cuuint64_t {0}_globalDim[{2}]= {{{4}}};
      cuuint64_t {0}_globalStride[{2}]= {{{5}}};
      cuuint32_t {0}_boxDim[{2}]= {{{6}}};
      cuuint32_t {0}_elementStrides[{2}]= {{{7}}};
      CUtensorMapInterleave {0}_interleave= (CUtensorMapInterleave){8};
      CUtensorMapSwizzle {0}_swizzle= (CUtensorMapSwizzle){9};
      CUtensorMapL2promotion {0}_l2Promotion= (CUtensorMapL2promotion){10};
      CUtensorMapFloatOOBfill {0}_oobFill= (CUtensorMapFloatOOBfill){11};
    
      CUresult {0}_result = CUTLASS_CUDA_DRIVER_WRAPPER_CALL(cuTensorMapEncodeTiled)(
        &{0}, {0}_type, {0}_tensorRank, {0}_globalAddress, {0}_globalDim, {0}_globalStride + 1, {0}_boxDim, {0}_elementStrides, {0}_interleave, {0}_swizzle, {0}_l2Promotion, {0}_oobFill);
    
      if ({0}_result != CUDA_SUCCESS) {{
              std::stringstream ss;
              ss << "Error: Failed to initialize the TMA descriptor {0}";
              snprintf(error_buf, ERROR_BUF_SIZE, "%s", ss.str().c_str());
              return -1;
      }}
    """
    

tilelang.jit.adapter.wrapper.TMA_IM2COL_DESC_INIT_FUNC _ = Multiline-String_Â¶
    Show Value
    
    
    """
      CUtensorMap {0};
      CUtensorMapDataType {0}_type= (CUtensorMapDataType){1};
      cuuint32_t {0}_tensorRank= {2};
      void *{0}_globalAddress= {3};
      cuuint64_t {0}_globalDim[{2}]= {{{4}}};
      cuuint64_t {0}_globalStride[{2}]= {{{5}}};
      cuuint32_t {0}_elementStrides[{2}]= {{{6}}};
      int {0}_lowerCorner[{2} - 2]= {{{7}}};
      int {0}_upperCorner[{2} - 2]= {{{8}}};
      cuuint32_t {0}_channelsPerPixel= {9};
      cuuint32_t {0}_pixelsPerColumn= {10};
      CUtensorMapInterleave {0}_interleave= (CUtensorMapInterleave){11};
      CUtensorMapSwizzle {0}_swizzle= (CUtensorMapSwizzle){12};
      CUtensorMapL2promotion {0}_l2Promotion= (CUtensorMapL2promotion){13};
      CUtensorMapFloatOOBfill {0}_oobFill= (CUtensorMapFloatOOBfill){14};
    
      CUresult {0}_result = CUTLASS_CUDA_DRIVER_WRAPPER_CALL(cuTensorMapEncodeIm2col)(
        &{0}, {0}_type, {0}_tensorRank, {0}_globalAddress, {0}_globalDim, {0}_globalStride + 1,
        {0}_lowerCorner, {0}_upperCorner, {0}_channelsPerPixel, {0}_pixelsPerColumn, {0}_elementStrides, {0}_interleave, {0}_swizzle, {0}_l2Promotion, {0}_oobFill);
    
      if ({0}_result != CUDA_SUCCESS) {{
              std::stringstream ss;
              ss << "Error: Failed to initialize the TMA descriptor {0}";
              snprintf(error_buf, ERROR_BUF_SIZE, "%s", ss.str().c_str());
              return -1;
      }}
    """
    

tilelang.jit.adapter.wrapper.KERNEL_LAUNCH_FUNC_CODE _ = Multiline-String_Â¶
    Show Value
    
    
    """
      {{
              cudaLaunchConfig_t config;
              cudaLaunchAttribute attribute[1];
              attribute[0].id = cudaLaunchAttributeProgrammaticStreamSerialization;
              attribute[0].val.programmaticStreamSerializationAllowed = 1;
              config.attrs = attribute;
              config.numAttrs = 1;
              config.stream = stream;
              config.gridDim = {0};
              config.blockDim = {1};
              config.dynamicSmemBytes = {2};
              cudaLaunchKernelEx(&config, {4}, {3});
      }}
    """
    

tilelang.jit.adapter.wrapper.KERNEL_CLUSTER_LAUNCH_FUNC_CODE _ = Multiline-String_Â¶
    Show Value
    
    
    """
      {{
              cudaLaunchConfig_t config;
              cudaLaunchAttribute attribute[2];
              attribute[0].id = cudaLaunchAttributeClusterDimension;
              attribute[0].val.clusterDim = {{{5}, {6}, {7}}};
              attribute[1].id = cudaLaunchAttributeProgrammaticStreamSerialization;
              attribute[1].val.programmaticStreamSerializationAllowed = 1;
              config.attrs = attribute;
              config.numAttrs = 2;
              config.stream = stream;
              config.gridDim = {0};
              config.blockDim = {1};
              config.dynamicSmemBytes = {2};
              cudaError_t cluster_attr_result = cudaFuncSetAttribute({4}, cudaFuncAttributeNonPortableClusterSizeAllowed, 1);
              if (cluster_attr_result != cudaSuccess) {{
                      snprintf(error_buf, ERROR_BUF_SIZE, "Failed to set cluster attribute for {4}: %s", cudaGetErrorString(cluster_attr_result));
                      return -1;
              }}
              cudaLaunchKernelEx(&config, {4}, {3});
      }}
    """
    

_class _tilelang.jit.adapter.wrapper.BaseWrapperÂ¶
    

Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

_abstract _wrap(_* args_, _** kwargs_)Â¶
    

tilelang.jit.adapter.wrapper.loggerÂ¶
    

_class _tilelang.jit.adapter.wrapper.TLCUDASourceWrapper(_scheduled_ir_module_ , _source_ , _target_ , _device_mod =None_, _host_mod =None_, _pass_configs =None_)Â¶
    

Parameters:
    

  * **scheduled_ir_module** (_tvm.IRModule_)

  * **source** (_str_)

  * **target** (_tvm.target.Target_)

  * **device_mod** (_tvm.IRModule_ _|__None_)

  * **host_mod** (_tvm.IRModule_ _|__None_)

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)




backend _ = 'tl'_Â¶
    

device_mod _: tvm.IRModule | None_ _ = None_Â¶
    

host_mod _: tvm.IRModule | None_ _ = None_Â¶
    

pass_configs _: dict[str, Any] | None_ _ = None_Â¶
    

modÂ¶
    

targetÂ¶
    

sourceÂ¶
    

function_names _: str | None_ _ = None_Â¶
    

dynamic_smem_buf _: int | None_ _ = None_Â¶
    

block_info _: list[int] | dict_ _ = [1, 1, 1]_Â¶
    

grid_info _: list[int] | dict_ _ = [1, 1, 1]_Â¶
    

tma_descriptor_args _: dict | None_ _ = None_Â¶
    

l2_persistent_map _: dict[str, dict] | None_Â¶
    

pdl_sync_map _: dict[str, int] | None_Â¶
    

srcpath _: str | None_ _ = None_Â¶
    

libpath _: str | None_ _ = None_Â¶
    

lib_code _: str | None_Â¶
    

is_tma_descriptor_arg(_arg_name_)Â¶
    

Parameters:
    

**arg_name** (_str_)

Return type:
    

[bool](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

create_dispatch_func(_code_ , _function_informations_)Â¶
    

get_declaration(_declare_kernel_code_)Â¶
    

Parameters:
    

**declare_kernel_code** (_str_)

Return type:
    

str

generate_l2_persistent_map(_function_name_)Â¶
    

Parameters:
    

**function_name** (_str_)

Return type:
    

str

generate_tma_descriptor_args(_desc_name_map_ , _desc_name_var_map_)Â¶
    

Parameters:
    

  * **desc_name_map** (_dict_ _[__str_ _,__str_ _]_)

  * **desc_name_var_map** (_dict_ _[__str_ _,__tilelang.tvm.tir.Var_ _]_)



Return type:
    

str

parse_source_information()Â¶
    

get_dynamic_symbolic_set(_prim_func_)Â¶
    

get_kernel_launch_code(_function_name_ , _grid_str_ , _block_str_ , _smem_str_ , _call_args_ , _cluster_dims_)Â¶
    

get_init_func()Â¶
    

update_lib_code(_code_)Â¶
    

Parameters:
    

**code** (_str_)

get_stream_type()Â¶
    

Return type:
    

dict[str, str]

_property _prim_funcÂ¶
    

_property _device_funcÂ¶
    

_property _host_funcÂ¶
    

_class _tilelang.jit.adapter.wrapper.TLHIPSourceWrapper(_scheduled_ir_module_ , _source_ , _target_ , _device_mod =None_, _host_mod =None_, _pass_configs =None_)Â¶
    

Bases: `TLCUDASourceWrapper`

A wrapper class for the TileLang HIP backend.

Parameters:
    

  * **scheduled_ir_module** (_tvm.IRModule_)

  * **source** (_str_)

  * **target** (_tvm.target.Target_)

  * **device_mod** (_tvm.IRModule_ _|__None_)

  * **host_mod** (_tvm.IRModule_ _|__None_)

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)




get_declaration(_declare_kernel_code_)Â¶
    

Parameters:
    

**declare_kernel_code** (_str_)

Return type:
    

str

get_kernel_launch_code(_function_name_ , _grid_str_ , _block_str_ , _smem_str_ , _call_args_ , _cluster_dims_)Â¶
    

get_init_func()Â¶
    

get_stream_type()Â¶
    

Return type:
    

dict[str, str]

_class _tilelang.jit.adapter.wrapper.TLCPUSourceWrapper(_scheduled_ir_module_ , _source_ , _target_ , _device_mod =None_, _host_mod =None_, _pass_configs =None_)Â¶
    

Parameters:
    

  * **scheduled_ir_module** (_tvm.IRModule_)

  * **source** (_str_)

  * **target** (_tvm.target.Target_)

  * **device_mod** (_tvm.IRModule_ _|__None_)

  * **host_mod** (_tvm.IRModule_ _|__None_)

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)




INIT_FUNC _ = Multiline-String_Â¶
    Show Value
    
    
    """
    #define ERROR_BUF_SIZE 1024
    static char error_buf[ERROR_BUF_SIZE];
    
    extern "C" const char* get_last_error() {
        return error_buf;
    }
    
    extern "C" int init() {
        error_buf[0] = '\0';
    
        return 0;
    }
    """
    

CALL_PREFIXÂ¶
    

backend _ = 'tl'_Â¶
    

device_mod _: tvm.IRModule | None_ _ = None_Â¶
    

host_mod _: tvm.IRModule | None_ _ = None_Â¶
    

pass_configs _: dict[str, Any] | None_ _ = None_Â¶
    

modÂ¶
    

targetÂ¶
    

sourceÂ¶
    

function_names _: str | None_ _ = None_Â¶
    

dynamic_smem_buf _: int | None_ _ = None_Â¶
    

srcpath _: str | None_ _ = None_Â¶
    

libpath _: str | None_ _ = None_Â¶
    

lib_code _: str | None_Â¶
    

create_call_func(_code_ , _function_informations_)Â¶
    

parse_source_information()Â¶
    

get_dynamic_symbolic_set(_prim_func_)Â¶
    

get_cpu_init_func()Â¶
    

update_lib_code(_code_)Â¶
    

Parameters:
    

**code** (_str_)

_property _prim_funcÂ¶
    

_class _tilelang.jit.adapter.wrapper.TLMetalSourceWrapper(_scheduled_ir_module_ , _source_ , _target_ , _device_mod =None_, _host_mod =None_, _pass_configs =None_)Â¶
    

Parameters:
    

  * **scheduled_ir_module** (_tvm.IRModule_)

  * **source** (_str_)

  * **target** (_tvm.target.Target_)

  * **device_mod** (_tvm.IRModule_ _|__None_)

  * **host_mod** (_tvm.IRModule_ _|__None_)

  * **pass_configs** (_dict_ _[__str_ _,__Any_ _]__|__None_)




modÂ¶
    

targetÂ¶
    

sourceÂ¶
    

pass_configs _ = None_Â¶
    

device_mod _ = None_Â¶
    

host_mod _ = None_Â¶
    

lib_codeÂ¶
    

update_lib_code(_code_)Â¶
    

Parameters:
    

**code** (_str_)

_class _tilelang.jit.adapter.wrapper.TLWrapper(_target_)Â¶
    

Bases: `BaseWrapper`

A wrapper class for the TileLang backend.

Parameters:
    

**target** (_tvm.target.Target_)

device_mod _: tvm.IRModule | None_ _ = None_Â¶
    

host_mod _: tvm.IRModule | None_ _ = None_Â¶
    

pass_configs _: dict[str, Any] | None_ _ = None_Â¶
    

target _: tvm.target.Target | None_ _ = None_Â¶
    

lib _: object | None_ _ = None_Â¶
    

scheduled_ir_module _ = None_Â¶
    

assign_optimized_module(_scheduled_ir_module_)Â¶
    

Parameters:
    

**scheduled_ir_module** (_tvm.IRModule_)

assign_pass_configs(_pass_configs_)Â¶
    

Parameters:
    

**pass_configs** (_dict_ _[__str_ _,__Any_ _]_)

assign_host_module(_host_mod_)Â¶
    

Parameters:
    

**host_mod** (_tvm.IRModule_)

assign_device_module(_device_mod_)Â¶
    

Parameters:
    

**device_mod** (_tvm.IRModule_)

wrap(_c_source_)Â¶
    

Parameters:
    

**c_source** (_str_)

_class _tilelang.jit.adapter.wrapper.TLPyWrapper(_target_)Â¶
    

Bases: `TLWrapper`

A wrapper class for the TileLang backend.

Parameters:
    

**target** (_tvm.target.Target_)

wrap(_py_source_)Â¶
    

Parameters:
    

**py_source** (_str_)

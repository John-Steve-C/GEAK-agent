# tilelang.autotuner.paramÂ¶

The auto-tune parameters.

## AttributesÂ¶

`BEST_CONFIG_PATH` |   
---|---  
`FUNCTION_PATH` |   
`LATENCY_PATH` |   
`DEVICE_KERNEL_PATH` |   
`HOST_KERNEL_PATH` |   
`EXECUTABLE_PATH` |   
`KERNEL_LIB_PATH` |   
`KERNEL_CUBIN_PATH` |   
`KERNEL_PY_PATH` |   
`PARAMS_PATH` |   
  
## ClassesÂ¶

`CompileArgs` | Compile arguments for the auto-tuner. Detailed description can be found in tilelang.jit.compile.  
---|---  
`ProfileArgs` | Profile arguments for the auto-tuner.  
`AutotuneResult` | Results from auto-tuning process.  
  
## Module ContentsÂ¶

tilelang.autotuner.param.BEST_CONFIG_PATH _ = 'best_config.json'_Â¶
    

tilelang.autotuner.param.FUNCTION_PATH _ = 'function.pkl'_Â¶
    

tilelang.autotuner.param.LATENCY_PATH _ = 'latency.json'_Â¶
    

tilelang.autotuner.param.DEVICE_KERNEL_PATH _ = 'device_kernel.cu'_Â¶
    

tilelang.autotuner.param.HOST_KERNEL_PATH _ = 'host_kernel.cu'_Â¶
    

tilelang.autotuner.param.EXECUTABLE_PATH _ = 'executable.so'_Â¶
    

tilelang.autotuner.param.KERNEL_LIB_PATH _ = 'kernel_lib.so'_Â¶
    

tilelang.autotuner.param.KERNEL_CUBIN_PATH _ = 'kernel.cubin'_Â¶
    

tilelang.autotuner.param.KERNEL_PY_PATH _ = 'kernel.py'_Â¶
    

tilelang.autotuner.param.PARAMS_PATH _ = 'params.pkl'_Â¶
    

_class _tilelang.autotuner.param.CompileArgsÂ¶
    

Compile arguments for the auto-tuner. Detailed description can be found in tilelang.jit.compile. .. attribute:: out_idx

> List of output tensor indices.

execution_backendÂ¶
    

Execution backend to use for kernel execution (default: âautoâ).

targetÂ¶
    

Compilation target, either as a string or a TVM Target object (default: âautoâ).

target_hostÂ¶
    

Target host for cross-compilation (default: None).

verboseÂ¶
    

Whether to enable verbose output (default: False).

pass_configsÂ¶
    

Additional keyword arguments to pass to the Compiler PassContext.

Refer to `tilelang.PassConfigKey` for supported options.
    

out_idx _: list[int] | int | None_ _ = None_Â¶
    

execution_backend _: Literal['auto', 'tvm_ffi', 'cython', 'nvrtc', 'torch']__ = 'auto'_Â¶
    

target _: Literal['auto', 'cuda', 'hip']__ = 'auto'_Â¶
    

target_host _: str | tvm.target.Target_ _ = None_Â¶
    

verbose _: [bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_ _ = False_Â¶
    

pass_configs _: dict[str, Any] | None_ _ = None_Â¶
    

compile_program(_program_)Â¶
    

Parameters:
    

**program** (_tvm.tir.PrimFunc_)

__hash__()Â¶
    

_class _tilelang.autotuner.param.ProfileArgsÂ¶
    

Profile arguments for the auto-tuner.

warmupÂ¶
    

Number of warmup iterations.

repÂ¶
    

Number of repetitions for timing.

timeoutÂ¶
    

Maximum time per configuration.

backendÂ¶
    

Profiler backend - âeventâ (CUDA events), âcuptiâ, or âcudagraphâ.

supply_typeÂ¶
    

Type of tensor supply mechanism.

ref_progÂ¶
    

Reference program for correctness validation.

supply_progÂ¶
    

Supply program for input tensors.

out_idxÂ¶
    

Union[List[int], int] = -1

supply_typeÂ¶
    

tilelang.TensorSupplyType = tilelang.TensorSupplyType.Auto

ref_progÂ¶
    

Callable = None

supply_progÂ¶
    

Callable = None

rtolÂ¶
    

float = 1e-2

atolÂ¶
    

float = 1e-2

max_mismatched_ratioÂ¶
    

float = 0.01

skip_checkÂ¶
    

bool = False

manual_check_progÂ¶
    

Callable = None

cache_input_tensorsÂ¶
    

bool = True

warmup _: int_ _ = 25_Â¶
    

rep _: int_ _ = 100_Â¶
    

timeout _: int_ _ = 30_Â¶
    

backend _: Literal['event', 'cupti', 'cudagraph']__ = 'event'_Â¶
    

supply_type _: tilelang.TensorSupplyType_Â¶
    

ref_prog _: Callable_ _ = None_Â¶
    

supply_prog _: Callable_ _ = None_Â¶
    

rtol _: float_ _ = 0.01_Â¶
    

atol _: float_ _ = 0.01_Â¶
    

max_mismatched_ratio _: float_ _ = 0.01_Â¶
    

skip_check _: [bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_ _ = False_Â¶
    

manual_check_prog _: Callable_ _ = None_Â¶
    

cache_input_tensors _: [bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_ _ = True_Â¶
    

__hash__()Â¶
    

_class _tilelang.autotuner.param.AutotuneResultÂ¶
    

Results from auto-tuning process.

latencyÂ¶
    

Best achieved execution latency.

configÂ¶
    

Configuration that produced the best result.

ref_latencyÂ¶
    

Reference implementation latency.

libcodeÂ¶
    

Generated library code.

funcÂ¶
    

Optimized function.

kernelÂ¶
    

Compiled kernel function.

latency _: float | None_ _ = None_Â¶
    

config _: dict | None_ _ = None_Â¶
    

ref_latency _: float | None_ _ = None_Â¶
    

libcode _: str | None_ _ = None_Â¶
    

func _: Callable | None_ _ = None_Â¶
    

kernel _: Callable | None_ _ = None_Â¶
    

save_to_disk(_path_ , _verbose =False_)Â¶
    

Parameters:
    

  * **path** (_pathlib.Path_)

  * **verbose** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




_classmethod _load_from_disk(_path_ , _compile_args_)Â¶
    

Parameters:
    

  * **path** (_pathlib.Path_)

  * **compile_args** (_CompileArgs_)



Return type:
    

AutotuneResult

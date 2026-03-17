# tilelang.tools.AnalyzerÂ¶

## AttributesÂ¶

`ARCH_CONFIGS` |   
---|---  
`logger` |   
  
## ClassesÂ¶

`AnalysisResult` | A data class to store the results of the analysis.  
---|---  
`Analyzer` | A class to analyze the performance of a TVM IR module.  
  
## Module ContentsÂ¶

tilelang.tools.Analyzer.ARCH_CONFIGSÂ¶
    

tilelang.tools.Analyzer.loggerÂ¶
    

_class _tilelang.tools.Analyzer.AnalysisResultÂ¶
    

A data class to store the results of the analysis. .. attribute:: total_flops

> Total floating-point operations.

total_global_bytesÂ¶
    

Total bytes transferred to/from global memory.

estimated_timeÂ¶
    

Estimated execution time (seconds).

tflopsÂ¶
    

Achieved TFLOPS (trillions of FLOPs per second).

bandwidth_GBpsÂ¶
    

Achieved memory bandwidth in GB/s.

total_flops _: int_Â¶
    

total_global_bytes _: int_Â¶
    

estimated_time _: float_Â¶
    

expected_tflops _: float_Â¶
    

expected_bandwidth_GBps _: float_Â¶
    

_class _tilelang.tools.Analyzer.Analyzer(_fn_ , _device_)Â¶
    

A class to analyze the performance of a TVM IR module. It calculates metrics such as FLOPs, memory bandwidth, and estimated execution time.

deviceÂ¶
    

total_flops _ = 0_Â¶
    

total_global_bytes _ = 0_Â¶
    

block_countsÂ¶
    

loop_stack _ = []_Â¶
    

global_buffersÂ¶
    

ir_pass()Â¶
    

Traverse and transform the IR module to extract performance-related information. :returns: The Analyzer instance. :rtype: self

calculate()Â¶
    

Calculate performance metrics based on the analysis. :returns: The calculated performance metrics. :rtype: AnalysisResult

Return type:
    

AnalysisResult

_classmethod _analysis(_fn_ , _device_)Â¶
    

Perform a full analysis of the given IR module or PrimFunc. :param fn: A TVM IRModule or PrimFunc to analyze. :param device: The target device information.

Returns:
    

The calculated performance metrics.

Return type:
    

AnalysisResult

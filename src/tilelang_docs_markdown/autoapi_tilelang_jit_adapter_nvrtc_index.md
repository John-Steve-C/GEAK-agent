# tilelang.jit.adapter.nvrtcÂ¶

NVRTC Backend for TileLang.

This module provides runtime compilation support using NVIDIAâs NVRTC API.

## SubmodulesÂ¶

  * [tilelang.jit.adapter.nvrtc.adapter](adapter/index.html)
  * [tilelang.jit.adapter.nvrtc.kernel_cache](kernel_cache/index.html)
  * [tilelang.jit.adapter.nvrtc.libgen](libgen/index.html)
  * [tilelang.jit.adapter.nvrtc.wrapper](wrapper/index.html)



## AttributesÂ¶

`is_nvrtc_available` |   
---|---  
`is_nvrtc_available` |   
  
## ClassesÂ¶

`NVRTCKernelAdapter` | Dummy NVRTCKernelAdapter that raises ImportError on instantiation.  
---|---  
  
## FunctionsÂ¶

`check_nvrtc_available`() | Check if NVRTC backend is available.  
---|---  
  
## Package ContentsÂ¶

tilelang.jit.adapter.nvrtc.is_nvrtc_available _ = False_Â¶
    

tilelang.jit.adapter.nvrtc.is_nvrtc_available _ = True_Â¶
    

tilelang.jit.adapter.nvrtc.check_nvrtc_available()Â¶
    

Check if NVRTC backend is available.

Raises:
    

**ImportError** â If cuda-python is not installed or cannot be imported

_class _tilelang.jit.adapter.nvrtc.NVRTCKernelAdapter(_* args_, _** kwargs_)Â¶
    

Dummy NVRTCKernelAdapter that raises ImportError on instantiation.

_classmethod _from_database(_* args_, _** kwargs_)Â¶
    

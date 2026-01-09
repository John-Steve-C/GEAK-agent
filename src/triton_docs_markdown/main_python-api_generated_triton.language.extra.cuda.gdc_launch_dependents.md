# triton.language.extra.cuda.gdc_launch_dependents¶  
  
triton.language.extra.cuda.gdc_launch_dependents(__semantic =None_)¶
    

This operation when launched with programmatic dependent launch signals that the next program may launch once all programs in the current kernel call this function or complete.

Repeated calls to this function have no effect past the first call, and the first call should be treated by the programmer as a hint to the runtime system to launch the next kernel.

This instruction is also safe to execute when programmatic dependent launch is disabled.

See <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#parallel-synchronization-and-communication-instructions-griddepcontrol> for more details.

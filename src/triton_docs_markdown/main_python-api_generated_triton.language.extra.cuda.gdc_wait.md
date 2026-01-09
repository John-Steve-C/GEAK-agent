# triton.language.extra.cuda.gdc_wait¶

triton.language.extra.cuda.gdc_wait(__semantic =None_)¶
    

GDC wait is a blocking instruction that waits for all instructions in a prior kernel to complete before continuing. This ensures all memory operations happening before the wait is visible to instructions after it, e.g. if the prior kernel writes to address “x” the new values will be visible in this kernel after the wait.

This instruction is also safe to execute when programmatic dependent launch is disabled.

See <https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#parallel-synchronization-and-communication-instructions-griddepcontrol> for more details.

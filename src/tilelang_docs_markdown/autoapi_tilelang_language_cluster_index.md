# tilelang.language.clusterÂ¶

## FunctionsÂ¶

`cluster_arrive_relaxed`() | Issue barrier.cluster.arrive.relaxed.aligned.  
---|---  
`cluster_arrive`() | Issue barrier.cluster.arrive.aligned.  
`cluster_wait`() | Issue barrier.cluster.wait.aligned.  
`cluster_sync`() | Issue cluster barrier arrive + wait (full synchronization).  
`block_rank_in_cluster`() | Return the 1-D rank of the calling CTA within its cluster (%%cluster_ctarank).  
  
## Module ContentsÂ¶

tilelang.language.cluster.cluster_arrive_relaxed()Â¶
    

Issue barrier.cluster.arrive.relaxed.aligned.

Return type:
    

tvm.tir.PrimExpr

tilelang.language.cluster.cluster_arrive()Â¶
    

Issue barrier.cluster.arrive.aligned.

Return type:
    

tvm.tir.PrimExpr

tilelang.language.cluster.cluster_wait()Â¶
    

Issue barrier.cluster.wait.aligned.

Return type:
    

tvm.tir.PrimExpr

tilelang.language.cluster.cluster_sync()Â¶
    

Issue cluster barrier arrive + wait (full synchronization).

Return type:
    

tvm.tir.PrimExpr

tilelang.language.cluster.block_rank_in_cluster()Â¶
    

Return the 1-D rank of the calling CTA within its cluster (%%cluster_ctarank).

Return type:
    

tvm.tir.PrimExpr

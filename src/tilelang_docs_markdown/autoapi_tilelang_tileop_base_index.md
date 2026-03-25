# tilelang.tileop.baseÂ¶

## ClassesÂ¶

`GemmWarpPolicy` | Enumeration for GEMM Warp Partitioning Policies.  
---|---  
  
## Module ContentsÂ¶

_class _tilelang.tileop.base.GemmWarpPolicyÂ¶
    

Bases: `enum.IntEnum`

Enumeration for GEMM Warp Partitioning Policies.

Square _ = 0_Â¶
    

FullRow _ = 1_Â¶
    

FullCol _ = 2_Â¶
    

is_square()Â¶
    

Check if the policy is a square partitioning.

Returns:
    

True if the policy is square, False otherwise.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_full_row()Â¶
    

Check if the policy is a full row partitioning.

Returns:
    

True if the policy is full row, False otherwise.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

is_full_col()Â¶
    

Check if the policy is a full column partitioning.

Returns:
    

True if the policy is full column, False otherwise.

Return type:
    

[bool](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_static _to_prime_factors(_num_)Â¶
    

Compute the prime factorization of a given number.

Parameters:
    

**num** (_int_) â The number to factorize.

Returns:
    

A list of prime factors of the number.

Return type:
    

list

compute_warp_partition(_M_ , _N_ , _num_warps_)Â¶
    

Compute the warp partition (m_warp, n_warp) based on the given policy.

Parameters:
    

  * **M** (_int_) â The number of rows in the GEMM workload.

  * **N** (_int_) â The number of columns in the GEMM workload.

  * **num_warps** (_int_) â The total number of warps available.



Returns:
    

A tuple (m_warp, n_warp) representing the partitioning of warps.

Return type:
    

tuple

Raises:
    

  * **ValueError** â If the policy is invalid or the partitioning fails.

  * **AssertionError** â If M or N is not divisible by the required factor for FullRow or FullCol policies.




_classmethod _from_warp_partition(_m_warp_ , _n_warp_)Â¶
    

Determine the warp policy based on the given warp partitioning.

Parameters:
    

  * **m_warp** (_int_) â Number of warps in the row dimension

  * **n_warp** (_int_) â Number of warps in the column dimension



Returns:
    

The corresponding warp policy

Return type:
    

GemmWarpPolicy

Examples
    
    
    >>> GemmWarpPolicy.from_block_row_cols(4, 1)  # All warps in rows
    GemmWarpPolicy.FullRow
    >>> GemmWarpPolicy.from_block_row_cols(1, 4)  # All warps in columns
    GemmWarpPolicy.FullCol
    >>> GemmWarpPolicy.from_block_row_cols(2, 2)  # Balanced distribution
    GemmWarpPolicy.Square
    

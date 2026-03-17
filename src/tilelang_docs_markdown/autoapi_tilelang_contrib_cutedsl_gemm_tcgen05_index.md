# tilelang.contrib.cutedsl.gemm_tcgen05Â¶

tcgen05 (SM100/Blackwell) MMA support for CuTeDSL backend.

Provides:
    

  * Tcgen05SmemDescriptor: 64-bit SMEM descriptor for tcgen05 MMA

  * initialize_tcgen05_descriptor: bitfield packing matching common.h layout

  * tcgen05mma_ss / tcgen05mma_ws_ss / tcgen05mma_ts: MMA PTX inline asm

  * tcgen05_mma_arrive: mbarrier arrive for MMA commit

  * tmem_allocate / tmem_deallocate: TMEM allocation/deallocation




## ClassesÂ¶

`Tcgen05SmemDescriptor` | 64-bit shared-memory descriptor for tcgen05 MMA (Blackwell).  
---|---  
  
## FunctionsÂ¶

`initialize_tcgen05_descriptor`(desc, start_address, ...) | Pack the tcgen05 SMEM descriptor bitfields.  
---|---  
`tcgen05mma_ss`(kind_dtype, desc_a, desc_b, tmem_c, ...) | tcgen05.mma.cta_group::1.kind::{kind} [tmem_c], desc_a, desc_b, desc_val, {masks}, p;  
`tcgen05mma_ws_ss`(kind_dtype, desc_a, desc_b, tmem_c, ...) | tcgen05.mma.ws.cta_group::1.kind::{kind} [tmem_c], desc_a, desc_b, desc_val, p, 0;  
`tcgen05mma_ts`(kind_dtype, tmem_a, desc_b, tmem_c, ...) | tcgen05.mma.cta_group::1.kind::{kind} [tmem_c], [tmem_a], desc_b, desc_val, {masks}, p;  
`tcgen05_mma_arrive`(mbar_ptr) | tcgen05.commit.cta_group::1.mbarrier::arrive::one.shared::cluster.b64 [mbar];  
`tmem_allocate`(tmem_buffer_ptr, num_cols) | tcgen05.alloc.cta_group::1.sync.aligned.shared::cta.b32 [dst], num_cols;  
`tmem_deallocate`(tmem_ptr, num_cols) | tcgen05.dealloc.cta_group::1.sync.aligned.b32 tmem_addr, num_cols;  
`tcgen05_ld_32dp32bNx`(N, pack16, tmem_start_col, ...) | Load N uint32 values from TMEM using tcgen05.ld.sync.aligned.32x32b.  
`tcgen05_ld_32dp64bNx`(N, pack16, tmem_start_col, ...) | Load from TMEM using 32dp64b pattern (2x 16x64b for lower/upper 16 rows).  
`tcgen05_ld_32dp128bNx`(N, pack16, tmem_start_col, ...) | Load from TMEM using 32dp128b pattern (2x 16x128b for lower/upper 16 rows).  
`tcgen05_ld_32dp256bNx`(N, pack16, tmem_start_col, ...) | Load from TMEM using 32dp256b pattern (2x 16x256b for lower/upper 16 rows).  
  
## Module ContentsÂ¶

_class _tilelang.contrib.cutedsl.gemm_tcgen05.Tcgen05SmemDescriptor(_desc_64 =None_)Â¶
    

64-bit shared-memory descriptor for tcgen05 MMA (Blackwell).

Mirrors tl::Tcgen05SMemDescriptor from common.h. Stored as two Int32 registers; recast to Int64 for the PTX operand.

Parameters:
    

**desc_64** (_cutlass.cute.Int64_)

descÂ¶
    

desc_i64Â¶
    

__add__(_offset_)Â¶
    

Add byte offset. Like C++ operator+, shifts offset >> 4.

tilelang.contrib.cutedsl.gemm_tcgen05.initialize_tcgen05_descriptor(_desc_ , _start_address_ , _leading_byte_offset_ , _stride_byte_offset_ , _base_offset_ , _leading_abs_ , _swizzle_mode_)Â¶
    

Pack the tcgen05 SMEM descriptor bitfields.

Matches the C++ `initialize_tcgen05_descriptor` in common.h:
    

Low 32 bits (reg32_[0]):
    

[0:14) start_address >> 4 [16:30) leading_byte_offset (already >>4 from TIR)

High 32 bits (reg32_[1]):
    

[0:14) stride_byte_offset (already >>4 from TIR) [14:16) version = 1 [17:20) base_offset & 0x7 [20:21) lbo_mode (leading_is_absolute ? 1 : 0) [29:32) layout_type (swizzle_mode & 0x7)

tilelang.contrib.cutedsl.gemm_tcgen05.tcgen05mma_ss(_kind_dtype_ , _desc_a_ , _desc_b_ , _tmem_c_ , _desc_val_ , _scale_out_ , _mask0_ , _mask1_ , _mask2_ , _mask3_)Â¶
    

tcgen05.mma.cta_group::1.kind::{kind} [tmem_c], desc_a, desc_b, desc_val, {masks}, p;

Guarded by elect_one_sync â only one thread in the warp issues the MMA. The TIR codegen also wraps calls in `if (threadIdx.x >> 5) == 0` which selects warp 0.

Parameters:
    

  * **kind_dtype** (_str_)

  * **desc_a** (_Tcgen05SmemDescriptor_)

  * **desc_b** (_Tcgen05SmemDescriptor_)

  * **tmem_c** (_int_)

  * **desc_val** (_int_)

  * **scale_out** (_int_)

  * **mask0** (_int_)

  * **mask1** (_int_)

  * **mask2** (_int_)

  * **mask3** (_int_)




tilelang.contrib.cutedsl.gemm_tcgen05.tcgen05mma_ws_ss(_kind_dtype_ , _desc_a_ , _desc_b_ , _tmem_c_ , _desc_val_ , _scale_out_)Â¶
    

tcgen05.mma.ws.cta_group::1.kind::{kind} [tmem_c], desc_a, desc_b, desc_val, p, 0;

Parameters:
    

  * **kind_dtype** (_str_)

  * **desc_a** (_Tcgen05SmemDescriptor_)

  * **desc_b** (_Tcgen05SmemDescriptor_)

  * **tmem_c** (_int_)

  * **desc_val** (_int_)

  * **scale_out** (_int_)




tilelang.contrib.cutedsl.gemm_tcgen05.tcgen05mma_ts(_kind_dtype_ , _tmem_a_ , _desc_b_ , _tmem_c_ , _desc_val_ , _scale_out_ , _mask0_ , _mask1_ , _mask2_ , _mask3_)Â¶
    

tcgen05.mma.cta_group::1.kind::{kind} [tmem_c], [tmem_a], desc_b, desc_val, {masks}, p;

Parameters:
    

  * **kind_dtype** (_str_)

  * **tmem_a** (_int_)

  * **desc_b** (_Tcgen05SmemDescriptor_)

  * **tmem_c** (_int_)

  * **desc_val** (_int_)

  * **scale_out** (_int_)

  * **mask0** (_int_)

  * **mask1** (_int_)

  * **mask2** (_int_)

  * **mask3** (_int_)




tilelang.contrib.cutedsl.gemm_tcgen05.tcgen05_mma_arrive(_mbar_ptr_)Â¶
    

tcgen05.commit.cta_group::1.mbarrier::arrive::one.shared::cluster.b64 [mbar];

Guarded by elect_one_sync â only one thread in the warp issues the commit.

Parameters:
    

**mbar_ptr** (_cutlass.cute.Pointer_)

tilelang.contrib.cutedsl.gemm_tcgen05.tmem_allocate(_tmem_buffer_ptr_ , _num_cols_)Â¶
    

tcgen05.alloc.cta_group::1.sync.aligned.shared::cta.b32 [dst], num_cols;

tmem_buffer_ptr: SMEM pointer that receives the allocated TMEM address. num_cols: number of columns to allocate.

Parameters:
    

  * **tmem_buffer_ptr** (_cutlass.cute.Pointer_)

  * **num_cols** (_int_)




tilelang.contrib.cutedsl.gemm_tcgen05.tmem_deallocate(_tmem_ptr_ , _num_cols_)Â¶
    

tcgen05.dealloc.cta_group::1.sync.aligned.b32 tmem_addr, num_cols;

tmem_ptr: SMEM pointer to the uint32 holding the TMEM address. num_cols: number of columns to deallocate.

Parameters:
    

  * **tmem_ptr** (_cutlass.cute.Pointer_)

  * **num_cols** (_int_)




tilelang.contrib.cutedsl.gemm_tcgen05.tcgen05_ld_32dp32bNx(_N_ , _pack16_ , _tmem_start_col_ , _tmem_col_offset_ , _dst_ptr_)Â¶
    

Load N uint32 values from TMEM using tcgen05.ld.sync.aligned.32x32b.

Matches tl::tcgen05_ld_32dp32bNx from copy_sm100.h. N: number of 32-bit elements to load (x-count, compile-time constant). pack16: if True, use 16-bit packing (not implemented yet). tmem_start_col: TMEM base column address. tmem_col_offset: additional column offset. dst_ptr: destination pointer (register memory).

Parameters:
    

  * **N** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)

  * **pack16** (_cutlass.cutlass_dsl.Constexpr_ _[_[_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _]_)

  * **tmem_start_col** (_int_)

  * **tmem_col_offset** (_int_)

  * **dst_ptr** (_cutlass.cute.Pointer_)




tilelang.contrib.cutedsl.gemm_tcgen05.tcgen05_ld_32dp64bNx(_N_ , _pack16_ , _tmem_start_col_ , _tmem_col_offset_ , _dst_ptr_)Â¶
    

Load from TMEM using 32dp64b pattern (2x 16x64b for lower/upper 16 rows).

Matches tl::tmem_ld_32dp64bNx from tcgen_05_ld.h. N: x-count for 16x64b instructions. Total output: 2*N i32 regs.

Parameters:
    

  * **N** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)

  * **pack16** (_cutlass.cutlass_dsl.Constexpr_ _[_[_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _]_)

  * **tmem_start_col** (_int_)

  * **tmem_col_offset** (_int_)

  * **dst_ptr** (_cutlass.cute.Pointer_)




tilelang.contrib.cutedsl.gemm_tcgen05.tcgen05_ld_32dp128bNx(_N_ , _pack16_ , _tmem_start_col_ , _tmem_col_offset_ , _dst_ptr_)Â¶
    

Load from TMEM using 32dp128b pattern (2x 16x128b for lower/upper 16 rows).

Matches tl::tmem_ld_32dp128bNx from tcgen_05_ld.h. N: x-count for 16x128b instructions. Total output: 4*N i32 regs. 16x128b.xN produces 2*N i32 regs per half.

Parameters:
    

  * **N** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)

  * **pack16** (_cutlass.cutlass_dsl.Constexpr_ _[_[_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _]_)

  * **tmem_start_col** (_int_)

  * **tmem_col_offset** (_int_)

  * **dst_ptr** (_cutlass.cute.Pointer_)




tilelang.contrib.cutedsl.gemm_tcgen05.tcgen05_ld_32dp256bNx(_N_ , _pack16_ , _tmem_start_col_ , _tmem_col_offset_ , _dst_ptr_)Â¶
    

Load from TMEM using 32dp256b pattern (2x 16x256b for lower/upper 16 rows).

Matches tl::tmem_ld_32dp256bNx from tcgen_05_ld.h. N: x-count for 16x256b instructions. Total output: 8*N i32 regs. 16x256b.xN produces 4*N i32 regs per half.

Parameters:
    

  * **N** (_cutlass.cutlass_dsl.Constexpr_ _[__int_ _]_)

  * **pack16** (_cutlass.cutlass_dsl.Constexpr_ _[_[_bool_](../../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _]_)

  * **tmem_start_col** (_int_)

  * **tmem_col_offset** (_int_)

  * **dst_ptr** (_cutlass.cute.Pointer_)




# triton.language.inline_asm_elementwise¶

triton.language.inline_asm_elementwise(_asm : str_, _constraints : str_, _args : Sequence_, _dtype : dtype | Sequence[dtype]_, _is_pure : bool_, _pack : int_, __semantic =None_)¶
    

Execute inline assembly over a tensor. Essentially, this is `map` where the function is inline assembly.

The input tensors `args` are implicitly broadcasted to the same shape.

`dtype` can be a tuple of types, in which case the output is a tuple of tensors.

Each invocation of the inline asm processes `pack` elements at a time. Exactly which set of inputs a block receives is unspecified. Input elements of size less than 4 bytes are packed into 4-byte registers.

This op does not support empty `dtype` – the inline asm must return at least one tensor, even if you don’t need it. You can work around this by returning a dummy tensor of arbitrary type; it shouldn’t cost you anything if you don’t use it.

Example using [PTX](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html) assembly:
    
    
    @triton.jit
    def kernel(A, B, C, D, BLOCK: tl.constexpr):
        a = tl.load(A + tl.arange(0, BLOCK)) # uint8 tensor
        b = tl.load(B + tl.arange(0, BLOCK)) # float32 tensor
    
        # For each (a,b) in zip(a,b), perform the following:
        # - Let ai be `a` converted to int32.
        # - Let af be `a` converted to float.
        # - Let m be the max of ai and b.
        # - Return ai and mi.
        # Do the above 4 elements at a time.
        (c, d) = tl.inline_asm_elementwise(
            asm="""
            {
                // Unpack `a` into `ai`.
                .reg .b8 tmp<4>;
                mov.b32 {tmp0, tmp1, tmp2, tmp3}, $8;
                cvt.u32.u8 $0, tmp0;
                cvt.u32.u8 $1, tmp1;
                cvt.u32.u8 $2, tmp2;
                cvt.u32.u8 $3, tmp3;
            }
            // Convert `ai` to float.
            cvt.rn.f32.s32 $4, $0;
            cvt.rn.f32.s32 $5, $1;
            cvt.rn.f32.s32 $6, $2;
            cvt.rn.f32.s32 $7, $3;
            // Take max of `ai` and `b`.
            max.f32 $4, $4, $9;
            max.f32 $5, $5, $10;
            max.f32 $6, $6, $11;
            max.f32 $7, $7, $12;
            """,
            constraints=(
                # 8 output registers, namely
                #   $0=ai0, $1=ai1, $2=ai2, $3=ai3,
                #   $4=m0,  $5=m1,  $6=m2,  $7=m3.
                "=r,=r,=r,=r,=r,=r,=r,=r,"
                # 5 input registers, namely
                #   $8=ai,
                #   $9=b0, $10=b1, $11=b2, $12=b3.
                # The four elements from `a` are all packed into one register.
                "r,r,r,r,r"),
            args=[a, b],
            dtype=(tl.int32, tl.float32),
            is_pure=True,
            pack=4,
        )
        tl.store(C + tl.arange(0, BLOCK), c)
        tl.store(D + tl.arange(0, BLOCK), d)
    

Parameters:
    

  * **asm** – assembly to run. Must match target’s assembly format.

  * **constraints** – asm constraints in [LLVM format](https://llvm.org/docs/LangRef.html#inline-asm-constraint-string)

  * **args** – the input tensors, whose values are passed to the asm block

  * **dtype** – the element type(s) of the returned tensor(s)

  * **is_pure** – if true, the compiler assumes the asm block has no side-effects

  * **pack** – the number of elements to be processed by one instance of inline assembly



Returns:
    

one tensor or a tuple of tensors of the given dtypes

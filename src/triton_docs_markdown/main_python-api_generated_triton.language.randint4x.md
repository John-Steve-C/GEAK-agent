# triton.language.randint4x¶

triton.language.randint4x(_seed_ , _offset_ , _n_rounds : constexpr = constexpr[10]_)¶
    

Given a `seed` scalar and an `offset` block, returns four blocks of random `int32`.

This is the maximally efficient entry point to Triton’s Philox pseudo-random number generator.

Parameters:
    

  * **seed** – The seed for generating random numbers.

  * **offsets** – The offsets to generate random numbers for.




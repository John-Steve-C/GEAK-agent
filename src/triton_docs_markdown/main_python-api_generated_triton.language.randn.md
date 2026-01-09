# triton.language.randn¶

triton.language.randn(_seed_ , _offset_ , _n_rounds : constexpr = constexpr[10]_)¶
    

Given a `seed` scalar and an `offset` block, returns a block of random `float32` in \\(\mathcal{N}(0, 1)\\).

Parameters:
    

  * **seed** – The seed for generating random numbers.

  * **offsets** – The offsets to generate random numbers for.




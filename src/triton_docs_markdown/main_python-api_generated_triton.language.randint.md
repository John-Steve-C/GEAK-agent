# triton.language.randint¶

triton.language.randint(_seed_ , _offset_ , _n_rounds : constexpr = constexpr[10]_)¶
    

Given a `seed` scalar and an `offset` block, returns a single block of random `int32`.

If you need multiple streams of random numbers, using randint4x is likely to be faster than calling randint 4 times.

Parameters:
    

  * **seed** – The seed for generating random numbers.

  * **offset** – The offsets to generate random numbers for.




# triton.language.max_constancy¶

triton.language.max_constancy(_input_ , _values_ , __semantic =None_)¶
    

Let the compiler know that the value first values in `input` are constant.

e.g. if `values` is [4], then each group of 4 values in `input` should all be equal, for example [0, 0, 0, 0, 1, 1, 1, 1].

# triton.language.swizzle2d¶

triton.language.swizzle2d(_i_ , _j_ , _size_i_ , _size_j_ , _size_g_)¶
    

Transforms the indices of a row-major size_i * size_j matrix into the indices of a column-major matrix for each group of size_g rows.

For example, for `size_i = size_j = 4` and `size_g = 2`, it will transform
    
    
    [[0 , 1 , 2 , 3 ],
     [4 , 5 , 6 , 7 ],
     [8 , 9 , 10, 11],
     [12, 13, 14, 15]]
    

into
    
    
    [[0, 2,  4 , 6 ],
     [1, 3,  5 , 7 ],
     [8, 10, 12, 14],
     [9, 11, 13, 15]]
    

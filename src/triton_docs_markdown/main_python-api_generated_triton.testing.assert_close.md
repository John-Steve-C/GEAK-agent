# triton.testing.assert_close¶  
  
triton.testing.assert_close(_x_ , _y_ , _atol =None_, _rtol =None_, _err_msg =''_)¶
    

Asserts that two inputs are close within a certain tolerance.

Parameters:
    

  * **x** (_scala_ _,__list_ _,__numpy.ndarray_ _, or_ _torch.Tensor_) – The first input.

  * **y** (_scala_ _,__list_ _,__numpy.ndarray_ _, or_ _torch.Tensor_) – The second input.

  * **atol** (_float_ _,__optional_) – The absolute tolerance. Default value is 1e-2.

  * **rtol** (_float_ _,__optional_) – The relative tolerance. Default value is 0.

  * **err_msg** (_str_) – The error message to use if the assertion fails.




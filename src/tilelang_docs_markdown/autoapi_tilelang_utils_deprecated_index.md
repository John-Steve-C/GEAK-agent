# tilelang.utils.deprecatedÂ¶

## FunctionsÂ¶

`deprecated_warning`(method_name, new_method_name[, ...]) | A function to indicate that a method is deprecated  
---|---  
`deprecated`(method_name, new_method_name[, ...]) | A decorator to indicate that a method is deprecated  
  
## Module ContentsÂ¶

tilelang.utils.deprecated.deprecated_warning(_method_name_ , _new_method_name_ , _phaseout_version =None_)Â¶
    

A function to indicate that a method is deprecated

Parameters:
    

  * **method_name** (_str_)

  * **new_method_name** (_str_)

  * **phaseout_version** (_str_)




tilelang.utils.deprecated.deprecated(_method_name_ , _new_method_name_ , _phaseout_version =None_)Â¶
    

A decorator to indicate that a method is deprecated

Parameters:
    

  * **method_name** (_str_) â The name of the method to deprecate

  * **new_method_name** (_str_) â The name of the new method to use instead

  * **phaseout_version** (_str_) â The version to phase out the method




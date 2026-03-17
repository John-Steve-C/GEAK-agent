# tilelang.language.dtypesÂ¶

## AttributesÂ¶

`AnyDType` |   
---|---  
`dtype_name` |   
`int_` |   
`__all__` |   
  
## ClassesÂ¶

`dtype` | Abstract base class for generic types.  
---|---  
`bool` | Abstract base class for generic types.  
  
## FunctionsÂ¶

`__dtype_call__`(self[, expr, is_size_var]) |   
---|---  
`__dtype_as_torch__`(self) | Convert TileLang dtype to PyTorch dtype.  
`__dtype_new__`(cls, value) |   
`__dtype_bytes__`(self) | Return the number of bytes for this dtype.  
`get_tvm_dtype`(value) |   
  
## Module ContentsÂ¶

_class _tilelang.language.dtypes.dtypeÂ¶
    

Bases: `Generic`[`_T`]

Abstract base class for generic types.

A generic type is typically declared by inheriting from this class parameterized with one or more type variables. For example, a generic mapping type might be defined as:
    
    
    class Mapping(Generic[KT, VT]):
        def __getitem__(self, key: KT) -> VT:
            ...
        # Etc.
    

This class can then be used as follows:
    
    
    def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
        try:
            return mapping[key]
        except KeyError:
            return default
    

_property _bits _: int_Â¶
    

Return type:
    

int

_property _bytes _: int_Â¶
    

Return type:
    

int

as_torch()Â¶
    

Return type:
    

torch.dtype

tilelang.language.dtypes.AnyDTypeÂ¶
    

tilelang.language.dtypes.dtype_name _ = 'float8_e4m3fn'_Â¶
    

tilelang.language.dtypes.int_Â¶
    

tilelang.language.dtypes.__dtype_call__(_self_ , _expr =None_, _is_size_var =False_)Â¶
    

Parameters:
    

  * **self** (_dtype_)

  * **is_size_var** (_bool_)



Return type:
    

tvm.tir.Var

tilelang.language.dtypes.__dtype_as_torch__(_self_)Â¶
    

Convert TileLang dtype to PyTorch dtype.

Parameters:
    

**self** (_dtype_)

Return type:
    

torch.dtype

tilelang.language.dtypes.__dtype_new__(_cls_ , _value_)Â¶
    

Parameters:
    

**value** (_AnyDType_)

Return type:
    

dtype

tilelang.language.dtypes.__dtype_bytes__(_self_)Â¶
    

Return the number of bytes for this dtype.

Parameters:
    

**self** (_dtype_)

Return type:
    

int

tilelang.language.dtypes.get_tvm_dtype(_value_)Â¶
    

Parameters:
    

**value** (_AnyDType_)

Return type:
    

dtype

_class _tilelang.language.dtypes.boolÂ¶
    

Bases: `dtype`

Abstract base class for generic types.

A generic type is typically declared by inheriting from this class parameterized with one or more type variables. For example, a generic mapping type might be defined as:
    
    
    class Mapping(Generic[KT, VT]):
        def __getitem__(self, key: KT) -> VT:
            ...
        # Etc.
    

This class can then be used as follows:
    
    
    def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
        try:
            return mapping[key]
        except KeyError:
            return default
    

tilelang.language.dtypes.__all__Â¶
    

# tilelang.language.eager.builderÂ¶

## AttributesÂ¶

`logger` |   
---|---  
`thread_local_storage` |   
`ContinueOrBreak` |   
`AnyFrame` |   
`TIR_CONTROL_FRAME` |   
`TIR_VAR_SCOPE_FRAME` |   
`EagerJITStage` |   
  
## ClassesÂ¶

`Frame` | Frame are virtual context managers used in frontend only  
---|---  
`MacroFrame` | Frame are virtual context managers used in frontend only  
`ExitedMacroFrame` | Frame are virtual context managers used in frontend only  
`BoolOpFrame` | Frame are virtual context managers used in frontend only  
`ContinueFrame` | Frame are virtual context managers used in frontend only  
`BreakFrame` | Frame are virtual context managers used in frontend only  
`SerialForWithStep` |   
`OutTensor` |   
`Ref` |   
`UnrollForWithStep` |   
`Builder` |   
`PrimFunc` | Abstract base class for generic types.  
`Macro` | Abstract base class for generic types.  
`TirTemplate` | Template for generating TIR PrimFunc with dynamic shape substitution.  
`JITFunc` | Internal wrapper for JIT-compiled functions.  
  
## FunctionsÂ¶

`unwrap_expr`(expr) | unwrap expr and convert it into PrimExpr like  
---|---  
`unwrap_cond`(expr) | unwrap expr and convert to bool condition  
`is_var`(v) |   
`macro`([func]) | Decorator that converts a Python function into a TileLang macro.  
`get_type_hints`(func) |   
`const`(name[, dtype]) | Declare constexpr variables for dynamic tensor dimensions (eager mode only).  
`substitute_primfunc`(prim_func, vmap) |   
`prim_func`([func, eager_jit]) |   
  
## Module ContentsÂ¶

tilelang.language.eager.builder.loggerÂ¶
    

tilelang.language.eager.builder.unwrap_expr(_expr_)Â¶
    

unwrap expr and convert it into PrimExpr like

Return type:
    

tvm.tir.expr.PrimExpr | int | float

tilelang.language.eager.builder.unwrap_cond(_expr_)Â¶
    

unwrap expr and convert to bool condition

tilelang.language.eager.builder.thread_local_storageÂ¶
    

_class _tilelang.language.eager.builder.FrameÂ¶
    

Frame are virtual context managers used in frontend only They do not have any runtime representation in the generated TIR.

__enter__()Â¶
    

__exit__(_exc_type_ , _exc_value_ , _traceback_)Â¶
    

_class _tilelang.language.eager.builder.MacroFrameÂ¶
    

Bases: `Frame`

Frame are virtual context managers used in frontend only They do not have any runtime representation in the generated TIR.

_class _tilelang.language.eager.builder.ExitedMacroFrameÂ¶
    

Bases: `Frame`

Frame are virtual context managers used in frontend only They do not have any runtime representation in the generated TIR.

_class _tilelang.language.eager.builder.BoolOpFrameÂ¶
    

Bases: `Frame`

Frame are virtual context managers used in frontend only They do not have any runtime representation in the generated TIR.

_class _tilelang.language.eager.builder.ContinueFrameÂ¶
    

Bases: `Frame`

Frame are virtual context managers used in frontend only They do not have any runtime representation in the generated TIR.

_class _tilelang.language.eager.builder.BreakFrameÂ¶
    

Bases: `Frame`

Frame are virtual context managers used in frontend only They do not have any runtime representation in the generated TIR.

_class _tilelang.language.eager.builder.SerialForWithStepÂ¶
    

start _: tvm.tir.expr.PrimExpr_Â¶
    

stop _: tvm.tir.expr.PrimExpr_Â¶
    

step _: tvm.tir.expr.PrimExpr_Â¶
    

annotations _: dict[str, Any] | None_ _ = None_Â¶
    

_class _tilelang.language.eager.builder.OutTensorÂ¶
    

shape _: collections.abc.Sequence[tvm.tir.expr.PrimExpr]_Â¶
    

dtype _: [tilelang.language.dtypes.dtype](../../dtypes/index.html#tilelang.language.dtypes.dtype "tilelang.language.dtypes.dtype")_Â¶
    

_property _stridesÂ¶
    

_class _tilelang.language.eager.builder.RefÂ¶
    

bufload _: tvm.tir.expr.BufferLoad_Â¶
    

_property _bufferÂ¶
    

store(_value_)Â¶
    

load()Â¶
    

_class _tilelang.language.eager.builder.UnrollForWithStepÂ¶
    

Bases: `SerialForWithStep`

tilelang.language.eager.builder.ContinueOrBreakÂ¶
    

tilelang.language.eager.builder.AnyFrameÂ¶
    

tilelang.language.eager.builder.TIR_CONTROL_FRAMEÂ¶
    

tilelang.language.eager.builder.TIR_VAR_SCOPE_FRAMEÂ¶
    

tilelang.language.eager.builder.is_var(_v_)Â¶
    

Parameters:
    

**v** (_Any_)

Return type:
    

[bool](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.language.eager.builder.EagerJITStageÂ¶
    

_class _tilelang.language.eager.builder.BuilderÂ¶
    

Bases: [`tilelang.language.eager.ast.BaseBuilder`](../ast/index.html#tilelang.language.eager.ast.BaseBuilder "tilelang.language.eager.ast.BaseBuilder")

frames _: list[AnyFrame]__ = []_Â¶
    

ir_builderÂ¶
    

name_inside_frame _: dict[str, AnyFrame]_Â¶
    

macro_arg_annotÂ¶
    

out_idx _ = []_Â¶
    

out_tensor_cnt _ = 0_Â¶
    

constexpr_varÂ¶
    

eager_jit _: EagerJITStage_ _ = 'none'_Â¶
    

eager_jit_subs _: dict[str, tvm.tir.expr.PrimExpr]_Â¶
    

current_file _ = '<unknown>'_Â¶
    

current_line _ = 0_Â¶
    

current_macro_name _ = '<unknown-macro>'_Â¶
    

macro_fileline_stack _: list[tuple[str, int, str]]__ = []_Â¶
    

_classmethod _current()Â¶
    

Return type:
    

Self

prim_func(_name_)Â¶
    

macro(_name =None_, _annotations =None_)Â¶
    

get()Â¶
    

Return type:
    

PrimFunc

find_frame_idx(_frame_ , _start =0_)Â¶
    

Parameters:
    

**frame** (_type_ _|__tuple_ _[__type_ _,__Ellipsis_ _]_)

Return type:
    

int | None

enter_frame(_frame_)Â¶
    

Parameters:
    

**frame** (_contextlib.AbstractContextManager_ _[__Any_ _]_)

check_continue_break()Â¶
    

with_frame(_frame_)Â¶
    

Parameters:
    

**frame** (_contextlib.AbstractContextManager_ _[__Any_ _]__|__None_)

ctx_if(_cond_)Â¶
    

ctx_then(_val_)Â¶
    

ctx_else(_val_)Â¶
    

eval(_val_)Â¶
    

Parameters:
    

**val** (_Any_)

ctx_for(_it_)Â¶
    

ctx_continue()Â¶
    

ctx_break()Â¶
    

ctx_while(_cond_)Â¶
    

bind(_name_ , _value_ , _annot =BaseBuilder.empty_)Â¶
    

unwrap_value(_value_)Â¶
    

Unwrap some tilelang objects to get their inner value

bind_immutable(_name_ , _value_)Â¶
    

Bind an immutable tilelang objects. The immutability means the result is usually not changed or re-assigned in a python block.

assign_slice(_lval_ , _sl_ , _value_ , _annot =BaseBuilder.empty_)Â¶
    

Parameters:
    

  * **lval** (_Any_)

  * **sl** (_slice_)

  * **value** (_Any_)




aug_assign(_op_ , _target_ , _aug_value_ , _name =None_)Â¶
    

Parameters:
    

**name** (_str_ _|__None_)

aug_assign_slice(_op_ , _target_ , _sl_ , _aug_value_)Â¶
    

boolop(_op_ , _left_ , _right =None_)Â¶
    

ifexp(_cond_ , _then_ , _otherwise_)Â¶
    

ret(_value =None_)Â¶
    

ctx_with(_ctx_)Â¶
    

assert_expr(_cond_ , _msg =None_)Â¶
    

rval(_name_ , _value_)Â¶
    

Parameters:
    

  * **name** (_str_)

  * **value** (_Any_)



Return type:
    

Any

macro_arg(_name_ , _value_)Â¶
    

prim_func_arg(_name_ , _value_)Â¶
    

arg(_name_ , _value_)Â¶
    

override(_name_)Â¶
    

Parameters:
    

**name** (_str_)

constexpr(_name_ , _dtype ='int32'_)Â¶
    

Parameters:
    

  * **name** (_str_)

  * **dtype** (_str_)



Return type:
    

tvm.tir.expr.Var

set_fileline(_filename_ , _lineno_ , _name_)Â¶
    

Parameters:
    

  * **filename** (_str_)

  * **lineno** (_int_)

  * **name** (_str_)




get_fileline_stack(_stacklevel =1_)Â¶
    

skip_kernel_ctx()Â¶
    

_class _tilelang.language.eager.builder.PrimFuncÂ¶
    

Bases: `Generic`[`_P`, `_T`], `tvm.tir.PrimFunc`

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
    

params _: list[tvm.tir.Var | tvm.tir.Buffer]_Â¶
    

body _: tvm.tir.Stmt_Â¶
    

ret_type _: tvm.ir.Type_Â¶
    

buffer_map _: tvm_ffi.container.Map[tvm.tir.Var, tvm.tir.Buffer]_Â¶
    

attrs _: tvm.Attrs | None_Â¶
    

span _: tvm.ir.base.Span | None_Â¶
    

ir_gen _: [tilelang.language.eager.ast.IRGenerator](../ast/index.html#tilelang.language.eager.ast.IRGenerator "tilelang.language.eager.ast.IRGenerator")[_P, _T] | None_Â¶
    

orig_func _: Callable[_P, _T] | None_Â¶
    

out_idx_override _: list[int] | None_Â¶
    

_class _tilelang.language.eager.builder.MacroÂ¶
    

Bases: `Generic`[`_P`, `_T`]

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
    

name _: str_Â¶
    

orig_func _: Callable[_P, _T]_Â¶
    

ir_gen _: [tilelang.language.eager.ast.IRGenerator](../ast/index.html#tilelang.language.eager.ast.IRGenerator "tilelang.language.eager.ast.IRGenerator")[_P, _T]_Â¶
    

annotations _: dict[str, Any]_Â¶
    

_property _source _: str_Â¶
    

Return type:
    

str

__call__(_* args_, _** kwargs_)Â¶
    

Parameters:
    

  * **args** (__P_)

  * **kwargs** (__P_)



Return type:
    

_T

__hash__()Â¶
    

__eq__(_other_)Â¶
    

tilelang.language.eager.builder.macro(_func =None_)Â¶
    

Decorator that converts a Python function into a TileLang macro. TileLang macro is very similar to PrimFunc, it can be used in prim_func or another macro. :param func: The Python function to be converted into a macro. This function will be analyzed

> and transformed into an IR generation function. The function can take any parameters (_P) and return any type (_T).

Returns:
    

  * _Macro[_P, _T]_ â A Macro object that wraps the original function with IR generation capabilities. The returned Macro preserves the original functionâs signature (parameters _P and return type _T) while adding metaprogramming capabilities.

  * _Example_

  * _âââ_ â >>> @macro â¦ def my_macro(x: T.int32) -> T.int32: â¦ return x ** 2 >>> @prim_func â¦ def my_func(A: T.Tensor((10,), T.int32), B: T.Tensor((10,), T.int32)): â¦ with T.Kernel(1) as _: â¦ for i in T.serial(10): â¦ B[i] = my_macro(A[i])




Parameters:
    

**func** (_Callable_ _[___P_ _,___T_ _]_)

Return type:
    

Macro[_P, _T]

See also

`Macro`
    

The class that wraps macro functions

`mutate`
    

The function that transforms Python code into IR generators

tilelang.language.eager.builder.get_type_hints(_func_)Â¶
    

tilelang.language.eager.builder.const(_name_ , _dtype ='int32'_)Â¶
    

Declare constexpr variables for dynamic tensor dimensions (eager mode only).

In eager mode, use T.const() to declare shape dimensions that will be inferred from actual tensor arguments at runtime.

Example:
    
    
    @tilelang.jit
    def kernel(A, B):
        M, N = T.const("M, N")
        A: T.Tensor[[M, N], T.float32]
        ...
    

Parameters:
    

  * **name** (_str_)

  * **dtype** (_str_)



Return type:
    

tvm.tir.expr.Var | tuple[tvm.tir.expr.Var, Ellipsis]

_class _tilelang.language.eager.builder.TirTemplateÂ¶
    

Bases: `Generic`[`_P`, `_T`]

Template for generating TIR PrimFunc with dynamic shape substitution.

For lazy-style functions, the PrimFunc is used directly without substitution. For eager-style functions, constexpr variables are substituted based on actual tensor shapes at runtime.

name _: str_Â¶
    

prim_func _: PrimFunc[_P, _T]_Â¶
    

matcher _: dict[tvm.tir.expr.Var, tuple[tvm.tir.Var, str, int, str]] | None_ _ = None_Â¶
    

constexprs _: set[tvm.tir.expr.Var]__ = None_Â¶
    

is_lazy_style _: [bool](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_ _ = False_Â¶
    

ir_gen _: [tilelang.language.eager.ast.IRGenerator](../ast/index.html#tilelang.language.eager.ast.IRGenerator "tilelang.language.eager.ast.IRGenerator")[_P, _T] | None_ _ = None_Â¶
    

_classmethod _create(_name_ , _prim_func_ , _constexpr_ , _ir_gen =None_)Â¶
    

Parameters:
    

  * **name** (_str_)

  * **prim_func** (_PrimFunc_ _[___P_ _,___T_ _]_)

  * **constexpr** (_set_ _[__tvm.tir.expr.Var_ _]_)

  * **ir_gen** ([_tilelang.language.eager.ast.IRGenerator_](../ast/index.html#tilelang.language.eager.ast.IRGenerator "tilelang.language.eager.ast.IRGenerator") _[___P_ _,___T_ _]__|__None_)



Return type:
    

TirTemplate[_P, _T]

_classmethod _from_lazy_style(_name_ , _prim_func_)Â¶
    

Create template from lazy-style function that returns PrimFunc directly.

Parameters:
    

  * **name** (_str_)

  * **prim_func** (_PrimFunc_ _[___P_ _,___T_ _]_)



Return type:
    

TirTemplate[_P, _T]

get_tir(_tensor_args_ , _given_tensor_args_ , _kwargs_)Â¶
    

_class _tilelang.language.eager.builder.JITFuncÂ¶
    

Bases: `Generic`[`_P`, `_T`]

Internal wrapper for JIT-compiled functions.

This class handles both lazy and eager execution styles:

  * **lazy style** : Function explicitly returns a PrimFunc. The original function is called directly to obtain the TIR.

  * **eager style** : Function uses the DSL builder pattern with tensor type annotations. The TIR is constructed by tracing the function body through the Builder.




The style is determined by _is_lazy_style() which checks if calling the original function returns a PrimFunc directly.

orig_func _: Callable[_P, _T]_Â¶
    

arg_names _: list[str]_Â¶
    

tensor_args _: dict[str, tvm.tir.Buffer | tvm.tir.expr.Var]_Â¶
    

tensor_args_defaults _: dict[str, Any]_Â¶
    

ir_gen _: [tilelang.language.eager.ast.IRGenerator](../ast/index.html#tilelang.language.eager.ast.IRGenerator "tilelang.language.eager.ast.IRGenerator")[_P, _T]_Â¶
    

mode _: Literal['auto', 'lazy', 'eager']__ = 'auto'_Â¶
    

__post_init__()Â¶
    

parse_args(_* args_, _** kwargs_)Â¶
    

Parse arguments and return cache key and tensor args.

get_tir(_* args_, _** kwargs_)Â¶
    

__call__(_* args_, _** kwargs_)Â¶
    

set_mode(_mode_)Â¶
    

Set the JIT execution mode (internal use only).

Parameters:
    

**mode** (_Literal_ _[__'lazy'__,__'eager'__]_)

__getattr__(_name_)Â¶
    

tilelang.language.eager.builder.substitute_primfunc(_prim_func_ , _vmap_)Â¶
    

tilelang.language.eager.builder.prim_func(_func =None_, _*_ , _eager_jit =False_)Â¶
    

Parameters:
    

  * **func** (_Callable_ _[___P_ _,___T_ _]_)

  * **eager_jit** ([_bool_](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

PrimFunc[_P, _T] | JITFunc[_P, _T]

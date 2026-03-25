# tilelang.language.eager.astÂ¶

## AttributesÂ¶

`Operator` |   
---|---  
`BoolOp` |   
  
## ClassesÂ¶

`QuoteVisitor` | A `NodeVisitor` subclass that walks the abstract syntax tree and  
---|---  
`BaseBuilder` |   
`DSLMutator` | A `NodeVisitor` subclass that walks the abstract syntax tree and  
`SpanAttacher` | A `NodeVisitor` subclass that walks the abstract syntax tree and  
`IRGenerator` | Abstract base class for generic types.  
  
## FunctionsÂ¶

`ast_has_span`(ast) |   
---|---  
`ast_get_span`(ast) |   
`ast_set_span`(ast, span) |   
`quote`(expr, *[, passes, span]) |   
`quote1`(expr, *[, passes, span]) |   
`quote_expr`(expr, **kws) |   
`get_operator_name`(operator) |   
`get_boolop_name`(boolop) |   
`eval_op`(op, left, right) |   
`eval_aug_assign`(op, left, sl, right) |   
`has_internal_prim_func`(func) |   
`mutate`(func) | Transform a Python function into an IR (Intermediate Representation) generator.  
  
## Module ContentsÂ¶

tilelang.language.eager.ast.ast_has_span(_ast_)Â¶
    

Parameters:
    

**ast** (_ast_has_span.ast_)

Return type:
    

[bool](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.language.eager.ast.ast_get_span(_ast_)Â¶
    

Parameters:
    

**ast** (_ast_get_span.ast_)

Return type:
    

tuple[int, int, int, int]

tilelang.language.eager.ast.ast_set_span(_ast_ , _span_)Â¶
    

Parameters:
    

  * **ast** (_ast_set_span.ast_)

  * **span** (_tuple_ _[__int_ _,__int_ _,__int_ _,__int_ _]_)




_class _tilelang.language.eager.ast.QuoteVisitor(_names_ , _passes =None_, _span =None_)Â¶
    

Bases: `ast.NodeTransformer`

A `NodeVisitor` subclass that walks the abstract syntax tree and allows modification of nodes.

The NodeTransformer will walk the AST and use the return value of the visitor methods to replace or remove the old node. If the return value of the visitor method is `None`, the node will be removed from its location, otherwise it is replaced with the return value. The return value may be the original node in which case no replacement takes place.

Here is an example transformer that rewrites all occurrences of name lookups (`foo`) to `data['foo']`:
    
    
    class RewriteName(NodeTransformer):
    
        def visit_Name(self, node):
            return Subscript(
                value=Name(id='data', ctx=Load()),
                slice=Constant(value=node.id),
                ctx=node.ctx
            )
    

Keep in mind that if the node youâre operating on has child nodes you must either transform the child nodes yourself or call the `generic_visit()` method for the node first.

For nodes that were part of a collection of statements (that applies to all statement nodes), the visitor may also return a list of nodes rather than just a single node.

Usually you use the transformer like this:
    
    
    node = YourTransformer().visit(node)
    

Parameters:
    

  * **names** (_dict_ _[__str_ _,__ast.AST_ _]_)

  * **passes** (_list_ _[__Any_ _]__|__None_)




namesÂ¶
    

passes _ = []_Â¶
    

span _ = None_Â¶
    

generic_visit(_node_)Â¶
    

Called if no explicit visitor function exists for a node.

Parameters:
    

**node** (_ast.AST_)

visit_Name(_node_)Â¶
    

Parameters:
    

**node** (_ast.Name_)

Return type:
    

Any

visit_Pass(_node_)Â¶
    

Parameters:
    

**node** (_ast.Pass_)

Return type:
    

Any

tilelang.language.eager.ast.quote(_expr_ , _*_ , _passes =None_, _span =None_, _** kws_)Â¶
    

Parameters:
    

  * **expr** (_str_)

  * **passes** (_list_ _[__Any_ _]__|__None_)



Return type:
    

list[ast.AST]

tilelang.language.eager.ast.quote1(_expr_ , _*_ , _passes =None_, _span =None_, _** kws_)Â¶
    

Parameters:
    

  * **expr** (_str_)

  * **passes** (_list_ _[__Any_ _]__|__None_)



Return type:
    

ast.AST

tilelang.language.eager.ast.quote_expr(_expr_ , _** kws_)Â¶
    

Parameters:
    

**expr** (_str_)

Return type:
    

ast.expr

tilelang.language.eager.ast.OperatorÂ¶
    

tilelang.language.eager.ast.BoolOpÂ¶
    

tilelang.language.eager.ast.get_operator_name(_operator_)Â¶
    

Parameters:
    

**operator** (_ast.operator_)

Return type:
    

Operator

tilelang.language.eager.ast.get_boolop_name(_boolop_)Â¶
    

Parameters:
    

**boolop** (_ast.boolop_)

Return type:
    

BoolOp

tilelang.language.eager.ast.eval_op(_op_ , _left_ , _right_)Â¶
    

Parameters:
    

  * **op** (_Operator_)

  * **left** (_Any_)

  * **right** (_Any_)



Return type:
    

Any

tilelang.language.eager.ast.eval_aug_assign(_op_ , _left_ , _sl_ , _right_)Â¶
    

Parameters:
    

  * **op** (_Operator_)

  * **left** (_Any_)

  * **sl** (_slice_)

  * **right** (_Any_)



Return type:
    

Any

_class _tilelang.language.eager.ast.BaseBuilderÂ¶
    

emptyÂ¶
    

get_parent_locals()Â¶
    

ctx_if(_cond_)Â¶
    

Return type:
    

collections.abc.Iterable[_T]

ctx_then(_val_)Â¶
    

Parameters:
    

**val** (__T_)

Return type:
    

collections.abc.Iterable[None]

ctx_else(_val_)Â¶
    

Parameters:
    

**val** (__T_)

Return type:
    

collections.abc.Iterable[None]

eval(_val_)Â¶
    

Parameters:
    

**val** (_Any_)

ctx_for(_range_)Â¶
    

Parameters:
    

**range** (_collections.abc.Iterable_ _[__Any_ _]_)

Return type:
    

collections.abc.Iterable[Any]

ctx_continue()Â¶
    

Return type:
    

[bool](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

ctx_break()Â¶
    

Return type:
    

[bool](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

ctx_while(_cond_)Â¶
    

Parameters:
    

**cond** (_Callable_ _[__[__]__,__Any_ _]_)

Return type:
    

collections.abc.Iterable[None]

bind(_name_ , _value_ , _annot =empty_)Â¶
    

Parameters:
    

  * **name** (_str_)

  * **value** (_Any_)

  * **annot** (_Any_)



Return type:
    

Any

unwrap_value(_value_)Â¶
    

assign_slice(_lval_ , _sl_ , _value_ , _annot =empty_)Â¶
    

Parameters:
    

  * **lval** (_Any_)

  * **sl** (_slice_)

  * **value** (_Any_)

  * **annot** (_Any_)




aug_assign(_op_ , _target_ , _aug_value_ , _name =None_)Â¶
    

Parameters:
    

  * **op** (_Operator_)

  * **target** (_Any_)

  * **aug_value** (_Any_)

  * **name** (_str_ _|__None_)



Return type:
    

Any

aug_assign_slice(_op_ , _target_ , _sl_ , _aug_value_)Â¶
    

Parameters:
    

  * **op** (_Operator_)

  * **target** (_Any_)

  * **sl** (_slice_)

  * **aug_value** (_Any_)




boolop(_op_ , _left_ , _right =None_)Â¶
    

Parameters:
    

  * **op** (_BoolOp_)

  * **left** (_Any_)

  * **right** (_Callable_ _[__[__]__,__Any_ _]__|__None_)



Return type:
    

Any

ifexp(_cond_ , _then_ , _otherwise_)Â¶
    

Parameters:
    

  * **cond** (_Any_)

  * **then** (_Callable_ _[__[__]__,__Any_ _]_)

  * **otherwise** (_Callable_ _[__[__]__,__Any_ _]_)



Return type:
    

Any

ret(_value_)Â¶
    

Parameters:
    

**value** (_Any_)

Return type:
    

Any

ctx_with(_ctx_)Â¶
    

Parameters:
    

**ctx** (_contextlib.AbstractContextManager_ _[__Any_ _]_)

Return type:
    

contextlib.AbstractContextManager[Any]

assert_expr(_cond_ , _msg_)Â¶
    

Parameters:
    

  * **cond** (_Any_)

  * **msg** (_Any_)




rval(_name_ , _value_)Â¶
    

Parameters:
    

  * **name** (_str_)

  * **value** (_Any_)




arg(_name_ , _value_)Â¶
    

Parameters:
    

  * **name** (_str_)

  * **value** (_Any_)




override(_name_)Â¶
    

Parameters:
    

**name** (_str_)

_class _tilelang.language.eager.ast.DSLMutator(_nonlocals_ , _globals_ , _filename_)Â¶
    

Bases: `ast.NodeTransformer`

A `NodeVisitor` subclass that walks the abstract syntax tree and allows modification of nodes.

The NodeTransformer will walk the AST and use the return value of the visitor methods to replace or remove the old node. If the return value of the visitor method is `None`, the node will be removed from its location, otherwise it is replaced with the return value. The return value may be the original node in which case no replacement takes place.

Here is an example transformer that rewrites all occurrences of name lookups (`foo`) to `data['foo']`:
    
    
    class RewriteName(NodeTransformer):
    
        def visit_Name(self, node):
            return Subscript(
                value=Name(id='data', ctx=Load()),
                slice=Constant(value=node.id),
                ctx=node.ctx
            )
    

Keep in mind that if the node youâre operating on has child nodes you must either transform the child nodes yourself or call the `generic_visit()` method for the node first.

For nodes that were part of a collection of statements (that applies to all statement nodes), the visitor may also return a list of nodes rather than just a single node.

Usually you use the transformer like this:
    
    
    node = YourTransformer().visit(node)
    

Parameters:
    

  * **nonlocals** (_dict_ _[__str_ _,__Any_ _]_)

  * **globals** (_dict_ _[__str_ _,__Any_ _]_)

  * **filename** (_str_)




tmp_counter _ = 0_Â¶
    

nonlocalsÂ¶
    

globalsÂ¶
    

extra_type_hints _: dict[str, Any]_Â¶
    

filenameÂ¶
    

get_tmp()Â¶
    

Return type:
    

str

visit_If(_node_)Â¶
    

Parameters:
    

**node** (_ast.If_)

visit_Expr(_node_)Â¶
    

Parameters:
    

**node** (_ast.Expr_)

visit_For(_node_)Â¶
    

Parameters:
    

**node** (_ast.For_)

visit_Continue(_node_)Â¶
    

Parameters:
    

**node** (_ast.Continue_)

visit_Break(_node_)Â¶
    

Parameters:
    

**node** (_ast.Break_)

visit_Assign(_node_)Â¶
    

Parameters:
    

**node** (_ast.Assign_)

Return type:
    

list[ast.AST]

visit_AugAssign(_node_)Â¶
    

Parameters:
    

**node** (_ast.AugAssign_)

Return type:
    

list[ast.AST]

visit_AnnAssign(_node_)Â¶
    

Parameters:
    

**node** (_ast.AnnAssign_)

visit_While(_node_)Â¶
    

visit_FunctionDef(_node_)Â¶
    

Parameters:
    

**node** (_ast.FunctionDef_)

visit_BoolOp(_node_)Â¶
    

Parameters:
    

**node** (_ast.BoolOp_)

visit_UnaryOp(_node_)Â¶
    

Parameters:
    

**node** (_ast.UnaryOp_)

visit_Compare(_node_)Â¶
    

Parameters:
    

**node** (_ast.Compare_)

Return type:
    

ast.expr

visit_IfExp(_node_)Â¶
    

Parameters:
    

**node** (_ast.IfExp_)

Return type:
    

ast.Expr

visit_Return(_node_)Â¶
    

Parameters:
    

**node** (_ast.Return_)

visit_With(_node_)Â¶
    

Parameters:
    

**node** (_ast.With_)

visit_Assert(_node_)Â¶
    

Parameters:
    

**node** (_ast.Assert_)

visit_Name(_node_)Â¶
    

Parameters:
    

**node** (_ast.Name_)

_class _tilelang.language.eager.ast.SpanAttacher(_filename_var_ , _func_name_var_)Â¶
    

Bases: `ast.NodeTransformer`

A `NodeVisitor` subclass that walks the abstract syntax tree and allows modification of nodes.

The NodeTransformer will walk the AST and use the return value of the visitor methods to replace or remove the old node. If the return value of the visitor method is `None`, the node will be removed from its location, otherwise it is replaced with the return value. The return value may be the original node in which case no replacement takes place.

Here is an example transformer that rewrites all occurrences of name lookups (`foo`) to `data['foo']`:
    
    
    class RewriteName(NodeTransformer):
    
        def visit_Name(self, node):
            return Subscript(
                value=Name(id='data', ctx=Load()),
                slice=Constant(value=node.id),
                ctx=node.ctx
            )
    

Keep in mind that if the node youâre operating on has child nodes you must either transform the child nodes yourself or call the `generic_visit()` method for the node first.

For nodes that were part of a collection of statements (that applies to all statement nodes), the visitor may also return a list of nodes rather than just a single node.

Usually you use the transformer like this:
    
    
    node = YourTransformer().visit(node)
    

Parameters:
    

  * **filename_var** (_str_)

  * **func_name_var** (_str_)




filename_varÂ¶
    

func_name_varÂ¶
    

visit(_node_)Â¶
    

Visit a node.

Parameters:
    

**node** (_ast.AST_)

_class _tilelang.language.eager.ast.IRGeneratorÂ¶
    

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
    

gen _: Callable[[BaseBuilder], Callable[_P, _T]]_Â¶
    

source _: str_Â¶
    

extra_type_hints _: dict[str, Any]_Â¶
    

tilelang.language.eager.ast.has_internal_prim_func(_func_)Â¶
    

Parameters:
    

**func** (_Callable_ _[___P_ _,___T_ _]_)

Return type:
    

[bool](../../dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

tilelang.language.eager.ast.mutate(_func_)Â¶
    

Transform a Python function into an IR (Intermediate Representation) generator. This function takes a regular Python function and performs AST (Abstract Syntax Tree) transformation to create an IRGenerator that can be used for code generation purposes. :param func: The Python function to be transformed. This should be a

> callable that will be analyzed and mutated at the AST level. The functionâs signature is preserved through generic type parameters _P (parameters) and _T (return type).

Returns:
    

An IRGenerator instance wrapping the transformed function.
    

The generator contains: \- gen: The compiled and mutated version of the original function \- source: The unparsed source code of the transformed AST as a string

Return type:
    

IRGenerator[_P, _T]

Parameters:
    

**func** (_Callable_ _[___P_ _,___T_ _]_)

Example
    
    
    >>> @mutate
    ... def my_function(x: int) -> int:
    ...     return x * 2
    >>> # my_function is now an IRGenerator that can be used for code generation
    

Note

  * The original functionâs closure variables and captured context are preserved

  * The transformation is performed at compile-time through AST manipulation

  * The returned IRGenerator maintains type information from the original function




# tilelang.autoddÂ¶

## AttributesÂ¶

`ASTPatKind` |   
---|---  
`JobBackend` |   
  
## ClassesÂ¶

`ASTRewrite` | Helper class that provides a standard way to create an ABC using  
---|---  
`GeneralRemove` | Helper class that provides a standard way to create an ABC using  
`CallFwdArg1` | Helper class that provides a standard way to create an ABC using  
`AttachFullFuncArgs` | Helper class that provides a standard way to create an ABC using  
`IntConstApply` | Helper class that provides a standard way to create an ABC using  
`BinOpFwdArg` | Helper class that provides a standard way to create an ABC using  
`ASTPat` |   
`ASTPatRewrite` | Helper class that provides a standard way to create an ABC using  
`ASTMutator` |   
`LabeledRewrite` |   
`RewriteAttacher` |   
`RewriteApplier` |   
`Task` |   
`PDD` |   
`TaskManager` | Helper class that provides a standard way to create an ABC using  
`ASTPDD` | Helper class that provides a standard way to create an ABC using  
`LinePDD` | Helper class that provides a standard way to create an ABC using  
`Ruff` | Helper class that provides a standard way to create an ABC using  
`AsyncPythonRunner` |   
`SubProcRunner` |   
`ParTaskManager` |   
`Args` |   
  
## FunctionsÂ¶

`ast_replace`(node, **changes) |   
---|---  
`parse_stmts`(s) |   
`parse_expr`(s) |   
`expr_to_zeros`(target) |   
`attach_rewrites`(tree, rewrites) |   
`apply_rewrites`(tree, target_labels) |   
`test_rewrite`(rewrite, code) |   
`ruff_fix_code`(code_string[, fix_lint, format_code]) |   
`clean_empty_pass`(code) |   
`main`(args) |   
`cli_main`([argv]) |   
  
## Module ContentsÂ¶

tilelang.autodd.ast_replace(_node_ , _** changes_)Â¶
    

Parameters:
    

**node** (_ast.AST_)

Return type:
    

ast.AST

tilelang.autodd.parse_stmts(_s_)Â¶
    

Parameters:
    

**s** (_str_)

Return type:
    

list[ast.stmt]

tilelang.autodd.parse_expr(_s_)Â¶
    

Parameters:
    

**s** (_str_)

Return type:
    

ast.expr

_class _tilelang.autodd.ASTRewriteÂ¶
    

Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

_abstract _get_name()Â¶
    

Return type:
    

str

_abstract _match(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

[bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

_abstract _rewrite(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

ast.AST | list[ast.AST] | None

_class _tilelang.autodd.GeneralRemoveÂ¶
    

Bases: `ASTRewrite`

Helper class that provides a standard way to create an ABC using inheritance.

name _: str_Â¶
    

target_type _: type[ast.AST]_Â¶
    

inside_list _: [bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_ _ = True_Â¶
    

replace_with _: ast.AST | list[ast.AST] | None_ _ = None_Â¶
    

get_name()Â¶
    

Return type:
    

str

match(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

[bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

rewrite(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

None

tilelang.autodd.expr_to_zeros(_target_)Â¶
    

Parameters:
    

**target** (_ast.expr_)

Return type:
    

ast.expr

_class _tilelang.autodd.CallFwdArg1Â¶
    

Bases: `ASTRewrite`

Helper class that provides a standard way to create an ABC using inheritance.

get_name()Â¶
    

Return type:
    

str

match(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

[bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

rewrite(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

ast.AST

_class _tilelang.autodd.AttachFullFuncArgsÂ¶
    

Bases: `ASTRewrite`

Helper class that provides a standard way to create an ABC using inheritance.

get_name()Â¶
    

Return type:
    

str

match(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

[bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

rewrite(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

ast.AST

_class _tilelang.autodd.IntConstApplyÂ¶
    

Bases: `ASTRewrite`

Helper class that provides a standard way to create an ABC using inheritance.

matcher _: Callable[[int], [bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")]_Â¶
    

apply _: Callable[[int], ast.AST]_Â¶
    

name _: str_Â¶
    

get_name()Â¶
    

Return type:
    

str

match(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

[bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

rewrite(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

ast.AST

_class _tilelang.autodd.BinOpFwdArgÂ¶
    

Bases: `ASTRewrite`

Helper class that provides a standard way to create an ABC using inheritance.

forward _: Literal['left', 'right']__ = 'left'_Â¶
    

get_name()Â¶
    

Return type:
    

str

match(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

[bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

rewrite(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

ast.AST

tilelang.autodd.ASTPatKindÂ¶
    

_class _tilelang.autodd.ASTPatÂ¶
    

tree _: ast.expr | list[ast.stmt]_Â¶
    

placeholders _: set[str]_Â¶
    

_classmethod _from_code(_kind_ , _code_ , _placeholders_)Â¶
    

Parameters:
    

  * **kind** (_ASTPatKind_)

  * **code** (_str_)

  * **placeholders** (_set_ _[__str_ _]_)



Return type:
    

ASTPat

match_placeholders(_node_)Â¶
    

Parameters:
    

**node** (_ast.AST_ _|__list_ _[__ast.AST_ _]_)

Return type:
    

dict[str, ast.AST] | [bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

match(_node_)Â¶
    

Parameters:
    

**node** (_ast.AST_)

Return type:
    

[bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

replace(_repl_)Â¶
    

Parameters:
    

**repl** (_dict_ _[__str_ _,__ast.AST_ _]_)

Return type:
    

ast.AST

_class _tilelang.autodd.ASTPatRewriteÂ¶
    

Bases: `ASTRewrite`

Helper class that provides a standard way to create an ABC using inheritance.

name _: str_Â¶
    

match_pat _: ASTPat_Â¶
    

rewrite_pat _: ASTPat_Â¶
    

checker _: Callable[[dict[str, ast.AST]], [bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")] | dict[str, Callable[[ast.AST], [bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")]] | None_ _ = None_Â¶
    

derived _: dict[str, Callable[[dict[str, ast.AST]], ast.AST]] | None_ _ = None_Â¶
    

_classmethod _from_code(_name_ , _kind_ , _match_ , _rewrite_ , _placeholders_ , _checker =None_, _derived =None_)Â¶
    

Parameters:
    

  * **name** (_str_)

  * **kind** (_ASTPatKind_)

  * **match** (_str_)

  * **rewrite** (_str_)

  * **placeholders** (_set_ _[__str_ _]_)

  * **checker** (_Callable_ _[__[__dict_ _[__str_ _,__ast.AST_ _]__]__,_[_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _]__|__dict_ _[__str_ _,__Callable_ _[__[__ast.AST_ _]__,_[_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _]__]__|__None_)

  * **derived** (_dict_ _[__str_ _,__Callable_ _[__[__dict_ _[__str_ _,__ast.AST_ _]__]__,__ast.AST_ _]__]__|__None_)



Return type:
    

ASTPatRewrite

get_name()Â¶
    

Return type:
    

str

match_placeholders(_node_)Â¶
    

Parameters:
    

**node** (_ast.AST_)

match(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

[bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")

rewrite(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_)

  * **field** (_str_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

ast.AST

_class _tilelang.autodd.ASTMutatorÂ¶
    

generic_visit(_node_)Â¶
    

visit(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_ _|__None_)

  * **field** (_str_ _|__None_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




_class _tilelang.autodd.LabeledRewriteÂ¶
    

label _: int_Â¶
    

rewrite _: ASTRewrite_Â¶
    

_class _tilelang.autodd.RewriteAttacher(_rewrites_)Â¶
    

Bases: `ASTMutator`

Parameters:
    

**rewrites** (_list_ _[__ASTRewrite_ _]_)

rewritesÂ¶
    

uid_counter _ = 0_Â¶
    

rewrite_counter _ = 0_Â¶
    

rewrite_namesÂ¶
    

visit(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_ _|__None_)

  * **field** (_str_ _|__None_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.autodd.attach_rewrites(_tree_ , _rewrites_)Â¶
    

Parameters:
    

  * **tree** (_ast.AST_)

  * **rewrites** (_list_ _[__ASTRewrite_ _]_)



Return type:
    

tuple[ast.AST, int, int]

_class _tilelang.autodd.RewriteApplier(_target_labels_)Â¶
    

Bases: `ASTMutator`

Parameters:
    

**target_labels** (_set_ _[__int_ _]_)

target_labelsÂ¶
    

applied_rewrites _: set[int]_Â¶
    

visited _: set[int]_Â¶
    

visit(_node_ , _parent_ , _field_ , _inside_list_)Â¶
    

Parameters:
    

  * **node** (_ast.AST_)

  * **parent** (_ast.AST_ _|__None_)

  * **field** (_str_ _|__None_)

  * **inside_list** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.autodd.apply_rewrites(_tree_ , _target_labels_)Â¶
    

Parameters:
    

  * **tree** (_ast.AST_)

  * **target_labels** (_set_ _[__int_ _]_)



Return type:
    

tuple[ast.AST, set[int]]

tilelang.autodd.test_rewrite(_rewrite_ , _code_)Â¶
    

Parameters:
    

  * **rewrite** (_ASTRewrite_)

  * **code** (_str_)




_class _tilelang.autodd.TaskÂ¶
    

source _: str_Â¶
    

applied _: list[int]_Â¶
    

masked _: list[int]_Â¶
    

with_source(_source_)Â¶
    

Parameters:
    

**source** (_str_)

Return type:
    

Task

_class _tilelang.autodd.PDD(_all_labels_ , _init_proba =0.93_)Â¶
    

Parameters:
    

  * **all_labels** (_list_ _[__int_ _]_)

  * **init_proba** (_float_)




all_labelsÂ¶
    

probasÂ¶
    

apply(_target_labels_)Â¶
    

Parameters:
    

**target_labels** (_set_ _[__int_ _]_)

Return type:
    

set[int]

generator()Â¶
    

Return type:
    

collections.abc.Iterable[Task]

update(_task_ , _is_interesting_)Â¶
    

Parameters:
    

  * **task** (_Task_)

  * **is_interesting** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




_class _tilelang.autodd.TaskManagerÂ¶
    

Bases: `abc.ABC`

Helper class that provides a standard way to create an ABC using inheritance.

_abstract _task_generator()Â¶
    

Return type:
    

collections.abc.Iterable[Task]

_abstract _task_update(_task_ , _is_interesting_)Â¶
    

Parameters:
    

  * **task** (_Task_)

  * **is_interesting** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




_classmethod _from_source(_source_ , _* args_, _** kwargs_)Â¶
    

Abstractmethod:
    

Parameters:
    

**source** (_str_)

Return type:
    

TaskManager

_class _tilelang.autodd.ASTPDD(_tree_ , _rewrites_ , _init_proba =0.93_)Â¶
    

Bases: `TaskManager`, `PDD`

Helper class that provides a standard way to create an ABC using inheritance.

Parameters:
    

  * **tree** (_ast.AST_)

  * **rewrites** (_list_ _[__ASTRewrite_ _]_)

  * **init_proba** (_float_)




_classmethod _from_source(_source_ , _* args_, _** kwargs_)Â¶
    

apply(_target_labels_)Â¶
    

Parameters:
    

**target_labels** (_set_ _[__int_ _]_)

Return type:
    

set[int]

task_generator()Â¶
    

Return type:
    

collections.abc.Iterable[Task]

task_update(_task_ , _is_interesting_)Â¶
    

Parameters:
    

  * **task** (_Task_)

  * **is_interesting** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




tilelang.autodd.ruff_fix_code(_code_string_ , _fix_lint =True_, _format_code =True_)Â¶
    

Parameters:
    

  * **code_string** (_str_)

  * **fix_lint** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **format_code** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))



Return type:
    

str

_class _tilelang.autodd.LinePDD(_source_ , _init_proba =0.93_)Â¶
    

Bases: `TaskManager`, `PDD`

Helper class that provides a standard way to create an ABC using inheritance.

Parameters:
    

  * **source** (_str_)

  * **init_proba** (_float_)




linesÂ¶
    

_classmethod _from_source(_source_ , _* args_, _** kwargs_)Â¶
    

task_generator()Â¶
    

Return type:
    

collections.abc.Iterable[Task]

task_update(_task_ , _is_interesting_)Â¶
    

Parameters:
    

  * **task** (_Task_)

  * **is_interesting** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




_class _tilelang.autodd.Ruff(_source_ , _fix_lint =True_, _format_code =True_)Â¶
    

Bases: `TaskManager`

Helper class that provides a standard way to create an ABC using inheritance.

Parameters:
    

  * **source** (_str_)

  * **fix_lint** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))

  * **format_code** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




sourceÂ¶
    

fix_lint _ = True_Â¶
    

format_code _ = True_Â¶
    

finished _ = False_Â¶
    

_classmethod _from_source(_source_ , _* args_, _** kwargs_)Â¶
    

Parameters:
    

**source** (_str_)

Return type:
    

Ruff

task_generator()Â¶
    

task_update(_task_ , _is_interesting_)Â¶
    

Parameters:
    

  * **task** (_Task_)

  * **is_interesting** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




_class _tilelang.autodd.AsyncPythonRunnerÂ¶
    

process _ = None_Â¶
    

input_queue _ = None_Â¶
    

output_queue _ = None_Â¶
    

lockÂ¶
    

start_proc()Â¶
    

stop_proc()Â¶
    

__enter__()Â¶
    

__exit__(_exc_type_ , _exc_value_ , _traceback_)Â¶
    

_async _run(_code_ , _timeout =5.0_)Â¶
    

Parameters:
    

  * **code** (_str_)

  * **timeout** (_float_)




_class _tilelang.autodd.SubProcRunnerÂ¶
    

__enter__()Â¶
    

__exit__(_exc_type_ , _exc_value_ , _traceback_)Â¶
    

_async _run(_code_ , _timeout =5.0_)Â¶
    

Parameters:
    

  * **code** (_str_)

  * **timeout** (_float_)




tilelang.autodd.clean_empty_pass(_code_)Â¶
    

Parameters:
    

**code** (_str_)

Return type:
    

str

tilelang.autodd.JobBackendÂ¶
    

_class _tilelang.autodd.ParTaskManagerÂ¶
    

err_msg _: str_Â¶
    

text _: str_Â¶
    

output_file _: pathlib.Path_Â¶
    

timeout _: int_ _ = 60_Â¶
    

num_workers _: int_ _ = 1_Â¶
    

backend _: JobBackend_ _ = 'runner'_Â¶
    

allow_larger _: [bool](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool")_ _ = False_Â¶
    

__post_init__()Â¶
    

_property _text_lenÂ¶
    

reset(_task_manager_)Â¶
    

Parameters:
    

**task_manager** (_TaskManager_)

_async _get_next_task()Â¶
    

Return type:
    

Task | None

_async _submit_result(_task_ , _is_interested_)Â¶
    

Parameters:
    

  * **task** (_Task_)

  * **is_interested** ([_bool_](../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool"))




post_proc(_text_)Â¶
    

_async _worker(_wid_)Â¶
    

Parameters:
    

**wid** (_int_)

_async _start_workers()Â¶
    

_async _stop_workers()Â¶
    

_async _run_async(_task_manager_)Â¶
    

Parameters:
    

**task_manager** (_TaskManager_)

_async _run_with(_cls_ , _* args_, _** kwargs_)Â¶
    

Parameters:
    

**cls** (_type_ _[__TaskManager_ _]_)

_class _tilelang.autodd.ArgsÂ¶
    

Bases: `NamedTuple`

source _: pathlib.Path_Â¶
    

err_msg _: str_Â¶
    

output _: pathlib.Path_Â¶
    

backend _: JobBackend_Â¶
    

timeout _: int_Â¶
    

jobs _: int_Â¶
    

_async _tilelang.autodd.main(_args_)Â¶
    

Parameters:
    

**args** (_Args_)

tilelang.autodd.cli_main(_argv =None_)Â¶
    

Parameters:
    

**argv** (_Sequence_ _[__str_ _]__|__None_)

Return type:
    

None

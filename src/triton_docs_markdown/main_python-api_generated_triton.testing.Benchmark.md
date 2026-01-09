# triton.testing.Benchmark¶

_class _triton.testing.Benchmark(_self_ , _x_names : List[str]_, _x_vals : List[Any]_, _line_arg : str_, _line_vals : List[Any]_, _line_names : List[str]_, _plot_name : str_, _args : Dict[str, Any]_, _xlabel : str = ''_, _ylabel : str = ''_, _x_log : bool = False_, _y_log : bool = False_, _styles =None_)¶
    

This class is used by the `perf_report` function to generate line plots with a concise API.

__init__(_self_ , _x_names : List[str]_, _x_vals : List[Any]_, _line_arg : str_, _line_vals : List[Any]_, _line_names : List[str]_, _plot_name : str_, _args : Dict[str, Any]_, _xlabel : str = ''_, _ylabel : str = ''_, _x_log : bool = False_, _y_log : bool = False_, _styles =None_)¶
    

Constructor. x_vals can be a list of scalars or a list of tuples/lists. If x_vals is a list of scalars and there are multiple x_names, all arguments will have the same value. If x_vals is a list of tuples/lists, each element should have the same length as x_names.

Parameters:
    

  * **x_names** (_List_ _[__str_ _]_) – Name of the arguments that should appear on the x axis of the plot.

  * **x_vals** (_List_ _[__Any_ _]_) – List of values to use for the arguments in `x_names`.

  * **line_arg** (_str_) – Argument name for which different values correspond to different lines in the plot.

  * **line_vals** (_List_ _[__Any_ _]_) – List of values to use for the arguments in `line_arg`.

  * **line_names** (_List_ _[__str_ _]_) – Label names for the different lines.

  * **plot_name** (_str_) – Name of the plot.

  * **args** (_Dict_ _[__str_ _,__Any_ _]_) – Dictionary of keyword arguments to remain fixed throughout the benchmark.

  * **xlabel** (_str_ _,__optional_) – Label for the x axis of the plot.

  * **ylabel** (_str_ _,__optional_) – Label for the y axis of the plot.

  * **x_log** (_bool_ _,__optional_) – Whether the x axis should be log scale.

  * **y_log** (_bool_ _,__optional_) – Whether the y axis should be log scale.

  * **styles** (_list_ _[__tuple_ _[__str_ _,__str_ _]__]_) – A list of tuples, where each tuple contains two elements: a color and a linestyle.




Methods

`__init__`(self, x_names, x_vals, line_arg, ...) | Constructor.  
---|---

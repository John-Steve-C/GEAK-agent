# tilelang.carver.roller.rasterizationÂ¶

Rasteration Plan For L2 Cache Locality

## ClassesÂ¶

`Rasterization` |   
---|---  
`NoRasterization` |   
`Rasterization2DRow` | Rasterization by Row, each Row line width is panel_width  
`Rasterization2DColumn` | Rasterization by Column, each column line width is panel_width  
  
## Module ContentsÂ¶

_class _tilelang.carver.roller.rasterization.RasterizationÂ¶
    

panel_width__ = None_Â¶
    

_abstract _get_code()Â¶
    

Return type:
    

list[str]

_property _panel_widthÂ¶
    

_class _tilelang.carver.roller.rasterization.NoRasterizationÂ¶
    

Bases: `Rasterization`

__repr__()Â¶
    

Return type:
    

str

get_code()Â¶
    

Return type:
    

list[str]

_class _tilelang.carver.roller.rasterization.Rasterization2DRow(_panel_width =4_)Â¶
    

Bases: `Rasterization`

Rasterization by Row, each Row line width is panel_width
    

> _________|

|_________ __________|

panel_width__ = 4_Â¶
    

__repr__()Â¶
    

Return type:
    

str

_abstract _get_code()Â¶
    

Return type:
    

list[str]

_class _tilelang.carver.roller.rasterization.Rasterization2DColumn(_panel_width =4_)Â¶
    

Bases: `Rasterization`

Rasterization by Column, each column line width is panel_width
    

> _

| | |

| | |

|_| |_|

panel_width__ = 4_Â¶
    

__repr__()Â¶
    

Return type:
    

str

get_device_function()Â¶
    

Return type:
    

str

get_code(_panel_width =None_)Â¶
    

Parameters:
    

**panel_width** (_int_)

Return type:
    

list[str]

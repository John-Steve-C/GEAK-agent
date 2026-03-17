# tilelang.tools.plot_layoutÂ¶

## FunctionsÂ¶

`plot_layout`(layout[, save_directory, name, colormap, ...]) | Plot the layout mapping as a 2D grid visualization.  
---|---  
`plot_fragment_tv`(frag[, save_directory, name, ...]) | Plot fragment in terms of thread and local index mapping.  
  
## Module ContentsÂ¶

tilelang.tools.plot_layout.plot_layout(_layout_ , _save_directory ='./tmp'_, _name ='layout'_, _colormap =None_, _verbose =False_, _formats ='pdf'_, _view ='input'_, _grid_shape =None_)Â¶
    

Plot the layout mapping as a 2D grid visualization.

Dispatches to Fragment-specific or Layout-specific plotting based on the type of the layout object.

Parameters:
    

  * **layout** (_T.Layout_ _or_ _T.Fragment_) â The layout object to visualize.

  * **save_directory** (_str_ _,__optional_) â Output directory (default â./tmpâ).

  * **name** (_str_ _,__optional_) â Base filename for saved images (default âlayoutâ).

  * **colormap** (_str_ _,__optional_) â Matplotlib colormap name. Defaults to âRdPuâ for Fragment, âSpectralâ for Layout.

  * **verbose** ([_bool_](../../language/dtypes/index.html#tilelang.language.dtypes.bool "tilelang.language.dtypes.bool") _,__optional_) â If True, print mapping details.

  * **formats** (_str_ _|__list_ _[__str_ _]__,__optional_) â Output format(s): âpdfâ, âpngâ, âsvgâ, âallâ, or comma-separated (default âpdfâ).

  * **view** (_str_ _,__optional_) â 

For T.Layout only: choose which space is shown as the 2D grid.

    * âinputâ (default): grid is input space, labels show output (flattened) coordinates.

    * âoutputâ: grid is output space, labels show input coordinates.

  * **grid_shape** (_tuple_ _[__int_ _,__int_ _]__|__None_ _,__optional_) â For view=âinputâ only: override the 2D grid shape (rows, cols). The product must match the total number of input elements.



Return type:
    

None

tilelang.tools.plot_layout.plot_fragment_tv(_frag_ , _save_directory =None_, _name ='layout'_, _apply_idx_fn =lambda *args: ..._, _colormap ='RdPu'_, _item_scale =0.75_, _formats ='pdf'_, _dpi =80_)Â¶
    

Plot fragment in terms of thread and local index mapping. :param frag: The fragment object that describes how indices are mapped. :type frag: T.Fragment :param save_directory: The directory where the output images will be saved. :type save_directory: str | None, optional :param name: The base name of the output files (default is âlayoutâ). :type name: str, optional :param apply_idx_fn: A function to apply to the source indices for labeling (default is identity). :type apply_idx_fn: function, optional :param colormap: The colormap to use for visualization (default is âRdPuâ). :type colormap: str, optional :param item_scale: The scale factor for each item in the plot (default is 0.75). :type item_scale: float, optional :param formats: The formats to save the image in (default is âpdfâ). :type formats: str | list[str], optional :param dpi: The resolution in dots per inch for the saved image (default is 80). :type dpi: int, optional

Parameters:
    

  * **frag** (_tilelang.language.Fragment_)

  * **save_directory** (_str_ _|__None_)

  * **name** (_str_)

  * **colormap** (_str_)

  * **item_scale** (_float_)

  * **formats** (_str_ _|__list_ _[__str_ _]_)




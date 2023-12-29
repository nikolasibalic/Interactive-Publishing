import copy
import numpy as np
from typing import List


class StaticWidget(object):
    """Base Class for Static Widgets"""
    def __init__(self, name=None, divclass=None):
        self.name = name
        if divclass is None:
            self.divargs = ""
        else:
            self.divargs = 'class:"{0}"'.format(divclass)

    def __repr__(self):
        return self.html()

    def _repr_html_(self):
        return self.html()

    def copy(self):
        return copy.deepcopy(self)

    def renamed(self, name):
        if (self.name is not None) and (self.name != name):
            obj = self.copy()
        else:
            obj = self
        obj.name = name
        return obj


class RangeWidget(StaticWidget):
    slider_html = ('<div class="wrap"><div class="left"><p><b>{paramName} =</b></p></div>'
                   '<div class="right"><input type="range" name="{name}" '
                   'min="{range[0]}" max="{range[1]}" step="{range[2]}" '
                   'value="{default}" style="{style}" '
                   'oninput="interactUpdate(this.parentNode);" '
                   'onchange="interactUpdate(this.parentNode);"></div></div>')
    def __init__(self, min:float, max:float, step:float=1, name=None,
                 default=None, width=350, divclass=None,
                 show_range=False):
        """Range (slider) widget

        Args:
            min (float): starting value for input value range
            max (float): end value for input value range
            step (float, optional): step size for input value range.
            name (_type_, optional): _description_.
            default (_type_, optional): _description_.
            width (int, optional): _description_.
            divclass (_type_, optional): _description_.
            show_range (bool, optional): _description_.
        """
        StaticWidget.__init__(self, name, divclass)
        self.datarange = (min, max, step)
        self.width = width
        self.show_range = show_range
        if default is None:
            self.default = min
        else:
            self.default = default

    def values(self):
        min, max, step = self.datarange
        return np.arange(min, max + step, step)


    def html(self):
        style = ""

        if self.width is not None:
            style += "width:{0}px; max-width:100%;".format(self.width)

        output = self.slider_html.format(paramName=self.name.replace("_"," "),
                                         name=self.name, range=self.datarange,
                                         default=self.default, style=style)
        if self.show_range:
            output = "{0} {1} {2}".format(self.datarange[0],
                                          output,
                                          self.datarange[1])
        return output


class RangeWidgetViridis(RangeWidget):
    slider_html = ('<div class="wrap"><div class="left"><p><b>{paramName} =</b></p></div>'
                   '<div class="right"><input class="viridisrange" type="range" name="{name}" '
                   'min="{range[0]}" max="{range[1]}" step="{range[2]}" '
                   'value="{default}" style="{style}" '
                   'oninput="interactUpdate(this.parentNode);" '
                   'onchange="interactUpdate(this.parentNode);"></div></div>')
    def __init__(self, min:float, max:float, step:float=1, name=None,
                 default=None, width=350, divclass=None,
                 show_range=False):
        """Range (slider) widget that has viridis colourbar on background.
        Useful for special parameter, e.g. time.

        Args:
            min (float): starting value for input value range
            max (float): end value for input value range
            step (float, optional): step size for input value range.
            name (_type_, optional): _description_.
            default (_type_, optional): _description_.
            width (int, optional): _description_.
            divclass (_type_, optional): _description_. 
            show_range (bool, optional): _description_. 
        """
        RangeWidget.__init__(self, min, max, step=step, name=name,
                 default=default, width=width, divclass=divclass,
                 show_range=show_range)


class DropDownWidget(StaticWidget):
    select_html = ('<div class="wrap"><div class="left"><p><b>{nameParam} =</b></p></div>'
                   '<div class="right"> <select name="{name}" '
                      'onchange="interactUpdate(this.parentNode);"> '
                      '{options}'
                      '</select></div></div>'
        )
    option_html = ('<option value="{value}" '
                      '{selected}>{label}</option>')
    def __init__(self, values:List[type[str | float]], name=None,
                 labels:List[str]=None, default=None, divclass=None,
                 delimiter="      "
                 ):
        """Drop down widget.

        Args:
            values (List[type[str | float]]): drop down option values
            name (_type_, optional): _description_. 
            labels (List[str], optional): labels for drop down options. By default
            they are same as values.
            default (_type_, optional): _description_. 
            divclass (_type_, optional): _description_. 
            delimiter (str, optional): _description_.

        Raises:
            ValueError: _description_
            ValueError: _description_
        """
        StaticWidget.__init__(self, name, divclass)
        self._values = values
        self.delimiter = delimiter
        if labels is None:
            labels = map(str, values)
        elif len(labels) != len(values):
            raise ValueError("length of labels must match length of values")
        self.labels = labels

        if default is None:
            self.default = values[0]
        elif default in values:
            self.default = default
        else:
            raise ValueError("if specified, default must be in values")

    def _single_option(self,label,value):
        if value == self.default:
            selected = ' selected '
        else:
            selected = ''
        return self.option_html.format(label=label,
                                       value=value,
                                       selected=selected)
    def values(self):
        return self._values
    def html(self):
        options = self.delimiter.join(
            [self._single_option(label,value)
             for (label,value) in zip(self.labels, self._values)]
        )
        return self.select_html.format(nameParam=self.name.replace("_"," "),
                                       name=self.name,
                                       options=options)

class RadioWidget(StaticWidget):
    radio_html = ('<input type="radio" name="{name}" value="{value}" '
                  '{checked} '
                  'onchange="interactUpdate(this.parentNode);">')

    def __init__(self, values:List[type[str | float]], name=None,
                 labels:List[str]=None, default=None, divclass=None,
                 delimiter="      "):
        """Radio button widget

        Args:
            values (List[str]): input option values
            name (_type_, optional): _description_. 
            labels (List[str], optional): _description_. 
            default (_type_, optional): _description_.
            divclass (_type_, optional): _description_. 
            delimiter (str, optional): _description_. .

        Raises:
            ValueError: _description_
            ValueError: _description_
        """
        StaticWidget.__init__(self, name, divclass)
        self._values = values
        self.delimiter = delimiter

        if labels is None:
            labels = map(str, values)
        elif len(labels) != len(values):
            raise ValueError("length of labels must match length of values")
        self.labels = labels

        if default is None:
            self.default = values[0]
        elif default in values:
            self.default = default
        else:
            raise ValueError("if specified, default must be in values")

    def _single_radio(self, value):
        if value == self.default:
            checked = 'checked="checked"'
        else:
            checked = ''
        return self.radio_html.format(name=self.name, value=value,
                                      checked=checked)

    def values(self):
        return self._values

    def html(self):
        preface = '<div class="wrap"><div class="left"><p><b>{paramName} = </b></p></div>'.format(
            paramName=self.name.replace("_"," "))
        return  preface + '<div class="right">' + self.delimiter.join(
            ["{0} {1}<span class='cbseparator'></span>".format(self._single_radio(value), label)
             for (label, value) in zip(self.labels, self._values)]) + "</div></div>"

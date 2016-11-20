# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.widget_list import widgets_in_module

from grumpyforms.api import Form, InputWidget as _InputWidget
import grumpyforms.fields

# dynamically create Genshi variants of all widgets from grumpyforms.
# That way Genshi users can import these variants conveniently via this module
symbols_ = globals()
for name, _widget in widgets_in_module(grumpyforms.fields, _InputWidget):
    widget_attrs = dict(_widget.__dict__)
    widget_attrs['template_engine'] = 'genshi'
    GenshiWidget = type('Genshi'+name, (_widget,), widget_attrs)
    symbols_[name] = GenshiWidget


class GenshiForm(Form):
    template_engine = 'genshi'

# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.api import Widget


class Label(Widget):
    for_ = None
    value = None
    template = 'label.jinja2'
    
    def _display_value(self, value):
        value = self.super()
        if value is not None:
            return value
        return self.value


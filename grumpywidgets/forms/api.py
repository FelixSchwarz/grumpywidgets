# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.api import Context, Widget


__all__ = ['InputWidget', 'Form']

class InputWidget(Widget):
    validator = None
    name = None
    label = None
    
    def __init__(self, name=None, **kwargs):
        if name is not None:
            kwargs['name'] = name
        super(InputWidget, self).__init__(**kwargs)


class Form(InputWidget):
    url = ''
    method = 'POST'
    charset = 'UTF-8'
    template = 'form.jinja2'
    
    def initialize_children(self, values):
        for child in self.children:
            child.context = Context()
            child_name = getattr(child, 'name', None)
            if (child_name is not None) and (child_name in values):
                child.context.value = values.pop(child_name)
        return values
    
    def display(self, value=None):
        values = self.initialize_children(value or dict())
        if values:
            first_key = values.keys()[0]
            raise ValueError("Unknown parameter '%s' passed to display()" % first_key)
        return self.super(value=values)

# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.api import Widget


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
    
    def display(self, value):
        form = '<form '
        if self.id is not None:
            form += 'id="%s" ' % unicode(self.id)
        if self.name is not None:
            form += 'name="%s" ' % unicode(self.name)
        if self.css_classes:
            form += 'class="%s" ' % ' '.join(self.css_classes)
        form += 'action="%s" method="%s" accept-charset="%s">' % (self.url, self.method, self.charset)
        
        child_values = value
        for child in self.children:
            child_value = None
            if hasattr(child, 'name'):
                child_name = getattr(child, 'name')
                child_value = child_values.pop(child_name, None)
            form += child.display(child_value)
        if child_values:
            first_key = child_values.keys()[0]
            raise ValueError("Unknown parameter '%s' passed to display()" % first_key)
        form += '</form>'
        return form


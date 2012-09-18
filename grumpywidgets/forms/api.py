# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.api import Widget


__all__ = ['InputWidget', 'Form']

class InputWidget(Widget):
    validator = None
    name = None
    label = None


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
        form += 'action="%s" method="%s" accept-charset="%s"></form>' % (self.url, self.method, self.charset)
        return form


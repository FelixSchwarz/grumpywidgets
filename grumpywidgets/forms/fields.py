# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.forms.api import InputWidget

__all__ = ['TextField']

class TextField(InputWidget):
    def display(self, value=None):
        field = '<input type="text" '
        if self.id is not None:
            field += 'id="%s" ' % self.id
        if self.name is not None:
            field += 'name="%s" ' % self.name
        if value is not None:
            field += 'value="%s" ' % value
        if self.css_classes:
            field += 'class="%s" ' % ' '.join(self.css_classes)
        field += '/>'
        return field

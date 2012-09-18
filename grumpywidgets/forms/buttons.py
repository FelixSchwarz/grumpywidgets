# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.forms.api import InputWidget

__all__ = ['SubmitButton']

class SubmitButton(InputWidget):
    value = None
    
    def display(self, value=None):
        button = '<input type="submit" '
        
        if self.id:
            button += 'id="%s" ' % self.id
        if self.name:
            button += 'name="%s" ' % self.name
        if self.value is not None:
            # self.value can be used to override any value from form data to 
            # prevent 'empty button text' as seen in ToscaWidgets
            value = self.value
        if value not in ('', None):
            button += 'value="%s" ' % value
        if self.css_classes:
            button += 'class="%s" ' % ' '.join(self.css_classes)
        button += '/>'
        return button


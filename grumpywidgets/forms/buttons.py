# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.forms.api import InputWidget

__all__ = ['SubmitButton']

class SubmitButton(InputWidget):
    value = None
    template = 'submit_button.jinja2'
    
    def template_variables(self, values):
        variables = self.super()
        if self.value is not None:
            # self.value can be used to override any value from form data to 
            # prevent 'empty button text' as seen in ToscaWidgets
            variables['value'] = self.value
        if ('value' in variables) and (variables['value'] in ('', None)):
            del variables['value']
        return variables


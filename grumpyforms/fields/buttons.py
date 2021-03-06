# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpyforms.api import InputWidget


__all__ = ['SubmitButton']

class SubmitButton(InputWidget):
    value = None
    template_name = 'submit_button'

    def template_variables(self, values, **widget_attributes):
        variables = super(SubmitButton, self).template_variables(values, **widget_attributes)
        if self.value is not None:
            # self.value can be used to override any value from form data to
            # prevent 'empty button text' as seen in ToscaWidgets
            variables['value'] = self.value
        if ('value' in variables) and (variables['value'] in ('', None)):
            del variables['value']
        return variables

    def is_field(self):
        return False

    def is_button(self):
        return True


# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.validators import BooleanCheckbox, StringValidator

from grumpywidgets.forms.api import InputWidget


__all__ = ['Checkbox', 'HiddenField']

class Checkbox(InputWidget):
    template = 'checkbox.jinja2'
    validator = BooleanCheckbox()


class HiddenField(InputWidget):
    template = 'hidden_field.jinja2'
    validator = StringValidator()


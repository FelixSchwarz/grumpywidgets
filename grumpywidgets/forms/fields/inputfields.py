# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.validators import StringValidator

from grumpywidgets.forms.api import InputWidget


__all__ = ['HiddenField', 'TextField']

class TextField(InputWidget):
    template = 'text_field.jinja2'
    validator = StringValidator(required=False)


class HiddenField(InputWidget):
    template = 'hidden_field.jinja2'
    validator = StringValidator()


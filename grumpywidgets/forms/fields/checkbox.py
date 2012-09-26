# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.validators import BooleanCheckbox

from grumpywidgets.forms.api import InputWidget


__all__ = ['Checkbox']

class Checkbox(InputWidget):
    template = 'checkbox.jinja2'
    validator = BooleanCheckbox()


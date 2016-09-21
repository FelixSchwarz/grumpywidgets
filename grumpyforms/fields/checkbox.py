# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.validators import BooleanCheckbox

from grumpyforms.api import InputWidget


__all__ = ['Checkbox']

class Checkbox(InputWidget):
    template_name = 'checkbox'
    validator = BooleanCheckbox()


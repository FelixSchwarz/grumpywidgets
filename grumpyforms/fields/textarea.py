# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.validators import StringValidator

from grumpyforms.api import InputWidget


__all__ = ['TextArea']

class TextArea(InputWidget):
    template = 'textarea.jinja2'
    validator = StringValidator()

    cols = 50
    rows = 10

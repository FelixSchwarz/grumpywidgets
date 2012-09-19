# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.forms.api import InputWidget

__all__ = ['TextField']

class TextField(InputWidget):
    template = 'text_field.jinja2'

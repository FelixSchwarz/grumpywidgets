# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from operator import itemgetter

from grumpyforms.api import InputWidget
from pycerberus.validators import OneOf


__all__ = ['SelectField']

class SelectField(InputWidget):
    template = 'select_field.jinja2'
    validator = OneOf([])
    
    options = ()
    def __init__(self, *args, **kwargs):
        self.super(*args, **kwargs)
        self.validator = OneOf(map(itemgetter(0), self.options))

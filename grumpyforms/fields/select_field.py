# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from operator import itemgetter

from pycerberus.validators import OneOf

from grumpyforms.api import InputWidget


__all__ = ['SelectField']

class SelectField(InputWidget):
    template_name = 'select_field'
    validator = None
    options = ()

    def __init__(self, *args, **kwargs):
        super(SelectField, self).__init__(*args, **kwargs)
        if self.validator is None:
            self.validator = OneOf(map(itemgetter(0), self.options))

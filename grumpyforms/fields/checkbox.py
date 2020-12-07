# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.validators import BooleanCheckbox

from grumpyforms.api import InputWidget


__all__ = ['Checkbox']

class Checkbox(InputWidget):
    template_name = 'checkbox'
    option_value = None
    readonly = None
    disabled = None

    def __init__(self, *args, **kwargs):
        super(Checkbox, self).__init__(*args, **kwargs)
        if self.validator is None:
            self.validator = self._build_validator()

    def _build_validator(self):
        option_value = self.option_value if (self.option_value is not None) else 'on'
        trueish = BooleanCheckbox.trueish
        falsish = BooleanCheckbox.falsish
        if self.option_value not in trueish:
            trueish = (option_value, str(option_value)) + trueish
            falsish = tuple(set(falsish) - set([option_value, str(option_value)]))
        return BooleanCheckbox(trueish=trueish, falsish=falsish)


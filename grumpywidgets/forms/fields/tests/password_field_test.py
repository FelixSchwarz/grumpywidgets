# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.forms.fields import PasswordField
from grumpywidgets.forms.fields.test_support import InputFieldTestTemplate
from grumpywidgets.lib.pythonic_testcase import *


class PasswordFieldTest(InputFieldTestTemplate):
    __test__ = True
    
    field_class = PasswordField
    
    def test_has_string_validator_by_default(self):
        text_field = PasswordField()
        
        assert_not_none(text_field.validator)
        self.assert_error(text_field, [])
        assert_equals('foo', text_field.validate('foo').value)
    
    def assert_error(self, widget, input_):
        context = widget.validate(input_)
        assert_true(context.contains_errors())


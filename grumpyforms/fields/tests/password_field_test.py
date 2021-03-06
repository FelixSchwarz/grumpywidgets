# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pythonic_testcase import *

from grumpyforms.fields import PasswordField
from grumpyforms.fields.test_support import InputFieldTestTemplate


class PasswordFieldTest(InputFieldTestTemplate):
    __test__ = True

    field_class = PasswordField

    def test_has_string_validator_by_default(self):
        text_field = PasswordField()

        assert_not_none(text_field.validator)
        self.assert_error(text_field, [])
        self.assert_error(text_field, '')
        assert_equals('foo', text_field.validate('foo').value)

    def assert_error(self, widget, input_):
        context = widget.validate(input_)
        assert_true(context.contains_errors())


class GenshiPasswordFieldTest(PasswordFieldTest):
    template_engine = 'genshi'

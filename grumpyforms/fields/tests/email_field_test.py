# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pythonic_testcase import *

from grumpyforms.fields import EmailField
from grumpyforms.fields.test_support import InputFieldTestTemplate


class EmailFieldFieldTest(InputFieldTestTemplate):
    __test__ = True

    field_class = EmailField

    def test_has_email_validator_by_default(self):
        text_field = self.field

        assert_not_none(text_field.validator)
        self.assert_error(text_field, [])
        self.assert_error(text_field, '')
        self.assert_error(text_field, 'foo')
        assert_equals('foo@domain.example',
                      text_field.validate('foo@domain.example').value)

    def assert_error(self, widget, input_):
        context = widget.validate(input_)
        assert_true(context.contains_errors())


class GenshiEmailFieldFieldTest(EmailFieldFieldTest):
    template_engine = 'genshi'

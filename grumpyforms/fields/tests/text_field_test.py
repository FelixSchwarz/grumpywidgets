# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pythonic_testcase import *

from grumpyforms.fields import TextField
from grumpyforms.fields.test_support import InputFieldTestTemplate


class TextFieldTest(InputFieldTestTemplate):
    __test__ = True

    field_class = TextField

    def test_has_string_validator_by_default(self):
        text_field = TextField()

        assert_not_none(text_field.validator)
        context = text_field.validate([])
        assert_true(context.contains_errors())
        assert_none(text_field.validate('').value)


class GenshiTextFieldTest(TextFieldTest):
    template_engine = 'genshi'

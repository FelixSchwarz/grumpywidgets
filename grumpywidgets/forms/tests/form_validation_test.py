# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.errors import InvalidDataError
from pycerberus.validators.basic_numbers import IntegerValidator

from grumpywidgets.forms.api import Form
from grumpywidgets.forms.fields import TextField
from grumpywidgets.lib.pythonic_testcase import *


class FormValidationTest(PythonicTestCase):
    def test_can_validate_empty_form(self):
        assert_equals({}, Form().validate({}))
    
    def test_can_validate_form_with_single_widget(self):
        class SimpleForm(Form):
            children = (
                TextField('foo', validator=IntegerValidator()),
            )
        assert_equals({'foo': 42}, SimpleForm().validate({'foo': '42'}))
    
    def test_raises_validation_exception_which_contains_all_child_exceptions(self):
        class MultiChildrenForm(Form):
            children = (
                TextField('foo', validator=IntegerValidator()),
                TextField('bar', validator=IntegerValidator()),
            )
        form = MultiChildrenForm()
        e = assert_raises(InvalidDataError, lambda: form.validate({}))
        errors = e.error_dict()
        assert_equals(['foo', 'bar'], list(errors.keys()))
    
    def test_returns_only_validated_values(self):
        class FilteringForm(Form):
            children = (
                TextField('foo', validator=IntegerValidator()),
            )
        form = FilteringForm()
        assert_equals({'foo': 42}, form.validate({'foo': '42', 'bar': None}))


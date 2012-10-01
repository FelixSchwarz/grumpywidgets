# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.validators import IntegerValidator

from grumpywidgets.forms.api import Form
from grumpywidgets.forms.fields import TextField
from grumpywidgets.lib.pythonic_testcase import *


class FormValidationTest(PythonicTestCase):
    def test_can_validate_empty_form(self):
        result = Form().validate({})
        assert_equals({}, result.value)
    
    def test_can_validate_form_with_single_widget(self):
        form = Form(children = (TextField('foo', validator=IntegerValidator()),))
        result = form.validate({'foo': '42'})
        assert_equals({'foo': 42}, result.value)
    
    def test_returns_context_on_validation_error_which_contains_all_child_errors(self):
        class MultiChildrenForm(Form):
            children = (
                TextField('foo', validator=IntegerValidator()),
                TextField('bar', validator=IntegerValidator()),
            )
        form = MultiChildrenForm()
        
        result = form.validate({})
        assert_true(result.contains_errors())
        assert_equals(['foo', 'bar'], list(result.errors))
    
    def test_returns_only_validated_values(self):
        class FilteringForm(Form):
            children = (
                TextField('foo', validator=IntegerValidator()),
            )
        
        result = FilteringForm().validate({'foo': '42', 'bar': None})
        assert_false(result.contains_errors())
        assert_equals({'foo': 42}, result.value)


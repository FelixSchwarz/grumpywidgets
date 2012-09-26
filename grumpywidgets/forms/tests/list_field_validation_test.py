# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.errors import InvalidDataError
from pycerberus.validators.basic_numbers import IntegerValidator

from grumpywidgets.forms.fields import ListField, TextField
from grumpywidgets.lib.pythonic_testcase import *


class ListFieldValidationTest(PythonicTestCase):
    
    def setUp(self):
        number_field = TextField('number', validator=IntegerValidator(required=False))
        self.list_field = ListField('list', children=(number_field, ))
    
    def test_can_validate_empty_list_field(self):
        assert_equals((), ListField().validate([]))
    
    def test_can_validate_form_with_single_widget(self):
        assert_equals(({'number': 42}, ), self.list_field.validate([{'number': '42'}]))
        assert_equals(({'number': None}, ), self.list_field.validate([{}]))
        assert_equals(({'number': 42}, {'number': 21}), 
                      self.list_field.validate([{'number': '42'}, {'number': '21'}, ]))
    
    def test_returns_only_validated_values(self):
        input_ = [{'number': '42', 'invalid': 'evil'}]
        assert_equals(({'number': 42}, ), self.list_field.validate(input_))
    
    def test_raises_validation_exception_which_contains_all_child_exceptions(self):
        input_ = [{'number': '42'}, {'number': 'invalid'}, ]
        e = self.assert_error(self.list_field, input_)
        errors = e.unpack_errors()
        
        assert_length(2, errors)
        assert_none(errors[0])
        assert_not_none(errors[1])
    
    def test_can_store_exception_information_in_context(self):
        input_ = [{'number': 'abc'}, {'number': '2'}, {'number': 'foo'}, ]
        self.assert_error(self.list_field, input_)
        
        assert_length(3, self.list_field.context.children)
        first = self.list_field.context.children[0][0]
        assert_true(first.context.contains_errors())
        assert_equals('abc', first.context.unvalidated_value)
        
        second = self.list_field.context.children[1][0]
        assert_false(second.context.contains_errors())
        assert_equals('2', second.context.unvalidated_value)
        
        third = self.list_field.context.children[2][0]
        assert_true(third.context.contains_errors())
        assert_equals('foo', third.context.unvalidated_value)
    
    # --- helpers -------------------------------------------------------------
    
    def assert_error(self, widget, input_):
        e = assert_raises(InvalidDataError, lambda: widget.validate(input_))
        return e



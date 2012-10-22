# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.validators import IntegerValidator

from grumpyforms.fields import ListField, TextField
from grumpywidgets.lib.pythonic_testcase import *


class ListFieldValidationTest(PythonicTestCase):
    
    def setUp(self):
        number_field = TextField('number', validator=IntegerValidator(required=False))
        self.list_field = ListField('list', children=(number_field, ))
    
    def test_can_validate_empty_list_field(self):
        assert_equals((), ListField().validate([]).value)
    
    def test_can_validate_form_with_single_widget(self):
        assert_equals(({'number': 42}, ), 
                      self.list_field.validate([{'number': '42'}]).value)
        assert_equals(({'number': None}, ), self.list_field.validate([{}]).value)
        assert_equals(({'number': 42}, {'number': 21}), 
                      self.list_field.validate([{'number': '42'}, {'number': '21'}, ]).value)
    
    def test_returns_only_validated_values(self):
        input_ = [{'number': '42', 'invalid': 'evil'}]
        context = self.list_field.validate(input_)
        assert_equals(({'number': 42}, ), context.value)
    
    def test_returns_context_on_validation_error_which_contains_all_child_errors(self):
        input_ = [{'number': '42'}, {'number': 'invalid'}, ]
        result = self.list_field.validate(input_)
        
        assert_true(result.contains_errors())
        errors = result.errors
        
        assert_length(2, errors)
        assert_equals({'number': None}, errors[0])
        
        error = errors[1]
        assert_equals(['number'], list(error.keys()))
        assert_not_none(error['number'])


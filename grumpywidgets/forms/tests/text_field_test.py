# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.


from grumpywidgets.forms.fields import TextField
from grumpywidgets.lib.pythonic_testcase import *
from pycerberus.errors import InvalidDataError


class TextFieldTest(PythonicTestCase):
    def test_can_render_basic_textfield(self):
        assert_equals('<input type="text" />', TextField().display())
    
    def test_can_render_value(self):
        assert_equals('<input type="text" value="foo" />', 
                      TextField().display(u'foo'))
    
    def test_can_render_name(self):
        class NamedField(TextField):
            name = 'username'
        assert_equals('<input type="text" name="username" />', 
                      NamedField().display())
    
    def test_can_render_id(self):
        class IDField(TextField):
            id = 'text-id'
        assert_equals('<input type="text" id="text-id" />', 
                      IDField().display())
    
    def test_can_render_css_classes(self):
        class StyledField(TextField):
            css_classes = ('text', 'username')
        assert_equals('<input type="text" class="text username" />', 
                      StyledField().display())
    
    def test_has_string_validator_by_default(self):
        text_field = TextField()
        
        assert_not_none(text_field.validator)
        assert_raises(InvalidDataError, lambda: text_field.validate([]))
        assert_equals(None, text_field.validate(''))


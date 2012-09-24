# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.


from grumpywidgets.forms.fields import HiddenField
from grumpywidgets.lib.pythonic_testcase import *
from pycerberus.errors import InvalidDataError


class HiddenFieldTest(PythonicTestCase):
    def test_can_render_basic_hiddenfield(self):
        assert_equals('<input type="hidden" />', HiddenField().display())
    
    def test_can_render_value(self):
        assert_equals('<input type="hidden" value="foo" />', 
                      HiddenField().display(u'foo'))
    
    def test_can_render_name(self):
        assert_equals('<input type="hidden" name="username" />', 
                      HiddenField(name='username').display())
    
    def test_can_render_id(self):
        assert_equals('<input type="hidden" id="text-id" />', 
                      HiddenField(id='text-id').display())
    
    def test_can_render_css_classes(self):
        assert_equals('<input type="hidden" class="text username" />', 
                      HiddenField(css_classes = ('text', 'username')).display())
    
    def test_has_string_validator_by_default(self):
        text_field = HiddenField()
        
        assert_not_none(text_field.validator)
        assert_raises(InvalidDataError, lambda: text_field.validate([]))
        assert_raises(InvalidDataError, lambda: text_field.validate([]))
        assert_equals('foo', text_field.validate('foo'))


from grumpyforms.fields import SelectField
from grumpywidgets.lib.pythonic_testcase import *

class SelectFieldTest(PythonicTestCase):
    def test_can_render_basic_field(self):
        expected = '<select>\n</select>'
        assert_equals(expected, SelectField().display())
    
    def test_can_render_basic_with_options(self):
        expected = '<select>\n<option value="a">1</option>\n<option value="b">foo</option>\n</select>'
        assert_equals(expected, SelectField(options=(['a', '1'], ['b', 'foo'])).display())
    
    def test_can_render_value(self):
        expected = '<select>\n<option value="a" selected="selected">1</option>\n</select>'
        assert_equals(expected, SelectField(options=[['a', '1']]).display(u'a'))
    
    def test_can_render_name(self):
        select = SelectField(name='type')
        expected = '<select name="type">\n</select>'
        assert_equals(expected, select.display())
    
    def test_can_render_id(self):
        select = SelectField(id='text-id')
        expected = '<select id="text-id">\n</select>'
        assert_equals(expected, select.display())
    
    def test_can_render_css_classes(self):
        select = SelectField(css_classes=('text', 'username'))
        expected = '<select class="text username">\n</select>'
        assert_equals(expected, select.display())
    
    def test_has_one_of_validator_by_default(self):
        select = SelectField(options=[['a', '1']])
        
        assert_not_none(select.validator)
        assert_true(select.validate('c').contains_errors())
        assert_false(select.validate('a').contains_errors())
        assert_equals(u'a', select.validate('a').value)

        
# TODO:
# multiple=True, in which case value should be an array? 

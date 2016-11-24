# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pythonic_testcase import *
from pycerberus.lib.attribute_dict import AttrDict

from grumpyforms.fields import SelectField
from grumpywidgets.testhelpers import assert_same_html, template_widget


class SelectFieldTest(PythonicTestCase):
    template_engine = 'jinja2'

    def _selectfield(self, **kwargs):
        return template_widget(SelectField, self.template_engine, kwargs)

    def test_can_render_basic_field(self):
        expected = '<select>\n</select>'
        assert_same_html(expected, self._selectfield().display())

    def test_can_render_basic_with_options(self):
        expected = '<select>\n<option value="a">1</option>\n<option value="b">foo</option>\n</select>'
        assert_same_html(expected, self._selectfield(options=(['a', '1'], ['b', 'foo'])).display())

    def test_can_render_value(self):
        expected = '<select>\n<option value="a" selected="selected">1</option>\n</select>'
        assert_same_html(expected, self._selectfield(options=[['a', '1']]).display(u'a'))

    def test_can_render_name(self):
        select = self._selectfield(name='type')
        expected = '<select name="type">\n</select>'
        assert_same_html(expected, select.display())

    def test_can_render_id(self):
        select = self._selectfield(id='text-id')
        expected = '<select id="text-id">\n</select>'
        assert_same_html(expected, select.display())

    def test_can_render_css_classes(self):
        select = self._selectfield(css_classes=('text', 'username'))
        expected = '<select class="text username">\n</select>'
        assert_same_html(expected, select.display())

    def test_has_one_of_validator_by_default(self):
        select = self._selectfield(options=[['a', '1']])

        assert_not_none(select.validator)
        assert_true(select.validate('c').contains_errors())
        assert_false(select.validate('a').contains_errors())
        assert_equals(u'a', select.validate('a').value)

    def test_can_configure_custom_validator(self):
        validator = AttrDict(
            revert_conversion=lambda value, context=None: 'a',
        )
        select = self._selectfield(options=[('a', '1'),], validator=validator)

        expected = '<select>\n<option value="a" selected="selected">1</option>\n</select>'
        assert_same_html(expected, select.display(u'foo'))
        assert_same_html(expected, select.display(u'bar'))

    def test_can_override_attributes_in_display(self):
        select = self._selectfield(name='foo')
        expected = '<select name="bar">\n</select>'
        assert_same_html(expected, select.display(name='bar'))


class GenshiSelectFieldTest(SelectFieldTest):
    template_engine = 'genshi'

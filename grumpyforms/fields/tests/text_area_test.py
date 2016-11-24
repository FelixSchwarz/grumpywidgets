# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pythonic_testcase import *

from grumpyforms.fields import TextArea
from grumpywidgets.testhelpers import assert_same_html, template_widget


class TextAreaTest(PythonicTestCase):
    template_engine = 'jinja2'

    def _textarea(self, **kwargs):
        return template_widget(TextArea, self.template_engine, kwargs)

    def test_can_render_basic_field(self):
        expected = '<textarea cols="50" rows="10"></textarea>'
        assert_same_html(expected, self._textarea().display())

    def test_can_render_value(self):
        expected = '<textarea cols="50" rows="10">foo</textarea>'
        assert_same_html(expected, self._textarea().display(u'foo'))

    def test_can_render_name(self):
        text_area = self._textarea(name='username')
        expected = '<textarea name="username" cols="50" rows="10"></textarea>'
        assert_same_html(expected, text_area.display())

    def test_can_render_id(self):
        text_area = self._textarea(id='text-id')
        expected = '<textarea id="text-id" cols="50" rows="10"></textarea>'
        assert_same_html(expected, text_area.display())

    def test_can_render_css_classes(self):
        text_area = self._textarea(css_classes=('text', 'username'))
        expected = '<textarea cols="50" rows="10" class="text username"></textarea>'
        assert_same_html(expected, text_area.display())

    def test_has_string_validator_by_default(self):
        text_area = self._textarea()

        assert_not_none(text_area.validator)
        context = text_area.validate([])
        assert_true(context.contains_errors())
        assert_none(text_area.validate('').value)
        assert_equals(u'foo\nbar', text_area.validate('foo\nbar').value)

    def test_can_specify_field_size(self):
        text_area = self._textarea(cols=20, rows=10)
        expected = '<textarea cols="20" rows="10"></textarea>'
        assert_same_html(expected, text_area.display())

    def test_can_override_attributes_in_display(self):
        text_area = self._textarea(name='username')
        expected = '<textarea name="foobar" cols="50" rows="10"></textarea>'
        assert_same_html(expected, text_area.display(name='foobar'))


class GenshiTextAreaTest(TextAreaTest):
    template_engine = 'genshi'

# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpyforms.fields import TextArea
from grumpywidgets.lib.pythonic_testcase import *


class TextAreaTest(PythonicTestCase):
    def test_can_render_basic_field(self):
        expected = '<textarea cols="50" rows="10"></textarea>'
        assert_equals(expected, TextArea().display())

    def test_can_render_value(self):
        expected = '<textarea cols="50" rows="10">foo</textarea>'
        assert_equals(expected, TextArea().display(u'foo'))

    def test_can_render_name(self):
        text_area = TextArea(name='username')
        expected = '<textarea name="username" cols="50" rows="10"></textarea>'
        assert_equals(expected, text_area.display())

    def test_can_render_id(self):
        text_area = TextArea(id='text-id')
        expected = '<textarea id="text-id" cols="50" rows="10"></textarea>'
        assert_equals(expected, text_area.display())

    def test_can_render_css_classes(self):
        text_area = TextArea(css_classes=('text', 'username'))
        expected = '<textarea cols="50" rows="10" class="text username"></textarea>'
        assert_equals(expected, text_area.display())

    def test_has_string_validator_by_default(self):
        text_area = TextArea()

        assert_not_none(text_area.validator)
        context = text_area.validate([])
        assert_true(context.contains_errors())
        assert_none(text_area.validate('').value)
        assert_equals(u'foo\nbar', text_area.validate('foo\nbar').value)

    def test_can_specify_field_size(self):
        text_area = TextArea(cols=20, rows=10)
        expected = '<textarea cols="20" rows="10"></textarea>'
        assert_equals(expected, text_area.display())


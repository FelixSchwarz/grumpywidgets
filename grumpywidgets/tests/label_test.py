# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pythonic_testcase import *

from grumpywidgets.testhelpers import template_widget
from grumpywidgets.widgets import Label


class LabelRenderingTest(PythonicTestCase):
    template_engine = 'jinja2'

    def _label(self, **kwargs):
        return template_widget(Label, self.template_engine, kwargs)

    def test_can_render_basic_label(self):
        assert_equals('<label></label>', self._label().display())

    def test_can_render_label_text(self):
        assert_equals('<label>Some text</label>', self._label().display('Some text'))
        assert_equals('<label>Some text</label>',
                      self._label(value='Some text').display())

    def test_can_render_label_id(self):
        id_label = self._label(id='label-id')
        assert_equals('<label id="label-id"></label>', id_label.display())

    def test_can_render_css_classes(self):
        styled_label = self._label(css_classes=('foo', 'bar'))
        assert_equals('<label class="foo bar">text</label>',
                      styled_label.display('text'))

    def test_can_render_for_attribute(self):
        for_label = self._label(for_='username')
        assert_equals('<label for="username">text</label>',
                      for_label.display('text'))

# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pythonic_testcase import *

from grumpyforms.fields import Checkbox
from grumpywidgets.testhelpers import assert_same_html, template_widget



class CheckboxRenderingTest(PythonicTestCase):
    template_engine = 'jinja2'

    def _checkbox(self, **kwargs):
        return template_widget(Checkbox, self.template_engine, kwargs)

    def test_can_render_unchecked_checkbox(self):
        assert_same_html('<input type="checkbox" />', self._checkbox().display())
        assert_same_html('<input type="checkbox" />', self._checkbox().display(None))
        assert_same_html('<input type="checkbox" />', self._checkbox().display(''))
        assert_same_html('<input type="checkbox" />', self._checkbox().display(False))

    def test_can_render_checked_state(self):
        checkbox = self._checkbox()
        checked_html = '<input type="checkbox" checked="checked" />'
        assert_same_html(checked_html, checkbox.display(u'on'))
        assert_same_html(checked_html, checkbox.display(True))

    def test_can_render_option_value(self):
        checkbox = self._checkbox(option_value='foo')
        checked_html = '<input type="checkbox" value="foo" checked="checked" />'
        assert_same_html(checked_html, checkbox.display(value=True))
        assert_same_html(checked_html, checkbox.display(value='foo'),
            message='validator should also accept the "option_value" as trueish')

    def test_can_use_falsish_values_as_true(self):
        checkbox = self._checkbox(option_value=0)
        checked_html = '<input type="checkbox" value="0" checked="checked" />'
        unchecked_html = '<input type="checkbox" value="0" />'
        assert_same_html(unchecked_html, checkbox.display(value=None))
        assert_same_html(unchecked_html, checkbox.display(value=False))
        assert_same_html(checked_html, checkbox.display(value=0))
        assert_same_html(checked_html, checkbox.display(value='0'))
        assert_same_html(checked_html, checkbox.display(value=True))
        assert_same_html(checked_html, checkbox.display(value='True'))

    def test_can_render_checkbox_name(self):
        assert_same_html('<input type="checkbox" name="foo" />',
                         self._checkbox(name='foo').display())

    def test_can_render_checkbox_id(self):
        assert_same_html('<input type="checkbox" id="foo-id" />',
                         self._checkbox(id='foo-id').display())

    def test_can_render_css_classes(self):
        assert_same_html('<input type="checkbox" class="checkbox send" />',
                         self._checkbox(css_classes = ('checkbox', 'send')).display())


class GenshiCheckboxRenderingTest(CheckboxRenderingTest):
    template_engine = 'genshi'

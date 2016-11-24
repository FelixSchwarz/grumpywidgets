# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pythonic_testcase import *

from grumpyforms.fields import Radiobutton
from grumpywidgets.testhelpers import assert_same_html, template_widget



class RadiobuttonRenderingTest(PythonicTestCase):
    template_engine = 'jinja2'

    def _radiobutton(self, **kwargs):
        return template_widget(Radiobutton, self.template_engine, kwargs)

    def test_can_render_unchecked_radiobutton(self):
        assert_same_html('<input type="radio" />', self._radiobutton().display())
        assert_same_html('<input type="radio" />', self._radiobutton().display(None))
        assert_same_html('<input type="radio" />', self._radiobutton().display(''))
        assert_same_html('<input type="radio" />', self._radiobutton().display(False))

    def test_can_render_checked_state(self):
        radiobutton = self._radiobutton()
        checked_html = '<input type="radio" checked="checked" />'
        assert_same_html(checked_html, radiobutton.display(u'on'))
        assert_same_html(checked_html, radiobutton.display(True))

    def test_can_render_option_value(self):
        radiobutton = self._radiobutton(option_value='foo')
        checked_html = '<input type="radio" value="foo" checked="checked" />'
        assert_same_html(checked_html, radiobutton.display(value=True))
        assert_same_html(checked_html, radiobutton.display(value='foo'),
            message='validator should also accept the "option_value" as trueish')

    def test_can_use_falsish_values_as_true(self):
        radiobutton = self._radiobutton(option_value=0)
        checked_html = '<input type="radio" value="0" checked="checked" />'
        unchecked_html = '<input type="radio" value="0" />'
        assert_same_html(unchecked_html, radiobutton.display(value=None))
        assert_same_html(unchecked_html, radiobutton.display(value=False))
        assert_same_html(checked_html, radiobutton.display(value=0))
        assert_same_html(checked_html, radiobutton.display(value='0'))
        assert_same_html(checked_html, radiobutton.display(value=True))
        assert_same_html(checked_html, radiobutton.display(value='True'))

    def test_can_render_radiobutton_name(self):
        assert_same_html('<input type="radio" name="foo" />',
                         self._radiobutton(name='foo').display())

    def test_can_render_radiobutton_id(self):
        assert_same_html('<input type="radio" id="foo-id" />',
                         self._radiobutton(id='foo-id').display())

    def test_can_render_css_classes(self):
        assert_same_html('<input type="radio" class="radio send" />',
                         self._radiobutton(css_classes = ('radio', 'send')).display())

    def test_can_override_attributes_in_display(self):
        radiobutton = self._radiobutton(name='username')
        expected = '<input type="radio" name="foobar" />'
        assert_same_html(expected, radiobutton.display(name='foobar'))

    def test_can_add_custom_attributes_via_display(self):
        radiobutton = self._radiobutton()
        expected = '<input type="radio" style="margin-top: 10px"/>'
        assert_same_html(expected, radiobutton.display(attrs={'style': 'margin-top: 10px'}))


class GenshiCheckboxRenderingTest(RadiobuttonRenderingTest):
    template_engine = 'genshi'

# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.


from grumpyforms.fields import Checkbox
from grumpywidgets.lib.pythonic_testcase import *


class CheckboxRenderingTest(PythonicTestCase):
    def test_can_render_unchecked_checkbox(self):
        assert_equals('<input type="checkbox" />', Checkbox().display())
        assert_equals('<input type="checkbox" />', Checkbox().display(None))
        assert_equals('<input type="checkbox" />', Checkbox().display(''))
        assert_equals('<input type="checkbox" />', Checkbox().display(False))

    def test_can_render_checked_state(self):
        checkbox = Checkbox()
        checked_html = '<input type="checkbox" checked="checked" />'
        assert_equals(checked_html, checkbox.display(u'on'))
        assert_equals(checked_html, checkbox.display(True))

    def test_can_render_checkbox_name(self):
        assert_equals('<input type="checkbox" name="foo" />',
                      Checkbox(name='foo').display())

    def test_can_render_checkbox_id(self):
        assert_equals('<input type="checkbox" id="foo-id" />',
                      Checkbox(id='foo-id').display())

    def test_can_render_css_classes(self):
        assert_equals('<input type="checkbox" class="checkbox send" />',
                      Checkbox(css_classes = ('checkbox', 'send')).display())


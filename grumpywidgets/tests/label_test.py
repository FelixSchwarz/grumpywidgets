# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.widgets import Label
from grumpywidgets.lib.pythonic_testcase import *


class LabelRenderingTest(PythonicTestCase):
    def test_can_render_basic_label(self):
        label = Label()
        assert_equals('<label></label>', label.display())
    
    def test_can_render_label_text(self):
        assert_equals('<label>Some text</label>', Label().display('Some text'))
        assert_equals('<label>Some text</label>', 
                      Label(value='Some text').display())
    
    def test_can_render_label_id(self):
        id_label = Label(id='label-id')
        assert_equals('<label id="label-id"></label>', id_label.display())
    
    def test_can_render_css_classes(self):
        styled_label = Label(css_classes=('foo', 'bar'))
        assert_equals('<label class="foo bar">text</label>', 
                      styled_label.display('text'))
    
    def test_can_render_for_attribute(self):
        for_label = Label(for_='username')
        assert_equals('<label for="username">text</label>', 
                      for_label.display('text'))

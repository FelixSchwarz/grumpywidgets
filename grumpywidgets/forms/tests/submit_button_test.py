# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.


from grumpywidgets.forms.fields import SubmitButton
from grumpywidgets.lib.pythonic_testcase import *


class SubmitButtonRenderingTest(PythonicTestCase):
    def test_can_render_basic_button(self):
        assert_equals('<input type="submit" />', SubmitButton().display())
        assert_equals('<input type="submit" />', SubmitButton().display(None))
        assert_equals('<input type="submit" />', SubmitButton().display(''))
    
    def test_can_render_button_with_custom_value(self):
        assert_equals('<input type="submit" value="Send" />', 
                      SubmitButton().display(u'Send'))
    
    def test_can_set_static_display_value(self):
        class LabelButton(SubmitButton):
            value = 'Send me'
        assert_equals('<input type="submit" value="Send me" />', 
                      LabelButton().display(None))
        assert_equals('<input type="submit" value="Send me" />', 
                      LabelButton().display('garbage'))
    
    def test_can_render_button_name(self):
        class NamedButton(SubmitButton):
            name = 'submitter'
        assert_equals('<input type="submit" name="submitter" />', 
                      NamedButton().display())
    
    def test_can_render_button_id(self):
        class IDButton(SubmitButton):
            id = 'submit-id'
        assert_equals('<input type="submit" id="submit-id" />', 
                      IDButton().display())
    
    def test_can_render_css_classes(self):
        class StyledButton(SubmitButton):
            css_classes = ('button', 'send')
        assert_equals('<input type="submit" class="button send" />', 
                      StyledButton().display())


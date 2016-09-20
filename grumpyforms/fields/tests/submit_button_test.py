# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pythonic_testcase import *

from grumpyforms.fields import SubmitButton
from grumpywidgets.testhelpers import assert_same_html, template_widget


class SubmitButtonTest(PythonicTestCase):
    def test_can_tell_about_classification(self):
        widget = SubmitButton()
        assert_false(widget.is_field())
        assert_true(widget.is_button())
        assert_false(widget.is_hidden())


class SubmitButtonRenderingTest(PythonicTestCase):
    template_engine = 'jinja2'

    def _submitbutton(self, **kwargs):
        return template_widget(SubmitButton, self.template_engine, kwargs)

    def test_can_render_basic_button(self):
        assert_same_html('<input type="submit" />', self._submitbutton().display())
        assert_same_html('<input type="submit" />', self._submitbutton().display(None))
        assert_same_html('<input type="submit" />', self._submitbutton().display(''))

    def test_can_render_button_with_custom_value(self):
        assert_same_html('<input type="submit" value="Send" />',
                         self._submitbutton().display(u'Send'))

    def test_can_set_static_display_value(self):
        class LabelButton(SubmitButton):
            value = 'Send me'
        label_button = template_widget(LabelButton, self.template_engine, {})
        assert_same_html('<input type="submit" value="Send me" />',
                         label_button.display(None))
        assert_same_html('<input type="submit" value="Send me" />',
                         label_button.display('garbage'))

    def test_can_render_button_name(self):
        class NamedButton(SubmitButton):
            name = 'submitter'
        named_button = template_widget(NamedButton, self.template_engine, {})
        assert_same_html('<input type="submit" name="submitter" />',
                         named_button.display())

    def test_can_render_button_id(self):
        class IDButton(SubmitButton):
            id = 'submit-id'
        id_button = template_widget(IDButton, self.template_engine, {})
        assert_same_html('<input type="submit" id="submit-id" />',
                         id_button.display())

    def test_can_render_css_classes(self):
        class StyledButton(SubmitButton):
            css_classes = ('button', 'send')
        styled_button = template_widget(StyledButton, self.template_engine, {})
        assert_same_html('<input type="submit" class="button send" />',
                         styled_button.display())


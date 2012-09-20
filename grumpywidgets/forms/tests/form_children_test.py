# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

import re

from pycerberus.errors import InvalidDataError
from pycerberus.validators import IntegerValidator

from grumpywidgets.forms.api import Form
from grumpywidgets.forms.buttons import SubmitButton
from grumpywidgets.forms.fields import TextField
from grumpywidgets.lib.pythonic_testcase import *


class FormChildrenRenderingTest(PythonicTestCase):
    def setUp(self):
        class SimpleForm(Form):
            children = (TextField('number', validator=IntegerValidator()), )
        self.form = SimpleForm()
    
    def test_can_render_single_child(self):
        expected = '<div class="fieldcontainer"><input type="text" name="number" /></div>'
        self.assert_child_html(expected, self.form.display({}), 
                               strip_container=False)
    
    def test_can_pass_values_to_children(self):
        class SimpleForm(Form):
            children = (
                SubmitButton('submit'),
            )
        expected = '<input type="text" name="number" value="send" />'
        self.assert_child_html(expected, self.form.display({'number': 'send'}))
    
    def test_raises_error_if_unknown_parameters_are_passed_for_display(self):
        e = assert_raises(ValueError, lambda: Form().display({'invalid': None}))
        assert_equals("Unknown parameter 'invalid' passed to display()", 
                      e.args[0])
    
    def test_can_display_errors_for_children(self):
        textfield = self.form.children[0]
        # simulate failed validation
        textfield.context.errors = (InvalidDataError('bad input', 'abc'),)
        assert_true(textfield.context.contains_errors())
        
        expected = u'<input type="text" name="number" />' + \
            '<span class="fielderror">bad input</span>'
        self.assert_child_html(expected, self.form.display())
    
    def assert_child_html(self, expected, rendered_form, strip_container=True):
        match = re.search('<form[^>]*>\s*(.+)\s*</form>', rendered_form.replace('\n', ''))
        child_html = match.group(1)
        if strip_container:
            match = re.search('<div[^>]*>\s*(.+)\s*</div>', child_html)
            child_html = match.group(1)
        assert_equals(expected, child_html)
    
    def test_can_redisplay_previous_values_after_failed_validation(self):
        assert_raises(InvalidDataError, lambda: self.form.validate({'number': 'abc'}))
        expected = u'<input type="text" name="number" value="abc" />' + \
            '<span class="fielderror">Please enter a number.</span>'
        self.assert_child_html(expected, self.form.display())
    
    def test_can_display_child_label(self):
        self.form.children[0].label = 'items'
        
        expected = '<label>items</label><input type="text" name="number" />'
        self.assert_child_html(expected, self.form.display())


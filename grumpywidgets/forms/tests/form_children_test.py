# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.


from grumpywidgets.forms.api import Form
from grumpywidgets.lib.pythonic_testcase import *
from grumpywidgets.forms.buttons import SubmitButton


class FormChildrenRenderingTest(PythonicTestCase):
    def test_can_render_single_child(self):
        class SimpleForm(Form):
            children = (
                SubmitButton('submit'),
            )
        expected = u'<form action="" method="POST" accept-charset="UTF-8">' + \
            '<input type="submit" name="submit" />' + \
            '</form>'
        rendered = SimpleForm().display({}).replace('\n', '')
        assert_equals(expected, rendered)
    
    def test_can_pass_values_to_children(self):
        class SimpleForm(Form):
            children = (
                SubmitButton('submit'),
            )
        expected = u'<form action="" method="POST" accept-charset="UTF-8">' + \
            '<input type="submit" name="submit" value="send" />' + \
            '</form>'
        rendered = SimpleForm().display({'submit': 'send'}).replace('\n', '')
        assert_equals(expected, rendered)
    
    def test_raises_error_if_unknown_parameters_are_passed_for_display(self):
        e = assert_raises(ValueError, lambda: Form().display({'invalid': None}))
        assert_equals("Unknown parameter 'invalid' passed to display()", 
                      e.args[0])


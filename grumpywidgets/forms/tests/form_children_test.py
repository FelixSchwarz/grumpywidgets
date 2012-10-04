# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.forms.api import Form
from grumpywidgets.forms.fields import TextField
from grumpywidgets.lib.pythonic_testcase import *


class FormChildrenInitializationTest(PythonicTestCase):
    def setUp(self):
        class SimpleForm(Form):
            children = (TextField('number'), )
        self.form = SimpleForm()
    
    def test_sets_parent_parameter_on_its_children(self):
        assert_equals(self.form, self.form.children[0].parent)



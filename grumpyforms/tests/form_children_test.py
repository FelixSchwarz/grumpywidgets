# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpyforms.api import Form
from grumpyforms.fields import TextField
from grumpywidgets.lib.pythonic_testcase import *


class FormChildrenInitializationTest(PythonicTestCase):
    class ChildForm(Form):
        children=(TextField('number'), )

    def setUp(self):
        self.form = self.ChildForm()

    def test_sets_parent_parameter_on_its_children(self):
        assert_equals(self.form, self.form.children[0].parent)

    def test_child_instances_are_not_shared_between_form_instances(self):
        second = self.ChildForm()

        self.form.children[0].name = 'foo'
        assert_equals('number', second.children[0].name)

    def test_creates_new_child_instances_on_copy(self):
        second = self.form.copy()

        self.form.children[0].name = 'foo'
        assert_equals('number', second.children[0].name)



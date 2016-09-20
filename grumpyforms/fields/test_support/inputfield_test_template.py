# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.lib.pythonic_testcase import *


__all__ = ['InputFieldTestTemplate']

class InputFieldTestTemplate(PythonicTestCase):
    # prevents nose from picking up this 'TestCase'
    __test__ = False

    field_class = None

    def setUp(self):
        self._field = None

    def test_can_render_basic_field(self):
        expected = '<input type="%s" />' % self.field.type
        assert_equals(expected, self.field.display())

    def test_can_render_value(self):
        expected = '<input type="%s" value="foo" />' % self.field.type
        assert_equals(expected, self.field.display(u'foo'))

    def test_can_render_name(self):
        self.set_field(self.field_class(name='username'))
        expected = '<input type="%s" name="username" />' % self.field.type
        assert_equals(expected, self.field.display())

    def test_can_render_id(self):
        self.set_field(self.field_class(id='text-id'))
        expected = '<input type="%s" id="text-id" />' % self.field.type
        assert_equals(expected, self.field.display())

    def test_can_render_css_classes(self):
        self.set_field(self.field_class(css_classes = ('text', 'username')))
        expected = '<input type="%s" class="text username" />' % self.field.type
        assert_equals(expected, self.field.display())

    # --- helpers -------------------------------------------------------------

    @property
    def field(self):
        if (self._field is None) and (self.field_class is not None):
            self.set_field(self.field_class())
        return self._field

    def set_field(self, a_field):
        self._field = a_field


# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.errors import InvalidDataError

from grumpywidgets.context import Context, CompoundContext, RepeatingContext
from grumpywidgets.lib.pythonic_testcase import *


class RepeatingContextTest(PythonicTestCase):

    def setUp(self):
        self.context = RepeatingContext(lambda: None)
        self.context.items = [Context(value='foo'), Context(value='bar')]

    # --- errors --------------------------------------------------------------

    def test_can_tell_if_child_contains_errors(self):
        assert_false(self.context.contains_errors())

        self.context.items[1].errors = (self.error(),)
        assert_true(self.context.contains_errors())

    # --- aggregate values ----------------------------------------------------

    def test_can_return_repeated_values(self):
        assert_equals(('foo', 'bar'), self.context.value)

    def test_can_return_values_from_nested_containers(self):
        complex_child = CompoundContext()
        complex_child.children = {'baz': Context(value='qux')}
        self.context.items = [complex_child]

        assert_equals(({'baz': 'qux'}, ), self.context.value)

    def test_can_return_repeated_errors(self):
        errors = (self.error(), )
        self.context.items[1].errors = errors

        assert_equals((None, errors), self.context.errors)

    def test_can_return_unvalidated_values(self):
        self.context.items[1].unvalidated_value = 'foo'

        assert_equals((None, 'foo'), self.context.unvalidated_value)

    # --- update values -------------------------------------------------------

    def test_can_set_new_values(self):
        values = ('baz', 'qox')
        self.context.update_value(values)

        assert_equals(values, self.context.value)

    def test_can_add_new_items_if_not_previously_set(self):
        values = ('foo', '42')
        self.context.update_value(values)

        assert_length(2, self.context.value)

    def test_raises_assertion_error_if_existing_length_does_not_match_given_values(self):
        assert_length(2, self.context.items)

        assert_raises(AssertionError, lambda: self.context.update_value(('foo', )))

    def test_can_set_unvalidated_values(self):
        values = ('foo', '42')
        self.context.update_value(unvalidated_value=values)

        assert_equals(values, self.context.unvalidated_value)

    def test_can_set_errors(self):
        values = (None, ('too big', 'not applicable'))
        self.context.update_value(errors=values)

        assert_equals(values, self.context.errors)

    def test_can_set_complex_value(self):
        complex_child = CompoundContext()
        complex_child.children = {'baz': Context(value='qux')}
        self.context.items = [complex_child]

        input_ = ({'baz': 'foo'}, )
        self.context.update_value(input_)
        assert_equals(input_, self.context.value)

    # --- helpers -------------------------------------------------------------

    def error(self, message='bad input', value=None):
        return InvalidDataError(message, value)

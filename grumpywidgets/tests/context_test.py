# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.errors import InvalidDataError
from pythonic_testcase import *

from grumpywidgets.context import FieldData


class FieldDataTest(PythonicTestCase):

    def setUp(self):
        self.context = FieldData()

    def error(self, message='bad input', value=None):
        return InvalidDataError(message, value)

    def test_can_set_attributes_during_initialization(self):
        assert_equals(5, FieldData(value=5).value)

        error = self.error()
        assert_equals([error], FieldData(errors=[error]).errors)

        assert_equals('42', FieldData(initial_value='42').initial_value)


    def test_can_clone_itself(self):
        self.context.value = {}
        self.context.errors = []

        clone = self.context.copy()
        clone.errors.append('new error')
        clone.value['new'] = 21

        assert_equals({}, self.context.value)
        assert_equals([], self.context.errors)
        assert_equals({'new': 21}, clone.value)
        assert_equals(['new error'], clone.errors)

    def test_knows_if_context_contains_errors(self):
        self.context.errors = None
        assert_false(self.context.contains_errors())

        self.context.errors = []
        assert_false(self.context.contains_errors())

        self.context.errors = (self.error(),)
        assert_true(self.context.contains_errors())

    def test_can_set_new_value(self):
        self.context.update_value('bar')

        assert_equals('bar', self.context.value)

    def test_can_set_unvalidated_attribute_when_updating_values(self):
        context = FieldData()
        context.update_value(initial_value='42')

        assert_equals('42', context.initial_value)

    def test_can_set_errors_attribute_when_updating_values(self):
        context = FieldData()
        context.update_value(errors=(4,))

        assert_equals((4,), context.errors)

    def test_single_error_is_converted_to_list(self):
        context = FieldData()
        context.update_value(errors=4)

        assert_equals((4,), context.errors)



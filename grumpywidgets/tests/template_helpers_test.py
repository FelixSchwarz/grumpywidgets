# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.errors import InvalidDataError
from pycerberus.lib.form_data import FieldData, RepeatingFieldData
from pythonic_testcase import *

from grumpywidgets import template_helpers as h


class TemplateHelpersTest(PythonicTestCase):
    def test_render_class(self):
        assert_equals(None, h.render_class([]))
        assert_equals('foo bar', h.render_class(['foo', 'bar']))

    # --- error_messages() ----------------------------------------------------

    def test_can_call_render_errors_if_no_error_occured(self):
        context = FieldData()
        assert_false(context.contains_errors())
        assert_equals((), h.error_messages(FieldData()))

        context.errors = []
        assert_equals((), h.error_messages(FieldData()))

    def test_can_render_single_error(self):
        context = FieldData(errors=(self.error(),))
        assert_equals(('bad input',), h.error_messages(context))

    def test_can_render_multiple_errors(self):
        errors = (self.error(), self.error(message='check failed'))
        context = FieldData(errors=errors)
        assert_equals(('bad input', 'check failed'), h.error_messages(context))

    def test_ignores_error_dict(self):
        # if 'errors' contains a dict, assume the errors refer to child widgets
        # which will be rendered later
        # usually 'context' would be a FormData in this case but it's
        # just easier to instantiate a basic FieldData for testing
        context = FieldData(errors=dict(foo=self.error()))
        assert_equals((), h.error_messages(context))

        # e.g. a ListField
        repeating_context = RepeatingFieldData(None)
        repeating_context.items = (context, )
        assert_equals((), h.error_messages(repeating_context))

    # --- helpers -------------------------------------------------------------

    def error(self, message='bad input', value=None):
        return InvalidDataError(message, value)


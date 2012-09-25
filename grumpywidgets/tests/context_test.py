# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.errors import InvalidDataError

from grumpywidgets.api import Context
from grumpywidgets.lib.pythonic_testcase import *


class ContextTest(PythonicTestCase):
    
    def setUp(self):
        self.context = Context()
    
    def error(self, message='bad input', value=None):
        return InvalidDataError(message, value)
    
    def test_can_set_attributes_during_initialization(self):
        assert_equals(5, Context(value=5).value)
        
        error = self.error()
        assert_equals([error], Context(errors=[error]).errors)
    
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
    
    def test_can_call_render_errors_if_no_error_occured(self):
        assert_false(self.context.contains_errors())
        assert_equals((), self.context.rendered_errors())
        
        self.context.errors = []
        assert_equals((), self.context.rendered_errors())
    
    def test_can_render_single_error(self):
        self.context.errors = (self.error(),)
        assert_equals(('bad input',), self.context.rendered_errors())
    
    def test_can_render_multiple_errors(self):
        self.context.errors = (self.error(), self.error(message='check failed'))
        assert_equals(('bad input', 'check failed'), self.context.rendered_errors())



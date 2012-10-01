# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.errors import InvalidDataError

from grumpywidgets.context import Context, CompoundContext, RepeatingContext
from grumpywidgets.lib.pythonic_testcase import *


class CompoundContextTest(PythonicTestCase):
    
    def setUp(self):
        self.context = CompoundContext()
        self.context.children.update({
            'foo': Context(value='foo'),
            'bar': Context(value=2, unvalidated_value='2'),
        })
    
    def test_can_access_children_as_attributes(self):
        foo = self.context.children['foo']
        assert_equals(foo, self.context.foo)
        
        assert_raises(AttributeError, lambda: self.context.invalid)
    
    def test_can_copy_itself(self):
        copied_context = self.context.copy()
        del self.context.children['foo']
        self.context.bar.value = 5
        
        assert_equals(['bar'], list(self.context.children))
        assert_equals(5, self.context.bar.value)
        
        assert_equals(['foo', 'bar'], list(copied_context.children))
        assert_equals(2, copied_context.bar.value)
    
    # --- errors --------------------------------------------------------------
    
    def test_can_tell_if_child_contains_errors(self):
        assert_false(self.context.contains_errors())
        
        self.context.foo.errors = (self.error(),)
        assert_true(self.context.contains_errors())
    
    def test_can_tell_if_container_child_contains_errors(self):
        child_container = CompoundContext()
        child_container.children = {'baz': Context(errors=(self.error(), ))}
        assert_true(child_container.contains_errors())
        
        self.context.children['complex'] = child_container
        assert_true(self.context.contains_errors())
    
    def test_can_detect_errors_for_repeated_children(self):
        repeated_context = RepeatingContext(None)
        repeated_context.items = [Context(value=1), Context(errors=(self.error(),))]
        self.context.children['items'] = repeated_context
        
        assert_true(self.context.contains_errors())
    
    # --- aggregate values ----------------------------------------------------
    
    def test_can_return_repeated_values(self):
        repeating_context = RepeatingContext(None)
        repeating_context.items = [Context(value=1), Context(value=None)]
        self.context.children = {'items': repeating_context}
        assert_equals((1, None), self.context.value['items'])
    
    def test_can_return_values_from_nested_containers(self):
        complex_child = CompoundContext()
        complex_child.children = {'baz': Context(value='qux')}
        self.context.children['complex'] = complex_child
        
        assert_equals({'baz': 'qux'}, self.context.value['complex'])
    
    def test_can_return_errors_from_nested_containers(self):
        errors = (self.error(), )
        complex_child = CompoundContext()
        complex_child.children = {'baz': Context(errors=errors)}
        self.context.children['complex'] = complex_child
        
        assert_equals({'baz': errors}, self.context.errors['complex'])
    
    def test_can_return_unvalidated_values_from_nested_containers(self):
        complex_child = CompoundContext()
        complex_child.children = {'baz': Context(unvalidated_value='42')}
        self.context.children['complex'] = complex_child
        
        assert_equals({'baz': '42'}, self.context.unvalidated_value['complex'])
    
    # --- update values -------------------------------------------------------
    
    def test_can_set_new_values(self):
        values = {'foo': 'baz', 'bar': 42}
        self.context.update_value(values)
        
        assert_equals(values, self.context.value)
    
    def test_does_not_change_unspecified_items_when_updating_values(self):
        self.context.update_value({'bar': 42})
        
        assert_equals({'foo': 'foo', 'bar': 42}, self.context.value)
    
    def test_can_set_unvalidated_values(self):
        values = {'foo': 'baz', 'bar': 42}
        self.context.update_value(unvalidated_value=values)
        
        assert_equals('baz', self.context.foo.unvalidated_value)
        assert_equals(42, self.context.bar.unvalidated_value)
    
    def test_ignores_unknown_children_when_setting_unvalidated_values(self):
        values = {'foo': 'baz', 'quox': 42}
        self.context.update_value(unvalidated_value=values)
        
        assert_equals('baz', self.context.foo.unvalidated_value)
        assert_equals(['foo', 'bar'], list(self.context.children))
    
    def test_can_set_errors(self):
        values = {'foo': ('too big', ), 'bar': None}
        self.context.update_value(errors=values)
        
        assert_equals({'foo': ('too big',), 'bar': None}, self.context.errors)
    
    def test_raises_exception_if_values_contain_unknown_key(self):
        values = dict(foo='s1', bar='e1', invalid=None)
        e = assert_raises(ValueError, lambda: self.context.update_value(values))
        assert_equals("unknown parameter 'invalid'", e.args[0])
    
    # --- helpers -------------------------------------------------------------
    
    def error(self, message='bad input', value=None):
        return InvalidDataError(message, value)
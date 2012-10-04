# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.forms.fields import ListField, TextField
from grumpywidgets.lib.pythonic_testcase import *


class ListFieldTest(PythonicTestCase):
    def test_adds_itself_to_path(self):
        assert_equals(('foo', ), ListField('foo').path())
    
    def test_sets_parent_parameter_on_its_children(self):
        list_field = ListField('foo', children=(TextField('bar'), ))
        assert_equals(list_field, list_field.children[0].parent)
    
    def test_can_generate_css_classes(self):
        list_field = ListField('foo')
        assert_contains('foo-list', list_field.css_classes_for_container())
        
        list_field.css_classes = ('baz', )
        assert_contains('baz', list_field.css_classes_for_container())
    
    def test_can_build_new_context_for_empty_input(self):
        list_field = ListField('foo', children=[TextField('name')])
        
        context = list_field.new_context([])
        assert_false(context.contains_errors())
        assert_length(0, context.items)
    
    def test_can_build_new_context_for_multiple_rows(self):
        list_field = ListField('foo', children=[TextField('name')])
        
        input_ = [{'name': 'bar'}, {'name': 'bar'}]
        context = list_field.new_context(unvalidated=input_)
        assert_equals(tuple(input_), context.unvalidated_value)
    
    def test_can_update_child_contexts(self):
        list_field = ListField('foo', children=(TextField('bar'), ))
        list_field.context.update_value([{'bar': 32}])
        
        assert_equals(({'bar': 32},), list_field.context.value)


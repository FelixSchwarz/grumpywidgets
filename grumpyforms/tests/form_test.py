# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.


from grumpyforms.api import Form
from grumpyforms.fields import TextField
from grumpywidgets.lib.pythonic_testcase import *


class FormTest(PythonicTestCase):
    def test_forms_return_empty_path(self):
        form = Form('foo')
        
        assert_none(form.parent)
        assert_equals((), form.path())
    
    def test_can_build_new_context(self):
        form = Form(children=[TextField('name')])
        
        context = form.new_context()
        assert_equals(['name'], list(context.children.keys()))
        assert_equals({'name': None}, context.value)
        assert_false(context.contains_errors())
    
    def test_can_build_new_context_with_unvalidated_values(self):
        form = Form('foo', children=[TextField('name')])
        
        context = form.new_context({'name': 'Foo Bar'})
        assert_false(context.contains_errors())
        
        assert_equals({'name': 'Foo Bar'}, context.unvalidated_value)


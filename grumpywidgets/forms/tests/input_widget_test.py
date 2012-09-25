# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from StringIO import StringIO

from pycerberus.api import BaseValidator, InvalidDataError
from pycerberus.validators import IntegerValidator

from grumpywidgets.forms.api import InputWidget, Form
from grumpywidgets.lib.pythonic_testcase import *


class InputWidgetInitializationTest(PythonicTestCase):
    def test_can_set_name_with_positional_argument(self):
        widget = InputWidget('foobar')
        assert_equals('foobar', widget.name)
    
    def test_can_set_name_with_named_argument(self):
        widget = InputWidget(name='foobar')
        assert_equals('foobar', widget.name)


class InputWidgetTest(PythonicTestCase):
    def test_knows_its_parent(self):
        widget = InputWidget('bar')
        form = Form('foo')
        widget.parent = form
        
        assert_equals(form, widget.parent)
        assert_equals(('bar',), widget.path())
    
    def test_returns_empty_path_if_widget_has_no_name(self):
        widget = InputWidget()
        assert_none(widget.name)
        
        assert_equals((), widget.path())
    
    def test_can_return_full_name(self):
        widget = InputWidget('bar')
        assert_equals('bar', widget.full_name())
        
        inner = Form('inner')
        widget.parent = inner
        assert_equals('bar', widget.full_name())
        
        outer = Form('outer')
        inner.parent = outer
        assert_equals('inner.bar', widget.full_name())


class InputWidgetValidationTest(PythonicTestCase):
    def test_returns_original_value_if_no_validator_found(self):
        widget = InputWidget('foobar')
        assert_none(widget.validate(None))
        assert_equals('foo', widget.validate('foo'))
        assert_equals([], widget.validate([]))
    
    def test_can_use_configured_validator(self):
        widget = InputWidget('foobar', validator=IntegerValidator())
        assert_equals(2, widget.validate('2'))
        assert_raises(InvalidDataError, lambda: widget.validate('abc'))


class InputWidgetRenderingTest(PythonicTestCase):
    def setUp(self):
        self.widget = InputWidget(template=StringIO('{{ value }}'))
    
    def test_use_value_from_context(self):
        self.widget.context.unvalidated_value = 'foo'
        assert_equals('foo', self.widget.display())
        
        self.widget.context.value = 'bar'
        assert_equals('bar', self.widget.display())
        assert_equals('', self.widget.display(''))
        assert_equals('baz', self.widget.display('baz'))
    
    def test_uses_widget_name_in_css_container_class(self):
        self.widget.name = 'username'
        
        assert_contains('username-container', self.widget.css_classes_for_container())
    
    def test_adds_css_class_to_container_on_validation_error(self):
        # simulate failed validation
        self.widget.context.errors = (InvalidDataError('bad input', 'abc'),)
        assert_true(self.widget.context.contains_errors())
        
        assert_contains('validationerror', self.widget.css_classes_for_container())
    
    def test_adds_css_class_to_container_for_required_fields(self):
        assert_none(self.widget.validator)
        assert_not_contains('requiredfield', self.widget.css_classes_for_container())
        
        self.widget.validator = IntegerValidator()
        assert_true(self.widget.validator.is_required())
        
        assert_contains('requiredfield', self.widget.css_classes_for_container())
    
    def test_can_add_css_classes_for_containers_if_widget_uses_basevalidator(self):
        self.widget.validator = BaseValidator()
        assert_false(hasattr(self.widget.validator, 'is_required'))
        
        assert_equals(set(['fieldcontainer']), 
                      set(self.widget.css_classes_for_container()))
    
    def test_can_specify_attributes_on_display(self):
        assert_false(hasattr(self.widget, 'user'))
        self.widget.template = StringIO('Hello {{ user }}!')
        
        assert_raises(TypeError, lambda: self.widget.display(user='foo'))
        self.widget.user = None
        assert_equals('Hello foo!', self.widget.display(user='foo'))


class InputWidgetLabelTest(PythonicTestCase):
    def setUp(self):
        self.widget = InputWidget(id='user', label='user name',
            template=StringIO('{{ value }}'))
    
    def test_input_widgets_have_no_labels_by_default(self):
        widget = InputWidget(id='user', template=StringIO('{{ value }}'))
        assert_none(widget.label)
        
        assert_none(widget.label_widget())
    
    def test_can_be_generated_from_string(self):
        label = self.widget.label_widget()
        
        assert_not_none(label)
        assert_equals('user', label.for_)
        assert_contains('user name', label.display())
    
    def test_has_no_reference_if_parent_has_no_id(self):
        self.widget.id = None
        
        label = self.widget.label_widget()
        assert_none(label.for_)
        assert_contains('user name', label.display())
    
    def test_can_autogenerate_id(self):
        label = self.widget.label_widget()
        assert_equals('user-label', label.id)
        assert_contains('id="user-label"', label.display())
    
    def test_has_no_id_if_parent_has_no_id(self):
        self.widget.id = None
        
        label = self.widget.label_widget()
        assert_none(label.id)
        assert_not_contains('id="', label.display())


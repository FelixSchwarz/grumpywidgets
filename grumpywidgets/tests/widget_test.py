# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from StringIO import StringIO

from grumpywidgets.api import Widget
from grumpywidgets.lib.pythonic_testcase import *


class WidgetInitializationTest(PythonicTestCase):
    def test_can_override_attributes_during_class_instantiation(self):
        class SimpleWidget(Widget):
            id = 'foo-bar'
            template = 'simplewidget.html'
            css_classes = ('foo',)
            children = ()
        child = SimpleWidget()
        
        widget = SimpleWidget(id='baz', template='baz.html', css_classes=[], children=[child])
        assert_equals('baz', widget.id)
        assert_equals('baz.html', widget.template)
        assert_equals((), widget.css_classes)
        assert_equals((child, ), widget.children)
    
    def test_raises_exception_for_unknown_parameters(self):
        e = assert_raises(TypeError, lambda: Widget(invalid='foo'))
        assert_equals("__init__() got an unexpected keyword argument 'invalid'",
                      e.args[0])
    
    def test_can_overide_attributes_from_subclasses(self):
        class CustomWidget(Widget):
            foobar = None
            def do_stuff(self):
                return 42
        widget = CustomWidget(foobar=21)
        assert_equals(21, widget.foobar)
        
        e= assert_raises(ValueError, lambda: CustomWidget(do_stuff=None))
        assert_equals("Must not override instance method 'do_stuff()'", 
                      e.args[0])
    
    def test_prevent_overriding_private_attributes(self):
        class CustomWidget(Widget):
            _secret = 42
        e = assert_raises(ValueError, lambda: CustomWidget(_secret=None))
        assert_equals("Must not override private attribute '_secret'", e.args[0])


class WidgetJinjaTemplatesTest(PythonicTestCase):
    def setUp(self):
        self.widget = Widget(template=StringIO('{{ value }}'))
    
    def test_can_use_jinja_template(self):
        widget = Widget(template=StringIO('Hello {{ value }}!'))
        assert_equals(u'Hello world!', 
                      widget.display('world'))
    
    def test_can_use_value_from_context(self):
        self.widget.context.value = 'baz'
        assert_equals('baz', self.widget.display())
    
    def test_prefers_explicit_value(self):
        self.widget.context.value = 'baz'
        assert_equals('bar', self.widget.display('bar'))


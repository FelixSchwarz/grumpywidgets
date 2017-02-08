# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from io import StringIO

from pythonic_testcase import *

from grumpywidgets import template_helpers
from grumpywidgets.api import Widget
from grumpywidgets.testhelpers import assert_same_html


class WidgetRenderingTest(PythonicTestCase):
    def setUp(self):
        self.widget = Widget(template=StringIO(u'{{ value }}'))

    def test_can_use_jinja_template(self):
        widget = Widget(template=StringIO(u'Hello {{ value }}!'))
        assert_equals(u'Hello world!', widget.display('world'))

    def test_can_use_genshi_template(self):
        tmpl_str = u'<p xmlns:py="http://genshi.edgewall.org/">Hello ${value}!</p>'
        widget = Widget(template=StringIO(tmpl_str), template_engine='genshi')
        assert_same_html(u'<p>Hello world!</p>', widget.display('world'))

    def test_can_use_value_from_context(self):
        self.widget.context.value = 'baz'
        assert_equals('baz', self.widget.display())

    def test_prefers_explicit_value(self):
        self.widget.context.value = 'baz'
        assert_equals('bar', self.widget.display('bar'))

    def test_can_specify_attributes_on_display(self):
        widget = Widget(template=StringIO(u'{{ verb }} {{ value }}'))
        widget.verb = 'hello'

        assert_equals(u'hello foo', widget.display('foo'))
        assert_equals(u'goodbye foo', widget.display('foo', verb='goodbye'))
        e = assert_raises(TypeError, lambda: widget.display('foo', invalid='bar'))
        assert_equals("display() got an unexpected keyword argument 'invalid'",
                      e.args[0])

    def test_widget_instance_available_in_template(self):
        template_variables = self.widget.template_variables(None)
        assert_contains('self_', template_variables)
        assert_equals(self.widget, template_variables['self_'])

    def test_helper_module_available_in_template(self):
        template_variables = self.widget.template_variables(None)
        assert_contains('h', template_variables)
        assert_equals(template_helpers, template_variables['h'])

    def test_can_serialize_to_html(self):
        widget = Widget(template=StringIO(u'foobar'))
        assert_equals(u'foobar', unicode(widget))


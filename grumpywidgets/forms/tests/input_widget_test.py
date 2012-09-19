# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from StringIO import StringIO

from pycerberus.api import InvalidDataError
from pycerberus.validators import IntegerValidator

from grumpywidgets.forms.api import InputWidget
from grumpywidgets.lib.pythonic_testcase import *


class InputWidgetInitializationTest(PythonicTestCase):
    def test_can_set_name_with_positional_argument(self):
        widget = InputWidget('foobar')
        assert_equals('foobar', widget.name)
    
    def test_can_set_name_with_named_argument(self):
        widget = InputWidget(name='foobar')
        assert_equals('foobar', widget.name)


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
    def test_use_value_from_context(self):
        widget = InputWidget(template=StringIO('{{ value }}'))
        widget.context.unvalidated_value = 'foo'
        assert_equals('foo', widget.display())
        
        widget.context.value = 'bar'
        assert_equals('bar', widget.display())
        assert_equals('', widget.display(''))
        assert_equals('baz', widget.display('baz'))

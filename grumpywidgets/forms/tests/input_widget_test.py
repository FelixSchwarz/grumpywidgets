# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.forms.api import InputWidget
from grumpywidgets.lib.pythonic_testcase import *


class InputWidgetInitializationTest(PythonicTestCase):
    def test_can_set_name_with_positional_argument(self):
        widget = InputWidget('foobar')
        assert_equals('foobar', widget.name)
    
    def test_can_set_name_with_named_argument(self):
        widget = InputWidget(name='foobar')
        assert_equals('foobar', widget.name)


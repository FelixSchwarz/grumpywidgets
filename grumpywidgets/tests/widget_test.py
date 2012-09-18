# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.api import Widget
from grumpywidgets.lib.pythonic_testcase import *


class DisplayWidgetTest(PythonicTestCase):
    def test_can_render_display_widget(self):
        class DummyWidget(Widget):
            def display(self, value):
                return u'Hello %s!' % value
        
        assert_equals(u'Hello world!', DummyWidget().display('world'))



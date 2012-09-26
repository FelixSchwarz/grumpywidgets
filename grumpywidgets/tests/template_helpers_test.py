# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets import template_helpers as h
from grumpywidgets.lib.pythonic_testcase import *


class TemplateHelpersTest(PythonicTestCase):
    def test_render_class(self):
        assert_equals(None, h.render_class([]))
        assert_equals('foo bar', h.render_class(['foo', 'bar']))

# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pythonic_testcase import *

from grumpyforms.api import InputWidget
import grumpyforms.fields
import grumpyforms.genshi_
from grumpywidgets.widget_list import widgets_in_module
from grumpywidgets.testhelpers import assert_same_html


class GenshiFieldsTest(PythonicTestCase):
    def test_can_retrieve_fields_with_genshi_support(self):
        checked_widgets = set()
        all_widgets = widgets_in_module(grumpyforms.fields, InputWidget)
        for name, widget in widgets_in_module(grumpyforms.genshi_, InputWidget):
            assert_equals('genshi', widget.template_engine,
                message='%s does not use Genshi' % name)
            checked_widgets.add(name)

        # ensure that at least some known widgets were checked
        assert_contains('Checkbox', checked_widgets)
        assert_contains('PasswordField', checked_widgets)
        assert_contains('SelectField', checked_widgets)

        for name, widget in all_widgets:
            assert_contains(name, checked_widgets,
                message='%s widget not exported via "genshi_" module' % name)
            assert_equals('jinja2', widget.template_engine,
                message='%s widget from grumpyforms.fields did change' % name)

    def test_genshi_fields_can_be_rendered(self):
        # ensure that dynamically created widgets really use the right template
        # so that they are functional
        box = grumpyforms.genshi_.Checkbox(name='foo')
        assert_same_html(u'<input type="checkbox" name="foo" />', box.display())

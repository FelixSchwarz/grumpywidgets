# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.lib.form_data import FieldData
from pythonic_testcase import *

from grumpywidgets.api import Widget


class WidgetTest(PythonicTestCase):
    def test_can_generate_container_id(self):
        assert_none(Widget().id_for_container())
        assert_equals('foo-container', Widget(id='foo').id_for_container())

    def test_can_specify_css_classes_for_container(self):
        assert_equals(('widgetcontainer', ), Widget().css_classes_for_container())

    def test_adapts_css_classes_for_container_for_fields(self):
        class FieldWidget(Widget):
            def is_field(self):
                return True
        assert_equals(set(['fieldcontainer', 'widgetcontainer']),
                      set(FieldWidget().css_classes_for_container()))

    def test_adapts_css_classes_for_container_for_hidden_widgets(self):
        class HiddenWidget(Widget):
            def is_hidden(self):
                return True
        assert_equals(set(['hiddencontainer', 'widgetcontainer']),
                      set(HiddenWidget().css_classes_for_container()))

    def test_adapts_css_classes_for_container_for_buttons(self):
        class ButtonWidget(Widget):
            def is_button(self):
                return True
        assert_equals(set(['buttoncontainer', 'widgetcontainer']),
                      set(ButtonWidget().css_classes_for_container()))

    def test_has_no_parent_by_default(self):
        assert_none(Widget().parent)

    def test_can_tell_about_classification(self):
        widget = Widget()
        assert_false(widget.is_field())
        assert_false(widget.is_button())
        assert_false(widget.is_hidden())

    def test_can_clone_itself(self):
        w = Widget()
        w.context = FieldData(value=42)

        cloned = w.copy()
        w.context.value = 21
        assert_equals(42, cloned.context.value)
        assert_equals(21, w.context.value)

    def test_can_create_new_context(self):
        widget = Widget()
        context = widget.new_context()

        assert_none(context.value)
        assert_equals((), context.errors)
        assert_none(context.initial_value)

        assert_not_equals(context, widget.new_context())

    def test_can_create_new_context_with_data(self):
        widget = Widget()
        context = widget.new_context(unvalidated='42')
        assert_none(context.value)
        assert_equals((), context.errors)
        assert_equals('42', context.initial_value)

    def test_can_specify_container_attributes(self):
        assert_equals(dict(), Widget().attributes_for_container())

        widget = Widget(container_attrs=dict(foo='bar'))
        assert_equals(dict(foo='bar'), widget.attributes_for_container())



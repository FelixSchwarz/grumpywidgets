# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

import re

from pycerberus.validators import StringValidator
from pythonic_testcase import *

from grumpyforms.fields import ListField, TextField
from grumpywidgets.widgets import Label


class ListFieldRenderingTest(PythonicTestCase):
    def setUp(self):
        string = StringValidator(max_length=10, required=False)
        self.list_field = ListField('foo', children=(
            TextField('start', validator=string),
            TextField('end', validator=string),
        ))
        self.empty_input = [dict(start=None, end=None)]

    def test_can_render_empty_list(self):
        list_field = ListField('foo', children=())

        html = self.simplify(list_field.display())
        assert_equals(u'<ul class="foo-list"></ul>', html)

    def test_can_render_list_field_with_complex_child(self):
        html = self.list_field.display(self.empty_input)
        expected = u'<ul class="foo-list">' + \
            '<li>' +\
                '<div class="start-container widgetcontainer fieldcontainer">' + \
                    '<input type="text" name="foo-1.start" />' + \
                '</div>' + \
                '<div class="end-container widgetcontainer fieldcontainer">' + \
                    '<input type="text" name="foo-1.end" />' + \
                '</div>' + \
            '</li>' + \
            '</ul>'
        assert_equals(expected, self.simplify(html))

    def test_can_render_child_label(self):
        start_field = self.list_field.children[0]
        # TODO: automatically generate ids for fields with labels
        start_field.id = 'start'
        start_field.label = 'Start'
        expected = u'<label id="start-label" for="start">Start</label>' + \
            '<input type="text" id="start" name="foo-1.start" />'

        html = self.simplify(self.list_field.display(self.empty_input))
        match = re.search('<div[^>]*>(.+?)</div>', html)
        assert_equals(expected, match.group(1))

    def test_can_pass_values_to_children(self):
        child_input = [dict(start='s1', end='e1')]
        html = self.simplify(self.list_field.display(child_input))
        assert_contains('<input type="text" name="foo-1.start" value="s1" />', html)
        assert_contains('<input type="text" name="foo-1.end" value="e1" />', html)

    def test_raises_exception_if_values_contain_unknown_key(self):
        child_input = [dict(start='s1', end='e1', invalid=None)]
        e = assert_raises(ValueError, lambda: self.list_field.display(child_input))
        assert_equals("unknown parameter 'invalid'", e.args[0])

    def test_can_render_display_widgets(self):
        list_field = ListField('foo', children=(Label(value='Bar'), ))

        expected = u'<ul class="foo-list">' + \
            '<li><div class="widgetcontainer"><label>Bar</label></div></li>' + \
        '</ul>'
        html = list_field.display([{}])
        assert_equals(expected, self.simplify(html))

    # --- multiple children ---------------------------------------------------

    def test_can_render_list_field_with_multiple_children(self):
        input_ = [{'start': 's1', 'end': 'e1'}, {'start': 's2', 'end': 'e2'}]
        html = self.list_field.display(input_)
        first_child = '<li>' +\
                '<div class="start-container widgetcontainer fieldcontainer">' + \
                    '<input type="text" name="foo-1.start" value="s1" />' + \
                '</div>' + \
                '<div class="end-container widgetcontainer fieldcontainer">' + \
                    '<input type="text" name="foo-1.end" value="e1" />' + \
                '</div>' + \
            '</li>'
        second_child = '<li>' + \
                '<div class="start-container widgetcontainer fieldcontainer">' + \
                    '<input type="text" name="foo-2.start" value="s2" />' + \
                '</div>' + \
                '<div class="end-container widgetcontainer fieldcontainer">' + \
                    '<input type="text" name="foo-2.end" value="e2" />' + \
                '</div>' + \
            '</li>'

        children_matches = re.findall('(<li>\s*.*?\s*</li>)', self.simplify(html))
        assert_equals(first_child, children_matches[0])
        assert_equals(second_child, children_matches[1])
        assert_length(2, children_matches)

    # --- multiple children ---------------------------------------------------

    def test_can_display_errors_for_children(self):
        input_ = [{'start': '', 'end': '12345678901'}]
        result = self.list_field.validate(input_)
        assert_true(result.contains_errors())

        self.list_field.set_context(result)
        expected = u'<ul class="foo-list">' + \
            '<li>' + \
                '<div class="start-container widgetcontainer fieldcontainer">' + \
                    '<input type="text" name="foo-1.start" />' + \
                '</div>' + \
                '<div class="end-container validationerror widgetcontainer fieldcontainer">' + \
                    '<input type="text" name="foo-1.end" value="12345678901" />' + \
                    '<span class="validationerror-message">Must be less than 10 characters long.</span>' + \
                '</div>' + \
            '</li>' + \
        '</ul>'
        html = self.simplify(self.list_field.display())
        assert_equals(expected, html)

    # --- helpers -------------------------------------------------------------

    def simplify(self, html):
        return re.sub('\s+', ' ', html).replace('> <', '><')


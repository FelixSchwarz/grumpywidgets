# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

import re

from pycerberus.errors import InvalidDataError
from pycerberus.validators import IntegerValidator

from grumpyforms.api import Form
from grumpyforms.fields import ListField, TextField
from grumpywidgets.lib.pythonic_testcase import *
from grumpywidgets.widgets import Label


class FormChildrenRenderingTest(PythonicTestCase):
    def setUp(self):
        class SimpleForm(Form):
            children = (TextField('number', validator=IntegerValidator(required=False)), )
        self.form = SimpleForm()
    
    # --- tests ---------------------------------------------------------------
    def test_can_render_single_child(self):
        expected = '<div class="number-container fieldcontainer">' + \
            '<input type="text" name="number" /></div>'
        self.assert_child_html(expected, self.form.display(), strip_container=False)
    
    def test_can_pass_values_to_children(self):
        expected = '<input type="text" name="number" value="send" />'
        self.assert_child_html(expected, self.form.display({'number': 'send'}))
    
    def test_raises_error_if_unknown_parameters_are_passed_for_display(self):
        e = assert_raises(ValueError, lambda: Form().display({'invalid': None}))
        assert_equals("unknown parameter 'invalid'", e.args[0])
    
    def test_can_display_errors_for_children(self):
        textfield = self.form.children[0]
        
        # simulate failed validation
        error_dict = {textfield.name: (InvalidDataError('bad input', 'abc'),)}
        self.form.context.update_value(errors=error_dict)
        assert_true(self.form.context.contains_errors())
        
        expected = u'<input type="text" name="number" />' + \
            '<span class="validationerror-message">bad input</span>'
        self.assert_child_html(expected, self.form.display())
    
    def test_can_redisplay_previous_values_after_failed_validation(self):
        result = self.form.validate({'number': 'abc'})
        assert_true(result.contains_errors())
        
        self.form.set_context(result)
        expected = u'<input type="text" name="number" value="abc" />' + \
            '<span class="validationerror-message">Please enter a number.</span>'
        self.assert_child_html(expected, self.form.display())
    
    def test_can_display_child_label(self):
        self.form.children[0].label = 'items'
        
        expected = '<label>items</label><input type="text" name="number" />'
        self.assert_child_html(expected, self.form.display())
    
    # --- child container ----------------------------------------------------
    
    def test_container_contains_css_class_with_child_name(self):
        container_html = self.child_container_html(self.form.display({}))
        self.assert_contains('class="number-container fieldcontainer"', container_html)
    
    def test_can_render_view_only_children(self):
        self.form.children = [Label(value='foo'), ]
        
        self.assert_child_html('<label>foo</label>', self.form.display())
        container_html = self.child_container_html(self.form.display({}))
        self.assert_contains('class="fieldcontainer"', container_html)
    
    def test_can_derive_container_id_from_child(self):
        self.form.children = [Label(value='text', id='foo'), ]
        
        self.assert_child_html('<label id="foo">text</label>', self.form.display())
        container_html = self.child_container_html(self.form.display({}))
        assert_contains('id="foo-container"', container_html)
    
    def test_adds_no_container_id_for_child_without_id(self):
        assert_none(self.form.children[0].id)
        
        container_html = self.child_container_html(self.form.display({}))
        assert_not_contains('id="', container_html)
    
    # --- compound fields -----------------------------------------------------
    
    def test_can_render_list_field_child(self):
        compound = ListField('foo', children=(TextField('id', validator=IntegerValidator()),))
        form = Form(children=(compound, ))
        
        input_ = {'foo': [{'id': 42}]}
        form_html = form.display(input_)
        assert_equals('<ul class="foo-list"></ul>', self.container_html('ul', form_html))
        
        item_html = self.child_html('ul', form_html)
        expected = '<div class="id-container requiredfield fieldcontainer">' + \
            '<input type="text" name="foo-1.id" value="42" />' + \
        '</div>'
        assert_equals(expected, self.child_html('li', item_html))
    
    def test_can_display_errors_for_list_field(self):
        text_field = TextField('id', validator=IntegerValidator(required=False))
        form = Form(children=(ListField('foo', children=(text_field,)), ))
        
        result = form.validate({'foo': [{'id': 'abc'}]})
        assert_true(result.contains_errors())
        
        form.set_context(result)
        form_html = form.display()
        item_html = self.child_html('ul', form_html)
        expected = '<div class="id-container validationerror fieldcontainer">' + \
            '<input type="text" name="foo-1.id" value="abc" />' + \
            '<span class="validationerror-message">Please enter a number.</span>' + \
        '</div>'
        assert_equals(expected, self.child_html('li', item_html))
    
    # --- helpers -------------------------------------------------------------
    
    def _split_html(self, container_tag, html):
        simple_html = re.sub('\s+', ' ', html).replace('> <', '><')
        regex_string = '(<%(tag)s[^>]*>)\s*(.*)\s*(</%(tag)s>)' % dict(tag=container_tag)
        match = re.search(regex_string, simple_html)
        assert_not_none(match)
        return (match.group(1) + match.group(3), match.group(2))
    
    def child_html(self, container_tag, html):
        return self._split_html(container_tag, html)[1]
    
    def assert_child_html(self, expected, rendered_form, strip_container=True):
        child_html = self.child_html('form', rendered_form)
        if strip_container:
            child_html = self.child_html('div', rendered_form)
        assert_equals(expected, child_html)
    
    def container_html(self, container_tag, html):
        return self._split_html(container_tag, html)[0]
    
    def child_container_html(self, rendered_form):
        child_html = self.child_html('form', rendered_form)
        return self.container_html('div', child_html)
    
    def assert_container_html(self, expected, rendered_form):
        assert_equals(expected, self.child_container_html(rendered_form))


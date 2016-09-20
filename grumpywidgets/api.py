# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from __future__ import absolute_import

import os

from . import template_helpers
from .context import Context
from .lib.simple_super import SuperProxy
from .jinja_support import render_jinja_template


__all__ = ['Widget']

this_dir = os.path.dirname(__file__)
grumpywidgets_template_dir = os.path.join(this_dir, 'templates')

class Widget(object):
    name = None
    id = None
    template = None
    css_classes = None
    container_attrs = None

    parent = None

    _template_path = grumpywidgets_template_dir
    super = SuperProxy()

    def __init__(self, **kwargs):
        self.context = None
        for key in kwargs.keys():
            if key.startswith('_'):
                raise ValueError("Must not override private attribute '%s'" % key)
            if not hasattr(self, key):
                continue
            if callable(getattr(self, key)):
                raise ValueError("Must not override instance method '%s()'" % key)
            value = kwargs.pop(key)
            if isinstance(value, list):
                value = tuple(value)
            try:
                setattr(self, key, value)
            except AttributeError:
                # the actual attribute is likely a property without setter
                # we can't detect that before...
                pass
        if kwargs:
            first_key = kwargs.keys()[0]
            raise TypeError("__init__() got an unexpected keyword argument '%s'" % first_key)
        if self.context is None:
            # for more complex widgets '.new_context()' might depend on class
            # attributes so let's call that method after initializing all
            # instance variables.
            self.context = self.new_context()

    def copy(self):
        klass = self.__class__
        attributes = self.widget_attributes()
        if 'parent' in attributes:
            del attributes['parent']
        for key in list(attributes):
            value = attributes[key]
            if not hasattr(value, 'copy'):
                continue
            attributes[key] = value.copy()
        return klass(**attributes)

    def new_context(self, unvalidated=None):
        return Context(unvalidated_value=unvalidated)

    def set_context(self, context):
        self.context = context

    def widget_attributes(self):
        attributes = dict()
        for key in dir(self):
            if key.startswith('_'):
                continue
            value = getattr(self, key)
            if callable(value):
                continue
            attributes[key] = value
        return attributes

    def template_variables(self, value, **widget_attributes):
        template_values = self.widget_attributes()
        css_classes = template_values.get('css_classes')
        if css_classes is not None:
            template_values['css_classes'] = ' '.join(css_classes)
        template_values.update(widget_attributes)

        value = self._display_value(value)
        if not isinstance(value, dict):
            template_values['value'] = value
        else:
            template_values.update(value)
        template_values['h'] = template_helpers
        template_values['self_'] = self
        return template_values

    def _render_template(self, template_variables):
        return render_jinja_template(self.template, template_variables, self._template_path)

    def _display_value(self, value):
        if value is not None:
            return value
        return self.context.value

    def display(self, value=None, **kwargs):
        unknown_parameters = set(kwargs).difference(set(self.widget_attributes()))
        if unknown_parameters:
            first = unknown_parameters.pop()
            raise TypeError("display() got an unexpected keyword argument '%s'" % first)
        variables = self.template_variables(value, **kwargs)
        return self._render_template(variables)

    def is_field(self):
        """Return True if this widget is an input field which may contain a
        value.

        This is typically true for all text-like fields, selection fields,
        checkboxes as well as hidden fields but not for buttons."""
        return False

    def is_button(self):
        """Return True if this widget is a button-like control which triggers
        an action (e.g. submitting a form)."""
        return False

    def is_hidden(self):
        """Return True if this widget is usually not visible to the user."""
        return False

    def css_classes_for_container(self):
        css_classes = ['widgetcontainer']
        if self.is_field():
            css_classes.append('fieldcontainer')
        if self.is_button():
            css_classes.append('buttoncontainer')
        if self.is_hidden():
            css_classes.append('hiddencontainer')
        return tuple(css_classes)

    def id_for_container(self):
        if self.id is None:
            return None
        return '%s-container' % self.id

    def attributes_for_container(self):
        return self.container_attrs or dict()


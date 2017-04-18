# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from __future__ import absolute_import

import os

from pycerberus.lib.form_data import FieldData

from . import template_helpers
from .lib.simple_super import SuperProxy
from .genshi_support import render_genshi_template
from .jinja_support import render_jinja_template
from .utils import provide_as_dict_item


__all__ = ['Widget']

this_dir = os.path.dirname(__file__)
grumpywidgets_template_dir = os.path.join(this_dir, 'templates')

class Widget(object):
    name = None
    id = None
    template = None
    template_name = None
    template_engine = 'jinja2'
    css_classes = None
    container_attrs = None

    parent = None

    _template_path = grumpywidgets_template_dir
    super = SuperProxy()

    def __init__(self, **kwargs):
        self.context = None
        self._template = None
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
        return FieldData(initial_value=unvalidated)

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

    @property
    def template(self):
        if self._template is not None:
            return self._template
        elif self.template_name is not None:
            return self.template_name + '.' + self.template_engine
        return None

    @template.setter
    def template(self, value):
        self._template = value

    def template_variables(self, value, **widget_attributes):
        template_values = self.widget_attributes()
        css_classes = template_values.get('css_classes')
        if css_classes is not None:
            template_values['css_classes'] = ' '.join(css_classes)
        template_values.update(widget_attributes)
        is_repeating_field_data = isinstance(self.context.meta, tuple)
        if not is_repeating_field_data:
            # currently no "meta" for RepeatingFieldData ("ListField") - ignored
            # for now
            for meta_key, meta_value in (self.context.meta or {}).items():
                template_value = template_values.get(meta_key)
                if template_value is None:
                    new_value = meta_value
                else:
                    new_values = {}
                    for key in set(meta_value).union(template_value):
                        if (key in meta_value) and (key in template_value):
                            # at some point we might have to decide what to do with
                            # conflicting keys - but I hope we can defer that decision as
                            # much as possible.
                            raise AssertionError('conflicting key %s - merging not supported yet' % key)
                        elif key in meta_value:
                            new_values[key] = meta_value[key]
                        else:
                            new_values[key] = template_value[key]
                    new_value = new_values
                template_values[meta_key] = new_value

        with provide_as_dict_item(self.context.meta, 'template_values', template_values):
            value = self._display_value(value)
            if isinstance(value, dict):
                assert (None not in value.keys())
                template_values.update(value)
            else:
                template_values['value'] = value
        template_values.update({
            'h': template_helpers,
            'self_': self,
        })
        return template_values

    def _render_template(self, template_variables):
        if self.template_engine == 'jinja2':
            return render_jinja_template(self.template, template_variables, self._template_path)
        elif self.template_engine == 'genshi':
            return render_genshi_template(self.template, template_variables, self._template_path)
        raise ValueError('unknown template engine %s' % self.template_engine)

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

    def __html__(self):
        return self.display()
    __unicode__ = __html__

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


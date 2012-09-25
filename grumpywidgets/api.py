# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from copy import deepcopy

from jinja2 import Environment, PackageLoader, Template

from grumpywidgets import template_helpers
from grumpywidgets.lib.simple_super import SuperProxy


__all__ = ['Widget']

class Widget(object):
    id = None
    template = None
    css_classes = None
    
    parent = None
    
    _template_path = ('grumpywidgets', 'templates')
    super = SuperProxy()
    
    def __init__(self, **kwargs):
        self.context = Context()
        
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
            setattr(self, key, value)
        if kwargs:
            first_key = kwargs.keys()[0]
            raise TypeError("__init__() got an unexpected keyword argument '%s'" % first_key)
    
    def copy(self):
        klass = self.__class__
        attributes = self.widget_attributes()
        for key in list(attributes):
            value = attributes[key]
            if not hasattr(value, 'copy'):
                continue
            attributes[key] = value.copy()
        return klass(**attributes)
    
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
        if hasattr(self.template, 'read'):
            template = Template(self.template.read())
            self.template.seek(0)
        else:
            env = Environment(loader=PackageLoader(*self._template_path))
            template = env.get_template(self.template)
        return template.render(**template_variables)
    
    def _display_value(self, value):
        if value is not None:
            return value
        return self.context.value
    
    def display(self, value=None, **kwargs):
        unknown_parameters = set(kwargs).difference(set(self.widget_attributes()))
        if unknown_parameters:
            first = unknown_parameters.pop()
            raise TypeError("__display__() got an unexpected keyword argument '%s'" % first)
        variables = self.template_variables(value, **kwargs)
        return self._render_template(variables)
    
    def css_classes_for_container(self):
        return ('fieldcontainer', )
    
    def id_for_container(self):
        if self.id is None:
            return None
        return '%s-container' % self.id


class Context(object):
    value = None
    errors = None
    
    def __init__(self, value=None, errors=None):
        self.value = value
        self.errors = errors
    
    def copy(self):
        klass = self.__class__
        attributes = dict(
            value=deepcopy(self.value), 
            errors=deepcopy(self.errors)
        )
        return klass(**attributes)
    __deepcopy__ = copy
    
    def contains_errors(self):
        if (self.errors is not None) and (len(self.errors) > 0):
            return True
        return False
    
    def rendered_errors(self):
        if not self.contains_errors():
            return ()
        rendered = []
        for error in self.errors:
            rendered.append(error.details().msg())
        return tuple(rendered)


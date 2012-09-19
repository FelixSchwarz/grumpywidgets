# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from jinja2 import Environment, PackageLoader, Template

from grumpywidgets.lib.simple_super import SuperProxy


__all__ = ['Widget']

class Widget(object):
    id = None
    template = None
    css_classes = None
    children = ()
    
    _template_path = ('grumpywidgets', 'templates')
    context = None
    super = SuperProxy()
    
    def __init__(self, **kwargs):
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
    
    def template_variables(self, values):
        
        template_values = dict()
        for key in dir(self):
            if key.startswith('_'):
                continue
            value = getattr(self, key)
            if callable(key):
                continue
            if (key == 'css_classes') and (value is not None):
                value = ' '.join(value)
            template_values[key] = value
        template_values['this'] = self
        if not isinstance(values, dict):
            values = dict(value=values)
        template_values.update(values)
        return template_values
    
    def _render_template(self, value):
        if hasattr(self.template, 'read'):
            template = Template(self.template.read())
        else:
            env = Environment(loader=PackageLoader(*self._template_path))
            template = env.get_template(self.template)
        return template.render(**self.template_variables(value))
    
    def display(self, value=None):
        return self._render_template(value)


class Context(object):
    value = None


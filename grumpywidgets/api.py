# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from jinja2 import Environment, PackageLoader, Template


__all__ = ['Widget']

class Widget(object):
    id = None
    template = None
    css_classes = None
    children = ()
    
    _template_path = ('grumpywidgets', 'templates')
    
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
    
    def _render_template(self, values):
        if hasattr(self.template, 'read'):
            template = Template(self.template.read())
        else:
            env = Environment(loader=PackageLoader(*self._template_path))
            template = env.get_template(self.template)
        return template.render(**values)
    
    def display(self, value):
        if not isinstance(value, dict):
            value = dict(value = value)
        return self._render_template(value)



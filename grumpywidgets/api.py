from jinja2 import Environment, PackageLoader, Template

from grumpywidgets import template_helpers
from grumpywidgets.context import Context
from grumpywidgets.lib.simple_super import SuperProxy


__all__ = ['Widget']

class Widget(object):
    name = None
    id = None
    template = None
    css_classes = None
    
    parent = None
    
    _template_path = ('grumpywidgets', 'templates')
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
            raise TypeError("display() got an unexpected keyword argument '%s'" % first)
        variables = self.template_variables(value, **kwargs)
        return self._render_template(variables)
    
    def css_classes_for_container(self):
        return ('widgetcontainer', )
    
    def id_for_container(self):
        if self.id is None:
            return None
        return '%s-container' % self.id


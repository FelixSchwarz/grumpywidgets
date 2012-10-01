# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from copy import deepcopy

from jinja2 import Environment, PackageLoader, Template

from grumpywidgets import template_helpers
from grumpywidgets.lib.simple_super import SuperProxy
from grumpywidgets.lib.pythonic_testcase import assert_equals


__all__ = ['Widget']

class Widget(object):
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
    
    def propagate_to_context(self, value, attribute_name='value'):
        # That's a bit of a hack, remove that if possible
        if attribute_name == 'errors':
            if not isinstance(value, (list, tuple)):
                value = (value, )
        setattr(self.context, attribute_name, value)
    
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
    def __init__(self, value=None, errors=None, unvalidated_value=None):
        self.value = value
        self.errors = errors
        self.unvalidated_value = unvalidated_value
    
    def copy(self):
        klass = self.__class__
        attributes = dict(
            value=deepcopy(self.value), 
            errors=deepcopy(self.errors),
            unvalidated_value=deepcopy(self.unvalidated_value),
        )
        return klass(**attributes)
    __deepcopy__ = copy
    
    def contains_errors(self):
        if (self.errors is not None) and (len(self.errors) > 0):
            return True
        return False
    
    def _is_list_like(self, value):
        # list(InvalidDataError) returns [<error msg>]
        return hasattr(value, '__iter__')
    
    def update_value(self, value=None, unvalidated_value=None, errors=None):
        if unvalidated_value is not None:
            self.unvalidated_value = unvalidated_value
        elif errors is not None:
            # pycerberus returns only a single error per validator, but 
            # containers like Form or ListField should not have to dive into 
            # the error dict and convert everything themself. Instead let's do 
            # it here in one central place. Also I think makes the API a bit 
            # more convenient.
            if not self._is_list_like(errors):
                errors = (errors, )
            self.errors = errors
        else:
            self.value = value


class RepeatingContext(object):
    def __init__(self, child_creator):
        self.items = []
        self.child_creator = child_creator
    
    def contains_errors(self):
        for item in self.items:
            if item.contains_errors():
                return True
        return False
    
    @property
    def errors(self):
        errors_ = []
        for context in self.items:
            errors_.append(context.errors)
        return tuple(errors_)
    
    def update_value(self, value=None, unvalidated_value=None, errors=None):
        if unvalidated_value is not None:
            attr_name = 'unvalidated_value'
            values = unvalidated_value
        elif errors is not None:
            attr_name = 'errors'
            values = errors
        else:
            attr_name = 'value'
            values = value
        if len(self.items) == 0:
            self._create_new_items(n=len(values))
        else:
            assert_equals(len(self.items), len(values))
        for context, value_ in zip(self.items, values):
            context.update_value(**{attr_name: value_})
    
    def _create_new_items(self, n):
        for i in range(n):
            context = self.child_creator()
            self.items.append(context)
    
    @property
    def value(self):
        values = []
        for context in self.items:
            values.append(context.value)
        return tuple(values)
    
    @property
    def unvalidated_value(self):
        values = []
        for context in self.items:
            values.append(context.unvalidated_value)
        return tuple(values)


class ContainerContext(object):
    def __init__(self):
        self.children = {}
    
    def __getattr__(self, name):
        if name not in self.children:
            klassname = self.__class__.__name__
            raise AttributeError('%s object has no child with name %r' % (klassname, name))
        return self.children[name]
    
    def contains_errors(self):
        for child in self.children.values():
            if child.contains_errors():
                return True
        return False
    
    @property
    def errors(self):
        errors_ = {}
        for name, contexts in self.children.items():
            errors_[name] = contexts.errors
        return errors_
    
    def update_value(self, value=None, unvalidated_value=None, errors=None):
        if unvalidated_value is not None:
            attr_name = 'unvalidated_value'
            values = dict()
            for name, value_ in unvalidated_value.items():
                if name in self.children:
                    values[name] = value_
        elif errors is not None:
            attr_name = 'errors'
            values = errors
        else:
            attr_name = 'value'
            values = value
        if values is None:
            return
        for name, value_ in values.items():
            if name not in self.children:
                raise ValueError("unknown parameter %r" % name)
            self.children[name].update_value(**{attr_name: value_})
    
    def copy(self):
        context = self.__class__()
        for name, child in self.children.items():
            context.children[name] = child.copy()
        return context
    __deepcopy__ = copy
    
    @property
    def value(self):
        values = {}
        for name, contexts in self.children.items():
            values[name] = contexts.value
        return values
    
    @property
    def unvalidated_value(self):
        values = {}
        for name, contexts in self.children.items():
            values[name] = contexts.unvalidated_value
        return values



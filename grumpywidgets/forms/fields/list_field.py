# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.errors import InvalidDataError
from pycerberus.schema import SchemaValidator
from pycerberus.validators import ForEach

from grumpywidgets.forms.api import InputWidget
from grumpywidgets.lib.pythonic_testcase import assert_true

__all__ = ['ListField']

class ListField(InputWidget):
    template = 'list_field.jinja2'
    children = ()
    
    def __init__(self, *args, **kwargs):
        self.super.__init__(*args, **kwargs)
        for child in self.children:
            # TODO: use a weakref to avoid memory hogging
            child.parent = self
    
    def validate(self, values):
        self._propagate_to_children(values, pop=False, attribute_name='unvalidated_value')
#        self.initialize_children(values, pop=False, attribute_name='unvalidated_value')
        try:
            validated_values = self.validator.process(values)
        except InvalidDataError, e:
            for children, errors in zip(self.context.children, e.unpack_errors()):
                for child in children:
                    if (not hasattr(child, 'name')) or (child.name is None):
                        continue
                    child_error = errors and errors.get(child.name) or None
                    if child_error is not None:
                        child_error = (child_error, )
                    child.context.errors = child_error
            raise
        return validated_values
    
    @property
    def validator(self):
        schema = SchemaValidator()
        for child in self.children:
            child_name = getattr(child, 'name', None)
            if child_name is None:
                continue
            child_validator = getattr(child, 'validator', None)
            if child_validator is None:
                continue
            schema.add(child_name, child_validator)
        return ForEach(schema)
    
    def css_classes_for_container(self):
        # skipping InputWidget because we don't want to have '<name>-container'
        # maybe not very elegant, actually ListField might turn out to be a 
        # regular container...
        classes = set()
        if self.name is not None:
            classes.add(self.name+'-list')
        if self.css_classes:
            classes = classes.union(set(self.css_classes))
        return tuple(classes)
    
    def initialize_children(self, number_items):
        self.context.children = []
        for i in range(number_items):
            children = []
            for child in self.children:
                clone = child.copy()
                children.append(clone)
            self.context.children.append(children)
    
    def _propagate_to_children(self, values, pop=True, attribute_name='value'):
        if not hasattr(self.context, 'children') or (len(self.context.children) != len(values)):
            self.initialize_children(len(values))
        for children, child_values in zip(self.context.children, values):
            for child in children:
                if hasattr(child, 'name'):
                    value = child_values.get(child.name)
                    if pop:
                        del child_values[child.name]
                    child.propagate_to_context(value, attribute_name)
        return values
    
    def display(self, value=None, **kwargs):
        self.propagate_to_context(value, pop=True, attribute_name='value')
        return self.super(value=None, **kwargs)
    
    def propagate_to_context(self, value, attribute_name='value', pop=False):
        if value is None:
            return
        if attribute_name == 'errors':
            # hack-ish, should probably be a separate method
            assert_true(len(value) in (0, 1), 'unsupported number of errors (not yet implemented')
            error = value[0].unpack_errors()
            value = error
        value = value or []
        values = self._propagate_to_children(value or [], pop=pop, attribute_name=attribute_name)
        if not pop:
            return
        for child_values in values:
            if child_values:
                first_key = list(child_values)[0]
                raise ValueError('unknown parameter %r' % first_key)
        return values



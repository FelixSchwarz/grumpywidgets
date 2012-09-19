# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.schema import SchemaValidator

from grumpywidgets.api import Widget
from grumpywidgets.lib.pythonic_testcase import assert_none
from pycerberus.errors import InvalidDataError


__all__ = ['InputWidget', 'Form']

class InputWidget(Widget):
    validator = None
    name = None
    label = None
    children = ()
    
    def __init__(self, name=None, **kwargs):
        if name is not None:
            kwargs['name'] = name
        super(InputWidget, self).__init__(**kwargs)
        self.context.unvalidated_value = None
    
    def validate(self, value):
        if self.validator is None:
            return value
        return self.validator.process(value)
    
    def display(self, value=None):
        if (value is None) and (self.context.value is None):
            if not hasattr(self.context, 'unvalidated_value'):
                print self
            value = self.context.unvalidated_value
        return self.super(value=value)


class Form(InputWidget):
    url = ''
    method = 'POST'
    charset = 'UTF-8'
    template = 'form.jinja2'
    
    def validate(self, values):
        assert_none(self.validator) # not supported for now
        self.initialize_children(values, pop=False, attribute_name='unvalidated_value')
        schema = SchemaValidator()
        for child in self.children:
            child_name = getattr(child, 'name', None)
            if child_name is None:
                continue
            child_validator = getattr(child, 'validator', None)
            if child_validator is None:
                continue
            schema.add(child_name, child_validator)
        try:
            validated_values = schema.process(values)
        except InvalidDataError, e:
            errors = e.error_dict()
            for key, value in errors.items():
                if not isinstance(value, (list, tuple)):
                    errors[key] = (value, )
            self.initialize_children(errors, pop=False, attribute_name='errors')
            raise
        return validated_values
    
    def initialize_children(self, values, pop=True, attribute_name='value'):
        for child in self.children:
            child_name = getattr(child, 'name', None)
            if (child_name is None) or (child_name not in values):
                continue
            value = values[child_name]
            if pop:
                del values[child_name]
            setattr(child.context, attribute_name, value)
        return values
    
    def display(self, value=None):
        values = self.initialize_children(value or dict())
        if values:
            first_key = values.keys()[0]
            raise ValueError("Unknown parameter '%s' passed to display()" % first_key)
        return self.super(value=values)

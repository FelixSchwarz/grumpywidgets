# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.errors import InvalidDataError
from pycerberus.schema import SchemaValidator

from grumpywidgets.api import Widget
from grumpywidgets.lib.pythonic_testcase import assert_none
from grumpywidgets.widgets import Label


__all__ = ['InputWidget', 'Form']

class InputWidget(Widget):
    validator = None
    name = None
    label = None
    
    def __init__(self, name=None, **kwargs):
        if name is not None:
            kwargs['name'] = name
        super(InputWidget, self).__init__(**kwargs)
        self.context.unvalidated_value = None
    
    def validate(self, value):
        if self.validator is None:
            return value
        return self.validator.process(value)
    
    def _display_value(self, value):
        value = self.super(value)
        if value is None:
            value = self.context.unvalidated_value
        if self.validator is None:
            return value
        return self.validator.stringify(value)
    
    def display(self, value=None):
        if (value is None) and (self.context.value is None):
            value = self.context.unvalidated_value
        return self.super(value=value)
    
    def label_widget(self):
        if self.label is None:
            return None
        id_ = self.id and self.id+'-label' or None
        label = Label(id=id_, for_=self.id, value=self.label)
        return label
    
    def css_classes_for_container(self):
        classes = self.super()
        if self.name is None:
            return classes
        return tuple(set(classes) | set([self.name+'-container']))


class Form(InputWidget):
    url = ''
    method = 'POST'
    charset = 'UTF-8'
    template = 'form.jinja2'
    children = ()
    
    def validate(self, values):
        assert_none(self.validator) # not supported for now
        self.initialize_children(values, pop=False, attribute_name='unvalidated_value')
        try:
            validated_values = self.validation_schema().process(values)
        except InvalidDataError, e:
            errors = dict()
            for key, value in e.error_dict().items():
                if not isinstance(value, (list, tuple)):
                    value = (value, )
                errors[key] = value
            self.initialize_children(errors, pop=False, attribute_name='errors')
            raise
        return validated_values
    
    def validation_schema(self):
        schema = SchemaValidator()
        for child in self.children:
            child_name = getattr(child, 'name', None)
            if child_name is None:
                continue
            child_validator = getattr(child, 'validator', None)
            if child_validator is None:
                continue
            schema.add(child_name, child_validator)
        return schema
    
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

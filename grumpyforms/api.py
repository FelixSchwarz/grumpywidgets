# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from __future__ import absolute_import

import os
import copy

from pycerberus.errors import InvalidDataError
from pycerberus.schema import SchemaValidator
from pythonic_testcase import assert_isinstance

from grumpywidgets.api import Widget
from grumpywidgets.context import Context, CompoundContext
from grumpywidgets.widgets import Label
from .variabledecode import variable_decode


__all__ = ['decode_parameters', 'InputWidget', 'Form']

def decode_parameters(parameters):
    return variable_decode(parameters)

this_dir = os.path.dirname(__file__)
grumpyforms_template_dir = os.path.join(this_dir, 'templates')

class InputWidget(Widget):
    validator = None
    name = None
    label = None

    _template_path = grumpyforms_template_dir
    template_engine = 'jinja2'

    def __init__(self, name=None, **kwargs):
        if name is not None:
            kwargs['name'] = name
        super(InputWidget, self).__init__(**kwargs)

    def validate(self, value):
        c = Context(unvalidated_value=value)
        if self.validator is not None:
            try:
                c.value = self.validator.process(value)
            except InvalidDataError, e:
                c.errors = (e, )
        else:
            c.value = value
        return c

    def _display_value(self, value):
        value = self.super(value)
        if value is None:
            value = self.context.unvalidated_value
        if self.validator is None:
            return value
        return self.validator.revert_conversion(value)

    def display(self, value=None, **kwargs):
        if (value is None) and (self.context.value is None):
            value = self.context.unvalidated_value
        return self.super(value=value, **kwargs)

    def label_widget(self):
        if self.label is None:
            return None
        id_ = self.id and self.id+'-label' or None
        label = Label(id=id_, for_=self.id, value=self.label)
        return label

    def is_field(self):
        return True

    def css_classes_for_container(self):
        classes = set(self.super())
        if self.name is not None:
            classes.add(self.name+'-container')
        if self.context.contains_errors():
            classes.add('validationerror')
        if (self.validator is not None):
            if hasattr(self.validator, 'is_required') and self.validator.is_required():
                classes.add('requiredfield')
        return tuple(classes)

    def path(self):
        parts = []
        if self.parent is not None:
            parts.extend(self.parent.path())
        if self.name is not None:
            parts.append(self.name)
        return tuple(parts)

    def full_name(self):
        return '.'.join(self.path())


class Form(InputWidget):
    url = ''
    method = 'POST'
    charset = 'UTF-8'
    enctype = None
    template_name = 'form'
    children = ()

    def __init__(self, *args, **kwargs):
        self.super.__init__(*args, **kwargs)
        self._initialize_children()

    def _initialize_children(self):
        instance_children = []
        for child in self.children:
            cloned_child = child.copy()
            # TODO: use a weakref to avoid memory hogging
            cloned_child.parent = self
            instance_children.append(cloned_child)
        self.children = instance_children

    def validate(self, values):
        context = self.new_context(unvalidated=values)
        try:
            schema = self.validation_schema()
            validated_values = schema.process(values)
        except InvalidDataError, e:
            context.update_value(errors=e.unpack_errors())
        else:
            context.update_value(validated_values)
        return context

    def validation_schema(self):
        if self.validator is None:
            schema = SchemaValidator()
        else:
            schema = copy.deepcopy(self.validator)
        for child in self.children:
            if child.name is None:
                continue
            child_validator = getattr(child, 'validator', None)
            if child_validator is None:
                continue
            schema.add(child.name, child_validator)
        return schema

    def display(self, value=None, **kwargs):
        if value is not None:
            self.context.update_value(value)
        return self.super(value=None, **kwargs)

    def children_(self):
        for child in self.children:
            child_name = getattr(child, 'name', None)
            if child_name not in self.context.children:
                context = child.new_context()
            else:
                context = self.context.children[child_name]
            child.set_context(context)
            yield child

    def path(self):
        if self.parent is None:
            return ()
        return self.super()

    def new_context(self, unvalidated=None):
        context = CompoundContext()
        for child in self.children:
            context.children[child.name] = child.new_context()
        if unvalidated is not None:
            context.update_value(unvalidated_value=unvalidated)
        return context

    def set_context(self, context):
        assert_isinstance(context, CompoundContext)
        self.context = context

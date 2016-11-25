# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.errors import InvalidDataError
from pycerberus.schema import SchemaValidator
from pycerberus.validators import ForEach
from pythonic_testcase import *

from grumpywidgets.context import FormData, RepeatingFieldData
from grumpyforms.api import InputWidget

__all__ = ['ListField']

class ListField(InputWidget):
    template_name = 'list_field'
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

    def _child_context_creator(self):
        container = FormData()
        for child in self.children:
            container.children[child.name] = child.new_context()
        return container.copy

    def new_context(self, unvalidated=None):
        context = RepeatingFieldData(self._child_context_creator())
        if unvalidated is not None:
            context.update_value(initial_value=unvalidated)
        return context

    def set_context(self, context):
        assert_isinstance(context, RepeatingFieldData)
        self.context = context

    def child_rows(self):
        self.context.count = 0
        for container_context in self.context.items:
            row = []
            self.context.count += 1
            for child in self.children:
                if child.name not in container_context.children:
                    context = child.new_context()
                else:
                    context = container_context.children[child.name]
                child.set_context(context)
                row.append(child)
            yield tuple(row)

    def validate(self, values):
        context = self.new_context(unvalidated=values)
        try:
            validated_values = self.validator.process(values)
        except InvalidDataError, e:
            for child_context, errors in zip(context.items, e.unpack_errors()):
                child_context.update_value(errors=errors)
        else:
            context.update_value(validated_values)
        return context

    @property
    def validator(self):
        schema = SchemaValidator()
        for child in self.children:
            if child.name is None:
                continue
            child_validator = getattr(child, 'validator', None)
            if child_validator is None:
                continue
            schema.add(child.name, child_validator)
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

    def display(self, value=None, **kwargs):
        if value is not None:
            self.context.update_value(value)
        return self.super(value=None, **kwargs)

    def path(self):
        parts = []
        if self.parent is not None:
            parts.extend(self.parent.path())
        if self.name is not None:
            widget_name = self.name
            if hasattr(self.context, 'count'):
                widget_name = '%s-%s' % (self.name, self.context.count)
            parts.append(widget_name)
        return tuple(parts)

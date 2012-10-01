# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.errors import InvalidDataError
from pycerberus.schema import SchemaValidator
from pycerberus.validators import ForEach

from grumpywidgets.api import RepeatingContext, ContainerContext
from grumpywidgets.forms.api import InputWidget
from grumpywidgets.lib.pythonic_testcase import assert_isinstance

__all__ = ['ListField']

class ListField(InputWidget):
    template = 'list_field.jinja2'
    children = ()
    
    def __init__(self, *args, **kwargs):
        self.super.__init__(*args, **kwargs)
        for child in self.children:
            # TODO: use a weakref to avoid memory hogging
            child.parent = self
    
    def _child_context_creator(self):
        container = ContainerContext()
        for child in self.children:
            container.children[child.name] = child.new_context()
        return container.copy
    
    def new_context(self, unvalidated=None):
        context = RepeatingContext(self._child_context_creator())
        if unvalidated is not None:
            context.update_value(unvalidated_value=unvalidated)
        return context
    
    def set_context(self, context):
        assert_isinstance(context, RepeatingContext)
        self.context = context
    
    def child_rows(self):
        for container_context in self.context.items:
            row = []
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


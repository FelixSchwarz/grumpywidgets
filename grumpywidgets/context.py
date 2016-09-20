# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from copy import deepcopy

from pythonic_testcase import *


__all__ = []

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
        self.count = 0

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


class CompoundContext(object):
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


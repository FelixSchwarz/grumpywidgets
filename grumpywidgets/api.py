# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

__all__ = ['Widget']

class Widget(object):
    id = None
    template = None
    css_classes = None
    children = ()
    
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
    
    def display(self, value):
        return unicode(value)



# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

__all__ = ['Widget']

class Widget(object):
    template = None
    id = None
    css_classes = None
    children = ()
    
    def display(self, value):
        return unicode(value)



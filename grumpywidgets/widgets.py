# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from __future__ import absolute_import

from .api import Widget


__all__ = ['Label']

class Label(Widget):
    for_ = None
    value = None
    template_name = 'label'

    def _display_value(self, value):
        value = self.super()
        if value is not None:
            return value
        return self.value


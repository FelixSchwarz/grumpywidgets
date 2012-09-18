# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from grumpywidgets.api import Widget


__all__ = ['InputWidget']

class InputWidget(Widget):
    validator = None
    name = None
    label = None


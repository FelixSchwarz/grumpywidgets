# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

import types


__all__ = ['widgets_in_module']

def widgets_in_module(module, basetype):
    for name in dir(module):
        if name.startswith('_'):
            continue
        symbol = getattr(module, name)
        if not isinstance(symbol, (types.TypeType, types.ClassType)):
            # issubclass below works only on classes
            continue
        if not issubclass(symbol, basetype):
            continue
        widget = symbol
        yield (name, widget)

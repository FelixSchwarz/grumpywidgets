# -*- coding: UTF-8 -*-
# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from contextlib import contextmanager


__all__ = ['provide_as_dict_item']

@contextmanager
def provide_as_dict_item(dictcontainer, key, value):
    is_dict_like = hasattr(dictcontainer, 'pop')
    if not is_dict_like:
        yield
    else:
        previous_value = dictcontainer.pop(key, None)
        dictcontainer[key] = value
        yield
        del dictcontainer[key]

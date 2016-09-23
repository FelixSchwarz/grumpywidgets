# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.


from .checkbox import Checkbox

__all__ = ['Radiobutton']

class Radiobutton(Checkbox):
    template_name = 'radiobutton'

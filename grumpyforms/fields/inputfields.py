# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.validators import EmailAddressValidator, StringValidator

from grumpyforms.api import InputWidget


__all__ = ['EmailField', 'HiddenField', 'PasswordField', 'TextField']

class TextLikeInputField(InputWidget):
    template_name = 'textlike_input_field'
    validator = StringValidator()


class EmailField(TextLikeInputField):
    type = 'email'
    validator = EmailAddressValidator()


class HiddenField(TextLikeInputField):
    type = 'hidden'

    def is_hidden(self):
        return True


class PasswordField(TextLikeInputField):
    type = 'password'


class TextField(TextLikeInputField):
    type = 'text'
    validator = StringValidator(required=False)


# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.


from grumpywidgets.forms.api import Form
from grumpywidgets.lib.pythonic_testcase import *


class FormTest(PythonicTestCase):
    def test_forms_return_empty_path(self):
        form = Form('foo')
        
        assert_none(form.parent)
        assert_equals((), form.path())


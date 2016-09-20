# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pythonic_testcase import *

from grumpyforms.api import Form


class FormAttributesTest(PythonicTestCase):
    def test_can_render_empty_form(self):
        class EmptyForm(Form):
            pass
        assert_equals('<form action="" method="POST" accept-charset="UTF-8"></form>',
                      EmptyForm().display(None))

    def test_can_render_url(self):
        class URLForm(Form):
            url = 'http://foo.example/submit.php'
        assert_equals('<form action="http://foo.example/submit.php" method="POST" accept-charset="UTF-8"></form>',
                      URLForm().display(None))

    def test_can_render_method(self):
        class MethodForm(Form):
            method = 'PUT'
        assert_equals('<form action="" method="PUT" accept-charset="UTF-8"></form>',
                      MethodForm().display(None))

    def test_can_render_form_name(self):
        class NamedForm(Form):
            name = 'named_form'
        assert_equals('<form name="named_form" action="" method="POST" accept-charset="UTF-8"></form>',
                      NamedForm().display(None))

    def test_can_render_form_id(self):
        class IDForm(Form):
            id = 'form-id'
        assert_equals('<form id="form-id" action="" method="POST" accept-charset="UTF-8"></form>',
                      IDForm().display(None))

    def test_can_render_charset(self):
        class CharsetForm(Form):
            charset = 'ISO-8859-1'
        assert_equals('<form action="" method="POST" accept-charset="ISO-8859-1"></form>',
                      CharsetForm().display(None))

    def test_can_render_css_classes(self):
        class StyledForm(Form):
            css_classes = ('foo', 'bar')
        assert_equals('<form class="foo bar" action="" method="POST" accept-charset="UTF-8"></form>',
                      StyledForm().display(None))

    def test_can_render_enctype(self):
        assert_equals('<form action="" method="POST" enctype="multipart/form-data" accept-charset="UTF-8"></form>',
                      Form(enctype='multipart/form-data').display(None))

    def test_can_specify_attributes_on_display(self):
        assert_contains('action="/login"', Form().display(url='/login'))


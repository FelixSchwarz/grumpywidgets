# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pythonic_testcase import *

from grumpyforms.api import Form
from grumpyforms.genshi_ import GenshiForm
from grumpywidgets.testhelpers import assert_same_html, flatten_stream


class FormRenderingTest(PythonicTestCase):
    template_engine = 'jinja2'

    def _form(self):
        form_class = Form
        form_class.template_engine = self.template_engine
        return form_class

    def test_can_render_empty_form(self):
        class EmptyForm(self._form()):
            pass
        assert_same_html('<form action="" method="POST" accept-charset="UTF-8"></form>',
                      EmptyForm().display(None))

    def test_can_render_url(self):
        class URLForm(self._form()):
            url = 'http://foo.example/submit.php'
        assert_same_html('<form action="http://foo.example/submit.php" method="POST" accept-charset="UTF-8"></form>',
                      URLForm().display(None))

    def test_can_render_method(self):
        class MethodForm(self._form()):
            method = 'PUT'
        assert_same_html('<form action="" method="PUT" accept-charset="UTF-8"></form>',
                      MethodForm().display(None))

    def test_can_render_form_name(self):
        class NamedForm(self._form()):
            name = 'named_form'
        assert_same_html('<form name="named_form" action="" method="POST" accept-charset="UTF-8"></form>',
                      NamedForm().display(None))

    def test_can_render_form_id(self):
        class IDForm(self._form()):
            id = 'form-id'
        assert_same_html('<form id="form-id" action="" method="POST" accept-charset="UTF-8"></form>',
                      IDForm().display(None))

    def test_can_render_charset(self):
        class CharsetForm(self._form()):
            charset = 'ISO-8859-1'
        assert_same_html('<form action="" method="POST" accept-charset="ISO-8859-1"></form>',
                      CharsetForm().display(None))

    def test_can_render_css_classes(self):
        class StyledForm(self._form()):
            css_classes = ('foo', 'bar')
        assert_same_html('<form class="foo bar" action="" method="POST" accept-charset="UTF-8"></form>',
                      StyledForm().display(None))

    def test_can_render_enctype(self):
        assert_same_html('<form action="" method="POST" enctype="multipart/form-data" accept-charset="UTF-8"></form>',
                      self._form()(enctype='multipart/form-data').display(None))

    def test_can_specify_attributes_on_display(self):
        rendered_form = self._form()().display(url='/login')
        assert_contains(' action="/login"', flatten_stream(rendered_form))


class FormWithGenshiRenderingTest(FormRenderingTest):
    template_engine = 'genshi'


class GenshiFormRenderingTest(FormRenderingTest):
    def _form(self):
        return GenshiForm


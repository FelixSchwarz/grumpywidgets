# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from pycerberus.api import Validator
from pycerberus.schema import SchemaValidator
from pycerberus.validators import IntegerValidator
from pythonic_testcase import *

from grumpyforms.api import Form
from grumpyforms.fields import TextField


class FormValidationTest(PythonicTestCase):
    def test_can_validate_empty_form(self):
        result = Form().validate({})
        assert_equals({}, result.value)

    def test_can_validate_form_with_single_widget(self):
        form = Form(children = (TextField('foo', validator=IntegerValidator()),))
        result = form.validate({'foo': '42'})
        assert_equals({'foo': 42}, result.value)

    def test_returns_context_on_validation_error_which_contains_all_child_errors(self):
        class MultiChildrenForm(Form):
            children = (
                TextField('foo', validator=IntegerValidator()),
                TextField('bar', validator=IntegerValidator()),
            )
        form = MultiChildrenForm()

        result = form.validate({})
        assert_true(result.contains_errors())
        assert_equals(['foo', 'bar'], list(result.errors))

    def test_returns_only_validated_values(self):
        class FilteringForm(Form):
            children = (
                TextField('foo', validator=IntegerValidator()),
            )

        result = FilteringForm().validate({'foo': '42', 'bar': None})
        assert_false(result.contains_errors())
        assert_equals({'foo': 42}, result.value)


class FormsWithValidationSchemasTest(PythonicTestCase):
    class AEqualsB(Validator):
        def messages(self):
            return dict(not_equal='A is not equal B')

        def validate(self, values, context):
            assert_contains('a', values)
            if values['a'] == values['b']:
                return
            error_a = self.exception('not_equal', values['a'], context)
            error_b = self.exception('not_equal', values['b'], context)
            self.raise_error('not_equal', values, context,
                             error_dict=dict(a=error_a, b=error_b))

    def match_form(self):
        class MatchingFieldsSchema(SchemaValidator):
            formvalidators = (self.AEqualsB(),)

        class MatchForm(Form):
            children = (
                TextField('a', validator=IntegerValidator()),
                TextField('b', validator=IntegerValidator()),
            )
            validator = MatchingFieldsSchema()
        return MatchForm()

    def test_can_predefine_validation_schema(self):
        form = self.match_form()

        result = form.validate(dict(a='1', b='1'))
        assert_false(result.contains_errors(), result.errors)
        assert_equals(dict(a=1, b=1), result.value)

        result = form.validate({'a': '1', 'b': '2'})
        assert_true(result.contains_errors())

    def form_with_shared_base_schema(self):
        class MatchingFieldsSchema(SchemaValidator):
            formvalidators = (self.AEqualsB(),)
        base_schema = MatchingFieldsSchema()

        class IntForm(Form):
            children = (
                TextField('a', validator=IntegerValidator()),
                TextField('b', validator=IntegerValidator()),
            )
            validator = base_schema

        class StringForm(Form):
            children = (TextField('a'), TextField('b'), TextField('c'), )
            validator = base_schema
        return IntForm(), StringForm()

    def test_can_copy_predefined_schema(self):
        int_form, string_form = self.form_with_shared_base_schema()

        # The problem might look harmless in this case - two forms returning the
        # same schema instance if you manually call '-validation_schema()'.
        # however this is a potential race condition if multiple threads are
        # involved. Also pycerberus is mostly thread-safe so we should prevent
        # this error.
        int_schema = int_form.validation_schema()
        # this is where the original error became apparent: The second form must
        # copy the schema instance.
        string_schema = string_form.validation_schema()

        assert_equals(dict(a=1, b=1), int_schema.process(dict(a='1', b='1')))
        assert_equals(dict(a='2', b='2', c='ab'),
                      string_schema.process(dict(a='2', b='2', c='ab')))


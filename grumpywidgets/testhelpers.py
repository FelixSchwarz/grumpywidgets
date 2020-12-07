# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

import re
from xml.etree import ElementTree

from htmlcompare import assert_same_html as assert_same_html_


__all__ = [
    'as_normalized_html',
    'assert_same_html',
    'flatten_stream',
    'reconfigure_widget',
    'template_widget',
]

def assert_same_html(expected, actual, message=None):
    assert_same_html_(expected, flatten_stream(actual), message=message)

def flatten_stream(value):
    if hasattr(value, '__unicode__'):
        # serialize Genshi stream to plain strings
        value = value.__unicode__()
    return value

def as_normalized_html(input_):
    # ----------------------------------------------------------------------
    # initial idea from Fredrik Lundh
    # http://mail.python.org/pipermail/xml-sig/2003-November/009997.html
    def parse_as_normalized_xml(xml):
        xml_document = ElementTree.fromstring(flatten_stream(xml))
        for node in xml_document.iter():
            if node.text:
                node.text = node.text.strip()
            if node.tail is not None:
                node.tail = node.tail.strip() or None
        return xml_document
    # ----------------------------------------------------------------------
    # to my suprise ElementTree.tostring() returns bytes and not a string
    # in Python 3, see https://bugs.python.org/issue10942
    # We could work around the issue by using "encoding='unicode'" but
    # unfortunately Python 2 doesn't know about the 'unicode' encoding.
    # So the simplest way to tackle this is to decode the bytes here.
    result = ElementTree.tostring(parse_as_normalized_xml(input_))
    if isinstance(result, bytes):
        return result.decode('utf8')
    return result


def extract_classes(html):
    class_str = re.findall('class="\s*([^"]+)\s*"', html)[0]
    return set(re.split('\s+', class_str))


def reconfigure_widget(widget, template_engine):
    template = widget.template
    template_extension = '.' + template_engine
    if not template.endswith(template_extension):
        new_template = template.replace('.jinja2', template_extension)
        widget.template = new_template
    widget.template_engine = template_engine
    return widget


def template_widget(widget, template_engine, kwargs=None):
    """
    Return a widget instance using the specified template engine.
    """
    if kwargs is None:
        kwargs = {}
    if 'template_engine' in kwargs:
        return kwargs
    kwargs['template_engine'] = template_engine
    return widget(**kwargs)

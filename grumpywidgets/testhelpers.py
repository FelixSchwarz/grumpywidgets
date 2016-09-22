# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

from xml.etree import ElementTree

from pythonic_testcase import assert_equals


__all__ = ['assert_same_html', 'reconfigure_widget', 'template_widget']

def assert_same_html(expected, actual, message=None):
    # We need to normalize all whitespace (XML pretty printing) as well as
    # dealing with <foo></foo> vs. <foo/>.
    # BeautifulSoup was not up to the task as it does not cope well with the
    # <foo/> variants (basically it assumes <foo>(other tags)</foo>)
    # ----------------------------------------------------------------------
    # initial idea from Fredrik Lundh
    # http://mail.python.org/pipermail/xml-sig/2003-November/009997.html
    def parse_as_normalized_xml(xml):
        xml_document = ElementTree.fromstring(xml)
        for node in xml_document.getiterator():
            if node.text:
                node.text = node.text.strip()
            node.tail = None
        return xml_document
    first_xml = ElementTree.tostring(parse_as_normalized_xml(expected))
    second_xml = ElementTree.tostring(parse_as_normalized_xml(actual))
    # ----------------------------------------------------------------------
    assert_equals(first_xml, second_xml, message=message)


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

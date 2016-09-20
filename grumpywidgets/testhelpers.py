# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.


__all__ = ['template_widget']

def template_widget(widget, template_engine, kwargs):
    """
    Return a widget instance using the specified template engine.
    """
    if 'template_engine' in kwargs:
        return kwargs
    kwargs['template_engine'] = template_engine

    template = widget.template
    template_extension = '.' + template_engine
    if not template.endswith(template_extension):
        template = template.replace('.jinja2', template_extension)
        kwargs['template'] = template
    return widget(**kwargs)

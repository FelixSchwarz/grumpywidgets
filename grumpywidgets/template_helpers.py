# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.


__all__ = ['render_class', 'render_label', 'error_messages']

def render_class(classes):
    if not classes:  # [], None, ''
        return None
    return ' '.join(classes)

def render_label(widget):
    if not hasattr(widget, 'label_widget'):
        return ''
    label = widget.label_widget()
    if not label:
        return ''
    return label.display()

def error_messages(context):
    if (not context.contains_errors()) or isinstance(context.errors, dict):
        return ()
    messages = []
    for error in context.errors:
        if isinstance(error, dict):
            continue
        messages.append(error.details().msg())
    return tuple(messages)

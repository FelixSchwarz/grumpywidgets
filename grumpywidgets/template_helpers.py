# This file is a part of GrumpyForms.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

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
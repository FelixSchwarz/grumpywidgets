# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

try:
    from genshi.template import MarkupTemplate, TemplateLoader
    is_genshi_available = True
except ImportError:
    is_genshi_available = False


__all__ = ['render_genshi_template']

def render_genshi_template(template, template_variables, template_path):
    if not is_genshi_available:
        raise ValueError('Genshi not available')
    if hasattr(template, 'read'):
        template_ = MarkupTemplate(template.read())
        template.seek(0)
    else:
        loader = TemplateLoader((template_path,))
        template_ = loader.load(template)
    return template_.generate(**template_variables).render('xml')

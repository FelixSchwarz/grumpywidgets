# This file is a part of GrumpyWidgets.
# The source code contained in this file is licensed under the MIT license.
# See LICENSE.txt in the main project directory, for more information.

try:
    from jinja2 import Environment, PackageLoader, Template
    from jinja2.loaders import FileSystemLoader
    is_jinja2_available = True
except ImportError:
    is_jinja2_available = False
import six

__all__ = ['render_jinja_template']

def render_jinja_template(template, template_variables, template_path):
    if not is_jinja2_available:
        raise ValueError('Jinja2 not available')
    if hasattr(template, 'read'):
        template_ = Template(template.read())
        template.seek(0)
    else:
        if isinstance(template_path, six.string_types):
            loader = FileSystemLoader(template_path)
        else:
            loader = PackageLoader(*template_path)
        env = Environment(loader=loader)
        template_ = env.get_template(template)
    return template_.render(**template_variables)

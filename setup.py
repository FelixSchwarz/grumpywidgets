#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

import setuptools


def requires_from_file(filename):
    requirements = []
    with open(filename, 'r') as requirements_fp:
        for line in requirements_fp.readlines():
            match = re.search('^\s*([a-zA-Z][^#]+?)(\s*#.+)?\n$', line)
            if match:
                requirements.append(match.group(1))
    return requirements

setuptools.setup(
    name = 'GrumpyWidgets',
    version = '0.3dev',

    description = 'A grumpy widget library',
    license = 'MIT',
    author = 'Felix Schwarz',
    author_email = 'felix.schwarz@oss.schwarz.eu',
    install_requires=requires_from_file('requirements.txt'),

    namespace_packages = [
        'grumpyforms',
        'grumpyforms.ext',
        'grumpywidgets',
        'grumpywidgets.ext',
    ],
    packages=setuptools.find_packages(),
    include_package_data = True,
    tests_require = ['nose'],
    test_suite = 'nose.collector',
    zip_safe=False,
)

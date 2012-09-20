#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import setuptools

setuptools.setup(
    name = 'GrumpyWidgets',
    version = '0.2dev',
    
    description = 'A grumpy widget library',
    license = 'MIT',
    author = 'Felix Schwarz',
    author_email = 'felix.schwarz@oss.schwarz.eu',
    
    install_requires=('jinja2', 'pycerberus>=0.5dev'),
    tests_require = ['nose'],
    test_suite = 'nose.collector',

    zip_safe=False,
    packages=setuptools.find_packages(),
)
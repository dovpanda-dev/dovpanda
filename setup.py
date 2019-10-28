#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
doclink = """
Documentation
-------------

The full documentation is at http://dovpanda.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name="dovpanda",
    version="0.0.1-alpha2",
    description='Directions overlay for working with pandas in an analysis environment',
    author="Dean Langsam",
    author_email="deanla@gmail.com",
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    long_description_content_type="text/markdown",
    url="https://github.com/dovpanda-dev/dovpanda",
    packages=['dovpanda'],
    install_requires=['pandas'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

    ],
    python_requires='>=3.6',
)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

if sys.version_info < (3, 2):
    print("ApiDoc requires Python 3.2 or later")
    raise SystemExit(1)

from setuptools.command.test import test as TestCommand
from setuptools import setup, find_packages


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


if (3, 2) <= sys.version_info < (3, 3):
    requirements = ['Jinja2 == 2.6', 'PyYAML', 'jsonschema']
else:
    requirements = ['Jinja2', 'PyYAML', 'jsonschema']


setup(
    name='ApiDoc',
    version='1.1a0',
    description='Api Documentation Generator',
    long_description='''ApiDoc is a documentation generator designe for API built with Python.
It's developed by Jérémy Derussé and SFR Business Team.

Full documentation available on http://apidoc.rtfd.org.''',
    author='Jérémy Derussé',
    author_email='jeremy.derusse@sfr.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
    platforms=['Any'],
    packages=find_packages(exclude=['tests', 'tests.*', 'example', 'example.*', 'docs', 'docs.*']),
    entry_points={
        'console_scripts': [
            'apidoc-analyse = apidoc.command.analyse:main',
            'apidoc-render = apidoc.command.render:main',
            'apidoc-watch = apidoc.command.watch:main',
        ],
    },
    include_package_data=True,
    package_data={'apidoc': [
        'template/*.html',
        'template/helper/*.html',
        'template/partial/*.html',
        'template/layout/*.html',
        'template/resource/css/*.css',
        'template/resource/js/*.js',
        'template/resource/font/*',
        'datas/schemas/*.yml',
        'command/logging.yml',
    ]},
    install_requires=requirements,
    tests_require=['mock', 'pytest'],
    cmdclass={'test': PyTest}
)

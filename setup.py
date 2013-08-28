#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

if sys.version_info < (3, 2):
    print("ApiDoc requires Python 3.2 or later")
    raise SystemExit(1)

from setuptools import setup, find_packages
from setup_cmd import ApiDocTest, Resource

from apidoc import __version__


if (3, 2) <= sys.version_info < (3, 3):
    requirements = ['Jinja2 == 2.6', 'PyYAML==3.10', 'jsonschema==2.0.0']
else:
    requirements = ['Jinja2', 'PyYAML==3.10', 'jsonschema==2.0.0']


setup(
    name='ApiDoc',
    version=__version__,
    description='Api Documentation Generator',
    long_description=open("README.rst").read() + "\n\n" + open("CHANGES.rst").read(),
    author='Jérémy Derussé',
    author_email='jeremy.derusse@sfr.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
    platforms=['Any'],
    license='GPLv3+',
    url='http://solutionscloud.github.io/apidoc/',
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
    tests_require=['pytest', 'mock'],
    extras_require={
        'ci': ['flake8', 'behave', 'coverage', 'coveralls', 'mock', 'pytest'],
        'contribute': ['flake8', 'behave', 'coverage', 'mock', 'pytest', 'Sphinx', 'yuicompressor'],
    },
    cmdclass={
        'test': ApiDocTest,
        'resources': Resource,
    }
)

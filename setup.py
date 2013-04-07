#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='ApiDoc',
    version='1.0',
    description='Api Documentation Generator',
    author='Jérémy Derussé',
    author_email='jeremy@derusse.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    platforms=['Any'],
    packages=find_packages(exclude=['tests', 'tests.*']),
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
        'template/resource/css/*.css',
        'template/resource/js/*.js',
        'template/resource/img/*.png',
    ]},
    install_requires=[
        'Jinja2',
        'PyYAML',
        'pyinotify'
    ]
)

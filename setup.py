#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

if sys.version_info < (3, 2):
    print("ApiDoc requires Python 3.2 or later")
    raise SystemExit(1)

from setuptools import setup, find_packages
from setup_cmd import ApiDocTest, Resource, read_requirements, patch_requirements

from apidoc import __version__

requirements = read_requirements("install.txt")
if (3, 2) <= sys.version_info < (3, 3):
    requirements = patch_requirements(requirements, "install-32.patch")

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
            'apidoc = apidoc.command.run:main',
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
        'settings/schemas/*.yml',
        'settings/logging.yml',
    ]},
    install_requires=requirements,
    tests_require=read_requirements("test.txt"),
    extras_require={
        'ci': read_requirements("ci.txt"),
        'contribute': read_requirements("contribute.txt"),
    },
    cmdclass={
        'test': ApiDocTest,
        'resources': Resource,
    }
)

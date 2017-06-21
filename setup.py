#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'six>=1.10.0'
]

test_requirements = [
    'pip==9.0.1'
    'bumpversion==0.5.3'
    'backports.tempfile==1.0rc1'
    'wheel==0.29.0'
    'watchdog==0.8.3'
    'flake8==3.3.0'
    'tox==2.7.0'
    'coverage==4.3.4'
    'six==1.10.0'
    'Sphinx==1.5.5'
    'cryptography==1.8.1'
    'PyYAML==3.12'
    'pytest==3.0.7'
]

setup(
    name='lookml-gen',
    version='0.1.7',
    description="Programmatically generate LookML",
    long_description=readme + '\n\n' + history,
    author="Joe Schmid",
    author_email='jschmid@symphonyrm.com',
    url='https://github.com/symphonyrm/lookml-gen',
    packages=[
        'lookmlgen',
    ],
    package_dir={'lookmlgen':
                 'lookmlgen'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='lookml-gen',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

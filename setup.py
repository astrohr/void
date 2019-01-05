#!/usr/bin/env python
# coding=utf-8

from setuptools import setup

setup(
    name='void',
    description='Visnjan Observatory Image Database',
    version='0.0.1',
    url='https://github.com/astrohr/void',
    author='astrohr',
    author_email='dagor@astro.hr',
    scripts=['scripts/void_sniffer', 'scripts/void_reducer'],
    packages=['void'],
    license='MIT',
    keywords='',
    install_requires=[
        'docopt>=0.6.2,<0.7',
        'astropy>=3.1.1,<3.2',
        'psycopg2>=2.7,<2.8',
    ],
    extras_require={'dev': ['flake8', 'black', 'coverage']},
)

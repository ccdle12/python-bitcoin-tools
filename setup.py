#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='bitcoin_tools',
      version='0.0.3',
      description='Bitcoin Tools Library',
      author='Christopher Coverdale',
      author_email='chris.coverdale24@gmail.com',
      url='https://github.com/ccdle12/python-bitcoin-tools',
      nclude_package_data=True,
      packages=['bitcoin_tools'],
      )
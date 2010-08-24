#!/usr/bin/env python
# encoding: utf-8
"""Ablage is a System for document archival.

It uses Amazon Webservices (SimpleDB and S3) for it's storage needs.
"""

# setup.py
# Created by Maximillian Dornseif on 2010-04-07 for HUDORA.
# Copyright (c) 2010 HUDORA. All rights reserved.

from setuptools import setup, find_packages
import codecs

setup(name='Ablage',
      # maintainer='XXX',
      # maintainer_email='xXXXx@hudora.de',
      version='1.0',
      description='Document archiving solution',
      long_description=codecs.open('README.rst', "r", "utf-8").read(),
      classifiers=['License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python'],
      # package_data={"%%MODULENAME%%": ["templates/%%MODULENAME%%/*.html", "reports/*.jrxml", "bin/*"]},
      packages=find_packages(),
      include_package_data=True,
      install_requires=['httplib2', 'boto'],
)

#!/usr/bin/env python
# encoding: utf-8
"""%%PROJECTNAME%% is xXXXx
"""

# setup.py
# Created by Maximillian Dornseif on 2010-04-07 for HUDORA.
# Copyright (c) 2010 HUDORA. All rights reserved.

from setuptools import setup, find_packages

setup(name='%%PROJECTNAME%%',
      # maintainer='XXX',
      # maintainer_email='xXXXx@hudora.de',
      version='1.0',
      description='xXXXx FILL IN HERE xXXXx',
      long_description=long_description=codecs.open('README.rst', "r", "utf-8").read(),
      classifiers=['License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python'],
      download_url='https://cybernetics.hudora.biz/nonpublic/eggs/',
      package_data={"%%MODULENAME%%": ["templates/%%MODULENAME%%/*.html", "reports/*.jrxml", "bin/*"]},
      packages=find_packages(),
      include_package_data=True,
      install_requires=['huTools', 'huDjango'],
)

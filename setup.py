#!/usr/bin/env python

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='tornado-utils',
      version='1.1',
      description='Utility scripts for a Tornado site',
      long_description=read('README.md'),
      author='Peter Bengtsson',
      author_email='mail@peterbe.com',
      url='http://github.com/peterbe/tornado-utils',
      classifiers=[
           'Programming Language :: Python :: 2',
           'Intended Audience :: Developers',
           'Operating System :: POSIX :: Linux',
           'Topic :: Software Development :: Testing'
           'Topic :: Software Development :: Build Tools'
      ],
)

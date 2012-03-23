#!/usr/bin/env python

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='tornado-utils',
      version='1.2',
      description='Utility scripts for a Tornado site',
      long_description=read('README.md'),
      author='Peter Bengtsson',
      author_email='mail@peterbe.com',
      url='http://github.com/peterbe/tornado-utils',
      packages = [
        'tornado_utils',
        'tornado_utils.send_mail',
        'tornado_utils.send_mail.backends',
        'tornado_utils.tests',
      ],
      classifiers=[
           'Programming Language :: Python :: 2',
           'Intended Audience :: Developers',
           'Operating System :: POSIX :: Linux',
      ],
)

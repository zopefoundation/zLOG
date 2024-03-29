##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for the zLOG package
"""
from setuptools import find_packages
from setuptools import setup


version = '4.0.dev0'

with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()

tests_require = [
    'zope.testrunner',
]

setup(name='zLOG',
      version=version,
      url='https://github.com/zopefoundation/zLOG',
      license='ZPL 2.1',
      description='A general logging facility',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.dev',
      long_description='\n\n'.join([README, CHANGES]),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Zope Public License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: Implementation :: CPython",
          "Framework :: Zope :: 5",
      ],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      python_requires='>=3.7',
      install_requires=[
          'ZConfig >= 3.4',
      ],
      extras_require=dict(test=tests_require),
      include_package_data=True,
      zip_safe=False,
      )

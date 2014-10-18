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
"""Setup for the zLOG egg package
"""
from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()

setup(name='zLOG',
      version = '2.12.0',
      url='http://cheeseshop.python.org/pypi/zLOG',
      license='ZPL 2.1',
      description='A general logging facility',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      long_description='\n\n'.join([README,CHANGES]),
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: Zope2",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      test_suite='zLOG.tests',
      install_requires=['ZConfig >= 2.9.2'],
      include_package_data=True,
      zip_safe=False,
      )

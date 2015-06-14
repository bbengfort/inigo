#!/usr/bin/env python
# setup
# Setup script for Inigo
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jun 14 17:12:15 2015 -0400
#
# Copyright (C) 2014-2015 Benjamin Bengfort
# For license information, see LICENSE.txt
#
# ID: setup.py [] benjamin@bengfort.com $

"""
Setup script for Inigo
"""

##########################################################################
## Imports
##########################################################################

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\"."
                      "Please install the setuptools package.")

##########################################################################
## Package Information
##########################################################################

version  = __import__('inigo').__version__

## Discover the packages
packages = find_packages(where=".", exclude=("tests", "bin", "docs", "fixtures", "register",))

## Load the requirements
requires = []
with open('requirements.txt', 'r') as reqfile:
    for line in reqfile:
        requires.append(line.strip())

## Define the classifiers
classifiers = (
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
)

## Define the keywords
keywords = ('pictures', 'archival',)

## Define the description
long_description = ""

## Define the configuration
config = {
    "name": "Inigo",
    "version": version,
    "description": "Tools for dealing with images on disk for archival purposes.",
    "long_description": long_description,
    "license": "MIT",
    "author": "Benjamin Bengfort",
    "author_email": "benjamin@bengfort.com",
    "url": "https://github.com/bbengfort/inigo",
    "download_url": 'https://github.com/bbengfort/inigo/tarball/v%s' % version,
    "packages": packages,
    "install_requires": requires,
    "classifiers": classifiers,
    "keywords": keywords,
    "zip_safe": True,
    "scripts": ['bin/inigo'],
}

##########################################################################
## Run setup script
##########################################################################

if __name__ == '__main__':
    setup(**config)

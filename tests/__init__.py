# tests
# Tests for the inigo package
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Dec 04 14:22:53 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Tests for the inigo package
"""

##########################################################################
## Imports
##########################################################################

import os
import unittest

##########################################################################
## Fixtures
##########################################################################

EXPECTED_VERSION = "0.2"

##########################################################################
## Initialization Tests
##########################################################################

class InitializationTest(unittest.TestCase):

    def test_initialization(self):
        """
        Assert the world is sane and 2+2=4
        """
        self.assertEqual(2+2, 4)

    def test_import(self):
        """
        Assert that we can import the inigo library
        """
        try:
            import inigo
        except ImportError:
            self.fail("Could not import the inigo library")

    def test_version(self):
        """
        Check the expected version matches
        """
        import inigo
        self.assertEqual(inigo.__version__, EXPECTED_VERSION)

    def test_version_extract(self):
        """
        Test the setup.py method of extracting the version
        """
        namespace = {}
        versfile = os.path.join(
            os.path.dirname(__file__), "..", "inigo", "__init__.py"
        )

        with open(versfile, 'r') as versf:
            exec(versf.read(), namespace)

        self.assertEqual(namespace['get_version'](), EXPECTED_VERSION)

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

import unittest

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
        Check the version is 1.0.0
        """
        import inigo
        self.assertEqual(inigo.__version__, "1.0.0")

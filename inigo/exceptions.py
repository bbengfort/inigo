# inigo.exceptions
# Exceptions hierarchy for the Inigo application
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Dec 04 14:36:41 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: exceptions.py [] benjamin@bengfort.com $

"""
Exceptions hierarchy for the Inigo application
"""

class InigoException(Exception):
    """
    Base exception class
    """
    pass

class NotADirectory(InigoException):
    """
    Trying to create a directory object with a path that doesn't exist
    """
    pass

class NotAFile(InigoException):
    """
    Trying to create a file meta object with a path that doesn't exit
    """
    pass

class PictureNotFound(InigoException):
    """
    Could not get a picture from the database when it was required.
    """
    pass

class ConsoleError(InigoException):
    """
    Captured on the command line for user feedback purposes
    """
    pass

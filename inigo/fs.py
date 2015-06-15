# inigo.fs
# Implements local file system operations
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Dec 04 14:32:32 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: fs.py [] benjamin@bengfort.com $

"""
Implements local file system operations
"""

##########################################################################
## Imports
##########################################################################

import os
import magic
import base64
import hashlib

from inigo.exceptions import *

##########################################################################
## Helper Methods
##########################################################################

def normalize_path(path):
    """
    Returns a normalized, absolute path expanding all variables.
    """
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    return os.path.abspath(path)

##########################################################################
## Node
##########################################################################

class Node(object):
    """
    Wraps os calls around a path.
    """

    def __init__(self, path):
        self.path = normalize_path(path)

    def stat(self):
        """
        Call os.stat on the path
        """
        return os.stat(self.path)

    def isfile(self):
        """
        Checks if this is a File
        """
        return self.__class__.__name__ == 'FileMeta'

    def isdir(self):
        """
        Checks if this is a Directory
        """
        return self.__class__.__name__ == 'Directory'

    def __str__(self):
        return self.path

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.path)

##########################################################################
## File
##########################################################################

class FileMeta(Node):
    """
    Implements a File object with extended functionality to gather meta data
    """

    def __init__(self, path, signature='sha256'):

        if not os.path.isfile(path):
            raise NotAFile("The specified path, '%s' is not a file", path)

        if signature not in hashlib.algorithms:
            raise TypeError('"%s" is not a valid hash algorithm', signature)

        self.sigalg = getattr(hashlib, signature)
        super(FileMeta, self).__init__(path)

    @property
    def mimetype(self):
        """
        Uses libmagic to guess the mimetype of the file
        """
        return magic.from_file(self.path, mime=True)

    @property
    def signature(self):
        """
        Computes the b64 encoded sha256 hash of the file
        """
        with open(self.path, 'rb') as f:
            sig = self.sigalg()
            chk = sig.block_size * 256
            for chunk in iter(lambda: f.read(chk), b''):
                sig.update(chunk)
        return base64.b64encode(sig.digest())

    def isfile(self):
        """
        Checks if this is a File
        """
        return True

##########################################################################
## Directory
##########################################################################

class Directory(Node):
    """
    Implements a Directory object with extended functionality
    """

    def __init__(self, path, recursive=False, maxdepth=None):
        """
        Instantiate a directory with a path. Recursive means that listing
        the directory will walk the tree from the directory root.
        """

        if not os.path.isdir(path):
            raise NotADirectory("The specified path, '%s' is not a directory", path)

        self.recursive = recursive
        self.maxdepth  = maxdepth
        super(Directory, self).__init__(path)

    def isdir(self):
        """
        Checks if this is a Directory
        """
        return True

    def list(self):
        """
        List the contents of the directory
        """

        if self.maxdepth is None and not self.recursive:
            self.maxdepth = 0

        for dirname, dirs, files, depth in self.walk():

            for dir in dirs:
                yield Directory(os.path.join(dirname, dir))

            for fle in files:
                yield FileMeta(os.path.join(dirname, fle))

            if self.maxdepth is not None and depth == self.maxdepth:
                dirs[:] = [] # Don't recurse any deeper

    def walk(self):
        """
        Overrides the os.walk and also provides a depth
        """
        startdepth = self.path.count(os.sep)
        for name, dirs, files in os.walk(self.path):
            depth = name.count(os.sep) - startdepth
            yield name, dirs, files, depth

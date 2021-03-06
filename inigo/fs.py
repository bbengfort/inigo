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
import shutil
import hashlib

from urlparse import urljoin
from inigo.exceptions import *
from inigo.utils.decorators import memoized
from inigo.utils.uname import hostname

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

    @property
    def hostname(self):
        """
        Returns the hostname and access protocol of the node.
        """
        return "file://{}".format(hostname())

    @property
    def uri(self):
        """
        Returns the uniform resource identifier of the node.
        """
        return urljoin(self.hostname, self.path)

    @property
    def directory(self):
        """
        Returns the parent directory of the node.
        """
        return Directory(os.path.dirname(self.path))

    def stat(self):
        """
        Call os.stat on the path
        """
        return os.stat(self.path)

    def copy(self, dst):
        """
        Copy this node from it's current location to the destination.
        Returns a new Node for the destination object.
        """
        directory = os.path.dirname(dst)
        if not os.path.exists(directory):
            os.makedirs(directory)

        shutil.copy(self.path, dst)
        shutil.copystat(self.path, dst)
        return self.__class__(dst)

    def move(self, dst):
        """
        Move this node from it's current location to the destination.
        Returns a new Node for the destination object.
        """
        directory = os.path.dirname(dst)
        if not os.path.exists(directory):
            os.makedirs(directory)

        shutil.move(self.path, dst)
        return self.__class__(dst)

    def remove(self):
        """
        Deletes the path from disk.
        """
        os.remove(self.path)

    def exists(self):
        """
        Check if the file exists on disk
        """
        return os.path.exists(self.path)

    def isfile(self):
        """
        Checks if this is a File
        """
        return os.path.isfile(self.path)

    def isdir(self):
        """
        Checks if this is a Directory
        """
        return os.path.isdir(self.path)

    def isimage(self):
        """
        Checks if this is an Image
        """
        if self.isfile():
            meta = FileMeta(self.path)
            if meta.mimetype.startswith('image'):
                return True
        return False

    def convert(self):
        """
        Converts the node into the appropriate subclass
        """
        if self.isdir():
            return Directory(self.path)

        if self.isfile():
            return FileMeta(self.path)

    def __str__(self):
        return self.path

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.uri)

##########################################################################
## File
##########################################################################

class FileMeta(Node):
    """
    Implements a File object with extended functionality to gather meta data
    """

    @classmethod
    def touch(cls, path, times=None, **kwargs):
        """
        Creates an empty file at the specified path.
        """
        with open(path, 'a') as f:
            os.utime(path, times)

        return cls(path, **kwargs)

    def __init__(self, path, signature='sha256'):
        super(FileMeta, self).__init__(path)

        if not os.path.isfile(self.path):
            raise NotAFile("The specified path, '%s' is not a file", self.path)

        if signature not in hashlib.algorithms:
            raise TypeError('"%s" is not a valid hash algorithm', signature)

        self.sigalg = getattr(hashlib, signature)

    @memoized
    def mimetype(self):
        """
        Uses libmagic to guess the mimetype of the file
        """
        return magic.from_file(self.path, mime=True)

    @memoized
    def filesize(self):
        """
        Uses stat to return the size of the file in bytes.
        """
        return self.stat().st_size

    @memoized
    def signature(self):
        """
        Computes the b64 encoded sha256 hash of the file
        """
        with open(self.path, 'rb') as f:
            sig = self.sigalg()
            chk = sig.block_size * 256
            for chunk in iter(lambda: f.read(chk), b''):
                sig.update(chunk)
        return unicode(base64.b64encode(sig.digest()))

##########################################################################
## Directory
##########################################################################

class Directory(Node):
    """
    Implements a Directory object with extended functionality
    """

    @classmethod
    def create(cls, path, **kwargs):
        """
        Creates a directory along with all parent directories.
        """
        if not os.path.exists(path):
            os.makedirs(path)
        return cls(path, **kwargs)

    def __init__(self, path, recursive=False, maxdepth=None):
        """
        Instantiate a directory with a path. Recursive means that listing
        the directory will walk the tree from the directory root.
        """
        super(Directory, self).__init__(path)

        if not os.path.isdir(self.path):
            raise NotADirectory("The specified path, '%s' is not a directory", self.path)

        self.recursive = recursive
        self.maxdepth  = maxdepth


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

    def copy(self, dst):
        """
        Copy this node from it's current location to the destination.
        Returns a new Node for the destination object.
        """
        shutil.copytree(self.path, dst)
        return self.__class__(dst)

    def remove(self, force=False):
        """
        Deletes the path from disk. If force is true, then uses rmtree.
        """
        if force:
            shutil.rmtree(self.path)
            return

        os.rmdir(self.path)

    def __len__(self):
        return len(list(self.list()))

#!/usr/bin/env python
# ingos
# Command line utility for Inigo
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Dec 04 14:58:33 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: inigos.py [] benjamin@bengfort.com $

"""
Command line utility for Inigo
"""

##########################################################################
## Imports
##########################################################################

import sys
import inigo
import argparse

from inigo.local import *
from inigo.stats import *

##########################################################################
## Command Variables
##########################################################################

VERSION = inigo.__version__
DESCRIPTION = "Command utility for Inigo project"
EPILOG = "Please submit bugs to Github issue tracker"

##########################################################################
## Main Method
##########################################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=DESCRIPTION, version=VERSION, epilog=EPILOG)
    parser.add_argument('path', nargs=1, type=str, help='Path of directory to evaluate')
    parser.add_argument('-R', dest='recursive', action='store_true', help='Recursively evaluate directory')
    parser.add_argument('-d', '--depth', type=int, default=None, help='Maximum depth of recursion')

    args = parser.parse_args()
    dir  = Directory(args.path[0], args.recursive, args.depth)

    mimetypes = FreqDist()
    for item in dir.list():
        if item.isfile():
            mimetypes[item.mimetype] += 1
            print "%s: %s" % (item, item.signature)

    for item in mimetypes.most_common():
        print "%s: %i" % item

# inigo.console.commands.discover
# Commands for discovery and interpretation of the file system
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jun 14 21:22:29 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txtc
#
# ID: discover.py [] benjamin@bengfort.com $

"""
Commands for discovery and interpretation of the file system
"""

##########################################################################
## Imports
##########################################################################

import colorama

from inigo.fs import Directory
from inigo.utils.stats import FreqDist
from inigo.utils.decorators import timeit
from inigo.console.utils import color_format
from inigo.console.commands.base import Command

##########################################################################
## Command
##########################################################################

class IdentifyTypesCommand(Command):

    name = "mimetypes"
    help = "returns the frequency of mimetypes in a given directory"

    args = {
        ## Manipulate the method of directory walking
        '-R': {
            'dest': 'recursive',
            'action': 'store_true',
            'help': 'Recursively evaluate directory'
        },
        ('-d', '--depth'): {
            'type': int,
            'default': None,
            'help': 'Maximum depth of recursion'
        },
        'path': {
            'nargs': 1,
            'type': str,
            'help': 'Path of directory to evaluate'
        }
    }

    @timeit
    def walk_directory(self, path, recursive, depth):
        """
        Returns a frequency distribution of mimetypes in a directory.
        Handler in a method for timing and to allow multiple paths walked.
        """
        dir  = Directory(path, recursive, depth)

        mimetypes = FreqDist()
        for item in dir.list():
            if item.isfile():
                mimetypes[item.mimetype] += 1

        return mimetypes

    def handle(self, args):

        mimetypes, elapsed = self.walk_directory(args.path[0], args.recursive, args.depth)

        output = [color_format("Mimetypes discovered in {}", colorama.Fore.WHITE, args.path[0])]
        for key, val in mimetypes.most_common():
            frequency = color_format("{: >6}", colorama.Fore.CYAN, val)
            mimetype  = color_format("{}", colorama.Fore.WHITE, key)
            output.append("  {} {}".format(frequency, mimetype))

        output.append(color_format("Discovery took {:0.3f} seconds", colorama.Fore.MAGENTA, elapsed))

        return "\n".join(output)

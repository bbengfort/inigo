# inigo.console.commands.debug
# A debug command for debugging on the commandline
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Jun 10 15:59:36 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: debug.py [] benjamin@bengfort.com $

"""
A debug command for debugging on the commandline
"""

##########################################################################
## Imports
##########################################################################

from inigo.config import settings
from inigo.fs import Node
from inigo.image import ImageMeta
from inigo.console.commands.base import Command

##########################################################################
## Command
##########################################################################

class DebugCommand(Command):

    name = "debug"
    help = "debugging utility for the inigo utility"

    args = {
        ## Print out the settings
        '--settings': {
            'default': False,
            'action': 'store_true',
            'help': 'print out the current settings'
        },
        'paths': {
            'nargs': '*',
            'metavar': 'PATH',
            'type': str,
            'help': 'display the fs properties of a file'
        }
    }

    def handle(self, args):
        if args.settings:
            print settings

        output = []
        for path in args.paths:
            output.append(self.handle_path(path))

        return "\n".join(output)

    def handle_path(self, path):
        node = Node(path)

        if node.isimage():
            return self.handle_image(ImageMeta(path))

        if node.isfile():
            return self.handle_file(node.convert())

        if node.isdir():
            return self.handle_directory(node.convert())

        raise TypeError("Could not identify type of {!r}".format(path))

    def handle_image(self, img):
        return "{!r} of size {} taken on {}".format(img, img.dimensions, img.date_taken)

    def handle_file(self, fm):
        return "{!r} with signature {}".format(fm, fm.signature)

    def handle_directory(self, dir):
        return "{!r} containing {} nodes".format(dir, len(dir))

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

# from inigo.config import settings
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
        }
    }

    def handle(self, args):
        if args.settings:
            print settings

        return ""

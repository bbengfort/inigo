# inigo.console.main
# The main Inigo command line utility program
#
# Author:   Benjamin Bengfort <bbengfort@windsorview.com>
# Created:  Wed Jun 10 15:37:49 2015 -0400
#
# Copyright (C) 2015 Windsor View Corporation
# For license information, see LICENSE.txt
#
# ID: main.py [] bbengfort@windsorview.com $

"""
The main Inigo command program.

This program is the core object that is imported by any command line
script, it defines the definition of the Inigo program.
"""

##########################################################################
## Imports
##########################################################################

import os
import sys
import colorama

from inigo.console.commands import *
from inigo.console.utils import color_format
from inigo.console.prog import ConsoleProgram

##########################################################################
## Command Line Variables
##########################################################################

DESCRIPTION = "Command utility for Inigo project"
EPILOG      = "Please submit bugs to Github issue tracker"
COMMANDS    = [
    DebugCommand,
]

##########################################################################
## The Smoak Command line Program
##########################################################################

class InigoUtility(ConsoleProgram):

    description = color_format(DESCRIPTION, colorama.Fore.CYAN)
    epilog      = color_format(EPILOG, colorama.Fore.MAGENTA)

    @classmethod
    def load(klass, commands=COMMANDS):
        utility = klass()
        for command in commands:
            utility.register(command)
        return utility

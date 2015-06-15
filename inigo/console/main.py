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
from inigo.console.prog import ConsoleProgram

##########################################################################
## Command Line Variables
##########################################################################

DESCRIPTION = "An administrative utility for the Inigo Project"
EPILOG      = "For any bugs or concerns, please use issues on Github"
COMMANDS    = [
    DebugCommand,
]

##########################################################################
## The Smoak Command line Program
##########################################################################

class InigoUtility(ConsoleProgram):

    description = colorama.Fore.CYAN + DESCRIPTION + colorama.Fore.RESET
    epilog      = colorama.Fore.MAGENTA + EPILOG + colorama.Fore.RESET

    @classmethod
    def load(klass, commands=COMMANDS):
        utility = klass()
        for command in commands:
            utility.register(command)
        return utility

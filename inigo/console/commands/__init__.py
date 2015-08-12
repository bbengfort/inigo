# inigo.console.commands
# A module containing all the Smoak commands
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Jun 10 15:40:21 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: inigo.console.commands.py [] benjamin@bengfort.com $

"""
A module containing all the Inigo commands
"""

##########################################################################
## Imports
##########################################################################

## Make sure all commands in this directory are imported!
from .debug import DebugCommand
from .discover import IdentifyTypesCommand
from .backup import BackupCommand
from .geocode import GeocodeCommand

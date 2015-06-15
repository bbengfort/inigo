# inigo.console.utils
# Console utility functions and helpers
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Jun 12 22:46:21 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: utils.py [] benjamin@bengfort.com $

"""
Console utility functions and helpers
"""

##########################################################################
## Imports
##########################################################################

import colorama

##########################################################################
## Console colors
##########################################################################

def color_format(string, color, *args, **kwargs):
    """
    Implements string formating along with color specified in colorama.Fore
    """
    string = string.format(*args, **kwargs)
    return color + string + colorama.Fore.RESET

# inigo.utils.uname.py
# Utilities for determining localhost information.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Aug 12 09:16:22 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: uname.py [] benjamin@bengfort.com $

"""
Utilities for determining localhost information.
"""

##########################################################################
## Imports
##########################################################################

import socket
import getpass

LOCAL_TLD = ".local"

##########################################################################
## Helper Functions
##########################################################################

def hostname():
    """
    Returns the unicode encoded hostname of the local machine
    """
    host = unicode(socket.gethostname())
    if u"." not in host:
        host += LOCAL_TLD
    return host


def username():
    """
    Returns the unicode encoded user name of the currently logged in user.
    """
    return unicode(getpass.getuser())

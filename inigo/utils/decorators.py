# inigo.utils.decorators
# Decorators and descriptors
#
# Author:   Benjamin Bengfort <bbengfort@windsorview.com>
# Created:  Sun Jun 14 20:46:27 2015 -0400
#
# Copyright (C) 2015 Windsor View Corporation
# For license information, see LICENSE.txt
#
# ID: decorators.py [] bbengfort@windsorview.com $

"""
Decorators and descriptors
"""

##########################################################################
## Imports
##########################################################################

import time

from functools import wraps

##########################################################################
## Timing decorators
##########################################################################

def timeit(func):
    """
    Returns the number of seconds that a function took along with the result
    """
    @wraps
    def timer(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        return result, (time.time() - start)
    return timer

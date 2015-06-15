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
    @wraps(func)
    def timer(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        return result, (time.time() - start)
    return timer

##########################################################################
## Property helpers
##########################################################################

class cached_property(object):
    """
    A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Deleting the attribute resets the property.
    Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
    """

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value

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
from dateutil.relativedelta import relativedelta

##########################################################################
## Memoization
##########################################################################

def memoized(fget):
    """
    Return a property attribute for new-style classes that only calls its
    getter on the first access. The result is stored and on subsequent
    accesses is returned, preventing the need to call the getter any more.

    https://github.com/estebistec/python-memoized-property
    """
    attr_name = '_{0}'.format(fget.__name__)

    @wraps(fget)
    def fget_memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fget(self))
        return getattr(self, attr_name)

    return property(fget_memoized)

##########################################################################
## Timer functions
##########################################################################

class Timer(object):
    """
    A context object timer. Usage:

        >>> with Timer() as timer:
        ...     do_something()
        >>> print timer.interval
    """

    def __init__(self, wall_clock=True):
        """
        If wall_clock is True then use time.time() to get the number of
        actually elapsed seconds. If wall_clock is False, use time.clock to
        get the process time instead.
        """
        self.wall_clock = wall_clock
        self.time = time.time if wall_clock else time.clock

    def humanizedelta(self, *args, **kwargs):
        """
        Wrapper around dateutil.relativedelta (same construtor args) and returns
        a humanized string representing the detla in a meaningful way.
        """
        delta = relativedelta(*args, **kwargs)
        attrs = ('years', 'months', 'days', 'hours', 'minutes', 'seconds')
        parts = [
            '%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1])
            for attr in attrs if getattr(delta, attr)
        ]

        return " ".join(parts)

    def __enter__(self):
        self.start    = self.time()
        return self

    def __exit__(self, type, value, tb):
        self.finish   = self.time()
        self.interval = self.finish - self.start

    def __str__(self):
        return self.humanizedelta(seconds=self.interval)


def timeit(func, wall_clock=True):
    """
    Returns the number of seconds that a function took along with the result
    """
    @wraps(func)
    def timer_wrapper(*args, **kwargs):
        """
        Inner function that uses the Timer context object
        """
        with Timer(wall_clock) as timer:
            result = func(*args, **kwargs)

        return result, timer
    return timer_wrapper

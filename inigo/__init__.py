# inigo
# Tools for dealing with images on disk for archival purposes
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Thu Dec 04 14:25:25 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Tools for dealing with images on disk for archival purposes
"""

##########################################################################
## Module Info
##########################################################################

__version_info__ = {
    'major': 0,
    'minor': 1,
    'micro': 0,
    'releaselevel': 'final',
    'serial': 1,
}


def get_version(short=False):
    """
    Prints the version.
    """
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ["%(major)i.%(minor)i" % __version_info__, ]
    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%s%i' % (__version_info__['releaselevel'][0],
                              __version_info__['serial']))
    return ''.join(vers)

##########################################################################
## Package Version
##########################################################################

__version__ = get_version()

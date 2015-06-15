# inigo.config
# Configuration for the Inigo utilities
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jun 14 22:06:23 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: config.py [] benjamin@bengfort.com $

"""
Configuration for the Inigo utilities
"""

##########################################################################
## Imports
##########################################################################

import os

from confire import Configuration
from confire import environ_setting

##########################################################################
## Base Paths
##########################################################################

PROJECT  = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

##########################################################################
## Credentials Configuration
##########################################################################

class PostgreSQLConfiguration(Configuration):

    host = environ_setting("PGHOST", "localhost")
    port = environ_setting("PGPORT", 5432)
    name = environ_setting("PGDATABASE", "inigo")
    user = environ_setting("PGUSER", "django")
    password = environ_setting("PGPASSWORD", "", required=False)

##########################################################################
## Application Configuration
##########################################################################

class InigoConfiguration(Configuration):

    CONF_PATHS = [
        '/etc/inigo.yaml',
        os.path.expanduser('~/.inigo.yaml'),
        os.path.abspath('conf/inigo.yaml')
    ]

    debug     = False
    testing   = True
    database  = PostgreSQLConfiguration()


settings = InigoConfiguration.load()

if __name__ == '__main__':
    print settings
# inigo.console.commands.geocode
# Incremental geocoding of the database from the command line.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Aug 12 07:43:35 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: geocode.py [] benjamin@bengfort.com $

"""
Incremental geocoding of the database from the command line.
"""

##########################################################################
## Imports
##########################################################################

import time
import colorama

from inigo.config import settings
from inigo.models import Picture, create_session
from inigo.models import GeocodeTask
from inigo.console.commands.base import Command
from inigo.console.utils import color_format
from inigo.utils.timez import humanizedelta, today
from inigo.utils.decorators import Timer

from geopy.geocoders import GoogleV3
from dateutil.tz import tzstr

from sqlalchemy import desc

##########################################################################
## Module Constants
##########################################################################

# From the Google API Docs
MAXIMUM_CALL_RATE  = 5
MAXIMUM_CALL_LIMIT = 2500

# PST Timezone for Google Rate limit
PST = tzstr('PST8PDT')

##########################################################################
## Command
##########################################################################

class GeocodeCommand(Command):

    name = "geocode"
    help = "incremental geocoding of the database"

    args = {
        ## Print out the settings
        ('-r', '--call-rate'): {
            'default': settings.geocode.call_rate,
            'type': int,
            'help': 'number of geocode requests per second'
        },
        ('-n', '--call-limit'): {
            'default': settings.geocode.call_limit,
            'type': int,
            'help': 'maximum number of requests to make'
        },
        ('-i', '--info'): {
            'default': False,
            'action': 'store_true',
            'help': 'show database information and exit'
        }
    }

    def handle(self, args):
        self.session = create_session()
        self.rate    = args.call_rate
        self.limit   = self.real_limit(args.call_limit)

        if self.rate > MAXIMUM_CALL_RATE:
            raise ValueError(
                "Call rate exceeds maximum call rate of {} requests per second"
                .format(MAXIMUM_CALL_RATE)
            )

        if self.limit > MAXIMUM_CALL_LIMIT:
            raise ValueError(
                "Call limit exeeds maximum limit of {} daily requests"
                .format(MAXIMUM_CALL_LIMIT)
            )

        # Show database information
        self.show_info()
        if args.info:
            # Exit if the info command is there
            return color_format("-- no geocoding executed --", colorama.Fore.MAGENTA)

        # Execute the geocoding
        with Timer() as timer:
            # Set up action variables
            count = errors = 0
            self.geocoder  = GoogleV3(api_key=settings.geocode.apikey)

            for idx, record in enumerate(self.get_queryset()):
                # Usage Limit Handling
                current = idx + 1
                if current > self.limit:
                    break

                # Rate Liimit Handling
                if current % self.rate == 0:
                    time.sleep(1)

                try:
                    self.handle_record(record)
                    count += 1
                except Exception as e:
                    errors += 1
                    print color_format(
                        "Could not geocode ({}, {}): {}", colorama.Fore.RED,
                        record.latitude, record.longitude, e
                    )

                    if args.traceback or errors > 10:
                        raise

        # Save log of geocoding
        log = GeocodeTask(requests=count+errors, errors=errors, elapsed=timer.interval)
        self.session.add(log)
        self.session.commit()

        return color_format(str(log), colorama.Fore.MAGENTA)

    def real_limit(self, limit):
        """
        Subtracts any logged requests for todays period from the limit around
        returns it as the theoretical new limit, as supplied by the log file.
        """
        # Query limit resets at midnight PST
        period  = today(PST)

        # Construct the task query for today
        tasks   = self.session.query(GeocodeTask)
        tasks   = tasks.filter(GeocodeTask.timestamp > period)

        # Compute requests already logged for today
        sofar   = sum(t.requests for t in tasks)
        print color_format(
            "Already made {} geocode requests during this usage period.",
            colorama.Fore.CYAN, sofar
        )

        # Return the new limit
        return limit - sofar

    def show_info(self):
        """
        Reads the database and discovers how many pictures require geocoding.
        """
        # Compute number of pictures in database
        total   = self.session.query(Picture).count()

        # Compute records requirements with database query
        count   = self.get_queryset().count()
        records = min(self.limit, count)
        eta     = humanizedelta(seconds=float(records) / float(self.rate))

        # Print information
        output = [
            "{} of {} database records require geocoding".format(count, total),
            "{} records can be geocoded in this run, taking approximately {}".format(
                records, eta
            ),
        ]

        print color_format("\n".join(output), colorama.Fore.CYAN)

    def get_queryset(self):
        """
        Returns the records that require geocoding in the database.
        """
        query   = self.session.query(Picture).order_by(desc(Picture.date_taken))
        query   = query.filter(Picture.latitude.isnot(None))
        query   = query.filter(Picture.longitude.isnot(None))
        query   = query.filter(Picture.location.is_(None))

        return query

    def handle_record(self, record):
        query    = "{},{}".format(record.latitude, record.longitude)
        result   = self.geocoder.reverse(query, exactly_one=True, sensor=False)

        record.location = unicode(result.address) if result else u""
        self.session.add(record)

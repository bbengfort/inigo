# inigo.image
# Handles data dealing with images, particularly EXIF for JPEG
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jun 14 22:32:17 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: image.py [] benjamin@bengfort.com $

"""
Handles data dealing with images, particularly EXIF for JPEG
"""

##########################################################################
## Imports
##########################################################################

from inigo.fs import FileMeta
from PIL import Image, ExifTags

from datetime import datetime
from dateutil.tz import tzutc

from inigo.config import settings
from inigo.utils.timez import epochptime
from inigo.utils.decorators import memoized
from inigo.exceptions import PictureNotFound
from inigo.models import STYPE, create_session
from inigo.models import Picture, Storage
from inigo.utils.timez import tzaware_now

from sqlalchemy.sql import exists

from geopy.geocoders import GoogleV3

##########################################################################
## Module Constants
##########################################################################

EXIF_DATE_FORMAT = "%Y:%m:%d %H:%M:%S"

##########################################################################
## Helper functions
##########################################################################

def convert_to_degrees(value):
    """
    Helper function to convert GPS coordinates stored in EXIF degrees to a
    decimal float format, though this function does not take into account
    N/S or E/W cardinality of the degree vector.
    """
    deg = float(value[0][0]) / float(value[0][1])
    mns = float(value[1][0]) / float(value[1][1])
    sec = float(value[2][0]) / float(value[2][1])

    return deg + (mns / 60.0) + (sec / 3600.0)

##########################################################################
## Image Node
##########################################################################

class ImageMeta(FileMeta):
    """
    Wraps a path and provides image meta data.
    """

    @property
    def exif(self):
        """
        Uses Pillow to extract the EXIF data
        """
        if not hasattr(self, '_exif'):
            self.read_image_data()
        return self._exif

    @property
    def dimensions(self):
        """
        Returns a tuple of the width and height of the image.
        """
        if not hasattr(self, '_dimensions'):
            self.read_image_data()
        return self._dimensions

    @memoized
    def date_taken(self):
        """
        Attempts to find the date taken. Returns any timestamp, even if it is
        just the date created on the file meta. Current logic for the method:

            1. Attempt to parse DateTimeOriginal from EXIF
            2. Return st_ctime from os.stat
        """
        dtorig = self.exif.get('DateTimeOriginal', None)
        if dtorig:
            return datetime.strptime(dtorig, EXIF_DATE_FORMAT).replace(tzinfo=tzutc())

        return epochptime(self.stat().st_ctime)

    @memoized
    def coordinates(self):
        """
        Returns the latitude and longitude as a tuple.
        """
        lat = lon = None

        # Decode the GPSInfo tags
        if "GPSInfo" in self.exif:
            self.exif["GPSInfo"] = {
                ExifTags.GPSTAGS[k]: v
                for k,v in self.exif["GPSInfo"].iteritems()
                if k in ExifTags.GPSTAGS
            }

            # Gather GPS data points
            gps_info = self.exif["GPSInfo"]
            gps_lat  = gps_info.get("GPSLatitude", None)
            gps_lon  = gps_info.get("GPSLongitude", None)
            gps_lat_ref = gps_info.get("GPSLatitudeRef", None)
            gps_lon_ref = gps_info.get("GPSLongitudeRef", None)

            # Perform GPS conversions
            if gps_lat and gps_lon and gps_lat_ref and gps_lon_ref:
                lat = convert_to_degrees(gps_lat)
                if gps_lat_ref != "N":
                    lat = 0 - lat

                lon = convert_to_degrees(gps_lon)
                if gps_lon_ref != "E":
                    lon = 0 - lon

            return (lat, lon)

    @memoized
    def address(self):
        """
        Reverses the address from the coordinates
        """
        if not self.coordinates:
            return

        geocoder = GoogleV3(api_key=settings.geocode.apikey)
        query    = "{},{}".format(*self.coordinates)
        result   = geocoder.reverse(query, exactly_one=True, sensor=False)

        if result:
            return result.address

    def read_image_data(self):
        """
        Reads the image data and returns specific information.
        """

        with Image.open(self.path) as img:
            # Read size data
            self._dimensions = img.size

            # Read EXIF data
            exifdata = img._getexif() if hasattr(img, "_getexif") else {}

            self._exif = {
                ExifTags.TAGS[k]: v
                for k,v in exifdata.iteritems()
                if k in ExifTags.TAGS
            } if exifdata else {}

    def save(self, session=None, commit=False):
        """
        Stores the image information in the database along with the current
        file path. Pass a session object in to use the same session for
        multiple saves.

        This method returns the session object. Will commit if required.
        """
        session  = session or create_session()

        if not session.query(exists().where(
                Picture.signature == self.signature
            )).scalar():

            session.add(Picture(
                signature     = self.signature,
                date_taken    = self.date_taken,
                latitude      = self.coordinates[0],
                longitude     = self.coordinates[1],
                width         = self.dimensions[0],
                height        = self.dimensions[1],
                mimetype      = unicode(self.mimetype),
                bytes         = self.filesize,
            ))

            if commit:
                session.commit()

        return session

    def save_storage(self, session=None, commit=False, **skwargs):
        """
        Saves the storage associated with this image and file meta.
        """
        session = session or create_session()

        # Fetch the picture from the database
        picture = session.query(Picture)
        picture = picture.filter(Picture.signature == self.signature).first()

        if not picture:
            raise PictureNotFound(
                "Must save the picture before assigning storages."
            )

        # Create the storage object
        sdata = {
            "stype": STYPE.ORIGINAL,
            "hostname": unicode(self.hostname),
            "filepath": unicode(self.path),
            "memo": None,
            "picture": picture,
            "modified": tzaware_now(),
        }
        sdata.update(skwargs)

        # Attempt to fetch the storage on the dependent keys
        storage = session.query(Storage)
        storage = storage.filter(Storage.stype == sdata['stype'])
        storage = storage.filter(Storage.hostname == sdata['hostname'])
        storage = storage.filter(Storage.filepath == sdata['filepath'])
        storage = storage.filter(Storage.picture == sdata['picture'])
        storage = storage.first() or Storage()

        # Set the new values on the storage object
        for key, val in sdata.iteritems():
            setattr(storage, key, val)

        session.add(storage)

        if commit:
            session.commit()

        return session


if __name__ == '__main__':
    import os
    from inigo.config import PROJECT
    img = ImageMeta(os.path.join(PROJECT, "fixtures/animals/land/cats/cat.jpg"))
    print img.date_taken
    print img.dimensions

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

from inigo.utils.timez import epochptime
from inigo.utils.decorators import memoized

##########################################################################
## Module Constants
##########################################################################

EXIF_DATE_FORMAT = "%Y:%m:%d %H:%M:%S"

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
                for k,v in exifdata.items()
                if k in ExifTags.TAGS
            } if exifdata else {}




if __name__ == '__main__':
    import os
    from inigo.config import PROJECT
    img = ImageMeta(os.path.join(PROJECT, "fixtures/animals/land/cats/cat.jpg"))
    print img.date_taken
    print img.dimensions

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
from inigo.utils.decorators import cached_property

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

    @cached_property
    def exif(self):
        """
        Uses Pillow to extract the EXIF data
        """
        with Image.open(self.path) as img:
            return {
                ExifTags.TAGS[k]: v
                for k,v in img._getexif().items()
                if k in ExifTags.TAGS
            }
            return img._getexif()

    @property
    def date_taken(self):
        """
        Attempts to find the date taken. Returns any timestamp, even if it is
        just the date created on the file meta. Current logic for the method:

            1. Attempt to parse DateTimeOriginal from EXIF
            2. Return st_ctime from os.stat
        """
        return datetime.strptime(self.exif['DateTimeOriginal'], EXIF_DATE_FORMAT)


if __name__ == '__main__':
    import os
    from inigo.config import PROJECT
    img = ImageMeta(os.path.join(PROJECT, "fixtures/animals/land/cats/cat.jpg"))
    print img.date_taken

# inigo.models
# SQLAlchemy models for interacting with the database
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Jul 05 15:56:45 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
SQLAlchemy models for interacting with the database
"""

##########################################################################
## Imports
##########################################################################

import os
import mimetypes

from collections import namedtuple

from sqlalchemy import create_engine
from sqlalchemy import Enum
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Unicode, UnicodeText
from sqlalchemy import Integer, Float, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from inigo.config import settings
from inigo.utils.timez import tzaware_now, humanizedelta
from inigo.utils.uname import hostname, username

##########################################################################
## Module Constants
##########################################################################

Base  = declarative_base()  # SQLAlchemy declarative extension
JPEG  = "image/jpeg"

# Create a named tuple of storage types
STYPE = ('ORIGINAL', 'BACKUP', 'CLOUD', 'DROBO')
STYPE = namedtuple("Enum", STYPE)(*STYPE)

##########################################################################
## Models for Image Meta Data
##########################################################################

class Storage(Base):
    """
    Contains information about the location of a photograph on disk, e.g. the
    original location of the photograph, the Drobo backup of the photograph,
    or a cloud location like S3 or Google Drive.
    """

    __tablename__ = "storages"

    id            = Column(Integer, primary_key=True)
    stype         = Column(Enum(*STYPE, name='STORAGE_TYPE'), default=STYPE.ORIGINAL)
    hostname      = Column(Unicode(255))
    filepath      = Column(Unicode(512), nullable=False)
    memo          = Column(Unicode(255))
    picture_id    = Column(Integer, ForeignKey('pictures.id'), nullable=False)
    picture       = relationship('Picture', backref='storages')
    created       = Column(DateTime(timezone=True), default=tzaware_now)
    modified      = Column(DateTime(timezone=True), default=tzaware_now)


class Picture(Base):
    """
    Contains meta information about a photograph discovered in the backup.
    """

    __tablename__ = "pictures"

    id            = Column(Integer, primary_key=True)
    signature     = Column(Unicode(44), nullable=False, unique=True)
    date_taken    = Column(DateTime(timezone=True))
    latitude      = Column(Float)
    longitude     = Column(Float)
    location      = Column(Unicode(255))
    width         = Column(Integer)
    height        = Column(Integer)
    mimetype      = Column(Unicode(64))
    bytes         = Column(Integer)
    description   = Column(UnicodeText)
    created       = Column(DateTime(timezone=True), default=tzaware_now)
    modified      = Column(DateTime(timezone=True), default=tzaware_now)

    @property
    def extension(self):
        """
        Returns the extension of the picture, guessed from the mimetype.
        """
        if self.mimetype == JPEG:
            return ".jpg"
        return mimetypes.guess_extension(self.mimetype, strict=False)

    def get_relative_backup_path(self):
        """
        Compute the backup path of the picture based on the date taken and
        the primary key, relative to the root backup location on disk.

        Should be of the following format:

            yyyy/mm-mmmm/yyyy-mm-dd-pk.jpg

        Note the extension is 'guessed' by the mimetypes library, but all
        image/jpeg mimetypes are going to be transformed to .jpg.
        """
        fname = "{}-{:07d}{}".format(
            self.date_taken.strftime("%Y-%m-%d"), self.id, self.extension
        )

        return os.path.join(
            self.date_taken.strftime("%Y"),
            self.date_taken.strftime("%m-%B"),
            fname
        )


##########################################################################
## Models for tasks and logging
##########################################################################


class GeocodeTask(Base):
    """
    Contains meta information about geocoding jobs on the database.
    """

    __tablename__ = "geocode_log"

    id            = Column(Integer, primary_key=True)
    timestamp     = Column(DateTime(timezone=True), default=tzaware_now)
    user          = Column(Unicode(64), default=username)
    host          = Column(Unicode(64), default=hostname)
    requests      = Column(Integer, default=0)
    errors        = Column(Integer, default=0)
    elapsed       = Column(Float, default=0.0)

    def __str__(self):
        return "Made {} geocode API requests with {} errors in {}".format(
            self.requests, self.errors, humanizedelta(seconds=self.elapsed)
        )


##########################################################################
## Database helper methods
##########################################################################

def get_engine(uri=None):
    uri = uri or settings.database.url
    return create_engine(uri)

def create_session(eng=None):
    eng = eng or get_engine()
    return sessionmaker(bind=eng)()

def syncdb(uri=None):
    Base.metadata.create_all(get_engine(uri))

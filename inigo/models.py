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

from sqlalchemy import create_engine
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

Base = declarative_base()  # SQLAlchemy declarative extension

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
    hostname      = Column(Unicode(255))
    filepath      = Column(Unicode(512), nullable=False)
    picture_id    = Column(Integer, ForeignKey('pictures.id'), nullable=False)
    picture       = relationship('Picture', backref='storages')


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

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

##########################################################################
## Module Constants
##########################################################################

Base = declarative_base()  # SQLAlchemy declarative extension

##########################################################################
## Models
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
    width         = Column(Integer)
    height        = Column(Integer)
    mimetype      = Column(Unicode(64))
    bytes         = Column(Integer)
    description   = Column(UnicodeText)

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

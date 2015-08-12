# inigo.console.commands.backup
# Runs the evaluation to backup a set of files to Drobo and save meta to db.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sun Aug 09 20:46:50 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txtc
#
# ID: backup.py [] benjamin@bengfort.com $

"""
Runs the evaluation backup to a set of files to Drobo and save meta to db.
"""

##########################################################################
## Imports
##########################################################################

import os
import colorama

from inigo.image import ImageMeta
from inigo.fs import Node, Directory
from inigo.models import create_session
from inigo.models import Picture, STYPE

from inigo.config import settings
from inigo.utils.decorators import Timer
from inigo.console.utils import color_format
from inigo.console.commands.base import Command

##########################################################################
## Command
##########################################################################

class BackupCommand(Command):

    name = "backup"
    help = "backs up the given directory to drobo and saves info to database."

    args = {
        ## Manipulate the method of directory walking
        '-R': {
            'dest': 'recursive',
            'action': 'store_true',
            'help': 'Recursively evaluate directory'
        },
        ('-d', '--depth'): {
            'type': int,
            'default': None,
            'help': 'Maximum depth of recursion'
        },
        'path': {
            'nargs': 1,
            'type': str,
            'help': 'Path of directory to backup'
        }
    }

    def backup(self, path, recursive, depth):
        """
        Walks a directory or handles a single file, storing images in a db.
        """
        session = create_session()
        node    = Node(path)

        # If node is a single file, handle it and move on
        if node.isimage():
            self.backup_image(node.convert(), session)
            return 1

        # Walk directory at recursion and depth
        count  = 0
        errors = 0
        duplicates = 0
        folder = Directory(path, recursive, depth)
        for idx, item in enumerate(folder.list()):
            if item.isimage():
                count += 1
                try:
                    result = self.backup_image(item, session)
                    if not result:
                        duplicates += 1
                except Exception as e:
                    print color_format(
                        "Exception at {}: {}",
                        colorama.Style.BRIGHT + colorama.Fore.RED,
                        item.path, e
                    )
                    errors += 1

            if idx % 1000 == 0:
                session.commit()

        session.commit()
        return count, duplicates, errors

    def backup_image(self, fm, session=None):
        """
        Handles an individual image backup.
        Returns new meta if it moved the file to the backup location, None if
        duplicatated or has already backed up the file. No matter what,
        database records should be maintained and updated.
        """
        imgsrc  = ImageMeta(fm.path)

        # Save the image metadata to the database
        session = imgsrc.save(session)
        session = imgsrc.save_storage(session)
        picture = session.query(Picture).filter(Picture.signature==imgsrc.signature).one()

        # Figure out backup path on disk
        dstpath = os.path.join(self.backupto, picture.get_relative_backup_path())
        if not os.path.exists(dstpath):
            imgdst = imgsrc.copy(dstpath)

            # Save the storages metadata to disk
            # NOTE: This methodology defaults to Drobo - need to fix.
            hostname = unicode(imgdst.hostname.replace("file://", "drobo://"))
            filepath = unicode(os.path.join("/", settings.drobo.root, picture.get_relative_backup_path()))
            session  = imgdst.save_storage(session, hostname=hostname, filepath=filepath, stype=STYPE.DROBO)

            return imgdst

        return None

    def handle(self, args):
        self.backupto = settings.drobo.get_drobo_path()

        with Timer() as timer:
            count, duplicates, errors = self.backup(args.path[0], args.recursive, args.depth)

        success = count - errors - duplicates
        return color_format("Backed up {} of {} images in {}", colorama.Fore.MAGENTA, success, count, timer)

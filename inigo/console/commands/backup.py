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

import colorama

from inigo.image import ImageMeta
from inigo.fs import Node, Directory
from inigo.models import create_session

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
        folder = Directory(path, recursive, depth)
        for idx, item in enumerate(folder.list()):
            if item.isimage():
                count += 1
                try:
                    self.backup_image(item, session)
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
        return count, errors

    def backup_image(self, fm, session=None):
        """
        Handles an individual image backup
        """
        img = ImageMeta(fm.path)

        # TODO: move the File
        img.save(session)

    def handle(self, args):

        with Timer() as timer:
            count, errors = self.backup(args.path[0], args.recursive, args.depth)

        success = count - errors
        return color_format("Backed up {} of {} images in {}", colorama.Fore.MAGENTA, success, count, timer)

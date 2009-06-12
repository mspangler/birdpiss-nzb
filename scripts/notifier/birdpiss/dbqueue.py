#!/usr/bin/env python
#
# Simple script that flushes the database queue and sends a notification email.
#
# Copyright (C) 2009 mspangler@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import MySQLdb
import os
import sys
from bp_logger import *
from notifier import *

class DbQueue:
    def __init__(self):
        self.logger = BpLogger()
        self.host = None
        self.username = None
        self.password = None
        self.database = None
        self.upload_dir = '/home/birdpiss/birdpiss.com/test/uploads'

    def process(self):
        try:
            db_handle = MySQLdb.connect(host=self.host, user=self.username, passwd=self.password, db=self.database)
        except Exception, ErrorMessage:
            self.logger.log_error('Error connecting to database: %s' % ErrorMessage)
            sys.exit(0)

        cursor = db_handle.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT Id, MediaPath, MediaName, Size, Requester, Notified FROM db_queue WHERE Notified = 0')
        result = cursor.fetchall()

        notifier = Notifier()

        try:
            for record in result:
                for content in os.listdir(self.upload_dir):
                    filename, extension = os.path.splitext(content)
                    file_size = os.path.getsize(content)
                    if filename.lower() == record['MediaName'].lower() and file_size == record['Size']:
                        self.logger.log.info('Found media: %s' % content)
                        if (notifier.notify(record['Requester'], record['MediaName'], extension)):
                            cursor.execute('UPDATE db_queue SET Notified = 1 WHERE Id = ' + record['Id'])
                            self.logger.log.info('Updated media as being sent - %s' % content)
                        else:
                            self.logger.log_error('Media could not be sent - %s' % content)
                        break
        finally:
            cursor.close()
            db_handle.close()
            notifier.close()

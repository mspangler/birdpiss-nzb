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

import logging
import logging.handlers
import os

class BpLogger:

    log = None
    email_log = None

    def __init__(self):
        if BpLogger.log is None or BpLogger.email_log is None:
            BpLogger.log = self.setup_logger()
            BpLogger.email_log = self.setup_email_logger()

    def log_error(self, error_msg):
        BpLogger.log.error(error_msg)
        BpLogger.email_log.error(error_msg)

    def setup_email_logger(self):
        # Create logger and set level to debug
        email_log = logging.getLogger('notifier_email')
        email_log.setLevel(logging.ERROR)

        # Create formatter and file handler
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh = logging.handlers.SMTPHandler('localhost', 'notifyError@birdpiss.com', 'mspangler@gmail.com', 'Notify Error Occurred')

        # Set formatter to file handler and set handler to logger
        fh.setFormatter(formatter)
        email_log.addHandler(fh)

        return email_log

    def setup_logger(self):
        # Create logger and set level to debug
        log = logging.getLogger('notifier')
        log.setLevel(logging.DEBUG)

        LOG_FILE = 'log.out'
        # Make sure the log file is there
        if os.path.exists(LOG_FILE) == False:
            f = file(LOG_FILE, 'w')

        # Create formatter and file handler
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=10000, backupCount=5)

        # Set formatter to file handler and set handler to logger
        fh.setFormatter(formatter)
        log.addHandler(fh)

        return log

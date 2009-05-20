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

import getopt
import os
import sys
from birdpiss import *

__version__ = 1.0

# Validation method to make sure we got the required information
def validate_input(dbQueue, logger):
    if dbQueue.host == None or dbQueue.host == '':
        logger.log_error('Invalid host: %s\n' % dbQueue.host)
        sys.exit(0)
    if dbQueue.username == None or dbQueue.username == '':
        logger.log_error('Invalid username: %s\n' % dbQueue.username)
        sys.exit(0)
    if dbQueue.password == None or dbQueue.password == '':
        logger.log_error('Invalid password: %s\n' % dbQueue.password)
        sys.exit(0)
    if dbQueue.database == None or dbQueue.database == '':
        logger.log_error('Invalid database: %s\n' % dbQueue.database)
        sys.exit(0)

logger = BpLogger()

# Sets up the command line options
try:
    opts, args = getopt.getopt(sys.argv[1:],\
                               'h:u:p:d:',\
                               ['host=', 'username=', 'password=', 'database=' ])
except getopt.GetoptError:
    logger.log_error('Please enter valid options')
    sys.exit(0)

dbQueue = DbQueue()

# Loop through the options to see what we're working with
for opt, arg in opts:
    if opt in ('-h', '--host'):
        dbQueue.host = arg
    elif opt in ('-u', '--username'):
        dbQueue.username = arg
    elif opt in ('-p', '--password'):
        dbQueue.password = arg
    elif opt in ('-d', '--database'):
        dbQueue.database = arg
    else:
        logger.log_error('INVALID argument "%s"' % arg)
        sys.exit(0)

validate_input(dbQueue, logger)

dbQueue.process()
sys.exit(0)

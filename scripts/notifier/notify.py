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

import MimeWriter
import MySQLdb
import cStringIO
import cgi
import getopt
import logging
import logging.handlers
import mimetools
import os
import smtplib
import sys
import urllib

_version__ = 1.0
email_log = None
log = None

class DbQueue:
    def __init__(self):
        self.host = None
        self.username = None
        self.password = None
        self.database = None
        self.upload_dir = '/home/birdpiss/birdpiss.com/test/uploads'

    def process(self):
        global log, email_log
        try:
            db_handle = MySQLdb.connect(host=self.host, user=self.username, passwd=self.password, db=self.database)
        except Exception, ErrorMessage:
            log_error('Error connecting to database: %s' % ErrorMessage)
            sys.exit(0)

        cursor = db_handle.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT Id, MediaPath, MediaName, Requester, Notified FROM db_queue WHERE Notified = 0')
        result = cursor.fetchall()

        notifier = Notifier()

        try:
            for record in result:
                for content in os.listdir(self.upload_dir):
                    filename, extension = os.path.splitext(content)
                    if filename == record['MediaName']:
                        log.info('Found media: %s' % content)
                        if (notifier.notify(record['Requester'], record['MediaName'], extension)):
                            log.info('Updated media as being sent - %s' % content)
                        else:
                            log_error('Media could not be sent - %s' % content)
                        break
        finally:
            cursor.close()
            db_handle.close()
            notifier.close()

class Notifier:
    def __init__(self):
        self.host = 'localhost'
        self.server = smtplib.SMTP(self.host)
        self.subject = 'Birdpiss Media Notifier'
        self.fromAddress = 'noreply@birdpiss.com'

    def notify(self, address, media_name, extension):
        log.info('Sending notification to %s for media - %s' % (address, media_name + extension))
        html = self.get_html(media_name, extension)
        out = cStringIO.StringIO()
        htmlin = cStringIO.StringIO(html)

        writer = MimeWriter.MimeWriter(out)
        writer.addheader('Subject', self.subject)
        writer.addheader('From', self.fromAddress)
        writer.addheader('To', address)
        writer.addheader('Mime-Version', '1.0')
        writer.startmultipartbody('alternative')
        writer.flushheaders()

        subpart = writer.nextpart()
        subpart.addheader('Content-Transfer-Encoding', 'quoted-printable')

        pout = subpart.startbody('text/html', [('charset', 'us-ascii')])
        mimetools.encode(htmlin, pout, 'quoted-printable')

        htmlin.close()
        writer.lastpart()

        msg = out.getvalue()
        out.close()

        try:
            self.server.sendmail(self.fromAddress, address, msg)
            log.info('Successfully sent notification to %s' % address)
            return True
        except Exception, ErrorMessage:
            log_error('Error sending notification to %s: %s' % (address, ErrorMessage))
            return False

    def get_html(self, media_name, extension):
        link_name = urllib.quote(media_name) + extension
        return """<html><head></head><body>
                      <p>
                        Your media is ready to be enjoyed.
                        <ul><li><a href="https://birdpiss.com/test/uploads/%s">%s</a></li></ul>
                      </p>
                  </body></html>""" % (link_name, media_name)

    def close(self):
        self.server.quit()

# Validation method to make sure we got the required information
def validate_input(dbQueue):
    global log
    if dbQueue.host == None or dbQueue.host == '':
        log_error('Invalid host: %s\n' % dbQueue.host)
        sys.exit(0)
    if dbQueue.username == None or dbQueue.username == '':
        log_error('Invalid username: %s\n' % dbQueue.username)
        sys.exit(0)
    if dbQueue.password == None or dbQueue.password == '':
        log_error('Invalid password: %s\n' % dbQueue.password)
        sys.exit(0)
    if dbQueue.database == None or dbQueue.database == '':
        log_error('Invalid database: %s\n' % dbQueue.database)
        sys.exit(0)

def log_error(error_msg):
    global log, email_log
    log.error(error_msg)
    email_log.error(error_msg)

def setup_email_logger():
    global email_log
    # Create logger and set level to debug
    email_log = logging.getLogger('notifier_email')
    email_log.setLevel(logging.ERROR)

    # Create formatter and file handler
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh = logging.handlers.SMTPHandler('localhost', 'notifyError@birdpiss.com', 'mspangler@gmail.com', 'Notify Error Occurred')

    # Set formatter to file handler and set handler to logger
    fh.setFormatter(formatter)
    email_log.addHandler(fh)

def setup_logger():
    global log
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

setup_email_logger()
setup_logger()

# Sets up the command line options
try:
    opts, args = getopt.getopt(sys.argv[1:],\
                               'h:u:p:d:',\
                               ['host=', 'username=', 'password=', 'database=' ])
except getopt.GetoptError:
    log_error('Please enter valid options')

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
        log_error('INVALID argument "%s"' % arg)

validate_input(dbQueue)

dbQueue.process()
sys.exit(0)


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
import cStringIO
import logging
import logging.handlers
import mimetools
import smtplib
import urllib
from bp_logger import *

class Notifier:
    def __init__(self):
        self.logger = BpLogger()
        self.host = 'localhost'
        self.server = smtplib.SMTP(self.host)
        self.subject = 'Birdpiss Media Notifier'
        self.fromAddress = 'noreply@birdpiss.com'

    def notify(self, address, media_name, extension):
        self.logger.log.info('Sending notification to %s for media - %s' % (address, media_name + extension))

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
            self.logger.log.info('Successfully sent notification to %s' % address)
            return True
        except Exception, ErrorMessage:
            self.logger.log_error('Error sending notification to %s: %s' % (address, ErrorMessage))
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

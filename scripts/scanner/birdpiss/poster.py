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

import json
import mimetools
import mimetypes
import sys
import urllib2

class User:
    def __init__(self):
        self.username = None
        self.password = None

class Poster:
    def __init__(self, user, media_type, media_file):
        self.user = user
        self.media_type = media_type
        self.media_file = media_file
        self.url = '127.0.0.1:8000/upload_media/'

    def post(self):
        sys.stdout.write('Uploading %s media...' % self.media_type)
        sys.stdout.flush()

        params = [('username', self.user.username), ('media_type', self.media_type)]
        files = [('media_file', 'media.txt', open(self.media_file).read())]
        success = self.post_multipart(params, files)

        if success:
            print '\nUpload was successful.'
        else:
            print '\nUpload failed.'

    # Recipe from: http://code.activestate.com/recipes/146306/
    def post_multipart(self, fields, files):
        content_type, body = self.encode_multipart_formdata(fields, files)
        headers = {'Content-Type': content_type,
                   'Content-Length': str(len(body))
                  }
        r = urllib2.Request('http://%s' % self.url, body, headers)
        try:
            response = urllib2.urlopen(r).read()
            return self.get_status(response)
        except Exception:
            # Might be behind proxy so try http
            sys.stdout.write('\nSecure mode failed.  You could be behind a proxy.  Trying unsecure mode...')
            sys.stdout.flush()
            r = urllib2.Request('http://%s' % self.url, body, headers)
            try:
                response = urllib2.urlopen(r).read()
                return self.get_status(response)
            except Exception, HTTPErrorMessage:
                print '\nError: %s' % HTTPErrorMessage
                return False

    def encode_multipart_formdata(self, fields, files):
        BOUNDARY = mimetools.choose_boundary()
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % self.get_content_type(filename))
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    def get_status(self, response):
        if response == "{ 'response' : 'success' }":
            return True
        return False


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

import os
import tempfile

class MediaFile:
    def __init__(self, media):
        self.media = media
        self.name = None
        self.hasErrors = False

    # Create a temporary file on the user's machine for the file upload
    def create(self):
        fd, self.name = tempfile.mkstemp(suffix='.csv', prefix='birdpiss-', text=True)
        f = os.fdopen(fd, 'w')

        # Sorts by file path
        keys = self.media.keys()
        keys.sort()

        for key in keys:
            try:
                f.write(key + ',' + self.media[key].encode('utf8') + '\n')
            except Exception, (ErrorNumber, ErrorMessage):
                self.hasErrors = True
                print 'Error: Unexpected error occurred.\n       File: %r\n       Exception: %r' % (key, ErrorMessage)
                continue
        f.close()

    # Deletes the temporary file for the user's machine
    def delete(self):
        os.remove(self.name)


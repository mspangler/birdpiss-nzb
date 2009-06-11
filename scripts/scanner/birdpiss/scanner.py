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

import locale
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
import os
import re
import sys
import time

# This class describes all the different types of media we'll be uploading.
class MediaType:
    MOVIE = 'movies'
    TV = 'tv'
    MUSIC = 'music'

# This class describes all the different ways to generate the media name.
class ScanType:
    FILES = 0
    DIRS = 1
    
class Media:
    def __init__(self, path, name, size):
        self.path = path
        self.name = name
        self.size = size

class Scanner:
    def __init__(self):
        self.twirl_state = 0
        self.start_scan = 0.0
        self.stop_scan = 0.0
        self.media = dict()
        self.video_pattern = re.compile('.avi|.mpg|.mpeg|.mkv|.m4v', re.IGNORECASE)
        self.audio_pattern = re.compile('.mp3|.m3u|.ogg|.flac', re.IGNORECASE)
        self.current_pattern = None
        self.media_type = 'movies'
        self.scan_type = 0
        self.recursive = False
        self.path = None

    # Scans the root path looking for media content
    def scan(self):

        if self.scan_type == ScanType.FILES:
            # Determine what file extensions we'll be looking for
            if self.media_type == MediaType.TV or self.media_type == MediaType.MOVIE:
                self.current_pattern = self.video_pattern
            elif self.media_type == MediaType.MUSIC:
                self.current_pattern = self.audio_pattern

        # Start the timer so we can measure the scanning performance
        if sys.platform == 'win32':
            self.start_scan = time.clock()
        else:
            self.start_scan = time.time()

        # Scan for the media
        if self.recursive:
            if self.scan_type == ScanType.FILES:
                for root in os.walk(self.path):
                    for content in root[2]:
                        self.add_file(content, os.path.join(root[0], content))
            elif self.scan_type == ScanType.DIRS:
                for root in os.walk(self.path):
                    for content in root[1]:
                        self.twirl()
                        self.add(os.path.join(root[0], content), content)
        else:
            if self.scan_type == ScanType.FILES:
                for content in os.listdir(self.path):
                    absolutePath = os.path.join(self.path, content)
                    if os.path.isfile(absolutePath):
                        self.add_file(content, absolutePath)
            elif self.scan_type == ScanType.DIRS:
                for content in os.listdir(self.path):
                    absolutePath = os.path.join(self.path, content)
                    if os.path.isdir(absolutePath):
                        self.twirl()
                        self.add(absolutePath, content)

        # Stop the the timer
        if sys.platform == 'win32':
            self.stop_scan = time.clock()
        else:
            self.stop_scan = time.time()

        # Clear the 'Scanning media...' output message
        print '                   '

    def add(self, path, name):
        try:
            self.media[path] = Media(path, name, str(os.path.getsize(path)))
        except Exception, ErrorMessage:
            print 'Error: Could not add the following file.'
            print '       File: %r\n       Exception: %r' % (path, ErrorMessage)

    # Makes sure the file is of a type we're aware of and adds it to the media list
    def add_file(self, content, absolutePath):
        self.twirl()
        extension = os.path.splitext(content)[1]
        if self.current_pattern.search(extension) != None:
            if self.media_type != MediaType.MUSIC:
                self.add(absolutePath, content)
            else:
                self.add(absolutePath, self.get_audio_tag_info(content, absolutePath, extension))

    # Grabs the audio tag information from the file
    def get_audio_tag_info(self, content, absolutePath, extension):
        if extension == '.mp3':
            try:
                audio = MP3(absolutePath, ID3=EasyID3)
                return self.get_tag(audio, content)
            except Exception, ErrorMessage:
                print 'Warn: Unexpected error occurred while getting ID3 info. - Will try and use filename instead.'
                print '      File: %r\n      Exception: %r' % (absolutePath, ErrorMessage)
                return content
        elif extension == '.flac':
            try:
                audio = FLAC(absolutePath)
                return self.get_tag(audio, content)
            except Exception, ErrorMessage:
                print 'Warn: Unexpected error occurred while getting FLAC info. - Will try and use filename instead.'
                print '      File: %r\n      Exception: %r' % (absolutePath, ErrorMessage)
                return content
        elif extension == '.ogg':
            try:
                audio = OggVorbis(absolutePath)
                return self.get_tag(audio, content)
            except Exception, ErrorMessage:
                print 'Warn: Unexpected error occurred while getting Ogg info. - Will try and use filename instead.'
                print '      File: %r\n      Exception: %r' % (absolutePath, ErrorMessage)
                return content
        else:
            return content

    def get_tag(self, audio, default):
        if audio.has_key('artist') and audio.has_key('album') and audio.has_key('title'):
            return audio['artist'][0] + ' - ' + audio['album'][0] + ' - ' + audio['title'][0]
        else:
            return default

    # Silly little processing indicator to show the user work is being done
    def twirl(self):
        symbols = ('|', '/', '-', '\\')
        sys.stdout.write('Scanning media... ' + symbols[ self.twirl_state ] + '\r')
        sys.stdout.flush()
        if self.twirl_state == len(symbols) - 1:
            self.twirl_state = -1
        self.twirl_state += 1

    # Outputs all the captured media and confirms the upload process
    def confirm(self):
        numFound = len(self.media)
        if numFound > 0:
            i = 1
            keys = self.media.keys()
            keys.sort()
            values = map(self.media.get, keys)
            for media in values:
                try:
                    print str(i) + '. ' + media.name
                    i += 1
                except Exception, ErrorMessage:
                    print 'Error: Unexpected error occurred on media title.\n       File: %r\n       Exception: %r' % (key, ErrorMessage)
                    continue

            print '\nTotal scanning seconds: %f' %(self.stop_scan - self.start_scan)
            locale.setlocale(locale.LC_ALL, '')
            print 'Found a total of ' + locale.format('%i', numFound, 1) + ' unique %s titles.\n' % self.media_type

            # Ask the user if what was captured is what they want to upload
            doUpload = raw_input('Continue and upload the %s information [y/n]? ' % self.media_type)
            if doUpload == 'y' or doUpload == 'Y':
                return True
            else:
                print 'Piss off then.'
                return False
        else:
            print 'Found a total of 0 %s titles.  Please refine your search options or use the --help switch.' % self.media_type
            return False


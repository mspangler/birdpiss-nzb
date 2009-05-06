#!/usr/bin/env python

import getopt
import os
import sys
import string

__version__ = 0.1

class MediaType:
    TV = 0
    MOVIE = 1
    MUSIC = 2

class ScanType:
    FILES = 0
    DIRS = 1

class User:
    def __init__(self):
        self.username = ''
        self.password = ''

class Content:
    def __init__(self, mediaType, name):
        self.mediaType = mediaType
        self.name = name

class MediaScanner:
    def __init__(self):
        self.media = []
        self.video_extensions = [ "avi", "mpg", "mpeg", "mkv", "m4v" ]
        self.audio_extensions = [ "mp3", "ogg" ]
        self.current_extensions = []
        self.media_type = 0
        self.scan_type = 0
        self.recursive = False
        self.path = ''

    # Scans the root path looking for media content
    def scan(self):
        if self.scan_type == ScanType.FILES:
            if self.media_type == MediaType.TV or self.media_type == MediaType.MOVIE:
                self.current_extensions = self.video_extensions
            elif self.media_type == MediaType.MUSIC:
                self.current_extensions = self.audio_extensions

        if self.recursive:
            for root, dirs, files in os.walk(self.path):
                if self.scan_type == ScanType.FILES:
                    for content in files:
                        self.add_file(content)
                elif self.scan_type == ScanType.DIRS:
                    for content in dirs:
                        self.media.append(Content(self.media_type, content))
        else:
            if self.scan_type == ScanType.FILES:
                for content in os.listdir(self.path):
                    if os.path.isfile(self.path + "/" + content):
                        self.add_file(content)
            elif self.scan_type == ScanType.DIRS:
                for content in os.listdir(self.path):
                    if os.path.isdir(self.path + "/" + content):
                        self.media.append(Content(self.media_type, content))

        print "\nAdded a total of " + str(len(self.media)) + " file(s)."

    # Makes sure the file is of a type we're aware of and adds it to the media list
    def add_file(self, content):
        file_type = string.lower(os.path.splitext(content)[1][1:])
        for type in self.current_extensions:
            if file_type == type:
                self.media.append(Content(self.media_type, content))
                break

# Helpful function to show how to use the script
def usage():
    print "birdpiss version " + str(__version__)
    print ""
    print "usage: python birdpiss.py [options]"
    print ""
    print "options:"
    print "-h, --help       view help and usage"
    print "-t, --tv         scan for tv show files"
    print "-m, --movies     scan for movie files"
    print "-a, --audio      scan for audio files"
    print "-d, --dirs       scan only directories - will use directory name for media name"
    print "-f, --files      scan only files - will use filename for media name"
    print "-R, --recursive  recursively search for content under the root path"
    print "-r, --root       specify the root path"
    print "-u, --user       specify your username"
    print "-p, --password   specify your password"
    print ""
    print "Examples:"
    print "         python birdpiss.py -afr /home/user/music -u username -p password"
    print "         python birdpiss.py -mfRr /home/user/movies -u username -p password"
    print '         python birdpiss.py -tdr "/home/user/tv shows" -u username -p password'
    print ""
    print "Source available at http://github.com/mspangler/birdpiss-nzb/tree/master"
    print ""
    sys.exit(0)

# Start of program
try:
    opts, args = getopt.getopt(sys.argv[1:], "htmadfRr:u:p:", ["help", "tv", "movies", "audio", "dirs", "files", "recursive", "root=", "username=", "password=" ])
except getopt.GetoptError:
    print "USAGE ERROR: Please enter valid options\n"
    usage()

user = User()
mediaScanner = MediaScanner()

for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
    elif opt in ("-t", "--tv"):
        mediaScanner.media_type = MediaType.TV
    elif opt in ("-m", "--movies"):
        mediaScanner.media_type = MediaType.MOVIE
    elif opt in ("-a", "--audio"):
        mediaScanner.media_type = MediaType.MUSIC
    elif opt in ("-d", "--dirs"):
        mediaScanner.scan_type = ScanType.DIRS
    elif opt in ("-f", "--files"):
        mediaScanner.scan_type = ScanType.FILES
    elif opt in ("-R", "--recursive"):
        mediaScanner.recursive = True
    elif opt in ("-r", "--root"):
        mediaScanner.path = arg
    elif opt in ("-u", "--username"):
        user.username = arg
    elif opt in ("-p", "--password"):
        user.password = arg

mediaScanner.scan()

# Test to show what the scanner picked up
for content in mediaScanner.media:
    print ">> added " + content.name

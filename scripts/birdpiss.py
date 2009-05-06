#!/usr/bin/env python

import getopt
import id3reader
import os
import re
import string
import sys

__version__ = 0.1
__twirl_state__ = 0

class MediaType:
    MOVIE = 0
    TV = 1
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
            if self.scan_type == ScanType.FILES:
                for root in os.walk(self.path):
                    for content in root[2]:
                        self.addFile(content, os.path.join(root[0], content))
                        if self.media_type == MediaType.MUSIC:
                            break
            elif self.scan_type == ScanType.DIRS:
                for root in os.walk(self.path):
                    for content in root[1]:
                        twirl()
                        self.media.append(Content(self.media_type, content))
        else:
            if self.scan_type == ScanType.FILES:
                for content in os.listdir(self.path):
                    absolutePath = os.path.join(self.path, content)
                    if os.path.isfile(absolutePath):
                        self.addFile(content, absolutePath)
            elif self.scan_type == ScanType.DIRS:
                for content in os.listdir(self.path):
                    if os.path.isdir(os.path.join(self.path, content)):
                        twirl()
                        self.media.append(Content(self.media_type, content))

    # Makes sure the file is of a type we're aware of and adds it to the media list
    def addFile(self, content, absolutePath):
        twirl()
        file_type = string.lower(os.path.splitext(content)[1][1:])
        for type in self.current_extensions:
            if file_type == type:
                if self.media_type != MediaType.MUSIC:
                    self.media.append(Content(self.media_type, content))
                else:
                    self.media.append(Content(self.media_type, self.getId3Info(content, absolutePath, type)))
                break

    # Grabs the Id3 information from the file
    def getId3Info(self, content, absolutePath, type):
        if absolutePath != None and type == 'mp3':
            id3r = id3reader.Reader(absolutePath)
            artist = id3r.getValue('performer')
            album = id3r.getValue('album')
            if artist != None and album != None:
                return artist + ' - ' + album
        return content

# Helpful function to show how to use the script
def usage():
    print "birdpiss version {0}".format(__version__)
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

def confirmation(mediaScanner):
    numFound = len(mediaScanner.media)
    if numFound > 0:
        i = 1
        for content in mediaScanner.media:
            try:
                print "{0}. {1}".format(i, content.name)
                i += 1
            except UnicodeEncodeError:
                print "UnicodeEncodeError exception was thrown " + str(content)
                continue

        print "\nFound a total of {0} file(s).\n".format(numFound)

        doUpload = raw_input("Would you like to continue and upload the file information? (y/n): ")
        if doUpload == 'y':
            print "You selected to upload the file information."
        else:
            print "You selected not to upload any information."
            sys.exit(0)
    else:
        print "\nFound a total of {0} file(s).  Please refine your search options.".format(numFound)
        sys.exit(0)

# Little processing indicator to show the user work is being done
def twirl():
    global __twirl_state__
    symbols = ('|', '/', '-', '\\')
    sys.stdout.write('Scanning media... ' + symbols[__twirl_state__] + '\r')
    if __twirl_state__ == len(symbols) - 1:
        __twirl_state__ = -1
    __twirl_state__ += 1

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
confirmation(mediaScanner)

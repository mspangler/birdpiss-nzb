#!/usr/bin/env python

import getopt
import os
import sys
import string

# globals
__version__ = 0.1
TV = 0
MOVIES = 1
MUSIC = 2
DIRS = 0
FILES = 1

# This class scans the users media folder looking for media to upload.
class MediaScanner:

    # Default constructor
    def __init__(self):    
        self.media = []
        self.video_extensions = [ "avi", "mpg", "mpeg", "mkv", "m4v" ]
        self.music_extensions = [ "mp3", "ogg" ]
        self.current_extensions = []
        self.media_type = 0
        self.scan_type = 0
        self.recursive = False
        self.path = ''
        self.user = ''
        self.password = ''
    
    # Helpful function to show how to use the script
    def usage(self):
        print "birdpiss version " + str(__version__) + "\n"
        print "usage: python birdpiss.py [options]\n"
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
        print "-p, --password   specify your password\n"
        print "Examples:"
        print "         python birdpiss.py -afr /home/user/music -u username -p password"
        print "         python birdpiss.py -mfRr /home/user/movies -u username -p password"
        print '         python birdpiss.py -tdr "/home/user/tv shows" -u username -p password\n'
        print "Source available at http://github.com/mspangler/birdpiss-nzb/tree/master\n"
        sys.exit(0)

    # Scans the root path looking for media content
    def scan(self):
        if self.media_type == TV or self.media_type == MOVIES:
            self.current_extensions = self.video_extensions
        elif self.media_type == MUSIC:
            self.current_extensions = self.music_extensions

        if self.recursive:
            for root, dirs, files in os.walk(self.path):                
                if self.scan_type == FILES:
                    # TODO: find a better way to add a list to another list
                    for content in files:
                        self.add_file(content)
                elif self.scan_type == DIRS:
                    # TODO: find a better way to add a list to another list
                    for content in dirs:
                        self.media.append(content)
        else:
            if self.scan_type == FILES:
                for content in os.listdir(self.path):
                    if os.path.isfile(self.path + "/" + content):
                        self.add_file(content)
            elif self.scan_type == DIRS:
                for content in os.listdir(self.path):
                    if os.path.isdir(self.path + "/" + content):
                        self.media.append(content)
                
        print "\nAdded a total of " + str(len(self.media)) + " file(s)."        

    # Makes sure the file is of a type we're aware of and adds it to the media list
    def add_file(self, content):
        file_type = string.lower(os.path.splitext(content)[1][1:])
        for type in self.current_extensions:
            if file_type == type:
                self.media.append(content)
                break

# Start of program
try:
    opts, args = getopt.getopt(sys.argv[1:], "htmadfRr:u:", ["help", "tv", "movies", "audio", "dirs", "files", "recursive", "root=", "user=", "password=" ])
except getopt.GetoptError:
    sys.exit(2)

mediaScanner = MediaScanner()

for opt, arg in opts:
    if opt in ("-h", "--help"):
        mediaScanner.usage()
    elif opt in ("-t", "--tv"):
        mediaScanner.media_type = TV
    elif opt in ("-m", "--movies"):
        mediaScanner.media_type = MOVIES
    elif opt in ("-a", "--audio"):
        mediaScanner.media_type = MUSIC
    elif opt in ("-d", "--dirs"):
        mediaScanner.scan_type = DIRS
    elif opt in ("-f", "--files"):
        mediaScanner.scan_type = FILES
    elif opt in ("-R", "--recursive"):
        mediaScanner.recursive = True
    elif opt in ("-r", "--root"):
        mediaScanner.path = arg
    elif opt in ("-u", "--user"):
        mediaScanner.user = arg
    elif opt in ("-p", "--password"):
        mediaScanner.password = arg

mediaScanner.scan()

# Test to show what the scanner picked up
for content in mediaScanner.media:
    print ">> added " + content


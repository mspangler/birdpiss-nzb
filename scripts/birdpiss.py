#!/usr/bin/env python

"""
  Simple script that scans your media and uploads the information.
"""

import getopt
import id3reader
import os
import re
import string
import sys
import time

# Globals
__version__ = 0.1
start_scan = 0
stop_scan = 0
twirl_state = 0

# This class describes all the different types of media we'll be uploading.
class MediaType:
    MOVIE = 0
    TV = 1
    MUSIC = 2

# This class describes all the different ways to generate the media name.
class ScanType:
    FILES = 0
    DIRS = 1

# The user who is generating the media and uploading the information.
class User:
    def __init__(self):
        self.username = ''
        self.password = ''

# The workhorse scanner that generates the media based on the input options.
class MediaScanner:
    def __init__(self):
        self.media = dict()
        self.video_pattern = re.compile("avi|mpg|mpeg|mkv|m4v")
        self.audio_pattern = re.compile("mp3|ogg")
        self.id3_pattern = re.compile("mp3")
        self.current_pattern = None
        self.media_type = 0
        self.scan_type = 0
        self.recursive = False
        self.path = ''

    # Scans the root path looking for media content
    def scan(self):
        global start_scan, stop_scan

        if self.scan_type == ScanType.FILES:
            # Determine what file extensions we'll be looking for
            if self.media_type == MediaType.TV or self.media_type == MediaType.MOVIE:
                self.current_pattern = self.video_pattern
            elif self.media_type == MediaType.MUSIC:
                self.current_pattern = self.audio_pattern

        if sys.platform == 'win32':
            start_scan = time.clock()
        else:
            start_scan = time.time()

        if self.recursive:
            if self.scan_type == ScanType.FILES:
                for root in os.walk(self.path):
                    for content in root[2]:
                        self.addFile(content, os.path.join(root[0], content))
            elif self.scan_type == ScanType.DIRS:
                for root in os.walk(self.path):
                    for content in root[1]:
                        twirl()
                        self.media[os.path.join(root[0], content)] = content
        else:
            if self.scan_type == ScanType.FILES:
                for content in os.listdir(self.path):
                    absolutePath = os.path.join(self.path, content)
                    if os.path.isfile(absolutePath):
                        self.addFile(content, absolutePath)
            elif self.scan_type == ScanType.DIRS:
                for content in os.listdir(self.path):
                    absolutePath = os.path.join(self.path, content)
                    if os.path.isdir(absolutePath):
                        twirl()
                        self.media[absolutePath] = content

        if sys.platform == 'win32':
            stop_scan = time.clock()
        else:
            stop_scan = time.time()
        print "                   "

    # Makes sure the file is of a type we're aware of and adds it to the media list
    def addFile(self, content, absolutePath):
        twirl()
        if self.current_pattern.search(string.lower(content), 1) != None:
            if self.media_type != MediaType.MUSIC:
                self.media[absolutePath] = content
            else:
                self.media[absolutePath] = self.getId3Info(content, absolutePath)

    # Grabs the Id3 information from the file
    def getId3Info(self, content, absolutePath):
        if self.id3_pattern.search(string.lower(content), 1) != None:
            try:
                id3r = id3reader.Reader(absolutePath)
                artist = id3r.getValue('performer')
                album = id3r.getValue('album')
                title = id3r.getValue('title')
                if artist != None and album != None and title != None:
                    return artist + ' - ' + album + ' - ' + title
            except:
                print "Warn: Unexpected error occured while getting Id3 info from file:\n      %s - Will use filename instead." % absolutePath
                return content
        return content

# Helpful function to show how to use the script
def usage():
    print "birdpiss version %s" % __version__
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

# Outputs all the captured media and confirms the upload process
def confirm(mediaScanner):
    global start_scan, stop_scan
    numFound = len(mediaScanner.media)
    if numFound > 0:
        i = 1
        keys = mediaScanner.media.keys()
        keys.sort()
        media = map(mediaScanner.media.get, keys)
        for content in media:
            try:
                print str(i) + '. ' + content
                i += 1
            except UnicodeEncodeError:
                # Some id3 tags contain invalid characters so we catch them and keep moving on
                print "Warn: UnicodeEncodeError exception was thrown"
                continue

        print "\nTotal scanning seconds: %s" %(stop_scan - start_scan)
        print "Found a total of %s unique media titles.\n" % numFound

        # Ask the user if what was captured is what they want to upload
        doUpload = raw_input("Continue and upload the media information? (y/n): ")
        if doUpload == 'y' or doUpload == 'Y':
            print "Would upload it but it's not built yet."
            # TODO: build then call the upload class
        else:
            print "Piss off then."
            sys.exit(0)
    else:
        print "Found a total of 0 media titles.  Please refine your search options or use the --help switch."
        sys.exit(0)

# Silly little processing indicator to show the user work is being done
def twirl():
    global twirl_state
    symbols = ('|', '/', '-', '\\')
    sys.stdout.write('Scanning media... ' + symbols[ twirl_state ] + '\r')
    sys.stdout.flush()
    if twirl_state == len(symbols) - 1:
        twirl_state = -1
    twirl_state += 1

# Validation method to make sure we got the required information
def validateInput(mediaScanner, user):
    if os.path.isdir(mediaScanner.path) == False:
        print "Invalid root directory: %s\n" % mediaScanner.path
        sys.exit(0)
""" if user.username == None or user.username == '':
        print "Invalid username. Use 'python birdpiss.py --help' for usage\n"
        sys.exit(0)
    if user.password == None or user.password == '':
        print "Invalid password. Use 'python birdpiss.py --help' for usage\n"
        sys.exit(0) """

# Sets up the command line options
try:
    opts, args = getopt.getopt(sys.argv[1:], "htmadfRr:u:p:", ["help", "tv", "movies", "audio", "dirs", "files", "recursive", "root=", "username=", "password=" ])
except getopt.GetoptError:
    print "Error: Please enter valid options\n"
    usage()

user = User()
mediaScanner = MediaScanner()

# Loop through the options to see what we're working with
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

validateInput(mediaScanner, user)
mediaScanner.scan()
confirm(mediaScanner)

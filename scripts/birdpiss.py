#!/usr/bin/env python

"""
  Simple script that scans your media and uploads the information.
"""

import getopt
import id3reader
import os
import re
import sys
import tempfile
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
        self.username = None
        self.password = None

# The workhorse scanner that generates the media based on the input options.
class Scanner:
    def __init__(self):
        self.media = dict()
        self.video_pattern = re.compile(".avi|.mpg|.mpeg|.mkv|.m4v", re.IGNORECASE)
        self.audio_pattern = re.compile(".mp3|.m3u|.ogg", re.IGNORECASE)
        self.id3_pattern = re.compile(".mp3", re.IGNORECASE)
        self.current_pattern = None
        self.media_type = 0
        self.scan_type = 0
        self.recursive = False
        self.path = None

    # Scans the root path looking for media content
    def scan(self):
        global start_scan, stop_scan

        if self.scan_type == ScanType.FILES:
            # Determine what file extensions we'll be looking for
            if self.media_type == MediaType.TV or self.media_type == MediaType.MOVIE:
                self.current_pattern = self.video_pattern
            elif self.media_type == MediaType.MUSIC:
                self.current_pattern = self.audio_pattern

        # Start the timer so we can measure the scanning performance
        if sys.platform == 'win32':
            start_scan = time.clock()
        else:
            start_scan = time.time()

        # Scan for the media
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

        # Stop the the timer
        if sys.platform == 'win32':
            stop_scan = time.clock()
        else:
            stop_scan = time.time()

        # Clear the 'Scanning media...' output message
        print "                   "

    # Makes sure the file is of a type we're aware of and adds it to the media list
    def addFile(self, content, absolutePath):
        twirl()
        if self.current_pattern.search(content) != None:
            if self.media_type != MediaType.MUSIC:
                self.media[absolutePath] = content
            else:
                self.media[absolutePath] = self.getAudioTagInfo(content, absolutePath)

    # Grabs the audio tag information from the file
    def getAudioTagInfo(self, content, absolutePath):
        if self.id3_pattern.search(content) != None:
            try:
                id3r = id3reader.Reader(absolutePath)
                artist = id3r.getValue('performer')
                album = id3r.getValue('album')
                title = id3r.getValue('title')
                if artist != None and album != None and title != None:
                    return artist + ' - ' + album + ' - ' + title
            except Exception as ex:
                print "\033[1;31mError: Unexpected error occurred while getting Id3 info.  Will try and use filename instead.\n       File: %r\n       Exception: %r\033[1;m" % (absolutePath, ex)
                return content
        return content

# Handles the creation and removal of our media file that will be posted to the website
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
            except Exception as ex:
                self.hasErrors = True
                print "\033[1;31mError: Unexpected error occurred.\n       File: %r\n       Exception: %r\033[1;m" % (key, ex)
                continue
        f.close()

    # Deletes the temporary file for the user's machine
    def delete(self):
        os.remove(self.name)
        print 'Removed media file: ' + self.name

# Handles the upload or posting of the media file and information
class Uploader:
    def __init__(self, user, media_type, media_file):
        self.user = user
        self.media_type = media_type
        self.media_file = media_file

    def upload(self):
        media = self.getMediaType()
        print 'Uploading ' + media + ' media file: %s' % self.media_file
        print 'Media upload was successful.'
        
    def getMediaType(self):
        media = ''
        if self.media_type == MediaType.MOVIE:
            media = 'movies'
        elif self.media_type == MediaType.TV:
            media = 'tv'
        elif self.media_type == MediaType.MUSIC:
            media = 'music'
        return media

# Common function that will post the media information
def post(user, media_type, media_file):
    uploader = Uploader(user, media_type, media_file)
    uploader.upload()

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
    print "         python birdpiss.py -aRr /home/user/music -u username -p password"
    print "         python birdpiss.py -mfRr /home/user/movies -u username -p password"
    print '         python birdpiss.py -tdr "/home/user/tv shows" -u username -p password'
    print ""
    print "Source available at http://github.com/mspangler/birdpiss-nzb/tree/master"
    print ""
    sys.exit(0)

# Outputs all the captured media and confirms the upload process
def confirm(scanner):
    global start_scan, stop_scan
    numFound = len(scanner.media)
    if numFound > 0:
        i = 1
        keys = scanner.media.keys()
        keys.sort()
        values = map(scanner.media.get, keys)
        for media in values:
            try:
                print str(i) + '. ' + media
                i += 1
            except Exception as ex:
                print "\033[1;31mError: Unexpected error occurred on media title.\n       File: %r\n       Exception: %r\033[1;m" % (key, ex)
                continue

        print "\nTotal scanning seconds: %s" %(stop_scan - start_scan)
        print "Found a total of %s unique media titles.\n" % numFound

        # Ask the user if what was captured is what they want to upload
        doUpload = raw_input("Continue and upload the media information? (y/n): ")
        if doUpload == 'y' or doUpload == 'Y':
            return True
        else:
            print "Piss off then."
            return False
    else:
        print "Found a total of 0 media titles.  Please refine your search options or use the --help switch."
        return False

# Silly little processing indicator to show the user work is being done
def twirl():
    global twirl_state
    symbols = ('|', '/', '-', '\\')
    sys.stdout.write('Scanning media... ' + '\033[1;32m' + symbols[ twirl_state ] + '\033[1;m\r')
    sys.stdout.flush()
    if twirl_state == len(symbols) - 1:
        twirl_state = -1
    twirl_state += 1

# Validation method to make sure we got the required information
def validateInput(scanner, user):
    if os.path.isdir(scanner.path) == False:
        print "\033[1;31mError: Invalid root directory: %s\033[1;m\n" % scanner.path
        sys.exit(0)
""" if user.username == None or user.username == '':
        print "\033[1;31mError: Invalid username. Use 'python birdpiss.py --help' for usage\033[1;m\n"
    if user.password == None or user.password == '':
        print "\033[1;31mError: Invalid password. Use 'python birdpiss.py --help' for usage\033[1;m\n" """

# Sets up the command line options
try:
    opts, args = getopt.getopt(sys.argv[1:], "htmadfRr:u:p:", ["help", "tv", "movies", "audio", "dirs", "files", "recursive", "root=", "username=", "password=" ])
except getopt.GetoptError:
    print "\033[1;31mError: Please enter valid options\033[1;m\n"
    usage()

user = User()
scanner = Scanner()

# Loop through the options to see what we're working with
for opt, arg in opts:
    if opt in ("-h", "--help"):
        usage()
    elif opt in ("-t", "--tv"):
        scanner.media_type = MediaType.TV
    elif opt in ("-m", "--movies"):
        scanner.media_type = MediaType.MOVIE
    elif opt in ("-a", "--audio"):
        scanner.media_type = MediaType.MUSIC
    elif opt in ("-d", "--dirs"):
        scanner.scan_type = ScanType.DIRS
    elif opt in ("-f", "--files"):
        scanner.scan_type = ScanType.FILES
    elif opt in ("-R", "--recursive"):
        scanner.recursive = True
    elif opt in ("-r", "--root"):
        scanner.path = arg
    elif opt in ("-u", "--username"):
        user.username = arg
    elif opt in ("-p", "--password"):
        user.password = arg

validateInput(scanner, user)
scanner.scan()

# Validate that the user wants to go forward with the captured media
if confirm(scanner):
    media_file = MediaFile(scanner.media)
    media_file.create()

    if media_file.hasErrors == False:
        post(user, scanner.media_type, media_file.name)
    else:
        # If errors occurred during the file creation process verify with the user if we should continue
        doCreate = raw_input("\nDue to errors not all media will be uploaded.  Continue? (y/n): ")
        if doCreate == 'y' or doCreate == 'Y':
            post(user, scanner.media_type, media_file.name)

    media_file.delete()

sys.exit(0)


#!/usr/bin/env python
#
# Simple script that scans your media and uploads the information.
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

from birdpiss import *
import getopt
import os
import sys

__version__ = 1.0

# Helpful function to show how to use the script
def usage():
    print 'birdpiss version %s' % __version__
    print ''
    print 'usage: python birdpiss.py [options]'
    print ''
    print 'options:'
    print '-h, --help       view help and usage'
    print '-t, --tv         scan for tv show files'
    print '-m, --movies     scan for movie files'
    print '-a, --audio      scan for audio files'
    print '-d, --dirs       scan only directories - will use directory name for media name'
    print '-f, --files      scan only files - will use filename for media name'
    print '-R, --recursive  recursively search for content under the root path'
    print '-r, --root       specify the root path'
    print '-u, --user       specify your username'
    print ''
    print 'Examples:'
    print '         python birdpiss.py -aRr /home/user/music -u username'
    print '         python birdpiss.py -mfRr /home/user/movies -u username'
    print '         python birdpiss.py -tdr "/home/user/tv shows" -u username'
    print ''
    print 'Source available at http://github.com/mspangler/birdpiss-nzb/tree/master'
    print ''
    sys.exit(0)

# Validation method to make sure we got the required information
def validate_input(scanner, user):
    if scanner.path == None or os.path.isdir(scanner.path) == False:
        print 'Error: Invalid root directory: %s\nUse "python birdpiss.py --help" for usage\n' % scanner.path
        sys.exit(0)
    if user.username == None or user.username == '':
        print 'Error: Invalid username. Use "python birdpiss.py --help" for usage\n'
        sys.exit(0)
"""    if user.password == None or user.password == '':
        print 'Error: Invalid password. Use "python birdpiss.py --help" for usage\n' """

# Common function that will post the media information
def update(user, media_type, media_file):
    poster = Poster(user, media_type, media_file)
    poster.post()

# Sets up the command line options
try:
    opts, args = getopt.getopt(sys.argv[1:],\
                               'htmadfRr:u:p:',\
                               ['help', 'tv', 'movies', 'audio', 'dirs', 'files', 'recursive', 'root=', 'username=', 'password=' ])
except getopt.GetoptError:
    print 'Error: Please enter valid options\n'
    usage()

user = User()
scanner = Scanner()

# Loop through the options to see what we're working with
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
    elif opt in ('-t', '--tv'):
        scanner.media_type = MediaType.TV
    elif opt in ('-m', '--movies'):
        scanner.media_type = MediaType.MOVIE
    elif opt in ('-a', '--audio'):
        scanner.media_type = MediaType.MUSIC
    elif opt in ('-d', '--dirs'):
        scanner.scan_type = ScanType.DIRS
    elif opt in ('-f', '--files'):
        scanner.scan_type = ScanType.FILES
    elif opt in ('-R', '--recursive'):
        scanner.recursive = True
    elif opt in ('-r', '--root'):
        scanner.path = arg
    elif opt in ('-u', '--username'):
        user.username = arg
    elif opt in ('-p', '--password'):
        user.password = arg
    else:
        print 'INVALID argument "%s"' % arg

validate_input(scanner, user)

try:
    scanner.scan()
except KeyboardInterrupt:
    print '                 '
    sys.exit(0)

# Validate that the user wants to go forward with the captured media
if scanner.confirm():
    media_file = MediaFile(scanner.media)
    media_file.create()

    if media_file.hasErrors == False:
        update(user, scanner.media_type, media_file.name)
    else:
        # If errors occurred during the file creation process verify with the user if we should continue
        doCreate = raw_input('\nDue to errors not all %s info will be uploaded.  Continue [y/n]? ' % scanner.media_type)
        if doCreate == 'y' or doCreate == 'Y':
            update(user, scanner.media_type, media_file.name)

    media_file.delete()

sys.exit(0)


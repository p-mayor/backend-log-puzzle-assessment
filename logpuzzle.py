#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700]
"GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-"
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6)
Gecko/20070725 Firefox/2.0.0.6"

"""


import os
import re
import sys
import urllib
import argparse


def helper_regex(item):
    '''returns characters after the last hyphen in item'''
    match = re.search(r'\w[^-]*$', item).group(0)
    return match.group(0)


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    output = []
    with open(filename, 'r') as f:
        for line in f:
            match = re.search(r'.*GET\s*([^\s]*)', line)
            if match.group(1).endswith('.jpg') and match.group(1).startswith(
                    '/edu'):
                output.append(match.group(1))

    output = list(set(output))

    output.sort(key=lambda item : re.search(r'\w[^-]*$', item).group(0))
    return output


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    if not os.path.exists(str(dest_dir)):
        os.mkdir(dest_dir)
    with open(str(dest_dir)+'/index.html', 'w') as html_file:
        for index, url in enumerate(img_urls):
            urllib.urlretrieve("http://code.google.com" + url, filename=str(dest_dir)+'/'
                               + str(index)+".jpg")
            html_file.write("<img src="+'"'+str(index)+".jpg"+'">')


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)
    for url in img_urls:
        print(url)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])

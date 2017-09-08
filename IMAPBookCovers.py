#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import ConfigParser
import fnmatch
import os
import re
import sys
from FetchEmail import FetchEmail
from shutil import move, rmtree
from lib import kindleunpack

CONFIG_FILE = "IMAPBookCovers.conf"
APNXFILE = None
EPUB_VER = '2'
USE_HD = True

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def find_asin(filenames):
    for filename in fnmatch.filter(filenames, '*.opf'):
        with open((os.path.join(root, filename)), 'r') as inF:
            for line in inF:
                if 'ASIN' in line:
                    m = re.search('^<meta.name="ASIN".content="([^"]+)".*', line)
                    if m:
                        print("Found book ASIN: %s" % m.group(1))
                        return m.group(1)
    return False

def find_cover(filenames):
    for filename in fnmatch.filter(filenames, 'cover*.jpeg'):
        return (os.path.join(root, filename))
    return False

if __name__ == "__main__":
    print("Searching for unread email with attachments")
    Config = ConfigParser.ConfigParser()
    Config.read(CONFIG_FILE)
    fe = FetchEmail(ConfigSectionMap("IMAP")['server'], ConfigSectionMap("IMAP")['user'], ConfigSectionMap("IMAP")['pass'])
    for email in fe.fetch_unread_messages_with_attachments_since():
        att_path = fe.save_attachment(email, ConfigSectionMap("KINDLE")['documents_dir'])
        if att_path is not False:
            print("Saved unreal email attachment: %s" % att_path)
            tmp_dir = ConfigSectionMap("KINDLE")['tmp_dir']
            kindleunpack.unpackBook(att_path, tmp_dir, APNXFILE, EPUB_VER, USE_HD)
            
            asin = False
            cover = False
            for root, dirnames, filenames in os.walk(tmp_dir):
                if asin is False:
                    asin = find_asin(filenames)
                if cover is False:
                    cover = find_cover(filenames)
            print("Copying book and cover to final location.")
            try:
                cover_img = "thumbnail_%s_EBOK_portrait.jpg" % asin
                move(cover, os.path.join(ConfigSectionMap("KINDLE")['thumbnails_dir'], cover_img))
                rmtree(tmp_dir)
            except IOError, e:
                print("Error moving cover image: %s" % str(e))
    sys.stderr.flush()
    sys.stdin.flush()
#!/usr/bin/env python
#ftp://portal.camera.calit2.net/ftp-links/cam_datasets/blastdb
#https://portal.camera.calit2.net/gridsphere/gridsphere?cid=sampledownloadtab
#from ftplib import FTP
from bs4 import BeautifulSoup
import requests
import os
import fnmatch
import re
import urllib2
import urllib
import csv

CAMERA_HOST = 'https://portal.camera.calit2.net'
CAMERA_DATA = CAMERA_HOST + '/gridsphere/gridsphere?cid=sampledownloadtab'
CAMERA_LOGIN = CAMERA_HOST + '/gridsphere/gridsphere?cid=login'
DOWNLOAD_DIR = '/var/www/downloads/camera/'


def download_sequences(url):
    file_name = url.split('/')[-1].split('#')[0].split('?')[0]
    local_file_name = DOWNLOAD_DIR + file_name
    print(ftp_line)
    print(local_file_name)
    try:
        urllib.urlretrieve(ftp_line, local_file_name)
    except IOError:
        print '******Could not retrieve ' + ftp_line

with open('password') as f:
    credentials = f.readline().strip().split(':')
s = requests.Session()
payload = {'username': credentials[0], 'password': credentials[1],
           'gs_action': 'gs_login'}
s.get(CAMERA_DATA)
r = s.post(url=CAMERA_LOGIN, data=payload)
html_doc = s.get(CAMERA_DATA)
#print(html_doc.status_code)
soup = BeautifulSoup(html_doc.text)
with open('download_list', 'rb') as csvfile:
    download_list = csv.reader(csvfile, delimiter=',')
    for row in download_list:
        sequence_file = ''
        for link in soup.find_all('a'):
            if row[0] in link.get('href'):
                ftp_line = link.get('href')
        for file in os.listdir(DOWNLOAD_DIR):
            if fnmatch.fnmatch(file, row[0] + '.V*.fa.gz'):
                sequence_file = file
        if sequence_file == '':
            download_sequences(ftp_line)
        else:
            file_name = ftp_line.split('/')[-1].split('#')[0].split('?')[0]
            # Pattern of the file we are interested in
            patterns = row[0] + r'\.V(\d+)\.fa\.gz$'
            pattern = re.compile(patterns)
            match = pattern.search(sequence_file)
            if match:
                print (match.group(1))
            #print sequence_file
            ftp_match = pattern.search(ftp_line)
            if ftp_match:
                print (ftp_match.group(1))
                if int(ftp_match.group(1)) > int(match.group(1)):
                    print('New version available')
                    download_sequences(ftp_line)
                    # Make sure local and remote file size are the same
                    statinfo = os.stat(file_name)
                    file_size = statinfo.st_size
                else:
                    local_size = os.stat(DOWNLOAD_DIR + file_name).st_size
                    site = urllib2.urlopen(ftp_line)
                    remote_size = site.info().get('Content-Length')
                    print 'Local size: ' + str(local_size)
                    print 'Remote size: ' + str(remote_size)
                    if int(local_size) != int(remote_size):
                        print('Downloading file ' + ftp_line)
                        os.remove(DOWNLOAD_DIR + file_name)
                        download_sequences(ftp_line)

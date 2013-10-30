#!/usr/bin/env python
from bs4 import BeautifulSoup
from urlparse import urlparse
import requests
import urllib

CAMERA_HOST = 'https://portal.camera.calit2.net'
CAMERA_DATA = CAMERA_HOST + '/gridsphere/gridsphere?cid=sampledownloadtab'
CAMERA_LOGIN = CAMERA_HOST + '/gridsphere/gridsphere?cid=login'

with open('password') as f:
    credentials = f.readline().strip().split(':')
s = requests.Session()
payload = {'username': credentials[0], 'password': credentials[1],
           'gs_action': 'gs_login'}
s.get(CAMERA_DATA)
r = s.post(url=CAMERA_LOGIN, data=payload)
html_doc = s.get(CAMERA_DATA)
soup = BeautifulSoup(html_doc.text)
for link in soup.find_all('a'):
    if ('.csv' in link.get('href')) or ('CAM_P' in link.get('href')):
        ftp_line = link.get('href')
        #print(ftp_line)
        url = urlparse(ftp_line)
        local_file_name = 'downloads/' + ftp_line.split('/')[-1].split('#')[0].split('?')[0]
        #print(local_file_name)
        try:
            urllib.urlretrieve(ftp_line, local_file_name)
        except IOError:
            print 'Could not retrieve ' + ftp_line
    #download_sequences()

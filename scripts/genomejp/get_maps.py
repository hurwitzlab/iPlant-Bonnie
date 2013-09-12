#!/usr/bin/env python
# get_maps.py

from bs4 import BeautifulSoup
import requests
import re


def rest_get(url):
    r = requests.get(url)
    results = r.text
    re.compile(r'DBLINKS.+///', re.DOTALL)
    filtered_text = re.sub(r'DBLINKS.+?///', '', results, flags=re.DOTALL)
    return filtered_text

BASE_URL = 'http://www.genome.jp'
GENE_URL = BASE_URL + '/dbget-bin/get_linkdb?-t+8+path:map'
REST_URL = 'http://rest.kegg.jp/get/'
ENZYME_URL = BASE_URL + '/dbget-bin/get_linkdb?-t+enzyme+path:map'
KEGG_MAPS = 'test_maps'
OUTPUT = 'output/'

maps = open(KEGG_MAPS, 'r')
with open(KEGG_MAPS, 'r') as f:
    for line in f.readlines():
        if line.startswith('     '):
            p = re.compile(r'     (\d+) (.+)')
            m = p.match(line)
            map_text = m.group(2)[:-1]
            kegg_map = m.group(1)
            url = GENE_URL + kegg_map
            print 'Requesting ' + url
            r = requests.get(url)
            soup = BeautifulSoup(r.text)
            links = soup.find_all('a')
            out = OUTPUT + kegg_map + map_text.replace(' ', '_')
            print out
            outfile = open(out, 'w')
            counter = 0
            query = ''
            for link in links:
                href = link.get('href')
                print href
                if href.startswith('/dbget-bin'):
                    counter += 1
                    query = query + link.text
                    if counter != 10:
                        query = query + '+'
                    if counter == 10:
                        rest_url = REST_URL + query
                        print rest_url
                        outfile.write(rest_get(rest_url))
                        query = ''
                        counter = 0
            if counter != 0:
                query = query[:-1]
                rest_url = REST_URL + query
                print rest_url
                outfile.write(rest_get(rest_url))
            outfile.close()

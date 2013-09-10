#!/usr/bin/env python
# get_maps.py

from bs4 import BeautifulSoup
import requests
import re

BASE_URL = 'http://www.genome.jp/dbget-bin/get_linkdb?-t+8+path:map'
KEGG_MAPS = 'test_maps'
OUTPUT = 'output/'

maps = open(KEGG_MAPS, 'r')
with open(KEGG_MAPS, 'r') as f:
    for line in f.readlines():
        if line.startswith('     '):
            map_text = re.findall(r'\D+', line.strip())
            kegg_map = re.search(r'\d+', line).group()
            url = BASE_URL + kegg_map
            r = requests.get(url)
            soup = BeautifulSoup(r.text)
            links = soup.find_all('a')
            out = OUTPUT + kegg_map + map_text[0].replace(' ', '_')
            print out
            outfile = open(out, 'w')
            for link in links:
                href = link.get('href')
                if href.startswith('/dbget-bin'):
                    r2 = requests.get(BASE_URL + href)
                    soup2 = BeautifulSoup(r2.text)
                    table = soup2.find('td', class_='fr4')
                    #outfile.write(table.get_text())
                    print soup2.title
            outfile.close()

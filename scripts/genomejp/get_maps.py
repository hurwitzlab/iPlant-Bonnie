#!/usr/bin/env python
# get_maps.py

from bs4 import BeautifulSoup
import requests
import re
BASE_URL = 'http://www.genome.jp'
GENE_URL = BASE_URL + '/dbget-bin/get_linkdb?-t+8+path:map'
ENZYME_URL = BASE_URL + '/dbget-bin/get_linkdb?-t+enzyme+path:map'
KEGG_MAPS = 'test_maps'
OUTPUT = 'output/'

maps = open(KEGG_MAPS, 'r')
with open(KEGG_MAPS, 'r') as f:
    for line in f.readlines():
        if line.startswith('     '):
            map_text = re.findall(r'\D+', line.strip())
            kegg_map = re.search(r'\d+', line).group()
            url = GENE_URL + kegg_map
            print 'Requesting ' + url
            r = requests.get(url)
            soup = BeautifulSoup(r.text)
            links = soup.find_all('a')
            out = OUTPUT + kegg_map + map_text[0].replace(' ', '_')
            print out
            outfile = open(out, 'w')
            for link in links:
                href = link.get('href')
                if href.startswith('/dbget-bin'):
                    url2 = BASE_URL + href
                    print 'Requesting ' + url2
                    r2 = requests.get(url2)
                    soup2 = BeautifulSoup(r2.text)
                    th_entry = soup2.find('th', text='Entry')
                    if th_entry:
                        entry = th_entry.find_next('td').text
                        outfile.write('Entry: ' +
                                      entry.strip().encode('utf8')
                                      + '\n')
                    else:
                        break
                    th_name = soup2.find('th', text='Name')
                    if th_name:
                        name = th_name.find_next('td').text
                        outfile.write('Name: ' + name.strip().encode('utf8')
                                      + '\n')
                    th_definition = soup2.find('th', text='Definition')
                    if th_definition:
                        definition = th_definition.find_next('td').text
                        outfile.write('Definition: '
                                      + definition.strip().encode('utf8')
                                      + '\n')
                    th_pathway = soup2.find('th', text='Pathway')
                    if th_pathway:
                        outfile.write('Pathway:\n')
                        pathway = th_pathway.find_next('td').find_next('td')
                        while True:
                            if ('class' in pathway.attrs and
                               pathway.attrs['class'][0] == 'td40'):
                                break
                            outfile.write(pathway.text.strip().encode('utf8')
                                          + '\n')
                            pathway = pathway.find_next('td')
                    th_brite = soup2.find('th', text='Brite')
                    if th_brite:
                        brite = th_brite.find_next('td').text
                        outfile.write('Brite:\n' +
                                      brite.strip().encode('utf8') + '\n')
                    outfile.write(80 * '=' + '\n')
            outfile.close()

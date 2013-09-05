#!/usr/bin/env python

import argparse
import os
#import shutil
from Bio import SeqIO
import glob


def split_fasta(infile, files_wanted, total_sequences):
    #seq_per_file = (total_sequences / files_wanted) + r
    #for record in SeqIO.parse(infile, 'fasta'):
    #    print record.id
    #infile.close()
    seq_per_file = (total_sequences / files_wanted) + 1
    print seq_per_file
    current_seq_count = 0
    total_seq_count = 0
    file_counter = 1
    outfile = open(outdir + '/query' + str(file_counter), 'w')
    for record in SeqIO.parse(infile, 'fasta'):
        current_seq_count += 1
        total_seq_count += 1
        SeqIO.write(record, outfile, 'fasta')
        if total_seq_count == total_sequences:
            break
        if current_seq_count == seq_per_file:
            current_seq_count = 0
            file_counter += 1
            outfile.close()
            outfile = open(outdir + '/query' + str(file_counter), 'w')
            print total_seq_count

parser = argparse.ArgumentParser(description='Split fasta file into \
                                              smaller pieces')
parser.add_argument('indir', help='Input directory')
parser.add_argument('outdir', help='Output directory')
parser.add_argument('-j', type=int, help='Number of jobs')
args = parser.parse_args()
indir = args.indir
outdir = args.outdir
if not os.path.exists(outdir):
    os.mkdir(outdir)
if args.j:
    jobs = args.j
else:
    jobs = 500
fasta = open(outdir + '/all_seqs', 'w+')
orig_dir = os.getcwd()
total_sequences = 0
for f in glob.glob(indir + '/*.fa'):
    infile = open(f, 'r')
    for line in infile:
        if line.startswith('>'):
            total_sequences += 1
        fasta.write(line)
    infile.close()
fasta.close()
print total_sequences
infile = open(outdir + '/all_seqs', 'rU')
split_fasta(infile, jobs, total_sequences)

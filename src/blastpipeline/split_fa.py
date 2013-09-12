#!/usr/bin/env python
# split_fa.py

"""
Split a directory full of fasta files into files with equal numbers of
sequences per file
"""

import argparse
import os
from Bio import SeqIO
import glob


def split_fasta(infile, outdir, files_wanted, total_sequences, file_counter):
    """
    Split fasta file into x number of files
    """
    seq_per_file = (total_sequences / files_wanted) + 1
    current_seq_count = 0
    total_seq_count = 0
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
    return file_counter


def main():
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
    file_counter = 1
    for f in glob.glob(indir + '/*.fa'):
        total_sequences = 0
        infile = open(f, 'rU')
        for line in infile:
            if line.startswith('>'):
                total_sequences += 1
        print total_sequences
        infile.seek(0)
        file_counter = split_fasta(infile, outdir, jobs,
                                   total_sequences, file_counter)
        print file_counter
        infile.close()

if __name__ == "__main__":
    main()

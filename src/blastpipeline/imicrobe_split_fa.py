#!/usr/bin/env python
# split_fa.py

"""
Split a directory full of fasta files into files with equal numbers of
sequences per file
"""

import argparse
import os
from subprocess import call
from Bio import SeqIO
import glob
from foundation import FoundationApi, FoundationJob
import json
import Queue
import time


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


def upload_split_fasta(path, outdir):
    env = os.environ.copy()
    env['irodsEnvFile'] = '/Users/dboss/.irods/.irodsEnv.imicrobe'
    retcode = call('iput -r ' + outdir + ' /iplant/home/imicrobe/scratch/' +
                   path, shell=True, env=env)


def main():
    parser = argparse.ArgumentParser(description='Split fasta file into \
                                                  smaller pieces')
    parser.add_argument('indir', help='Input directory')
    parser.add_argument('outdir', help='Output directory')
    parser.add_argument('-j', type=int, help='Number of jobs')
    parser.add_argument('--ipuser', required=True, help='iPlant Userid')
    parser.add_argument('--ipoutput', required=True,
                        help='iPlant archive directory')
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
    fapi = FoundationApi.FoundationApi()
    fapi.super_authenticate('imicrobe')
    print 'Make directory scratch/' + args.ipoutput
    results = fapi.make_directory(args.ipoutput)
    print results
    results = fapi.make_directory(args.ipoutput + '/' + outdir)
    print results
    upload_split_fasta(args.ipoutput, outdir)
    counter = 0
    jobs = []
    finished_jobs = []
    failed_jobs = []
    for filename in os.listdir(outdir):
        inputs = {'inputSeqs': '/imicrobe/scratch/' + args.ipoutput + '/' +
                  filename}
        parameters = {'output': 'blastout.' + str(counter),
                      'processorCount': 12,
                      'blastdbs': '/scratch/projects/tacc/iplant/SIMAP/fileshare.csb.univie.ac.at/simap/sequences.fa',
                      'type': 'blastx', 'descriptions': '10',
                      'eval': '1', 'aln': '10',
                      'archivePath': '/imicrobe/scratch/jobs/job-' +
                      args.ipoutput + str(counter)}
        blast_job = FoundationJob.FoundationJob(fapi, 'blast-lonestar-2.2.25',
                                                'iMicrobe Blast 2.2.25 SIMAP',
                                                archive='true', inputs=inputs,
                                                parameters=parameters)
        jobs.append(blast_job)
        counter += 1
    for job in jobs:
        print job.submit()
    while (len(jobs) > 0):
        for job in jobs:
            job.update_status()
            if job.job_status['result']['status'] == 'ARCHIVING_FINISHED':
                finished_jobs.append(job)
                jobs.remove(job)
            elif job.job_status['result']['status'] == 'FAILED':
                print('Job ID: ' + str(job.job_status['result']['id']) +
                      'status =' + job.job_status['result']['status'])
                failed_jobs.append(job)
                jobs.remove(job)
            else:
                # we need to remove the failed job ids as well.
                print('Job ID: ' + str(job.job_status['result']['id']) +
                      'status = ' + job.job_status['result']['status'])
                time.sleep(1)
            time.sleep(10)
    print('All jobs have finished!')


if __name__ == "__main__":
    main()

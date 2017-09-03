#!/usr/bin/python3

import os
import glob
import requests

PCAPS_PATH = '/home/quizumba/pcaps/exit-hourly'
EXE_PATH = '/home/quizumba/pcaps/exit-hourly/exe'

pcap_dir = os.path.join(PCAPS_PATH, 'pcap')

# list *.gz files
gzfiles = glob.glob("%s" % os.path.join(PCAPS_PATH, '*.gz'))

for gzfile in gzfiles:
    # extract files from .pcap.gz
    os.system('mkdir %s' % pcap_dir)
    os.system('cp %s %s' % (gzfile, pcap_dir))
    os.system('cd %s && gunzip *.gz' % pcap_dir)

    os.system('cd %s && tcpflow -r *.pcap -a' % pcap_dir)
    os.system('cd %s && foremost -i *' % pcap_dir)

    exe_files = glob.glob("%s" % os.path.join(pcap_dir, 'output', 'exe', '*'))
    for exe_file in exe_files:
        with open(exe_file, 'rb') as f:
            filename = '%s.exe' % abs(hash(f))

        os.system('cp %s %s' % (exe_file, os.path.join(EXE_PATH, filename)))

    os.system('rm -rf %s' % pcap_dir)

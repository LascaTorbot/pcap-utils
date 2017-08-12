#!/usr/bin/python3

import os
import glob
import requests
import time

REST_URL = 'http://10.1.1.237:8090/tasks/create/file'
PCAPS_PATH = '/home/quizumba/pcaps/exit-hourly'
SLEEP_TIME = 60 # an hour

pcap_dir = os.path.join(PCAPS_PATH, 'pcap')

while True:
    # list *.gz files
    gzfiles = glob.glob("%s" % os.path.join(PCAPS_PATH, '*.gz'))
    # get last gzfile
    gzfiles.sort(reverse=True)
    if len(gzfiles) > 0:
        gzfile = gzfiles[0]

        # extract files from .pcap.gz
        os.system('mkdir %s' % pcap_dir)
        os.system('cp %s %s' % (gzfile, pcap_dir))
        os.system('cd %s && gunzip *.gz' % pcap_dir)

        os.system('cd %s && tcpflow -r *.pcap -a' % pcap_dir)
        os.system('cd %s && foremost -i *' % pcap_dir)

        exe_files = glob.glob("%s" % os.path.join(pcap_dir, 'output', 'exe', '*'))
        for exe_file in exe_files:
            with open(exe_file, 'rb') as f:
                files = {'file': ('temp_file_name', f)}
                r = requests.post(REST_URL, files=files)
                print(r.json())

        os.system('rm -rf %s' % pcap_dir)

    print('sleep time:', SLEEP_TIME)
    time.sleep(SLEEP_TIME)

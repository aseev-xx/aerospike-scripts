#!/home/venv/test1/bin/python36

import glob
from os.path import basename
import subprocess
import multiprocessing
import json
import time
import random

from memory_profiler import profile

def get_disks():
    disks = []

    for device in glob.glob('/dev/sd[a-z]'):
        disks.append('/dev/' + basename(device))

    return disks

def ret_smart(disk):
    cmd = '/sbin/smartctl-trunk -j -a {}'.format(disk)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    if result.returncode == 0:
        return result.stdout
    else:
        if result.stderr:
            Style.error('Preprocess failed: ')
            print(result.stderr)
            return ''

def format_smart_output(smart):
    j = json.loads(smart)
    return j

def get_metrics(m_list):

    len_l = len(m_list)
    average = sum(m_list) / len_l
    m_list.sort()
    median = m_list[int(len_l/2)-1]
    variance = sum((xi - median) ** 2 for xi in m_list) / len_l
   
    data = {'average': average, 'median': median, 'variance': variance }
    
    return data

@profile
def one_proc():
    disks = get_disks()

    result = []

    for disk in disks:
        result.append(format_smart_output(ret_smart(disk)))

@profile
def multi_proc():
    disks = get_disks()

    with multiprocessing.Pool(processes=len(disks)) as pool:
        result = pool.map(ret_smart, disks)

def thread_proc():
    pass

def async_proc():
    pass

def timer(test_func):
    complete_total_time = []

    for i in range(2):
        time_start = time.time()

        test_func()

        total_time = time.time() - time_start
        print("Total time: {}".format(total_time));
        complete_total_time.append(total_time)

        slp = random.uniform(1,10)
        time.sleep(slp)

    res = get_metrics(complete_total_time)
    print("Complete result: \nAverage time: {average} seconds\nMedian time: {median} seconds\nVariance: {variance} seconds".format(**res))

def main():

    timer(one_proc)
    timer(multi_proc)


if __name__ == '__main__':
    main()

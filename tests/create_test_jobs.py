#!/usr/bin/python

import random
import string
import os
from datetime import datetime

from megacron import api

TAB_FILE = './test.tab'
uid = os.getuid()
NUM_OF_JOBS = 5
cron_strings = {}

def create_test_tab():
    job_num = 1
    while job_num <= NUM_OF_JOBS:
        cron_strings.setdefault(job_num, [])
        create_test_intervals(job_num)
        cron_strings[job_num].append(create_test_commands(job_num))
        job_num += 1

    with open(TAB_FILE,'w') as tab:
        for line in cron_strings.iterkeys():
            for item in cron_strings[line]:
                tab.write(item)
    tab.close()

    test_jobs = []
    with open(TAB_FILE, 'r') as tab:
        for job in tab:
            tmp = job.strip().split(' ')
            interval = string.joinfields(tmp[:5], ' ')
            cmd = string.joinfields(tmp[5:], ' ')
            test_jobs.append(api.Job(interval, cmd, uid, datetime.now()))
    tab.close()

    return test_jobs

def create_test_commands(job_num):
    job_string = str(job_num)
    command_strings = [' echo test ' + job_string + '\n', ' echo test ' \
    + job_string + ' > ' + job_string + '.txt \n']

    return (command_strings[random.randrange(len(command_strings))])

def create_test_intervals(job_num):
    fields = []

    minute = random.randrange(0,59)
    hour = random.randrange(0,23)
    day_of_month = random.randrange(1,31)
    month = random.randrange(1,12)
    day_of_week = random.randrange(0,6)

    interval_fields = [minute, hour, day_of_month, month, day_of_week]

    for field in interval_fields:
        field_value = field     # a temporary variable to save the value of field
        if field_value % 2 == 0 and field_value != 0:
            field = '*'
            if field_value % 4 == 0 and field_value != 0:
                field = field + ('/' + str(field_value))

        fields.append(str(field))
        interval_strings = ' '.join(fields)
    
    cron_strings[job_num].append(interval_strings)

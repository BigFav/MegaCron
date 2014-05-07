#!/usr/bin/python

import random
import string
import os
from datetime import datetime

from megacron import api

TAB_FILE = './test.tab'
api.FILE_NAME = './testdb.p'

uid = os.getuid()


def cleanup():
    # Kill the temporary tab file
    if(os.access(TAB_FILE, os.F_OK)):
        os.remove(TAB_FILE)
    # Kill the temporary database
    if(os.access(api.FILE_NAME, os.F_OK)):
        os.remove(api.FILE_NAME)


def check_job_fields(self, jobs_list, test_jobs, uid):
    current = 0
    for job in jobs_list:
        self.assertEqual(job.interval, test_jobs[current].interval)
        self.assertEqual(job.command, test_jobs[current].command)
        self.assertEqual(job.user_id, test_jobs[current].user_id)
        self.assertEqual(job.last_time_run, test_jobs[current].last_time_run)
        self.assertEqual(job._id, test_jobs[current]._id)
        current += 1


def check_worker_fields(self, workers_list, test_workers):
    current = 0
    for worker in test_workers:
        self.assertEqual(worker.heartbeat, workers_list[current].heartbeat)
        self.assertEqual(worker._id, workers_list[current]._id)
        current += 1


def check_schedule_fields(self, schedules_list, test_schedules):
    current = 0
    for schedule in test_schedules:
        self.assertEqual(schedule.time_to_run,
                         schedules_list[current].time_to_run)
        self.assertEqual(schedule.job, schedules_list[current].job)
        self.assertEqual(schedule.worker, schedules_list[current].worker)
        self.assertEqual(schedule._id, schedules_list[current]._id)
        current += 1


def check_heartbeat_value(self, worker, previous_heartbeats,
                          checkpoint1, checkpoint2, current1):
    self.assertTrue(worker.heartbeat > checkpoint1 and
                    worker.heartbeat < checkpoint2 and
                    worker.heartbeat > previous_heartbeats[current] and
                    previous_heartbeats[current] < checkpoint1)


def create_test_tab(num_of_jobs, uid):
    # Will contain parsed auto-generated crontab entries
    cron_strings = {}
    job_num = 1
    while job_num <= num_of_jobs:
        cron_strings.setdefault(job_num, [])
        create_test_intervals(cron_strings[job_num])
        cron_strings[job_num].append(create_test_commands(job_num,
                                     cron_strings[job_num]))
        job_num += 1
    with open(TAB_FILE, 'w') as tab:
        for line in cron_strings.iterkeys():
            rand = random.randrange(100)
            # Approximately 30% chance that we will include a comment
            if(rand > 85):
                tab.write('#')
            if(rand >= 70 and rand < 85):
                tab.write('# ')
            # Approximately 15% chance that we will include a blank line
            if(rand >= 50 and rand < 70):
                tab.write('\n')
            for item in cron_strings[line]:
                tab.write(item)
    # Will contain assembled job-interval strings
    test_jobs = []
    with open(TAB_FILE, 'r') as tab:
        for job in tab:
            first_char = job[0]
            if first_char != '\n':
                tmp = job.strip().split(' ')
                interval = string.joinfields(tmp[:5], ' ')
                cmd = string.joinfields(tmp[5:], ' ')
                test_jobs.append(api.Job(interval, cmd, uid, datetime.now()))
    return test_jobs


def create_test_commands(job_num, cron_job):
    job_string = str(job_num)
    command_strings = [' echo test ' + job_string + '\n', ' echo test ' +
                       job_string + ' > ' + job_string + '.txt \n']
    return (command_strings[random.randrange(len(command_strings))])


def create_test_intervals(cron_job):
    # Will contain random interval field values to be assembled
    fields = []
    minute = random.randrange(0, 59)
    hour = random.randrange(0, 23)
    day_of_month = random.randrange(1, 31)
    month = random.randrange(1, 12)
    day_of_week = random.randrange(0, 6)
    interval_fields = [minute, hour, day_of_month, month, day_of_week]
    for field in interval_fields:
        # A temporary variable
        field_value = field
        if field_value % 2 == 0 and field_value != 0:
            field = '*'
            if field_value % 4 == 0 and field_value != 0:
                field = field + ('/' + str(field_value))
        fields.append(str(field))
        interval_strings = ' '.join(fields)
    cron_job.append(interval_strings)

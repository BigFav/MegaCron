#!/usr/bin/python

import os
from datetime import datetime

from create_test_jobs import create_test_tab, uid
from megacron import api

api.FILE_NAME = './testdb.p'

test_jobs = create_test_tab()

def test_set_jobs():
    api.set_jobs(test_jobs, uid)

def test_get_jobs():
    jobs_list = api.get_jobs()
    current = 0
    for job in jobs_list:
        if job.interval == test_jobs[current].interval:
            print 'PASS'
        else:
            print 'FAIL'
        current += 1


# def main():
test_set_jobs()
test_get_jobs()

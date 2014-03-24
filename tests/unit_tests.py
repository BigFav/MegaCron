#!/usr/bin/python

import unittest
import os

from datetime import datetime

from create_test_jobs import create_test_tab, cleanup, test_job_fields, uid
from megacron import api

api.FILE_NAME = './testdb.p'

class TestJobsFunctions(unittest.TestCase):        

    def test_set_jobs_none(self):
        num_of_jobs = 0
        checkpoint = datetime.now()
        self.test_jobs = create_test_tab(num_of_jobs) # create a crontab with 0 jobs
        api.set_jobs(self.test_jobs, uid)
        db_creation_time = datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
        new_time = db_creation_time.replace(second=db_creation_time.second + 1)
        self.assertTrue(new_time > checkpoint)
        cleanup()

    def test_set_jobs_one(self):
    	num_of_jobs = 1
        checkpoint = datetime.now()
        self.test_jobs = create_test_tab(num_of_jobs) # create a crontab with 1 job
        api.set_jobs(self.test_jobs, uid)
    	db_creation_time = datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
    	new_time = db_creation_time.replace(second=db_creation_time.second + 1)
        self.assertTrue(new_time > checkpoint)
        cleanup()

    def test_set_jobs_many(self):
        num_of_jobs = 100
    	checkpoint = datetime.now()
        self.test_jobs = create_test_tab(num_of_jobs) # create a crontab with 100 jobs
        api.set_jobs(self.test_jobs, uid)
    	db_creation_time = datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
    	new_time = db_creation_time.replace(second=db_creation_time.second + 1)
        self.assertTrue(new_time > checkpoint)
        cleanup()


    def test_get_jobs_none(self):
        num_of_jobs = 0
        self.test_jobs = create_test_tab(num_of_jobs) # create a crontab with 0 jobs
        api.set_jobs(self.test_jobs, uid)
        self.jobs_list = api.get_jobs()
        self.assertEqual(len(self.jobs_list), num_of_jobs) # check that number of jobs is equal to num_of_jobs
        test_job_fields(self)
        cleanup()

    def test_get_jobs_one(self):
        num_of_jobs = 1
        self.test_jobs = create_test_tab(num_of_jobs) # create a crontab with 1 job
        api.set_jobs(self.test_jobs, uid)
        self.jobs_list = api.get_jobs()
        self.assertEqual(len(self.jobs_list), num_of_jobs) # check that number of jobs is equal to num_of_jobs
        test_job_fields(self)
        cleanup()

    def test_get_jobs_many(self):
        num_of_jobs = 100
        self.test_jobs = create_test_tab(num_of_jobs) # create a crontab with 100 jobs
        api.set_jobs(self.test_jobs, uid)
        self.jobs_list = api.get_jobs()
        self.assertEqual(len(self.jobs_list), num_of_jobs) # check that number of jobs is equal to num_of_jobs
        test_job_fields(self)
        cleanup()


if __name__ == '__main__':
    unittest.main()

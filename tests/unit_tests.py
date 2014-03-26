#!/usr/bin/python

import unittest
import os

from datetime import datetime

from create_test_jobs import create_test_tab, cleanup, test_job_fields, uids
from megacron import api

api.FILE_NAME = './testdb.p'

class TestJobsFunctions(unittest.TestCase):        

#### TEST SET_JOBS([Job], uid) ####
    def test_set_jobs_none(self):
        num_of_jobs = 0
        checkpoint = datetime.now()
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 0 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        db_creation_time = datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
        new_time = db_creation_time.replace(second=db_creation_time.second + 1)
        self.assertTrue(new_time > checkpoint) # check that the jobs have been set just now
        cleanup()

    def test_set_jobs_one(self):
    	num_of_jobs = 1
        checkpoint = datetime.now()
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 1 job
        api.set_jobs(self.test_jobs, uids['uid1'])
    	db_creation_time = datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
    	new_time = db_creation_time.replace(second=db_creation_time.second + 1)
        self.assertTrue(new_time > checkpoint) # check that the jobs have been set just now
        cleanup()

    def test_set_jobs_many(self):
        num_of_jobs = 10
    	checkpoint = datetime.now()
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 10 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
    	db_creation_time = datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
    	new_time = db_creation_time.replace(second=db_creation_time.second + 1)
        self.assertTrue(new_time > checkpoint) # check that the jobs have been set just now
        cleanup()

#### TEST GET_JOBS() ####
    def test_get_jobs_none(self):
        num_of_jobs = 0
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 0 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list_uid1= api.get_jobs()
        self.assertEqual(len(self.jobs_list_uid1), num_of_jobs) # check that number of jobs is equal to num_of_jobs
        test_job_fields(self, uids['uid1'], self.jobs_list_uid1) # verify that the information we get is the same as what was set
        cleanup()

    def test_get_jobs_one(self):
        num_of_jobs = 1
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 1 job
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list_uid1= api.get_jobs()
        self.assertEqual(len(self.jobs_list_uid1), num_of_jobs) # check that number of jobs is equal to num_of_jobs
        test_job_fields(self, uids['uid1'], self.jobs_list_uid1) # verify that the information we get is the same as what was set
        cleanup()

    def test_get_jobs_many(self):
        num_of_jobs = 10
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 10 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list_uid1= api.get_jobs()
        self.assertEqual(len(self.jobs_list_uid1), num_of_jobs) # check that number of jobs is equal to num_of_jobs
        test_job_fields(self, uids['uid1'], self.jobs_list_uid1) # verify that the information we get is the same as what was set
        cleanup()

#### TEST GET_JOBS_FOR_USER(uid) ####
    def test_get_jobs_for_user_empty_jobs(self):
        num_of_jobs = 0
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 0 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])
        self.assertEqual(len(self.jobs_list_uid1), num_of_jobs) # check that number of jobs for uids['uid1'] is equal to num_of_jobs
        cleanup()

    def test_get_jobs_for_user_many_jobs(self):
        num_of_jobs = 10
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 0 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])
        self.assertEqual(len(self.jobs_list_uid1), num_of_jobs) # check that number of jobs for uids['uid1'] is equal to num_of_jobs
        cleanup()

    def test_get_jobs_for_user_multiple(self):
        num_of_jobs1 = 1
        self.test_jobs = create_test_tab(num_of_jobs1, uids['uid1']) # add 1 job to the tabfile for uids['uid1']
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])
        test_job_fields(self, uids['uid1'], self.jobs_list_uid1) # verify that the information we get is the same as what was set
        num_of_jobs2 = 0
        self.test_jobs = create_test_tab(num_of_jobs2, uids['uid2']) # add 0 jobs to the tabfile for uids['uid1']
        api.set_jobs(self.test_jobs, uids['uid2'])
        self.jobs_list_uid2 = api.get_jobs_for_user(uids['uid2'])
        test_job_fields(self, uids['uid1'], self.jobs_list_uid2) # verify that the information we get is the same as what was set
        num_of_jobs3 = 4
        self.test_jobs = create_test_tab(num_of_jobs3, uids['uid3']) # add 4 jobs to the tabfile for uids['uid1']
        api.set_jobs(self.test_jobs, uids['uid3'])
        self.jobs_list_uid3 = api.get_jobs_for_user(uids['uid3'])
        test_job_fields(self, uids['uid1'], self.jobs_list_uid3) # verify that the information we get is the same as what was set
        self.assertEqual(len(self.jobs_list_uid1), num_of_jobs1) # check that number of jobs for uids['uid1'] is equal to num_of_jobs1
        self.assertEqual(len(self.jobs_list_uid2), num_of_jobs2) # check that number of jobs for uid2 is equal to num_of_jobs2
        self.assertEqual(len(self.jobs_list_uid3), num_of_jobs3) # check that number of jobs for uid2 is equal to num_of_jobs3
        cleanup()

if __name__ == '__main__':
    unittest.main()

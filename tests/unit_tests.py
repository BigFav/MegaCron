#!/usr/bin/python

import unittest
import os
import random

from datetime import datetime

from create_test_jobs import create_test_tab, cleanup, check_job_fields, check_worker_fields, uids
from megacron import api

api.FILE_NAME = './testdb.p'

class TestJobsFunctions(unittest.TestCase):        


#### TEST GET_JOBS() ####
    def test_get_jobs_empty_jobs(self):
        num_of_jobs = 0
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 0 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list = api.get_jobs()
        self.assertEqual(len(self.jobs_list), num_of_jobs) # check that number of jobs is equal to num_of_jobs
        check_job_fields(self, self.test_jobs, uids['uid1'], self.jobs_list) # verify that the information we get is the same as what was set
        cleanup()

    def test_get_jobs_one_job(self):
        num_of_jobs = 1
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 1 job
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list = api.get_jobs()
        self.assertEqual(len(self.jobs_list), num_of_jobs) # check that number of jobs is equal to num_of_jobs
        check_job_fields(self, self.test_jobs, uids['uid1'], self.jobs_list) # verify that the information we get is the same as what was set
        cleanup()

    def test_get_jobs_many_jobs(self):
        num_of_jobs = 10
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 10 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list = api.get_jobs()
        self.assertEqual(len(self.jobs_list), num_of_jobs) # check that number of jobs is equal to num_of_jobs
        check_job_fields(self, self.test_jobs, uids['uid1'], self.jobs_list) # verify that the information we get is the same as what was set
        cleanup()


#### TEST GET_JOBS_FOR_USER(uid) ####
    def test_get_jobs_for_user_empty_jobs(self):
        num_of_jobs = 0
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 0 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])
        self.assertEqual(len(self.jobs_list_uid1), num_of_jobs) # check that number of jobs for uid1 is equal to num_of_jobs
        cleanup()

    def test_get_jobs_for_user_many_jobs(self):
        num_of_jobs = 10
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 0 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])
        self.assertEqual(len(self.jobs_list_uid1), num_of_jobs) # check that number of jobs for uid1 is equal to num_of_jobs
        cleanup()

    def test_get_jobs_for_user_multiple(self):
        num_of_jobs_uid1 = 1
        self.test_jobs_uid1 = create_test_tab(num_of_jobs_uid1, uids['uid1']) # add 1 job to the tabfile for uid1
        api.set_jobs(self.test_jobs_uid1, uids['uid1'])
        self.jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])
        num_of_jobs_uid2 = 0
        self.test_jobs_uid2 = create_test_tab(num_of_jobs_uid2, uids['uid2']) # add 0 jobs to the tabfile for uid2
        api.set_jobs(self.test_jobs_uid2, uids['uid2'])
        self.jobs_list_uid2 = api.get_jobs_for_user(uids['uid2'])
        num_of_jobs_uid3 = 4
        self.test_jobs_uid3 = create_test_tab(num_of_jobs_uid3, uids['uid3']) # add 4 jobs to the tabfile for uid3
        api.set_jobs(self.test_jobs_uid3, uids['uid3'])
        self.jobs_list_uid3 = api.get_jobs_for_user(uids['uid3'])
        self.assertEqual(len(self.jobs_list_uid1), num_of_jobs_uid1) # check that number of jobs for uid1 is equal to num_of_jobs_uid1
        self.assertEqual(len(self.jobs_list_uid2), num_of_jobs_uid2) # check that number of jobs for uid2 is equal to num_of_jobs_uid2
        self.assertEqual(len(self.jobs_list_uid3), num_of_jobs_uid3) # check that number of jobs for uid3 is equal to num_of_jobs_uid3
        check_job_fields(self, self.test_jobs_uid1, uids['uid1'], self.jobs_list_uid1) # verify that the information we get is the same as what was set
        check_job_fields(self, self.test_jobs_uid2, uids['uid2'], self.jobs_list_uid2) # verify that the information we get is the same as what was set
        check_job_fields(self, self.test_jobs_uid3, uids['uid3'], self.jobs_list_uid3) # verify that the information we get is the same as what was set
        cleanup()

    def test_get_jobs_for_user_none(self):
        self.jobs_list_uid4 = api.get_jobs_for_user(uids['uid4'])        
        self.assertTrue(len(self.jobs_list_uid4) == 0) # check that number of jobs for uid4 is equal to 0
        num_of_jobs_uid1 = 1
        self.test_jobs_uid1 = create_test_tab(num_of_jobs_uid1, uids['uid1']) # add 1 job to the tabfile for uids['uid1']
        api.set_jobs(self.test_jobs_uid1, uids['uid1'])
        self.jobs_list_uid4 = api.get_jobs_for_user(uids['uid4'])
        self.assertTrue(len(self.jobs_list_uid4) == 0) # check that number of jobs for uid4 is equal to 0


#### TEST SET_JOBS([Job], uid) ####
    def test_set_jobs_empty_jobs(self):
        num_of_jobs = 0
        checkpoint = datetime.now()
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 0 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        db_creation_time = datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
        new_time = db_creation_time.replace(second=db_creation_time.second + 1)
        self.assertTrue(new_time > checkpoint) # check that the jobs have been set just now
        cleanup()

    def test_set_jobs_one_job(self):
        num_of_jobs = 1
        checkpoint = datetime.now()
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 1 job
        api.set_jobs(self.test_jobs, uids['uid1'])
        db_creation_time = datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
        new_time = db_creation_time.replace(second=db_creation_time.second + 1)
        self.assertTrue(new_time > checkpoint) # check that the jobs have been set just now
        cleanup()

    def test_set_jobs_many_jobs(self):
        num_of_jobs = 10
        checkpoint = datetime.now()
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 10 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        db_creation_time = datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
        new_time = db_creation_time.replace(second=db_creation_time.second + 1)
        self.assertTrue(new_time > checkpoint) # check that the jobs have been set just now
        cleanup()


#### TEST SET_JOB_TIME(Job) ####
    def test_set_job_time_one_job(self):
        checkpoint1 = datetime.now()
        num_of_jobs = 1
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 0 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        job = self.test_jobs.pop() # pop the only job in the list to modify its time
        api.set_job_time(job)
        checkpoint2 = datetime.now()
        self.assertTrue(job.last_time_run > checkpoint1 and job.last_time_run < checkpoint2) # check that the job's time was updated correctly
        cleanup()

    def test_set_job_time_random_job_from_multiple(self):
        checkpoint1 = datetime.now()
        num_of_jobs = 3
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1']) # create a crontab with 0 jobs
        api.set_jobs(self.test_jobs, uids['uid1'])
        job = self.test_jobs.pop(random.randrange(len(self.test_jobs))) # pop random job in list to modify its time
        api.set_job_time(job)
        checkpoint2 = datetime.now()
        self.assertTrue(job.last_time_run > checkpoint1 and job.last_time_run < checkpoint2) # check that the job's time was updated correctly
        cleanup()


#### TEST CREATE_WORKER() ####
    def test_create_worker_one(self):
        num_of_workers = 1
        workers_list = []
        checkpoint1 = datetime.now()
        workers_list.append(api.create_worker()) # create 1 worker and add it to a list for bookkeeping
        checkpoint2 = datetime.now()
        check_worker_fields(self, checkpoint1, checkpoint2, workers_list)
        cleanup()

    def test_create_worker_many(self):
        num_of_workers = 10
        workers_list = []
        checkpoint1 = datetime.now()
        for job in xrange(num_of_workers):
            workers_list.append(api.create_worker()) # create 10 workers and add them to a list for bookkeeping
        checkpoint2 = datetime.now()
        check_worker_fields(self, checkpoint1, checkpoint2, workers_list)
        cleanup()

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python

import unittest
import os
import random
from datetime import datetime

from create_test_jobs import create_test_tab, cleanup, uids, \
     check_job_fields, check_worker_fields
from megacron import api

api.FILE_NAME = './testdb.p'

class TestJobsFunctions(unittest.TestCase):        

    def tearDown(self):
       cleanup()

#### TEST GET_JOBS() ####
    def test_get_jobs_empty_jobs(self):
        num_of_jobs = 0
        # Create a crontab with zero jobs
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list = api.get_jobs()
        # Verify that the jobs list is empty
        self.assertEqual(len(self.jobs_list), num_of_jobs)
        # Verify that the information we get matches what was set
        check_job_fields(self, self.jobs_list, self.test_jobs, uids['uid1'])

    def test_get_jobs_one_job(self):
        num_of_jobs = 1
        # Create a crontab with one job
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list = api.get_jobs()
        # Verify that the jobs list contains exactly one job
        self.assertEqual(len(self.jobs_list), num_of_jobs)
        # Verify that the information we get matches what was set
        check_job_fields(self, self.jobs_list, self.test_jobs, uids['uid1'])

    def test_get_jobs_many_jobs(self):
        num_of_jobs = 10
        # Create a crontab with many jobs
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list = api.get_jobs()
        self.assertEqual(len(self.jobs_list), num_of_jobs)
        # Verify that the information we get matches what was set
        check_job_fields(self, self.jobs_list, self.test_jobs, uids['uid1'])

#### TEST GET_JOBS_FOR_USER(uid) ####
    def test_get_jobs_for_user_empty_jobs(self):
        num_of_jobs = 0
        # Create a crontab with zero jobs
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])
        # Verify that the jobs list for uid1 is empty
        self.assertEqual(len(self.jobs_list_uid1), num_of_jobs)

    def test_get_jobs_for_user_many_jobs(self):
        num_of_jobs = 10
        # Create a crontab with many jobs
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(self.test_jobs, uids['uid1'])
        self.jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])
        # Verify that the jobs list for uid1
        # contains the correct number of jobs
        self.assertEqual(len(self.jobs_list_uid1), num_of_jobs)

    def test_get_jobs_for_user_some_users_some_jobs(self):
        num_of_jobs_uid1 = 1
        # Add one job to the tabfile for uid1
        self.test_jobs_uid1 = create_test_tab(num_of_jobs_uid1, uids['uid1'])
        api.set_jobs(self.test_jobs_uid1, uids['uid1'])
        self.jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])

        num_of_jobs_uid2 = 0
        # Add zero jobs to the tabfile for uid2
        self.test_jobs_uid2 = create_test_tab(num_of_jobs_uid2, uids['uid2'])
        api.set_jobs(self.test_jobs_uid2, uids['uid2'])
        self.jobs_list_uid2 = api.get_jobs_for_user(uids['uid2'])

        num_of_jobs_uid3 = 4
        # Add some jobs to the tabfile for uid3
        self.test_jobs_uid3 = create_test_tab(num_of_jobs_uid3, uids['uid3'])
        api.set_jobs(self.test_jobs_uid3, uids['uid3'])
        self.jobs_list_uid3 = api.get_jobs_for_user(uids['uid3'])

        # Verify that the jobs list for uid1 contains
        # the correct number of jobs
        self.assertEqual(len(self.jobs_list_uid1), num_of_jobs_uid1)
        # Verify that the jobs list for uid2 contains
        # the correct number of jobs
        self.assertEqual(len(self.jobs_list_uid2), num_of_jobs_uid2)
        # Verify that the jobs list for uid3 contains
        # the correct number of jobs
        self.assertEqual(len(self.jobs_list_uid3), num_of_jobs_uid3)
        # Verify that the information we get matches what was set
        check_job_fields(self, self.jobs_list_uid1, self.test_jobs_uid1, 
        uids['uid1'])
        # Verify that the information we get matches what was set
        check_job_fields(self, self.jobs_list_uid2, self.test_jobs_uid2,
        uids['uid2'])
        # Verify that the information we get matches what was set
        check_job_fields(self, self.jobs_list_uid3, self.test_jobs_uid3,
        uids['uid3'])

    def test_get_jobs_for_user_some_users_empty_jobs(self):
        self.jobs_list_uid4 = api.get_jobs_for_user(uids['uid4'])
        # Verify that the jobs_list for uid4 is empty       
        self.assertFalse(len(self.jobs_list_uid4))
        num_of_jobs_uid1 = 1
        # Add one job to the tabfile uid1
        self.test_jobs_uid1 = create_test_tab(num_of_jobs_uid1, uids['uid1'])
        api.set_jobs(self.test_jobs_uid1, uids['uid1'])
        self.jobs_list_uid4 = api.get_jobs_for_user(uids['uid4'])
        # Verify that the jobs_list for uid4 is empty
        self.assertFalse(len(self.jobs_list_uid4))

#### TEST SET_JOBS([Job], uid) ####
    def test_set_jobs_empty_jobs(self):
        num_of_jobs = 0
        chkpnt = datetime.now()
        # Create a crontab with zero jobs
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(self.test_jobs, uids['uid1'])
        db_creation_time \
        = datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
        new_time = \
        db_creation_time.replace(second=db_creation_time.second + 1)
        # Verify that the jobs have been set just now
        self.assertTrue(new_time > chkpnt)

    def test_set_jobs_one_job(self):
        num_of_jobs = 1
        chkpnt = datetime.now()
        # Create a crontab with one job
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(self.test_jobs, uids['uid1'])
        db_creation_time = \
        datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
        new_time = \
        db_creation_time.replace(second=db_creation_time.second + 1)
        # Verify that the jobs have been set just now
        self.assertTrue(new_time > chkpnt)

    def test_set_jobs_many_jobs(self):
        num_of_jobs = 10
        chkpnt = datetime.now()
        # Create a crontab with many jobs
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(self.test_jobs, uids['uid1'])
        db_creation_time = \
        datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
        new_time = \
        db_creation_time.replace(second=db_creation_time.second + 1)
        # Verify that the jobs have been set just now
        self.assertTrue(new_time > chkpnt)

#### TEST SET_JOB_TIME(Job) ####
    def test_set_job_time_one_job(self):
        chkpnt1 = datetime.now()
        num_of_jobs = 1
        # Create a crontab with one job
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(self.test_jobs, uids['uid1'])
        # Pop the only job in the list to modify its time
        job = self.test_jobs.pop()
        api.set_job_time(job)
        chkpnt2 = datetime.now()
        # Verify that the job's last time run was updated correctly
        self.assertTrue(job.last_time_run > chkpnt1 and
        job.last_time_run < chkpnt2)

    def test_set_job_time_random_job_from_many(self):
        chkpnt1 = datetime.now()
        num_of_jobs = 10
        # Create a crontab with many jobs
        self.test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(self.test_jobs, uids['uid1'])
        # Pop a random job in list to modify its time
        job = self.test_jobs.pop(random.randrange(len(self.test_jobs)))
        api.set_job_time(job)
        chkpnt2 = datetime.now()
        # Verify that the job's last time run was updated correctly
        self.assertTrue(job.last_time_run > chkpnt1 and
        job.last_time_run < chkpnt2)

#### TEST CREATE_WORKER() ####
    def test_create_worker_one_worker(self):
        num_of_workers = 1
        test_workers = []
        chkpnt1 = datetime.now()
        # Create one worker and add them to a list for bookkeeping
        test_workers.append(api.create_worker())
        chkpnt2 = datetime.now()
        current = 1
        for worker in test_workers:
        	# Verify that the worker has been created just now
            self.assertTrue(worker.heartbeat > chkpnt1 and
            worker.heartbeat < chkpnt2)
            current += 1

    def test_create_worker_many_workers(self):
        num_of_workers = 10
        test_workers = []
        chkpnt1 = datetime.now()
        for job in xrange(num_of_workers):
        	# Create many workers and add them to a list for bookkeeping
            test_workers.append(api.create_worker())
        chkpnt2 = datetime.now()
        current = 1
        for worker in test_workers:
        	# Verify that the workers have been created just now
            self.assertTrue(worker.heartbeat > chkpnt1 and
            worker.heartbeat < chkpnt2)
            current += 1

#### TEST GET_WORKERS() ####
    def test_get_workers_empty_workers(self):
    	num_of_workers = 0
    	workers_list = api.get_workers()
    	# Verify that workers list is empty
    	self.assertEqual(len(workers_list), num_of_workers)

    def test_get_workers_one_worker(self):
    	num_of_workers = 1
        test_workers = []
        # Create one worker and add them to a list for bookkeeping
        test_workers.append(api.create_worker())
    	workers_list = api.get_workers()
        # Verify that the workers list contains exactly one worker
    	self.assertEqual(len(workers_list), num_of_workers)
    	# Verify that the information we get is the same as what was set
        check_worker_fields(self, workers_list, test_workers)

    def test_get_workers_many_workers(self):
    	num_of_workers = 10
        test_workers = []
        for job in xrange(num_of_workers):
        	# Create workers and add them to a list for bookkeeping
            test_workers.append(api.create_worker())
    	workers_list = api.get_workers()
    	# Verify that the workers list contains the correct number of workers
    	self.assertEqual(len(workers_list), num_of_workers)
        check_worker_fields(self, workers_list, test_workers)

### TEST GET_NEXT_WORKER() ####
    def test_get_next_worker_empty_workers(self):
    	next_worker = api.get_next_worker()
    	# Verify that the next worker does not exist
    	self.assertEqual(next_worker, None)

    def test_get_next_worker_one_worker(self):
    	num_of_workers = 1
    	test_workers, workers_list = [], []
    	# Create one worker and add it to a list for bookkeeping
    	test_workers.append(api.create_worker())
    	workers_list.append(api.get_next_worker())
    	# Verify that the workers list contains exactly one worker
    	self.assertEqual(len(workers_list), num_of_workers)
    	check_worker_fields(self, workers_list, test_workers)

    def test_get_next_worker_one_worker_many_requests(self):
    	num_of_workers = 1
    	num_of_requests = 10
    	test_workers, workers_list = [], []
    	for request in xrange(num_of_requests):
    		 # Create workers and add them to a list for bookkeeping
    	    test_workers.append(api.create_worker())
    	for request in xrange(num_of_requests):
    		# Get workers and add them to a list for bookkeeping
    	    workers_list.append(api.get_next_worker())
    	    # Verify that the workers list contains
    	    # as many workersas there were requests
    	self.assertEqual(len(workers_list), num_of_requests)
    	check_worker_fields(self, workers_list, test_workers)

if __name__ == '__main__':
    unittest.main()

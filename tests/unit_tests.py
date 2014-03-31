#!/usr/bin/python2

import unittest
import os
import random
import math
from datetime import datetime

from test_support_functions import create_test_tab, cleanup, uids, \
     check_job_fields, check_worker_fields, check_heartbeat_value
from megacron import api

api.FILE_NAME = './testdb.p'

class TestApiFunctions(unittest.TestCase):        

    def tearDown(self):
       cleanup()

# #### TEST GET_JOBS() ####
#     def test_get_jobs_empty_jobs(self):
#         num_of_jobs = 0
#         # Create a crontab with zero jobs
#         test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
#         api.set_jobs(test_jobs, uids['uid1'])
#         jobs_list = api.get_jobs()
#         # Verify that the jobs list is empty
#         self.assertEqual(len(jobs_list), num_of_jobs)
#         # Verify that the information we get matches what was set
#         check_job_fields(self, jobs_list, test_jobs, uids['uid1'])

#     def test_get_jobs_one_job(self):
#         num_of_jobs = 1
#         # Create a crontab with one job
#         test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
#         api.set_jobs(test_jobs, uids['uid1'])
#         jobs_list = api.get_jobs()
#         # Verify that the jobs list contains exactly one job
#         self.assertEqual(len(jobs_list), num_of_jobs)
#         # Verify that the information we get matches what was set
#         check_job_fields(self, jobs_list, test_jobs, uids['uid1'])

#     def test_get_jobs_many_jobs(self):
#         num_of_jobs = 10
#         # Create a crontab with many jobs
#         test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
#         api.set_jobs(test_jobs, uids['uid1'])
#         jobs_list = api.get_jobs()
#         self.assertEqual(len(jobs_list), num_of_jobs)
#         # Verify that the information we get matches what was set
#         check_job_fields(self, jobs_list, test_jobs, uids['uid1'])

# #### TEST GET_JOBS_FOR_USER(uid) ####
#     def test_get_jobs_for_user_empty_jobs(self):
#         num_of_jobs = 0
#         # Create a crontab with zero jobs
#         test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
#         api.set_jobs(test_jobs, uids['uid1'])
#         jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])
#         # Verify that the jobs list for uid1 is empty
#         self.assertEqual(len(jobs_list_uid1), num_of_jobs)

#     def test_get_jobs_for_user_many_jobs(self):
#         num_of_jobs = 10
#         # Create a crontab with many jobs
#         test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
#         api.set_jobs(test_jobs, uids['uid1'])
#         jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])
#         # Verify that the jobs list for uid1
#         # contains the correct number of jobs
#         self.assertEqual(len(jobs_list_uid1), num_of_jobs)

#     def test_get_jobs_for_user_some_users_some_jobs(self):
#         num_of_jobs_uid1 = 1
#         # Add one job to the tabfile for uid1
#         test_jobs_uid1 = create_test_tab(num_of_jobs_uid1, uids['uid1'])
#         api.set_jobs(test_jobs_uid1, uids['uid1'])
#         jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])

#         num_of_jobs_uid2 = 0
#         # Add zero jobs to the tabfile for uid2
#         test_jobs_uid2 = create_test_tab(num_of_jobs_uid2, uids['uid2'])
#         api.set_jobs(test_jobs_uid2, uids['uid2'])
#         jobs_list_uid2 = api.get_jobs_for_user(uids['uid2'])

#         num_of_jobs_uid3 = 4
#         # Add some jobs to the tabfile for uid3
#         test_jobs_uid3 = create_test_tab(num_of_jobs_uid3, uids['uid3'])
#         api.set_jobs(test_jobs_uid3, uids['uid3'])
#         jobs_list_uid3 = api.get_jobs_for_user(uids['uid3'])

#         # Verify that the jobs list for uid1 contains
#         # the correct number of jobs
#         self.assertEqual(len(jobs_list_uid1), num_of_jobs_uid1)
#         # Verify that the jobs list for uid2 contains
#         # the correct number of jobs
#         self.assertEqual(len(jobs_list_uid2), num_of_jobs_uid2)
#         # Verify that the jobs list for uid3 contains
#         # the correct number of jobs
#         self.assertEqual(len(jobs_list_uid3), num_of_jobs_uid3)
#         # Verify that the information we get matches what was set
#         check_job_fields(self, jobs_list_uid1, test_jobs_uid1, 
#         uids['uid1'])
#         # Verify that the information we get matches what was set
#         check_job_fields(self, jobs_list_uid2, test_jobs_uid2,
#         uids['uid2'])
#         # Verify that the information we get matches what was set
#         check_job_fields(self, jobs_list_uid3, test_jobs_uid3,
#         uids['uid3'])

#     def test_get_jobs_for_user_some_users_empty_jobs(self):
#         jobs_list_uid4 = api.get_jobs_for_user(uids['uid4'])
#         # Verify that the jobs_list for uid4 is empty       
#         self.assertFalse(len(jobs_list_uid4))
#         num_of_jobs_uid1 = 1
#         # Add one job to the tabfile uid1
#         test_jobs_uid1 = create_test_tab(num_of_jobs_uid1, uids['uid1'])
#         api.set_jobs(test_jobs_uid1, uids['uid1'])
#         jobs_list_uid4 = api.get_jobs_for_user(uids['uid4'])
#         # Verify that the jobs_list for uid4 is empty
#         self.assertFalse(len(jobs_list_uid4))

# #### TEST SET_JOBS([Job], uid) ####
#     def test_set_jobs_empty_jobs(self):
#         checkpoint1 = datetime.now()
#         num_of_jobs = 0
#         # Create a crontab with zero jobs
#         test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
#         api.set_jobs(test_jobs, uids['uid1'])
#         # Query metadata for the database file creation time
#         db_creation_time \
#         = datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
#         # We are comparing different orders of time, so offset by one second
#         new_time = \
#         db_creation_time.replace(second=db_creation_time.second + 1)
#         checkpoint2 = datetime.now()
#         checkpoint2 = checkpoint2.replace(second=checkpoint2.second + 1)
#         # Verify that the jobs have been set just now
#         self.assertTrue(new_time > checkpoint1 and new_time < checkpoint2)

#     def test_set_jobs_one_job(self):
#         checkpoint1 = datetime.now()
#         num_of_jobs = 1
#         # Create a crontab with one job
#         test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
#         api.set_jobs(test_jobs, uids['uid1'])
#         # Query metadata for the database file creation time
#         db_creation_time = \
#         datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
#         # We are comparing different orders of time, so offset by one second
#         new_time = \
#         db_creation_time.replace(second=db_creation_time.second + 1)
#         # Verify that the jobs have been set just now
#         checkpoint2 = datetime.now()
#         checkpoint2 = checkpoint2.replace(second=checkpoint2.second + 1)
#         # Verify that the jobs have been set just now
#         self.assertTrue(new_time > checkpoint1 and new_time < checkpoint2)

#     def test_set_jobs_many_jobs(self):
#         checkpoint1 = datetime.now()
#         num_of_jobs = 10
#         # Create a crontab with many jobs
#         test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
#         api.set_jobs(test_jobs, uids['uid1'])
#         # Query metadata for the database file creation time
#         db_creation_time = \
#         datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
#         # We are comparing different orders of time, so offset by one second
#         new_time = \
#         db_creation_time.replace(second=db_creation_time.second + 1)
#         # Verify that the jobs have been set just now
#         checkpoint2 = datetime.now()
#         checkpoint2 = checkpoint2.replace(second=checkpoint2.second + 1)
#         # Verify that the jobs have been set just now
#         self.assertTrue(new_time > checkpoint1 and new_time < checkpoint2)

# #### TEST SET_JOB_TIME(Job) ####
#     def test_set_job_time_one_job(self):
#         checkpoint1 = datetime.now()
#         num_of_jobs = 1
#         # Create a crontab with one job
#         test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
#         api.set_jobs(test_jobs, uids['uid1'])
#         # Pop the only job in the list to modify its time
#         job = test_jobs.pop()
#         api.set_job_time(job)
#         checkpoint2 = datetime.now()
#         # Verify that the job's last time run was updated correctly
#         self.assertTrue(job.last_time_run > checkpoint1 and
#         job.last_time_run < checkpoint2)

#     def test_set_job_time_random_job_from_many(self):
#         checkpoint1 = datetime.now()
#         num_of_jobs = 10
#         # Create a crontab with many jobs
#         test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
#         api.set_jobs(test_jobs, uids['uid1'])
#         # Pop a random job in list to modify its time
#         job = test_jobs.pop(random.randrange(len(test_jobs)))
#         api.set_job_time(job)
#         checkpoint2 = datetime.now()
#         # Verify that the job's last time run was updated correctly
#         self.assertTrue(job.last_time_run > checkpoint1 and
#         job.last_time_run < checkpoint2)

# #### TEST CREATE_WORKER() ####
#     def test_create_worker_one_worker(self):
#         checkpoint1 = datetime.now()
#         num_of_workers = 1
#         test_workers = []
#         # Create one worker and add them to a list for bookkeeping
#         test_workers.append(api.create_worker())
#         checkpoint2 = datetime.now()
#         current = 1
#         # Verify that the worker has been created just now
#         self.assertTrue(test_workers[0].heartbeat > checkpoint1 and
#         test_workers[0].heartbeat < checkpoint2)
#         current += 1

#     def test_create_worker_many_workers(self):
#         checkpoint1 = datetime.now()
#         num_of_workers = 10
#         test_workers = []
#         for job in range(num_of_workers):
#         	# Create many workers and add them to a list for bookkeeping
#             test_workers.append(api.create_worker())
#         checkpoint2 = datetime.now()
#         current = 1
#         for worker in test_workers:
#         	# Verify that the workers have been created just now
#             self.assertTrue(worker.heartbeat > checkpoint1 and
#             worker.heartbeat < checkpoint2)
#             current += 1

# #### TEST GET_WORKERS() ####
#     def test_get_workers_empty_workers(self):
#     	num_of_workers = 0
#     	workers_list = api.get_workers()
#     	# Verify that workers list is empty
#     	self.assertEqual(len(workers_list), num_of_workers)

#     def test_get_workers_one_worker(self):
#     	num_of_workers = 1
#         test_workers = []
#         # Create one worker and add them to a list for bookkeeping
#         test_workers.append(api.create_worker())
#     	workers_list = api.get_workers()
#         # Verify that the workers list contains exactly one worker
#     	self.assertEqual(len(workers_list), num_of_workers)
#     	# Verify that the information we get is the same as what was set
#         check_worker_fields(self, workers_list, test_workers)

#     def test_get_workers_many_workers(self):
#     	num_of_workers = 10
#         test_workers = []
#         for job in range(num_of_workers):
#         	# Create workers and add them to a list for bookkeeping
#             test_workers.append(api.create_worker())
#     	workers_list = api.get_workers()
#     	# Verify that the workers list contains the correct number of workers
#     	self.assertEqual(len(workers_list), num_of_workers)
#         check_worker_fields(self, workers_list, test_workers)

# #### TEST GET_NEXT_WORKER() ####
#     def test_get_next_worker_empty_workers(self):
#         # Try to get the next worker from an empty pool
#     	next_worker = api.get_next_worker()
#     	# Verify that the next worker does not exist
#     	self.assertEqual(next_worker, None)

#     def test_get_next_worker_one_worker(self):
#     	num_of_workers = 1
#     	test_workers, workers_list = [], []
#     	# Create one worker and add it to a list for bookkeeping
#     	test_workers.append(api.create_worker())
#     	workers_list.append(api.get_next_worker())
#     	# Verify that the workers list contains exactly one worker
#     	self.assertEqual(len(workers_list), num_of_workers)
#         # Verify that the information we get is the same as what was set
#     	check_worker_fields(self, workers_list, test_workers)

#     def test_get_next_worker_one_worker_many_requests(self):
#     	num_of_workers = 1
#     	num_of_requests = 10
#     	test_workers, workers_list = [], []
#     	# Create one worker and it to a list for bookkeeping
#     	test_workers.append(api.create_worker())
#         # Verify that the test workers list contains exactly one worker
#         self.assertEqual(len(test_workers), num_of_workers)
#     	for request in range(num_of_requests):
#     		# Get workers and add them to a list for
#             # comparison with list of test workers
#             workers_list.append(api.get_next_worker())
# 	    # Verify that the workers list contains
# 	    # as many workers as there were requests
#     	self.assertEqual(len(workers_list), num_of_requests)
#     	# Verify that the information we get is the same as what was set
#         check_worker_fields(self, workers_list, test_workers)

#     def test_get_next_worker_many_workers_more_requests(self):
#         num_of_workers = 10
#         num_of_requests = 12
#         test_workers, workers_list = [], []
#         for worker in range(num_of_workers):
#             # Create many workers and add them to a list for bookkeeping
#             test_workers.append(api.create_worker())
#         # Verify that the test workers list contains
#         # the correct number of workers
#         self.assertEqual(len(test_workers), num_of_workers)
#         for request in range(num_of_requests):
#             # Get more workers than available in the test workers list
#             # (popped workers are pushed to the end of the queue)
#             # and add them to a list for comparison
#             workers_list.append(api.get_next_worker())
#         # Verify that the workers list contains
#         # as many worker sas there were requests
#         self.assertEqual(len(workers_list), num_of_requests)
#         # Verify that the information we get is the same as what was set
#         check_worker_fields(self, workers_list, test_workers)

# #### TEST DESTORY_WORKER(Worker) ####
#     def test_destroy_worker_empty_workers(self):
#         test_workers = []
#         # Verify that we do not destroy nonexistent workers
#         with self.assertRaises(ValueError):
#             api.destroy_worker(test_workers)

#     def test_destroy_worker_one_worker(self):
#         test_workers = []
#         # Create one worker and add it to a list for bookkeeping
#         test_workers.append(api.create_worker())
#         # Kill the only worker in the list
#         api.destroy_worker(test_workers[0])
#         # Try to get a worker from an empty pool
#         next_worker = api.get_next_worker()
#         # Verify that the next worker does not exist
#         self.assertEqual(next_worker, None)

#     def test_destroy_worker_many_workers(self):
#         # Number of workers and floor(requests) + ceiling(requests) are equal 
#         num_of_workers = 9
#         # Automatic flooring care of Python
#         num_of_requests = num_of_workers/2
#         test_workers, workers_list = [], []
#         for worker in range(num_of_workers):
#             # Create many workers and add them to a list for bookkeeping
#             test_workers.append(api.create_worker())
#         # Kill the floor of half of the workers in the list
#         for request in range(num_of_requests):
#             api.destroy_worker(test_workers.pop())
#         workers_list = api.get_workers()
#         # Verify that the correct workers are still in the list
#         check_worker_fields(self, workers_list, test_workers)
#         # Kill the floor of half of the workers in the list
#         while test_workers:
#             api.destroy_worker(test_workers.pop())
#         # Try to get a worker from an empty pool
#         next_worker = api.get_next_worker()
#         # Verify that the next worker does not exist
#         self.assertEqual(next_worker, None)

#     def test_destroy_worker_many_workers_random_workers(self):
#         # Number of workers and floor(requests) + ceiling(requests) are equal 
#         num_of_workers = 9
#         # Leave one worker remaining for comparison at the end
#         num_of_requests = num_of_workers - 1
#         # Automatic flooring care of Python
#         test_workers, workers_list = [], []
#         for worker in range(num_of_workers):
#             # Create many workers and add them to a list for bookkeeping
#             test_workers.append(api.create_worker())
#         # Kill number of requests random worker in the list
#         for request in range(num_of_requests):
#             random_worker = random.randrange(len(test_workers))
#             api.destroy_worker(test_workers.pop(random_worker))
#         workers_list = api.get_workers()
#         # Verify that the workers list contains exactly one worker
#         self.assertEqual(len(workers_list), 1)
#         # Verify that the correct remaining worker is still in the list
#         check_worker_fields(self, workers_list, test_workers)

#### TEST UPDATE_HEARTBEAT(Worker) ####
    def test_update_heartbeat_empty_workers(self):
        test_workers = []
        # Verify that we do not update nonexistent workers
        with self.assertRaises(ValueError):
            api.update_heartbeat(test_workers)

    def test_update_heartbeat_deleted_worker(self):
        test_workers = []
        # Create a temporary worker in the test workers list
        to_be_deleted = test_workers.append(api.create_worker())
        # Destroy the only worker in the list
        api.destroy_worker(api.get_next_worker())
        # Verify that we do not update nonexistent workers
        with self.assertRaises(ValueError):
            api.update_heartbeat(to_be_deleted)

    def test_update_heartbeat_one_worker(self):
        test_workers, workers_list = [], []
        # Create one worker and it to a list for bookkeeping
        test_workers.append(api.create_worker())
        # Get the original heartbeat of the only worker
        previous_heartbeats = []
        previous_heartbeats.append(test_workers[0].heartbeat)
        # Old heartbeat is before checkpoint, new heartbeat should be after
        checkpoint1 = datetime.now()
        api.update_heartbeat(test_workers[0])
        workers_list = api.get_workers()
        checkpoint2 = datetime.now()
        # Verify that the heartbeat has been updated correctly and previous
        # heartbeat was not an unexpected value
        check_heartbeat_value(self, workers_list[0], previous_heartbeats,
        checkpoint1, checkpoint2, 0)

    def test_update_heartbeat_one_worker_many_requests(self):
        num_of_requests = 10
        test_workers, workers_list = [], []
        # Create many workers and them to a list for bookkeeping
        test_workers.append(api.create_worker())
        # Get the original heartbeat of the only worker
        previous_heartbeats = []
        previous_heartbeats.append(test_workers[0].heartbeat)
        checkpoint1 = datetime.now()
        for request in range(num_of_requests):
            api.update_heartbeat(test_workers[0])
            workers_list = api.get_workers()
            checkpoint2 = datetime.now()
            # Verify that the heartbeat has been updated correctly and previous
            # heartbeat was not an unexpected value
            check_heartbeat_value(self, workers_list[0], previous_heartbeats,
            checkpoint1, checkpoint2, 0)

    def test_update_heartbeat_many_workers_many_requests(self):
        num_of_workers = 10
        test_workers, workers_list= [], []
        previous_heartbeats = []
        # Create many workers and them to a list for bookkeeping
        for worker in range(num_of_workers):
            test_workers.append(api.create_worker())
        # Get the original heartbeat of each worker
        for worker in test_workers:
            previous_heartbeats.append(worker.heartbeat)
        checkpoint1 = datetime.now()
        for worker in test_workers:
            api.update_heartbeat(worker)
        workers_list = api.get_workers()
        checkpoint2 = datetime.now()
        # Verify that the heartbeats have been updated correctly and previous
        # heartbeats were not an unexpected value
        current = 0
        for worker in workers_list:
            check_heartbeat_value(self, worker, previous_heartbeats,
            checkpoint1, checkpoint2, current)
            current += 1

    def test_update_heartbeat_many_workers_random_worker(self):
        # Number of workers and floor(requests) + ceiling(requests) are equal 
        num_of_workers = 10
        test_workers, workers_list= [], []
        previous_heartbeats = []
        # Create many workers and them to a list for bookkeeping
        for worker in range(num_of_workers):
            test_workers.append(api.create_worker())
        # Get the original heartbeat of each worker
        checkpoint1 = datetime.now()
        for worker in test_workers:
            previous_heartbeats.append(worker.heartbeat)
            random_worker = random.randrange(num_of_workers)
        api.update_heartbeat(test_workers[random_worker])
        workers_list = api.get_workers()
        checkpoint2 = datetime.now()
        # Verify that the random worker's heartbeat has been updated correctly
        # and its previous heartbeat was not an unexpected value
        check_heartbeat_value(self, workers_list[random_worker], 
        previous_heartbeats, checkpoint1, checkpoint2, random_worker)

if __name__ == '__main__':
    unittest.main()

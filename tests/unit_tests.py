#!/usr/bin/python2

import unittest
import os
import random
import math
from datetime import datetime

from test_support_functions import create_test_tab, cleanup, uids, \
     check_job_fields, check_worker_fields, check_schedule_fields, \
     check_heartbeat_value
from megacron import api

api.FILE_NAME = './testdb.p'

class TestApiFunctions(unittest.TestCase):        

    def tearDown(self):
       cleanup()

#### TEST GET_JOBS() ####
    def test_get_jobs_empty_jobs(self):
        num_of_jobs = 0
        # Create a crontab with zero jobs
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        # Verify that the jobs list is empty
        self.assertEqual(len(jobs_list), num_of_jobs)
        # Verify that the information we get matches what was set
        check_job_fields(self, jobs_list, test_jobs, uids['uid1'])

    def test_get_jobs_one_job(self):
        num_of_jobs = 1
        # Create a crontab with one job
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        # Verify that the jobs list contains exactly one job
        self.assertEqual(len(jobs_list), num_of_jobs)
        # Verify that the information we get matches what was set
        check_job_fields(self, jobs_list, test_jobs, uids['uid1'])

    def test_get_jobs_many_jobs(self):
        num_of_jobs = 10
        # Create a crontab with many jobs
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        self.assertEqual(len(jobs_list), num_of_jobs)
        # Verify that the information we get matches what was set
        check_job_fields(self, jobs_list, test_jobs, uids['uid1'])

#### TEST GET_JOBS_FOR_USER(uid) ####
    def test_get_jobs_for_user_empty_jobs(self):
        num_of_jobs = 0
        # Create a crontab with zero jobs
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])
        # Verify that the jobs list for uid1 is empty
        self.assertFalse(len(jobs_list_uid1))

    def test_get_jobs_for_user_many_jobs(self):
        num_of_jobs = 10
        # Create a crontab with many jobs
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])
        # Verify that the jobs list for uid1
        # contains the correct number of jobs
        self.assertEqual(len(jobs_list_uid1), num_of_jobs)

    def test_get_jobs_for_user_some_users_some_jobs(self):
        num_of_jobs_uid1 = 1
        # Add one job to the tabfile for uid1
        test_jobs_uid1 = create_test_tab(num_of_jobs_uid1, uids['uid1'])
        api.set_jobs(test_jobs_uid1, uids['uid1'])
        jobs_list_uid1 = api.get_jobs_for_user(uids['uid1'])

        num_of_jobs_uid2 = 0
        # Add zero jobs to the tabfile for uid2
        test_jobs_uid2 = create_test_tab(num_of_jobs_uid2, uids['uid2'])
        api.set_jobs(test_jobs_uid2, uids['uid2'])
        jobs_list_uid2 = api.get_jobs_for_user(uids['uid2'])

        num_of_jobs_uid3 = 4
        # Add some jobs to the tabfile for uid3
        test_jobs_uid3 = create_test_tab(num_of_jobs_uid3, uids['uid3'])
        api.set_jobs(test_jobs_uid3, uids['uid3'])
        jobs_list_uid3 = api.get_jobs_for_user(uids['uid3'])

        # Verify that the jobs list for uid1 contains
        # the correct number of jobs
        self.assertEqual(len(jobs_list_uid1), num_of_jobs_uid1)
        # Verify that the jobs list for uid2 contains
        # the correct number of jobs
        self.assertEqual(len(jobs_list_uid2), num_of_jobs_uid2)
        # Verify that the jobs list for uid3 contains
        # the correct number of jobs
        self.assertEqual(len(jobs_list_uid3), num_of_jobs_uid3)
        # Verify that the information we get matches what was set
        check_job_fields(self, jobs_list_uid1, test_jobs_uid1, 
        uids['uid1'])
        # Verify that the information we get matches what was set
        check_job_fields(self, jobs_list_uid2, test_jobs_uid2,
        uids['uid2'])
        # Verify that the information we get matches what was set
        check_job_fields(self, jobs_list_uid3, test_jobs_uid3,
        uids['uid3'])

    def test_get_jobs_for_user_some_users_empty_jobs(self):
        jobs_list_uid4 = api.get_jobs_for_user(uids['uid4'])
        # Verify that the jobs_list for uid4 is empty       
        self.assertFalse(len(jobs_list_uid4))
        num_of_jobs_uid1 = 1
        # Add one job to the tabfile uid1
        test_jobs_uid1 = create_test_tab(num_of_jobs_uid1, uids['uid1'])
        api.set_jobs(test_jobs_uid1, uids['uid1'])
        jobs_list_uid4 = api.get_jobs_for_user(uids['uid4'])
        # Verify that the jobs_list for uid4 is empty
        self.assertFalse(len(jobs_list_uid4))

#### TEST SET_JOBS([Job], uid) ####
    def test_set_jobs_empty_jobs(self):
        checkpoint1 = datetime.now()
        num_of_jobs = 0
        # Create a crontab with zero jobs
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        # Query metadata for the database file creation time
        db_creation_time \
        = datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
        # We are comparing different orders of time, so offset by one second
        new_time = \
        db_creation_time.replace(second=db_creation_time.second + 1)
        checkpoint2 = datetime.now()
        checkpoint2 = checkpoint2.replace(second=checkpoint2.second + 1)
        # Verify that the jobs have been set just now
        self.assertTrue(new_time > checkpoint1 and new_time < checkpoint2)

    def test_set_jobs_one_job(self):
        checkpoint1 = datetime.now()
        num_of_jobs = 1
        # Create a crontab with one job
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        # Query metadata for the database file creation time
        db_creation_time = \
        datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
        # We are comparing different orders of time, so offset by one second
        new_time = \
        db_creation_time.replace(second=db_creation_time.second + 1)
        # Verify that the jobs have been set just now
        checkpoint2 = datetime.now()
        checkpoint2 = checkpoint2.replace(second=checkpoint2.second + 1)
        # Verify that the jobs have been set just now
        self.assertTrue(new_time > checkpoint1 and new_time < checkpoint2)

    def test_set_jobs_many_jobs(self):
        checkpoint1 = datetime.now()
        num_of_jobs = 10
        # Create a crontab with many jobs
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        # Query metadata for the database file creation time
        db_creation_time = \
        datetime.fromtimestamp(os.stat(api.FILE_NAME).st_mtime)
        # We are comparing different orders of time, so offset by one second
        new_time = \
        db_creation_time.replace(second=db_creation_time.second + 1)
        # Verify that the jobs have been set just now
        checkpoint2 = datetime.now()
        checkpoint2 = checkpoint2.replace(second=checkpoint2.second + 1)
        # Verify that the jobs have been set just now
        self.assertTrue(new_time > checkpoint1 and new_time < checkpoint2)

#### TEST SET_JOB_TIME(Job) ####
    def test_set_job_time_one_job(self):
        checkpoint1 = datetime.now()
        num_of_jobs = 1
        # Create a crontab with one job
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        # Pop the only job in the list to modify its time
        job = test_jobs.pop()
        api.set_job_time(job)
        checkpoint2 = datetime.now()
        # Verify that the job's last time run was updated correctly
        self.assertTrue(job.last_time_run > checkpoint1 and
        job.last_time_run < checkpoint2)

    def test_set_job_time_random_job_from_many(self):
        checkpoint1 = datetime.now()
        num_of_jobs = 10
        # Create a crontab with many jobs
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        # Pop a random job in list to modify its time
        job = test_jobs.pop(random.randrange(len(test_jobs)))
        api.set_job_time(job)
        checkpoint2 = datetime.now()
        # Verify that the job's last time run was updated correctly
        self.assertTrue(job.last_time_run > checkpoint1 and
        job.last_time_run < checkpoint2)

#### TEST CREATE_WORKER() ####
    def test_create_worker_one_worker(self):
        checkpoint1 = datetime.now()
        test_workers = []
        # Create one worker and add them to a list for bookkeeping
        test_workers.append(api.create_worker())
        checkpoint2 = datetime.now()
        current = 1
        # Verify that the worker has been created just now
        self.assertTrue(test_workers[0].heartbeat > checkpoint1 and
        test_workers[0].heartbeat < checkpoint2)
        current += 1

    def test_create_worker_many_workers(self):
        checkpoint1 = datetime.now()
        num_of_workers = 10
        test_workers = []
        for job in range(num_of_workers):
        	# Create many workers and add them to a list for bookkeeping
            test_workers.append(api.create_worker())
        checkpoint2 = datetime.now()
        current = 1
        for worker in test_workers:
        	# Verify that the workers have been created just now
            self.assertTrue(worker.heartbeat > checkpoint1 and
            worker.heartbeat < checkpoint2)
            current += 1

#### TEST GET_WORKERS() ####
    def test_get_workers_empty_workers(self):
    	num_of_workers = 0
    	workers_list = api.get_workers()
    	# Verify that workers list is empty
    	self.assertFalse(len(workers_list))

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
        for job in range(num_of_workers):
        	# Create workers and add them to a list for bookkeeping
            test_workers.append(api.create_worker())
    	workers_list = api.get_workers()
    	# Verify that the workers list contains the correct number of workers
    	self.assertEqual(len(workers_list), num_of_workers)
        check_worker_fields(self, workers_list, test_workers)

#### TEST GET_NEXT_WORKER() ####
    def test_get_next_worker_empty_workers(self):
        # Try to get the next worker from an empty pool
    	next_worker = api.get_next_worker()
    	# Verify that the next worker does not exist
    	self.assertEqual(next_worker, None)

    def test_get_next_worker_one_worker(self):
    	num_of_workers = 1
    	test_workers = []
    	# Create one worker and add it to a list for bookkeeping
    	test_workers.append(api.create_worker())
        workers_list = []
    	workers_list.append(api.get_next_worker())
    	# Verify that the workers list contains exactly one worker
    	self.assertEqual(len(workers_list), num_of_workers)
        # Verify that the information we get is the same as what was set
    	check_worker_fields(self, workers_list, test_workers)

    def test_get_next_worker_one_worker_many_requests(self):
    	num_of_workers = 1
    	num_of_requests = 10
    	test_workers = []
    	# Create one worker and it to a list for bookkeeping
    	test_workers.append(api.create_worker())
        # Verify that the test workers contains exactly one worker
        self.assertEqual(len(test_workers), num_of_workers)
        workers_list = []
    	for request in range(num_of_requests):
    		# Get workers and add them to a list for
          # comparison with list of test workers
            workers_list.append(api.get_next_worker())
	    # Verify that the workers list contains
	    # as many workers as there were requests
    	self.assertEqual(len(workers_list), num_of_requests)
    	# Verify that the information we get is the same as what was set
        check_worker_fields(self, workers_list, test_workers)

    def test_get_next_worker_many_workers_more_requests(self):
        num_of_workers = 10
        num_of_requests = 12
        test_workers = []
        for worker in range(num_of_workers):
            # Create many workers and add them to a list for bookkeeping
            test_workers.append(api.create_worker())
        # Verify that the test workers contains
        # the correct number of workers
        self.assertEqual(len(test_workers), num_of_workers)
        workers_list = []
        for request in range(num_of_requests):
            # Get more workers than available in the test workers
            # (popped workers are pushed to the end of the queue)
            # and add them to a list for comparison
            workers_list.append(api.get_next_worker())
        # Verify that the workers list contains
        # as many workers as there were requests
        self.assertEqual(len(workers_list), num_of_requests)
        # Verify that the information we get is the same as what was set
        check_worker_fields(self, workers_list, test_workers)

#### TEST DESTORY_WORKER(Worker) ####
    def test_destroy_worker_empty_workers(self):
        test_workers = []
        # Verify that we do not destroy nonexistent workers
        with self.assertRaises(ValueError):
            api.destroy_worker(test_workers)

    def test_destroy_worker_one_worker(self):
        test_workers = []
        # Create one worker and add it to a list for bookkeeping
        test_workers.append(api.create_worker())
        # Kill the only worker in the list
        api.destroy_worker(test_workers[0])
        # Try to get a worker from an empty pool
        next_worker = api.get_next_worker()
        # Verify that the next worker does not exist
        self.assertEqual(next_worker, None)

    def test_destroy_worker_many_workers(self):
        # Number of workers and floor(requests) + ceiling(requests) are equal 
        num_of_workers = 9
        # Automatic flooring care of Python
        num_of_requests = num_of_workers/2
        test_workers = []
        for worker in range(num_of_workers):
            # Create many workers and add them to a list for bookkeeping
            test_workers.append(api.create_worker())
        # Kill the floor of half of the workers in the list
        for request in range(num_of_requests):
            api.destroy_worker(test_workers.pop())
        workers_list = []
        workers_list = api.get_workers()
        # Verify that the correct workers are still in the list
        check_worker_fields(self, workers_list, test_workers)
        # Remove the rest of the test workers
        while test_workers:
            api.destroy_worker(test_workers.pop())
        # Try to get a worker from an empty pool
        next_worker = api.get_next_worker()
        # Verify that the next worker does not exist
        self.assertEqual(next_worker, None)

    def test_destroy_worker_many_workers_random_workers(self):
        # Number of workers and floor(requests) + ceiling(requests) are equal 
        num_of_workers = 9
        # Leave one worker remaining for comparison at the end
        num_of_requests = num_of_workers - 1
        # Automatic flooring care of Python
        test_workers = []
        for worker in range(num_of_workers):
            # Create many workers and add them to a list for bookkeeping
            test_workers.append(api.create_worker())
        # Kill number of requests random worker in the list
        for request in range(num_of_requests):
            random_worker = random.randrange(len(test_workers))
            api.destroy_worker(test_workers.pop(random_worker))
        workers_list = []
        workers_list = api.get_workers()
        # Verify that the workers list contains exactly one worker
        self.assertEqual(len(workers_list), 1)
        # Verify that the correct remaining worker is still in the list
        check_worker_fields(self, workers_list, test_workers)

#### TEST UPDATE_HEARTBEAT(Worker) ####
    def test_update_heartbeat_empty_workers(self):
        test_workers = []
        # Verify that we do not update nonexistent workers
        with self.assertRaises(ValueError):
            api.update_heartbeat(test_workers)

    def test_update_heartbeat_deleted_worker(self):
        test_workers = []
        # Create a temporary worker in the test workers
        to_be_deleted = test_workers.append(api.create_worker())
        # Destroy the only worker in the list
        api.destroy_worker(api.get_next_worker())
        # Verify that we do not update nonexistent workers
        with self.assertRaises(ValueError):
            api.update_heartbeat(to_be_deleted)

    def test_update_heartbeat_one_worker(self):
        test_workers = []
        # Create one worker and it to a list for bookkeeping
        test_workers.append(api.create_worker())
        # Get the original heartbeat of the only worker
        previous_heartbeats = []
        previous_heartbeats.append(test_workers[0].heartbeat)
        # Old heartbeat is before checkpoint, new heartbeat should be after
        checkpoint1 = datetime.now()
        api.update_heartbeat(test_workers[0])
        workers_list = []
        workers_list = api.get_workers()
        checkpoint2 = datetime.now()
        # Verify that the heartbeat has been updated correctly and previous
        # heartbeat was not an unexpected value
        check_heartbeat_value(self, workers_list[0], previous_heartbeats,
        checkpoint1, checkpoint2, 0)

    def test_update_heartbeat_one_worker_many_requests(self):
        num_of_requests = 10
        test_workers = []
        # Create many workers and them to a list for bookkeeping
        test_workers.append(api.create_worker())
        # Get the original heartbeat of the only worker
        previous_heartbeats = []
        previous_heartbeats.append(test_workers[0].heartbeat)
        checkpoint1 = datetime.now()
        workers_list = []
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
        test_workers = []
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
        workers_list = []
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
        test_workers = []
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
        workers_list = []
        workers_list = api.get_workers()
        checkpoint2 = datetime.now()
        # Verify that the random worker's heartbeat has been updated correctly
        # and its previous heartbeat was not an unexpected value
        check_heartbeat_value(self, workers_list[random_worker], 
        previous_heartbeats, checkpoint1, checkpoint2, random_worker)

#### TEST ADD_SCHEDULES([Schedule]) ####
    def test_add_schedules_one_job_one_schedule(self):
        num_of_jobs = 1
        num_of_schedules = num_of_jobs
        # Create a crontab with one job
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        test_workers = []
        # Create one worker and add them to a list for bookkeeping
        test_workers.append(api.create_worker())
        # Create a schedule for the only job
        test_schedules = []
        test_schedules.append(api.Schedule(datetime.now(), test_jobs[0], 
        test_workers[0]))
        api.add_schedules(test_schedules)
        schedules_list = api.get_schedules(test_workers[0])
        # Verify that the schedules list contains exactly one schedule
        self.assertEqual(len(schedules_list), num_of_schedules)

    def test_add_schedules_one_job_many_schedules(self):
        num_of_jobs = 1
        num_of_schedules = 10
        # Create a crontab with one job
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        test_workers = []
        # Create one worker and add them to a list for bookkeeping
        test_workers.append(api.create_worker())
        # Create many schedules for the only job
        test_schedules = []
        for schedule in range(num_of_schedules):
            test_schedules.append(api.Schedule(datetime.now(), test_jobs[0], 
            test_workers[0]))
        api.add_schedules(test_schedules)
        schedules_list = api.get_schedules(test_workers[0])
        # Verify that the schedules list contains exactly one schedule
        self.assertEqual(len(schedules_list), num_of_schedules)

    def test_add_schedules_many_jobs_many_schedules(self):
        num_of_jobs = 10
        num_of_schedules = num_of_jobs
        # Create a crontab with many jobs
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        test_workers = []
        # Create one worker and add them to a list for bookkeeping
        test_workers.append(api.create_worker())
        # Create many schedules for the only job
        test_schedules = []
        for schedule in range(num_of_schedules):
            test_schedules.append(api.Schedule(datetime.now(), test_jobs[0], 
            test_workers[0]))
        api.add_schedules(test_schedules)
        schedules_list = api.get_schedules(test_workers[0])
        # Verify that the schedules list contains exactly one schedule
        self.assertEqual(len(schedules_list), num_of_schedules)

#### TEST GET_SCHEDULES(Worker) ####
    def test_get_schedules_one_worker_one_schedule(self):
        num_of_jobs = 1
        num_of_schedules = num_of_jobs
        # Create a crontab with one job
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        test_workers = []
        # Create one worker and add them to a list for bookkeeping
        test_workers.append(api.create_worker())
        # Create a schedule for the only job
        test_schedules = []
        test_schedules.append(api.Schedule(datetime.now(), test_jobs[0], 
        test_workers[0]))
        api.add_schedules(test_schedules)
        schedules_list = api.get_schedules(test_workers[0])
        # Verify that the information we get matches what was set
        check_schedule_fields(self, schedules_list, test_schedules)


    def test_get_schedules_one_worker_many_schedules(self):
        num_of_jobs = 10
        num_of_schedules = num_of_jobs
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        test_workers = []
        # Create one worker and add them to a list for bookkeeping
        test_workers.append(api.create_worker())
        # Create a schedule for the only job
        test_schedules = []
        for job in range(num_of_jobs):
            test_schedules.append(api.Schedule(datetime.now(), test_jobs[job], 
            test_workers[0]))
        api.add_schedules(test_schedules)
        schedules_list = api.get_schedules(test_workers[0])
        # Verify that the information we get matches what was set
        check_schedule_fields(self, schedules_list, test_schedules)

    def test_get_schedules_many_workers_one_schedule(self):
        num_of_jobs = 1
        num_of_schedules = num_of_jobs
        num_of_workers = 10
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        test_workers = []
        # Create many workers and add them to a list for bookkeeping
        for worker in range(num_of_workers):
            test_workers.append(api.create_worker())
        # Create a schedule belonging to each worker containing the only job
        test_schedules = []
        for worker in test_workers:
            test_schedules.append(api.Schedule(datetime.now(), test_jobs[0], 
            worker))
        api.add_schedules(test_schedules)
        # Aggregate each worker's schedules into a single list for comparison
        # with test schedules
        schedules_for_workers = []
        for worker in test_workers:
            schedules_list = api.get_schedules(worker)
            schedules_for_workers.extend(schedules_list)
        # Verify that the information we get matches what was set
        check_schedule_fields(self, schedules_for_workers, 
        test_schedules)

    def test_get_schedules_many_workers_many_schedules(self):
        num_of_jobs = 10
        num_of_schedules = num_of_jobs
        num_of_workers = num_of_schedules
        num_of_workers = 10
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        test_workers = []
        # Create many workers and add them to a list for bookkeeping
        for worker in range(num_of_workers):
            test_workers.append(api.create_worker())
        # Create a schedule belonging to each worker representing the only job
        test_schedules = []
        for worker in test_workers:
        	for job in jobs_list:
                    test_schedules.append(api.Schedule(datetime.now(), 
                    job, worker))
        api.add_schedules(test_schedules)
        # Aggregate each worker's schedules into a single list for comparison
        # with test schedules
        schedules_for_workers = []
        for worker in test_workers:
            schedules_list = api.get_schedules(worker)
            schedules_for_workers.extend(schedules_list)
        # Verify that the information we get matches what was set
        check_schedule_fields(self, schedules_for_workers, 
        test_schedules)

#### TEST DESTORY_WORKER(Worker) ####
    def test_remove_schedule_empty_schedules(self):
        test_schedules = []
        # Verify that we do not destroy nonexistent workers
        with self.assertRaises(ValueError):
            api.destroy_worker(test_schedules)

    def test_remove_schedule_one_schedule(self):
        num_of_jobs = 1
        num_of_schedules = num_of_jobs
        # Create a crontab with one job
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        test_workers = []
        # Create one worker and add them to a list for bookkeeping
        test_workers.append(api.create_worker())
        # Create a schedule for the only job
        test_schedules = []
        test_schedules.append(api.Schedule(datetime.now(), test_jobs[0], 
        test_workers[0]))
        api.add_schedules(test_schedules)
        # Kill the only schedule in the list
        api.remove_schedule(test_schedules[0])
        schedules_list = api.get_schedules(test_workers[0])
        # Verify that the schedules list is empty
        self.assertFalse(len(schedules_list))

    def test_remove_schedule_many_schedules(self):
        # Number of jobs and floor(requests) + ceiling(requests) are equal 
        num_of_jobs = 9
        num_of_schedules = num_of_jobs
        # Automatic flooring care of Python
        num_of_requests = num_of_jobs/2 
        # Create a crontab with many jobs
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        test_workers = []
        # Create one worker and add them to a list for bookkeeping
        test_workers.append(api.create_worker())
        # Create a schedule for many jobs
        test_schedules = []
        for schedule in range(num_of_schedules):
            test_schedules.append(api.Schedule(datetime.now(),
            test_jobs[schedule], test_workers[0]))
        api.add_schedules(test_schedules)
        # Kill the floor of half of the workers in the list
        for request in range(num_of_requests):
            api.remove_schedule(test_schedules.pop())
        schedules_list = api.get_schedules(test_workers[0])
        # Verify that the correct remaining schedules are still in the list
        check_schedule_fields(self, schedules_list, test_schedules)
        # Remove all remaining test schedules
        while test_schedules:
            api.remove_schedule(test_schedules.pop())
        # Try to get schedules from an empty pool
        schedules_list = api.get_schedules(test_workers[0])
        # Verify that the next worker does not exist
        self.assertFalse(len(schedules_list))

    def test_destroy_schedules_many_schedules_random_schedules(self):
        # Number of jobs and floor(requests) + ceiling(requests) are equal 
        num_of_jobs = 9
        num_of_schedules = num_of_jobs
        # Leave one schedule remaining for comparison at the end
        num_of_requests = num_of_jobs - 1
        # Create a crontab with many jobs
        test_jobs = create_test_tab(num_of_jobs, uids['uid1'])
        api.set_jobs(test_jobs, uids['uid1'])
        jobs_list = api.get_jobs()
        test_workers = []
        # Create one worker and add them to a list for bookkeeping
        test_workers.append(api.create_worker())
        test_schedules = []
        for schedule in range(num_of_schedules):
            test_schedules.append(api.Schedule(datetime.now(),
            test_jobs[schedule], test_workers[0]))
        api.add_schedules(test_schedules)
        # Kill number of requests random schedules in the list
        for request in range(num_of_requests):
            random_schedule = random.randrange(len(test_schedules))
            api.remove_schedule(test_schedules.pop(random_schedule))
        schedules_list = []
        schedules_list = api.get_schedules(test_workers[0])
        # Verify that the schedules list contains exactly one schedule
        self.assertEqual(len(schedules_list), 1)
        # Verify that the correct remaining schedule is still in the list
        check_schedule_fields(self, schedules_list, test_schedules)

if __name__ == '__main__':
    unittest.main()

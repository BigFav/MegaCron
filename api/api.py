#!/usr/bin/python

import sys
import pickle
import os
import fcntl

from datetime import datetime
from collections import deque

sys.path.append("..")

FILE_NAME = "../db.p"


class Job:
    def __init__(self, interval, command, user_id, last_time_run, _id=None):
        self.interval = interval
        self.command = command
        self.user_id = user_id
        self.last_time_run = last_time_run
        self._id = _id

    def __eq__(self, other):
        return self._id == other._id


class Schedule:
    def __init__(self, time_to_run, job, worker, _id=None):
        self.time_to_run = time_to_run
        self.job = job
        self.worker = worker
        self._id = _id

    def __eq__(self, other):
        return self._id == other._id


class Worker:
    def __init__(self, heartbeat, _id=None):
        self.heartbeat = heartbeat
        self._id = _id

    def __eq__(self, other):
        return self._id == other._id


def get_jobs():
    return _read_file()['jobs']


def get_jobs_for_user(user_id):
    jobs = _read_file()['jobs']
    return [job for job in jobs if job.user_id == user_id]


def set_jobs(jobs, user_id):
    file = _read_file()

    # Give them an id if they don't already have one
    for job in jobs:
        if job._id is None:
            job._id = file['next_job_id']
            file['next_job_id'] += 1

    file['jobs'] = [job for job in file['jobs'] if job.user_id != user_id]
    file['jobs'].extend(jobs)

    _write_file(file)


def set_job_fun(file, job):
    for f_job in file['jobs']:
        if f_job._id == job._id:
            f_job.last_time_run = job.last_time_run
            return


def set_job_time(job):
    _rw_file_l(set_job_fun, job)


def get_schedules(worker):
    schedules = _read_file_l()['schedules']
    return [schedule for schedule in schedules if schedule.worker == worker]


def add_schedules_fun(file, schedules):
    # Give them an id if they don't already have one
    for schedule in schedules:
        if schedule._id is None:
            schedule._id = file['next_schedule_id']
            file['next_schedule_id'] += 1

    file['schedules'].extend(schedules)


def add_schedules(schedules):
    _rw_file_l(add_schedules_fun, schedules)


def add_schedule_fun(file, schedule):
    file['schedules'].append(schedule)


def add_schedule(schedule):
    _rw_file_l(add_schedule_fun, schedule)


def remove_schedule_fun(file, schedule):
    file['schedules'].remove(schedule)


def remove_schedule(schedule):
    _rw_file_l(remove_schedule_fun, schedule)


def get_heartbeat(worker):
    workers = _read_file()['workers']
    for w in workers:
        if w == worker:
            return w
            break

    return None


def update_heartbeat(worker):
    file = _read_file()
    for w in file['workers']:
        if w == worker:
            w.heartbeat = datetime.now()
            break

    _write_file(file)


def get_next_worker():
    file = _read_file()

    workers = file['workers']
    if len(workers) == 0:
        return None

    next_worker = workers.popleft()
    workers.append(next_worker)

    _write_file(file)
    return next_worker


def get_workers():
    return _read_file_l()['workers']


def create_worker_fun(file, null):
    id = file['next_worker_id']
    worker = Worker(datetime.now(), id)
    file['workers'].append(worker)
    file['next_worker_id'] += 1

    return worker


def create_worker():
    return _rw_file_l(create_worker_fun, "")


def destroy_worker_fun(file, worker):
    file['workers'].remove(worker)


def destroy_worker(worker):
    _rw_file_l(destroy_worker_fun, worker)


def _read_file():
    try:
        with open(FILE_NAME, "rb") as file:
            return pickle.load(file)
    except IOError:
        return {
            'jobs': [],
            'schedules': [],
            'workers': deque(),
            'next_job_id': 1,
            'next_schedule_id': 1,
            'next_worker_id': 1
        }


def _write_file(data):
    with open(FILE_NAME+'~', "wb") as file:
        pickle.dump(data, file)
    os.rename(FILE_NAME+'~', FILE_NAME)


def _read_file_l():
    try:
        with open(FILE_NAME, "rb") as file:
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)
            load = pickle.load(file)
            fcntl.flock(file.fileno(), fcntl.LOCK_UN)
        return load
    except IOError:
        return {
            'jobs': [],
            'schedules': [],
            'workers': deque(),
            'next_job_id': 1,
            'next_schedule_id': 1,
            'next_worker_id': 1
        }


def _write_file_l(data):
    with open(FILE_NAME, "wb") as file:
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        pickle.dump(data, file)
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)


def _rw_file_l(f, data):
    with open(FILE_NAME, "rb+") as fd:
        fcntl.flock(fd.fileno(), fcntl.LOCK_EX)
        file = pickle.load(fd)

        ret = f(file, data)

        fd.seek(0)
        pickle.dump(file, fd)
        fcntl.flock(fd.fileno(), fcntl.LOCK_UN)

    return ret

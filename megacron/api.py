import pickle
import os
import fcntl
import errno
from datetime import datetime
from collections import deque

from megacron import config

FILE_NAME = config.get_option("Database", "shared_filesystem_path")


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
    with OpenFileLocked() as file:
        return file['jobs']


def get_jobs_for_user(user_id):
    with OpenFileLocked() as file:
        return [j for j in file['jobs'] if j.user_id == user_id]


def set_jobs(jobs, user_id):
    with OpenFileLocked(write=True) as file:
        # Give them an id if they don't already have one
        for job in jobs:
            if job._id is None:
                job._id = file['next_job_id']
                file['next_job_id'] += 1

        file['jobs'] = [j for j in file['jobs'] if j.user_id != user_id]
        file['jobs'].extend(jobs)


def set_job_time(job):
    with OpenFileLocked(write=True) as file:
        for f_job in file['jobs']:
            if f_job._id == job._id:
                f_job.last_time_run = job.last_time_run
                return


def get_schedules(worker):
    with OpenFileLocked() as file:
        return [s for s in file['schedules'] if s.worker == worker]


def add_schedules(schedules):
    with OpenFileLocked(write=True) as file:
        # Give them an id if they don't already have one
        for schedule in schedules:
            if schedule._id is None:
                schedule._id = file['next_schedule_id']
                file['next_schedule_id'] += 1

        file['schedules'].extend(schedules)


def add_schedule(schedule):
    with OpenFileLocked(write=True) as file:
        file['schedules'].append(schedule)


def remove_schedule(schedule):
    with OpenFileLocked(write=True) as file:
        file['schedules'].remove(schedule)


def get_heartbeat(worker):
    with OpenFileLocked() as file:
        for w in file['workers']:
            if w == worker:
                return w
                break

    return None


def update_heartbeat(worker):
    with OpenFileLocked(write=True) as file:
        for w in file['workers']:
            if w == worker:
                w.heartbeat = datetime.now()
                break


def get_next_worker():
    with OpenFileLocked(write=True) as file:
        workers = file['workers']
        if len(workers) == 0:
            return None

        next_worker = workers.popleft()
        workers.append(next_worker)

    return next_worker


def get_workers():
    with OpenFileLocked() as file:
        return file['workers']


def create_worker():
    worker = Worker(datetime.now(), id)

    with OpenFileLocked(write=True) as file:
        worker._id = file['next_worker_id']
        file['workers'].append(worker)
        file['next_worker_id'] += 1

    return worker


def destroy_worker(worker):
    with OpenFileLocked(write=True) as file:
        file['workers'].remove(worker)


class OpenFileLocked:
    def __init__(self, write=False):
        self._write = write

    def __enter__(self):
        # Create directory if it doesn't exist
        dir_name = os.path.dirname(FILE_NAME)
        try:
            os.makedirs(dir_name)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        # Open file with a lock and create it if it doesn't exist
        flag = os.O_RDWR if self._write is True else os.O_RDONLY
        mode = "rb+" if self._write is True else "rb"
        self._file = os.fdopen(os.open(FILE_NAME, os.O_CREAT | flag), mode)

        # Acquire a file lock
        op = fcntl.LOCK_EX if self._write is True else fcntl.LOCK_SH
        fcntl.flock(self._file.fileno(), op)

        try:
            self.data = pickle.load(self._file)
        except EOFError:
            self.data = {
                'jobs': [],
                'schedules': [],
                'workers': deque(),
                'next_job_id': 1,
                'next_schedule_id': 1,
                'next_worker_id': 1
            }

        if self._write is False:
            self._file.close()

        return self.data

    def __exit__(self, type, value, traceback):
        if self._write is True:
            self._file.truncate()
            self._file.seek(0)
            pickle.dump(self.data, self._file, protocol=2)
            self._file.close()

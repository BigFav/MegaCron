import sys
from datetime import datetime

from megacron import api


def get_worker_status():
    L = len(api.get_workers())
    if (L == 1):
        print "1 worker is up"
    else:
        print "%d workers are up" % L


def get_num_jobs():
    L = len(api.get_jobs())
    if (L == 1):
        print "1 job in queue"
    else:
        print "%d jobs in queue" % L


def get_next_schedule_time():
    now = datetime.now()
    comp = datetime.max
    for worker in api.get_workers():
        for schedule in api.get_schedules(worker):
            if (comp > schedule.time_to_run > now):
                comp = schedule.time_to_run
    print "The next job will be ran at " + comp.strftime("%d %B %Y %I:%M%p")


def get_num_users():
    users = set()
    for job in api.get_jobs():
        users.add(jobs.user_id)
    L = len(users)
    if (L == 1):
        print "1 user has a job"
    else:
        print "%d users have jobs" % L


def get_num_schedules():
    sum = 0
    for worker in api.get_workers():
        sum += len(api.get_schedules(worker))
    if (sum == 1):
        print "There is 1 schedule"
    else:
        print "There are %d schedules" % sum


def main():
    get_worker_status()
    get_num_jobs()
    get_num_schedules()
    get_next_schedule_time()
    get_num_users()

import sys
from datetime import datetime

from megacron import API

def get_worker_status():
    L = len(API.get_workers())
    if (L == 1):
        print "1 worker is up"
    else:
        print "%d workers are up" % L
        
def get_num_jobs():
    L = len(API.get_jobs())
    if (L == 1):
        print "1 job in queue"
    else:
        print "%d jobs in queue" % L
        
def get_next_schedule_time():
    now = datetime.now()
    comp = datetime.max
    for worker in API.get_workers():
        for schedule in API.get_schedules(worker):
            if (schedule.time_to_run < comp and schedule.time_to_run > now):
                comp = schedule.time_to_run
    print "The next job will be ran at " + comp.strftime("%d %B %Y %I:%M%p")
    
def get_num_users():
    users = set()
    for job in API.get_jobs():
        users.add(jobs.user_id)
    L = len(users)
    if (L == 1):
        print "1 user has a job"
    else:
        print "%d users have jobs" % L

def get_num_schedules():
    sum = 0
    for worker in API.get_workers():
        sum += len(API.get_schedules(worker)):
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

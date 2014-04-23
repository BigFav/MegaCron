import sys
from datetime import datetime

from megacron import api

import argparse


def get_worker_status():
    L = len(api.get_workers())
    if L == 1:
        print("1 worker is up")
    else:
        print("%d workers are up" % L)


def get_num_jobs():
    L = len(api.get_jobs())
    if L == 1:
        print("1 job in queue")
    else:
        print("%d jobs in queue" % L)


def get_next_schedule_time():
    now = datetime.now()
    comp = datetime.max
    for worker in api.get_workers():
        for schedule in api.get_schedules(worker):
            if comp > schedule.time_to_run > now:
                comp = schedule.time_to_run
    if comp != datetime.max:
        print("The next job will run at " + comp.strftime("%d %B %Y %I:%M%p"))
    else:
        print("No scheduled jobs to run")


def get_num_users():
    users = set()
    for job in api.get_jobs():
        users.add(job.user_id)
    L = len(users)
    if L == 1:
        print("1 user has a job")
    else:
        print("%d users have jobs" % L)


def get_num_schedules():
    sum = 0
    for worker in api.get_workers():
        sum += len(api.get_schedules(worker))
    if sum == 1:
        print("There is 1 schedule")
    else:
        print("There are %d schedules" % sum)


def main():
    parser = argparse.ArgumentParser(description='Provides stats for MegaCron')
    parser.add_argument("-ws", "--workerstatus", help="show worker status",
                        action="store_true")
    parser.add_argument("-nj", "--numjobs", help="show number of jobs",
                        action="store_true")
    parser.add_argument("-ns", "--numscheds", help="show number of schedules",
                        action="store_true")
    parser.add_argument("-xs", "--nextsched",
                        help="show next scheduled job time",
                        action="store_true")
    parser.add_argument("-u", "--numusers",
                        help="show number of users with jobs",
                        action="store_true")
    parser.add_argument("-a", "--all", help="show all status options",
                        action="store_true")
    args = parser.parse_args()
    if args.all or args.workerstatus:
        get_worker_status()
    if args.all or args.numjobs:
        get_num_jobs()
    if args.all or args.numscheds:
        get_num_schedules()
    if args.all or args.nextsched:
        get_next_schedule_time()
    if args.all or args.numusers:
        get_num_users()

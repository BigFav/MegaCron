#!/usr/bin/python

import sys
sys.path.append("../API")

from crontab import CronTab
from croniter import croniter
from datetime import datetime
from datetime import timedelta
from operator import attrgetter
import time
import sched
import API

SCHEDULER_UPDATE_INTERVAL = timedelta(seconds=15)
WORKER_HEARTBEAT_TIMEOUT = timedelta(seconds=20)

def sortSchedules (schedules):

	return sorted(schedules, key=attrgetter('timeToRun'))


def createSchedules(events):

	schedules = []

	for job in API.getJobs():
		
		#Adding Schedules for jobs within SCHEDULER_UPDATE_INTERVAL
		cmd = CronTab(tab="""%s %s""" % (job.interval, job.command))		#these two lines
		command = cmd.crons.pop()
		cmd_sch = command.schedule(date_from = datetime.now())			#allow us to obtain next timeToRun
	
		nxt = cmd_sch.get_next()
		while (nxt - datetime.now()) < SCHEDULER_UPDATE_INTERVAL:
                    job.lastTimeRun = nxt

                    worker = API.getNextWorker()
                    if not worker:
                        break

		    schedule = API.Schedule(nxt, job, worker)
		    schedules.append(schedule)
                    API.setJobTime(job)
		    nxt = cmd_sch.get_next()

        API.addSchedules(sortSchedules(schedules))
        events.enter(SCHEDULER_UPDATE_INTERVAL.total_seconds(), 1, createSchedules, (events,))

def checkWorkerHeartbeat(events):
    for worker in API.getWorkers():
        if (datetime.now() - worker.heartbeat) > WORKER_HEARTBEAT_TIMEOUT:
            for schedule in API.getSchedules(worker):
                schedule.worker = API.getNextWorker()

            API.destroyWorker(worker)

    events.enter(WORKER_HEARTBEAT_TIMEOUT.total_seconds(), 1, checkWorkerHeartbeat, (events,))

events = sched.scheduler(time.time, time.sleep)

while True:
    createSchedules(events)
    checkWorkerHeartbeat(events)
    events.run()


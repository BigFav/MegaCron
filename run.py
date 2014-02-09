#!/usr/local/python

from crontab import CronTab
from croniter import croniter
from datetime import datetime
from datetime import timedelta
import time
import API

SCHEDULER_UPDATE_INTERVAL = timedelta(seconds=15).total_seconds()

def sortSchedules (schedules):

	schedules.sort(schedules.sort(key=lambda schedule: schedule.timeToRun, reverse=False))

	return schedules


def jobs2Schedules (jobs):

	schedules = []

	while (len(jobs) > 0):
		
		job = jobs.pop()
		print job.lastTimeRun
		if job.lastTimeRun < datetime.now():
			cmd = CronTab(tab="%s %s" % (job.interval, job.command))		#these two lines
			command = cmd.crons.pop()
			cmd_sch = command.schedule(date_from = datetime.now())			#allow us to obtain next timeToRun
			
			next = cmd_sch.get_next()
			API.scheduleJob(job, next)
			print next
			schedule = API.Schedule(next, job, worker=None)
			schedules.append(schedule)

	return schedules


while True:

	jobs = API.getJobs()
	
	schedules = sortSchedules(jobs2Schedules(jobs))

	workers = API.getWorkers()
	worker = workers.pop()
	
	for schedule in schedules:

		schedule.worker = worker

	API.addSchedules(schedules)

 	time.sleep(SCHEDULER_UPDATE_INTERVAL)								#so your processor doesn't explode


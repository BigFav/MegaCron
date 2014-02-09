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

	for job in jobs:
		
		#Adding Schedules for jobs within SCHEDULER_UPDATE_INTERVAL
		cmd = CronTab(tab="""%s %s""" % (job.interval, job.command))		#these two lines
		command = cmd.crons.pop()
		cmd_sch = command.schedule(date_from = datetime.now())			#allow us to obtain next timeToRun
		
		nxt = cmd_sch.get_next()
                print "%s %s" % (job.interval,job.command)
		print nxt
		print (nxt - datetime.now()).total_seconds() 
		while (nxt - datetime.now()).total_seconds() < SCHEDULER_UPDATE_INTERVAL:
		    print "here"	
		    job.lastTimeRun = nxt
		    schedule = API.Schedule(nxt, job, worker=None)
		    schedules.append(schedule)
                    API.setJobTime(job)
		    nxt = cmd_sch.get_next()
	print schedules
	return schedules


while True:

	jobs = API.getJobs()
	
	schedules = sortSchedules(jobs2Schedules(jobs))
	print schedules
	workers = API.getWorkers()
	
	for schedule in schedules:
		worker = workers.pop()
		schedule.worker = worker

	API.addSchedules(schedules)

 	time.sleep(SCHEDULER_UPDATE_INTERVAL)								#so your processor doesn't explode


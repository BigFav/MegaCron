from crontab import CronTab
from croniter import croniter
from datetime import datetime
from datetime import timedelta
from operator import attrgetter
import time
import API

SCHEDULER_UPDATE_INTERVAL = timedelta(seconds=15).total_seconds()

def sortSchedules (schedules):

	return sorted(schedules, key=attrgetter('timeToRun'))


def jobs2Schedules (jobs):

	schedules = []

	for job in jobs:
		
		#Adding Schedules for jobs within SCHEDULER_UPDATE_INTERVAL
		cmd = CronTab(tab="""%s %s""" % (job.interval, job.command))		#these two lines
		command = cmd.crons.pop()
		cmd_sch = command.schedule(date_from = datetime.now())			#allow us to obtain next timeToRun
	
		nxt = cmd_sch.get_next()
		while (nxt - datetime.now()).total_seconds() < SCHEDULER_UPDATE_INTERVAL:
                    job.lastTimeRun = nxt
		    schedule = API.Schedule(nxt, job, worker=None)
		    schedules.append(schedule)
                    API.setJobTime(job)
		    nxt = cmd_sch.get_next()

	return schedules


while True:

	jobs = API.getJobs()
	schedules = sortSchedules(jobs2Schedules(jobs))

	workers = API.getWorkers()
	num_workers = len(workers)

	if num_workers:
		for i,schedule in enumerate(schedules):
			worker = workers[i % num_workers]
			schedule.worker = worker

		API.addSchedules(schedules)

 	time.sleep(SCHEDULER_UPDATE_INTERVAL)								#so your processor doesn't explode


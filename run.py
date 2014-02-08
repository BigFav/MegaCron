from crontab import CronTab
from croniter import croniter
from datetime import datetime
from datetime import timedelta
import time
import API

def sortSchedules (schedules):

	return schedules.sort(key=lambda schedule: schedule.timeToRun, reverse=False)


def jobs2Schedules (jobs):

	schedules = []

	while (len(jobs) > 0)):
		
		job = jobs.pop()
		
		cmd = CronTab(tab="%s %s" % (job.interval, job.command)			#these two lines
		cmd_sch = cmd.getSchedule(date_from=datetime.now())				#allow us to obtain next timeToRun
		
		schedule = API.schedule(cmd_sch.get_next, job, worker=None, completedTime=None)
		
	 	schedules.append(schedule)

	 return schedules


while True:

	schedules = sortSchedules(jobs2Schedules(API.getJobs()))

	workers = API.getWorkers()
	
	worker = workers.pop()
	
	for schedule in schedules:

		schedule.worker = worker

	API.addSchedule(schedules)

 	time.sleep(3600)													#so your processor doesn't explode


from crontab import CronTab
from croniter import croniter
from datetime import datetime
from datetime import timedelta
import time
import string
import subprocess
import os

def preprocessJob (job):
	return string.joinfields(job.split(' ')[5:], ' ')

def preprocessExt (job, ft_ext):
	return ft_ext[job.split('/')[-1].partition('.')[2][:2]]


jobs = CronTab(tabfile='crontab.tab')
#check if jobs are valid!!!!!
count = len(jobs)
schedules = [job.schedule(date_from=datetime.now()) for job in jobs]
jobs = map(str, jobs)
ft_ext = { 'sh':'bash', 'py':'python', 'pl':'perl', '':'' }				#supports bash, python, perl, and single commands
cmds = []
for job in jobs:
	job = string.joinfields(job.split(' ')[5:], ' ')
	typ = ""
	if job[:7] != "python ":
		typ = ft_ext[job.split('/')[-1].partition('.')[2][:2]]
	cmds.append("%s %s" % (typ, job))
nxt = [schedule.get_next() for schedule in schedules]


def sortSchedules (schedules):

	return schedules.sort(key=lambda schedule: schedule.timeToRun, reverse=False)


def jobs2Schedules (jobs):

	schedules = []

	while (len(jobs) > 0)):
		
		job = jobs.pop()
		
		cmd = CronTab(tab="%s %s" % (job.interval, job.command)			#these two lines
		cmd_sch = cmd.getSchedule(date_from=datetime.now())				#allow us to obtain next timeToRun
		
		schedule = api.schedule(cmd_sch.get_next, job, worker=None, completedTime=None)
		
	 	schedules.append(schedule)

	 return schedules


while True:

	workers = []

	schedules = sortSchedules(jobs2Schedules)

	workers = getWorkers()
	
	worker = workers.pop()
	
	for schedule in schedules:

		schedule.worker = worker

 	time.sleep(3600)													#so your processor doesn't explode


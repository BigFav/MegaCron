from crontab import CronTab
from croniter import croniter
from datetime import datetime
from datetime import timedelta
import time
import string
import subprocess

def preprocessJob (job):
	return string.joinfields(job.split(' ')[5:], ' ')

def preprocessExt (job, ft_ext):
	return ft_ext[job.split('/')[-1].partition('.')[2][:2]]


jobs = CronTab(tabfile='crontab.tab')
#check if jobs are valid!!!!!
count = len(jobs)
schedules = [job.schedule(date_from=datetime.now()) for job in jobs]
jobs = map(str, jobs)
ft_ext = { 'sh':'bash', 'py':'python', 'pl':'perl', '':'' } #supports bash, python, perl, and single commands
args = []
for job in jobs:
	job = string.joinfields(job.split(' ')[5:], ' ')
	typ = ""
	if job[:7] != "python ":
		typ = ft_ext[job.split('/')[-1].partition('.')[2][:2]]
	print "%s %s" % (typ, job)
	args.append("%s %s" % (typ, job))
nxt = [schedule.get_next() for schedule in schedules]

while True:
	gaps = []
	for i in range(count):
		delta = nxt[i] - datetime.now()
		gap = delta.total_seconds()
		gaps.append(gap)
		#Could probably map this so it's faster
		if abs(gap) < 1:
			subprocess.call(args[i], shell=True) #this gets replaced
			nxt[i] = schedules[i].get_next()
		elif gap < 0:
			nxt[i] = schedules[i].get_next()
	time.sleep(int(min(gaps))) #so your processor doesn't explode

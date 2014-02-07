from crontab import CronTab
from croniter import croniter
from datetime import datetime
from datetime import timedelta
#import WorkQueue
import time
import string
import subprocess

def preprocessJob (job):
	return string.joinfields(job.split(' ')[5:], ' ')

ft_ext = { 'sh':'bash', 'py':'', 'pl':'perl', '':'' } #supports bash, python, perl, and single commands 
def preprocessExt (job):
	return ft_ext[job.split('/')[-1].partition('.')[2][:2]]


jobs = CronTab(tabfile='crontab.tab')
#check if jobs are valid!!!!!
count = len(jobs)
schedules = [job.schedule(date_from=datetime.now()) for job in jobs]
jobs = map(str, jobs)
jobs = map(preprocessJob, jobs)
typs = map(preprocessExt, jobs)
args = ["%s %s" % (typ, job) for (typ, job) in zip(typs, jobs)]
nxt = [schedule.get_next() for schedule in schedules]

#workQ = WorkQueue()
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

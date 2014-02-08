from crontab import CronTab
from croniter import croniter
from datetime import datetime
from datetime import timedelta
import time
import string
import os
import subprocess
from API.py import getJobs
from API.py import setJobs

uid = str(os.getuid())
jobs_c = getJobs(uid)
tbfile = "crontab.tab"
with open(tbfile, 'w') as tab:
	for schedule in schedules:
		tab.write("%s %s\n" % (schedule.interval, schedule.command))

editor = os.getenv('EDITOR')
if editor:
	os.system("%s %s" % (editor, tbfile))
else:
	subprocess.call("vim %s" % tbfile, shell=True)


jobs_c = CronTab(tabfile=tbfile)
jobs_c = map(str, jobs_c)
jobs = []
for job in jobs_c:
	tmp = job.split(' ')
	interval = string.joinfields(tmp[:5], ' ')
	cmd = string.joinfields(tmp[5:], ' ')
	jobs.append(Job(interval, cmd, uid))

setJobs(jobs)

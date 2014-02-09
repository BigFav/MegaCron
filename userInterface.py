import sys
import string
import subprocess
import os
from crontab import CronTab
import API
from datetime import datetime


uid = str(os.getuid())

if len(sys.argv) < 3:
	tbfile = "crontab.tab"
	jobs_old = API.getJobsForUser(uid)
	with open(tbfile, 'w') as tab:
		for job in jobs_old:
			tab.write("%s %s\n" % (job.interval, job.command))

	editor = os.getenv('EDITOR')
	if editor:
		os.system("%s %s" % (editor, tbfile))
	else:
		subprocess.call("vim %s" % tbfile, shell=True)
elif sys.argv[1] == '-u':
	tbfile = sys.argv[2]


jobs_old = CronTab(tabfile=tbfile)
jobs_old = map(str, jobs_old)
jobs_new = []
for job in jobs_old:
	tmp = job.split(' ')
	interval = string.joinfields(tmp[:5], ' ')
	cmd = string.joinfields(tmp[5:], ' ')
	jobs_new.append(API.Job(interval, cmd, uid, datetime.min))

API.setJobs(jobs_new, uid)

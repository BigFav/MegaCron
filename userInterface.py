import string
import subprocess
import os
from crontab import CronTab
import API

uid = str(os.getuid())
jobs_old = API.getJobs(uid)
tbfile = "crontab.tab"
with open(tbfile, 'w') as tab:
	for job in jobs_old:
		tab.write("%s %s\n" % (job.interval, job.command))

editor = os.getenv('EDITOR')
if editor:
	os.system("%s %s" % (editor, tbfile))
else:
	subprocess.call("vim %s" % tbfile, shell=True)


jobs_old = CronTab(tabfile=tbfile)
jobs_old = map(str, jobs_old)
jobs_new = []
for job in jobs_old:
	tmp = job.split(' ')
	interval = string.joinfields(tmp[:5], ' ')
	cmd = string.joinfields(tmp[5:], ' ')
	jobs_new.append(API.Job(interval, cmd, uid))

API.setJobs(jobs_new, uid)

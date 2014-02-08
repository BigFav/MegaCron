from crontab import CronTab
import string
import os
import subprocess

uid = os.getuid()
schedules = DATABASE.getSchedules(uid)
tbfile = "crontab.tab"
with open(tbfile, 'w') as tab:
	for schedule in schedules:
		tab.write("%s %s\n" % (schedule.interval, schedule.command))

editor = os.getenv('EDITOR')
if editor:
	os.system("%s %s" % (editor, tbfile))
else:
	subprocess.call("vim %s" % tbfile, shell=True)

jobs = CronTab(tabfile=tbfile)
jobs = map(str, jobs)
schedules = []
for job in jobs:
	tmp = job.split(' ')
	interval = string.joinfields(tmp[:5], ' ')
	cmd = string.joinfields(tmp[5:], ' ')
	schedule = schedule()
	schedule.interval = interval
	schedule.command = cmd
	schedules.append(schedule)

DATABASE.setSchedules(schedules, uid)


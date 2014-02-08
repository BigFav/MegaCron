from crontab import CronTab
from croniter import croniter
from datetime import datetime
from datetime import timedelta
import time
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
cron_schedules = [job.schedule(date_from=datetime.now()) for job in jobs]
jobs = map(str, jobs)
schedules = []
for job in jobs:
	tmp = job.split(' ')
	interval = string.joinfields(tmp[:5], ' ')
	cmd = string.joinfields(tmp[5:], ' ')
	schedule = schedule()
	schedule.interval = interval
	schedule.command = cmd
	schedule.userId = uid
	schedule.next_attempt = cron_schedules[i].get_next()
	schedules.append(schedule)

DATABASE.setSchedules(schedules, uid)


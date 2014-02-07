from crontab import CronTab
from croniter import croniter
from datetime import datetime
from datetime import timedelta
import subprocess

ft_ext = { 'sh':'bash', 'py':'python', 'pl':'perl' }

cron = CronTab(tabfile='crontab.tab')
for job in cron: #not generalized yet for more than one, but thats trivial
	job.enable() #can be removed
	schedule = job.schedule(date_from=datetime.now())
	job = str(job).split(' ')[5] #throw away time stuff
	typ = str(job).split('/') 
	typ = typ[len(typ)-1] #get command
	if '.' in typ:
		typ = ft_ext[typ.partition('.')[2]] #get file type
		args = [typ, job]
	#else:
		#if no '.'
		#will also check against validjob()

nxt = schedule.get_next()
while True:
	delta = nxt - datetime.now()
	#Could probably map this so it's faster
	if abs(delta.total_seconds()) < 1:
		subprocess.call(args)
		nxt = schedule.get_next()
	elif delta.total_seconds() < 0:
		nxt = schedule.get_next()

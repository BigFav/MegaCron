from crontab import CronTab
from croniter import croniter
from datetime import datetime
from datetime import timedelta
import array
import string
import time

def timing(f, n, a):
	print f
	r = range(n)
	t1 = time.clock()
	for i in r:
		f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a); f(a);

	t2 = time.clock()
	print round(t2-t1, 3)


def preprocessJob (job):
	return string.joinfields(str(job).split(' ')[5:], ' ')

def preprocessJob2 (job):
	return string.joinfields(job.split(' ')[5:], ' ')

ft_ext = { 'sh':'bash', 'py':'', 'pl':'perl', '':'' } #supports bash, python, perl, and single commands 
def preprocessExt (job):
	return ft_ext[job.split('/')[-1].partition('.')[2][:2]]

def preprocessExt2 (job, ft):
	print type(ft)
	print type(job)
	return ft[job.split('/')[-1].partition('.')[2][:2]]

def f1(test):
	jobs = test 
	#check if jobs are valid!!!!!
	count = len(jobs)
	schedules = [job.schedule(date_from=datetime.now()) for job in jobs]
	jobs = map(preprocessJob, jobs)
	typs = map(preprocessExt, jobs)
	args = ["%s %s" % (typ, job) for (typ, job) in zip(typs, jobs)]
def f2(test):
	jobs = test 
	#check if jobs are valid!!!!!
	count = len(jobs)
	schedules = [job.schedule(date_from=datetime.now()) for job in jobs]
	jobs = map(str, jobs)
	jobs = map(preprocessJob2, jobs)
	typs = map(preprocessExt, jobs)
	args = ["%s %s" % (typ, job) for (typ, job) in zip(typs, jobs)]
def f3(test):
	jobs = test 
	#check if jobs are valid!!!!!
	count = len(jobs)
	schedules = [job.schedule(date_from=datetime.now()) for job in jobs]
	jobs = map(str, jobs)
	args = []
	ft = { 'sh':'bash', 'py':'', 'pl':'perl', '':'' } #supports bash, python, perl, and single commands 
	for job in jobs:
		job = string.joinfields(job.split(' ')[5:], ' ')
		typ = ft[job.split('/')[-1].partition('.')[2][:2]]
		args.append("%s %s" % (typ, job))
def f4(test):
	jobs = test 
	#check if jobs are valid!!!!!
	count = len(jobs)
	schedules = [job.schedule(date_from=datetime.now()) for job in jobs]
	jobs = map(str, jobs)
	typs = []
	ft = { 'sh':'bash', 'py':'', 'pl':'perl', '':'' } #supports bash, python, perl, and single commands 
	for job in jobs:
		job = string.joinfields(job.split(' ')[5:], ' ')
		typs.append(ft[job.split('/')[-1].partition('.')[2][:2]])
	args = ["%s %s" % (typ, job) for (typ, job) in zip(typs, jobs)]


testdata = CronTab(tabfile='testcron.tab')
testfuncs = f2, f3, f4
for f in testfuncs: print f.func_name, f(testdata)
for f in testfuncs: timing(f, 8, testdata)

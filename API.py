import pickle
import os
from datetime import datetime

FILE_NAME = "db.p"

class Job:
    def __init__(self, interval, command, userId, lastTimeRun=None, id=None):
        self.interval = interval
        self.command = command
        self.userId = userId
        self.lastTimeRun = lastTimeRun
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

class Schedule:
    def __init__(self, timeToRun, job, worker=None, id=None):
        self.timeToRun = timeToRun
        self.job = job
        self.worker = worker
        self.id = id
        
    def __eq__(self, other):
        return self.id == other.id

class Worker:
    def __init__(self, heartbeat, id=None):
        self.heartbeat = heartbeat
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

def getJobs():
    return __readFile()['jobs']

def getJobsForUser(userId):
    jobs = __readFile()['jobs']
    return [job for job in jobs if job.userId == userId]    

def setJobs(jobs, userId):
    file = __readFile()

    # Give them an id if they don't already have one
    for job in jobs:
        if job.id != None:
            job.id = file['nextJobId']
            file['nextJobId'] += 1

    file['jobs'] = [job for job in file['jobs'] if job.userId != userId]
    file['jobs'].extend(jobs)

    __writeFile__(file)
    os.rename(FILE_NAME+'~', FILE_NAME)

def getSchedules(worker):
    schedules = __readFile()['schedules']
    return [schedule for schedule in schedules if schedule.worker == worker]

def addSchedules(schedules):
    file = __readFile()

    # Give them an id if they don't already have one
    for schedule in schedules:
        if schedule.id != None:
            schedule.id = file['nextScheduleId']
            file['nextScheduleId'] += 1

    file['schedules'].extend(schedules)

    __writeFile(file)

def removeSchedule(schedule):
    file = __readFile()

    file['schedules'].remove(schedule)

    __writeFile(file)

def getHeartbeat(worker):
    workers = __readFile()['workers']
    for w in workers:
        if w == worker:
            return w
            break

    return None

def updateHeartbeat(worker):
    file = __readFile()
    for w in file['workers']:
        if w == worker:
            w.heartbeat = datetime.now()
            break
    
    __writeFile(file)

def getWorkers():
    return __readFile()['workers']

def createWorker():
    file = __readFile()
    id = file['nextWorkerId']

    file['workers'].append(Worker(datetime.now(), id))
    file['nextWorkerId'] += 1
    
    __writeFile(file)

    return id

def __readFile():
    try:
        with open(FILE_NAME,"rb") as file:
            return pickle.load(file)
    except IOError:
        return {
            'jobs': [],
            'schedules': [],
            'workers': [],
            'nextJobId': 1,
            'nextScheduleId': 1,
            'nextWorkerId': 1
        }

def __writeFile(data):
    with open(FILE_NAME,"wb") as file:
        pickle.dump(data, file)

def __writeFile__(data):
    with open(FILE_NAME+"~","wb") as file:
        pickle.dump(data, file)

import API
import subprocess
import time
from datetime import datetime, timedelta

SCHEDULES_UPDATE_INTERVAL = timedelta(seconds=10)#minutes=10)

schedules = None
nextSchedulesUpdateTime = datetime.now()

def runSchedules(worker):
    global schedules
    global nextSchedulesUpdateTime

    if nextSchedulesUpdateTime <= datetime.now():
        schedules = API.getSchedules(worker)
        nextSchedulesUpdateTime = datetime.now() + SCHEDULES_UPDATE_INTERVAL

    if len(schedules) > 0:
        schedule = schedules.pop()
        secondsToSleep = (schedule.timeToRun - datetime.now()).total_seconds()
        if secondsToSleep > 0:
            time.sleep(min(SCHEDULES_UPDATE_INTERVAL.total_seconds(), secondsToSleep))

        if schedule.timeToRun <= datetime.now():
            subprocess.call(schedule.job.command, shell=True)
            API.removeSchedule(schedule)
    else:
        time.sleep(SCHEDULES_UPDATE_INTERVAL.total_seconds())

worker = API.createWorker()
while True:
    runSchedules(worker)

#!/usr/bin/python

import sys
sys.path.append("../API")

import API
import subprocess
import signal
import sys
import time
import sched
from datetime import datetime, timedelta

SCHEDULES_UPDATE_INTERVAL = timedelta(seconds=10)#minutes=10)
HEARTBEAT_UPDATE_INTERVAL = timedelta(seconds=10)

schedules = []
worker = API.createWorker()

def signal_handler(signal, frame):
    global worker
    API.destroyWorker(worker)
    sys.exit(0)

def updateSchedules(events):
    global worker
    global schedules

    schedules = API.getSchedules(worker)
    runSchedules(events)

    events.enter(SCHEDULES_UPDATE_INTERVAL.total_seconds(), 1, updateSchedules, (events,))

def runSchedules(events):
    global schedules

    if len(schedules) > 0:
        schedule = schedules[-1]
        secondsToNextRun = (schedule.timeToRun - datetime.now()).total_seconds()
        if secondsToNextRun <= 0:
            subprocess.call(schedule.job.command, shell=True)
            API.removeSchedule(schedule)
            schedules.pop()

        events.enter(secondsToNextRun, 1, runSchedules, (events,))

def heartbeat(events):
    global worker

    API.updateHeartbeat(worker)
    events.enter(HEARTBEAT_UPDATE_INTERVAL.total_seconds(), 1, heartbeat, (events,))

signal.signal(signal.SIGINT, signal_handler)
events = sched.scheduler(time.time, time.sleep)

while True:
    heartbeat(events)
    updateSchedules(events)
    events.run()


#!/usr/bin/python

import sys
import subprocess
import signal
import time
import sched
from datetime import datetime, timedelta

sys.path.append("../api")
import api

SCHEDULES_UPDATE_INTERVAL = timedelta(seconds=10)
HEARTBEAT_UPDATE_INTERVAL = timedelta(seconds=10)

_schedules = []
_worker = api.create_worker()


def _signal_handler(signal, frame):
    global _worker
    api.destroy_worker(_worker)
    sys.exit(0)


def update_schedules(events):
    global _worker
    global _schedules

    _schedules = api.get_schedules(_worker)
    _run_schedules(events)

    delay = SCHEDULES_UPDATE_INTERVAL.total_seconds()
    events.enter(delay, 1, update_schedules, (events,))


def _run_schedules(events):
    global _schedules

    if len(_schedules) > 0:
        schedule = _schedules[-1]
        time_to_run = schedule.time_to_run
        seconds_to_next_run = (time_to_run - datetime.now()).total_seconds()
        if seconds_to_next_run <= 0:
            subprocess.call(schedule.job.command, shell=True)
            api.remove_schedule(schedule)
            _schedules.pop()

        events.enter(seconds_to_next_run, 1, _run_schedules, (events,))


def heartbeat(events):
    global _worker

    api.update_heartbeat(_worker)
    delay = HEARTBEAT_UPDATE_INTERVAL.total_seconds()
    events.enter(delay, 1, heartbeat, (events,))


if __name__ == '__main__':
    signal.signal(signal.SIGINT, _signal_handler)
    events = sched.scheduler(time.time, time.sleep)

    while True:
        heartbeat(events)
        update_schedules(events)
        events.run()

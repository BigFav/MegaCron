import pwd
import os
import subprocess
from datetime import datetime, timedelta

from megacron import api

SCHEDULES_UPDATE_INTERVAL = timedelta(seconds=10)
HEARTBEAT_UPDATE_INTERVAL = timedelta(seconds=10)

worker = api.create_worker()
_schedules = []
_run_schedules_event = None


def cleanup():
    global worker
    api.destroy_worker(worker)


def update_schedules(events):
    global worker
    global _schedules
    global _run_schedules_event

    _schedules = api.get_schedules(worker)

    # Cancel the existing event because _run_schedules will create a new one.
    if _run_schedules_event is not None:
        events.cancel(_run_schedules_event)

    _run_schedules(events)

    delay = SCHEDULES_UPDATE_INTERVAL.total_seconds()
    events.enter(delay, 1, update_schedules, (events,))


def _run_schedules(events):
    global _schedules
    global _run_schedules_event

    if len(_schedules) > 0:
        schedule = _schedules[-1]
        time_to_run = schedule.time_to_run
        seconds_to_next_run = (time_to_run - datetime.now()).total_seconds()
        if seconds_to_next_run <= 0:
            _run_command(schedule.job.command, schedule.job.user_id)
            api.remove_schedule(schedule)
            _schedules.pop()

            _run_schedules_event = events.enter(seconds_to_next_run, 1,
                                                _run_schedules, (events,))

    _run_schedules_event = None


def _run_command(command, uid):
    passwd = pwd.getpwuid(uid)

    env = os.environ.copy()
    env['HOME'] = passwd.pw_dir
    env['LOGNAME'] = passwd.pw_name
    env['USER'] = passwd.pw_name

    def preexec():
        os.setgid(passwd.pw_gid)
        os.setuid(uid)

    subprocess.Popen(command, preexec_fn=preexec, shell=True, env=env)


def heartbeat(events):
    global worker

    api.update_heartbeat(worker)

    delay = HEARTBEAT_UPDATE_INTERVAL.total_seconds()
    events.enter(delay, 1, heartbeat, (events,))

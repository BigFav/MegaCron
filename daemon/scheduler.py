import sys
from datetime import datetime, timedelta
from operator import attrgetter

from crontab import CronTab

sys.path.append("../api")
import api
import worker

SCHEDULER_UPDATE_INTERVAL = timedelta(seconds=15)
WORKER_HEARTBEAT_TIMEOUT = timedelta(seconds=20)


def sort_schedules(schedules):
    return sorted(schedules, key=attrgetter('time_to_run'))


def create_schedules(events):
    schedules = []

    for job in api.get_jobs():
        # Adding Schedules for jobs within SCHEDULER_UPDATE_INTERVAL
        cmd = CronTab(tab="%s %s" % (job.interval, job.command))
        command = cmd.crons.pop()
        cmd_sch = command.schedule(date_from=datetime.now())

        nxt = cmd_sch.get_next()  # get next time to run
        while (nxt - datetime.now()) < SCHEDULER_UPDATE_INTERVAL:
            job.lastTimeRun = nxt

            next_worker = api.get_next_worker()
            if next_worker is None:
                break

            schedule = api.Schedule(nxt, job, next_worker)
            schedules.append(schedule)
            api.set_job_time(job)
            nxt = cmd_sch.get_next()

    api.add_schedules(sort_schedules(schedules))

    delay = SCHEDULER_UPDATE_INTERVAL.total_seconds()
    events.enter(delay, 1, create_schedules, (events,))


def check_worker_heartbeat(events):
    for w in api.get_workers():
        if (datetime.now() - w.heartbeat) > WORKER_HEARTBEAT_TIMEOUT:
            for schedule in api.get_schedules(w):
                schedule.worker = api.get_next_worker()

            api.destroy_worker(w)

    delay = WORKER_HEARTBEAT_TIMEOUT.total_seconds()
    events.enter(delay, 1, check_worker_heartbeat, (events,))


def check_scheduler(events):
    for w in api.get_workers():
        if (datetime.now() - w.heartbeat) <= WORKER_HEARTBEAT_TIMEOUT:
            if w == worker.worker:
                create_schedules(events)
                check_worker_heartbeat(events)
            else:
                delay = WORKER_HEARTBEAT_TIMEOUT.total_seconds()
                events.enter(delay, 1, check_scheduler, (events,))

            return

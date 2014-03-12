import sys
import signal
import sched
import time

from megacron.daemon import scheduler, worker


def _signal_handler(signal, frame):
    worker.cleanup()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, _signal_handler)
    events = sched.scheduler(time.time, time.sleep)

    scheduler.check_scheduler(events)

    worker.heartbeat(events)
    worker.update_schedules(events)

    events.run()

#!/usr/bin/python

import sys
import signal
import sched
import time

sys.path.append("../api")
import scheduler
import worker


def _signal_handler(signal, frame):
    worker.cleanup()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, _signal_handler)
    events = sched.scheduler(time.time, time.sleep)

    worker.heartbeat(events)
    worker.update_schedules(events)

    scheduler.check_scheduler(events)

    events.run()

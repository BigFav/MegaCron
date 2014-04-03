import sys
import os
import signal
import sched
import time
import argparse

import daemon
from lockfile.pidlockfile import PIDLockFile

from megacron.daemon import scheduler, worker


def _signal_handler(signal, frame):
    worker.cleanup()
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description='A distributed cron-like daemon')
    parser.add_argument('-f', dest='foreground', action='store_const',
                        const=False, help='run in foreground')
    args = parser.parse_args()

    if os.geteuid() != 0:
        sys.exit('%s must be run as root.' % os.path.basename(sys.argv[0]))

    context = daemon.DaemonContext(
        pidfile=PIDLockFile('/var/run/megacron.pid'),
        detach_process=args.foreground,
    )
    context.signal_map = {
        signal.SIGINT: _signal_handler,
        signal.SIGTERM: _signal_handler
    }

    with context:
        worker.init_worker()

        events = sched.scheduler(time.time, time.sleep)

        scheduler.check_scheduler(events)

        worker.heartbeat(events)
        worker.update_schedules(events)

        events.run()

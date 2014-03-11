import sys
import string
import subprocess
import os
from datetime import datetime

from megacron import api


def main():
    uid = os.getuid()

    if len(sys.argv) < 3:
        tb_file = "crontab.tab"
        jobs_old = api.get_jobs_for_user(uid)
        with open(tb_file, 'w') as tab:
            for job in jobs_old:
                tab.write("%s %s\n" % (job.interval, job.command))

        editor = os.getenv('EDITOR')
        if editor is not None:
            os.system("%s %s" % (editor, tb_file))
        else:
            subprocess.call("vim %s" % tb_file, shell=True)
    elif sys.argv[1] == '-u':
        tb_file = sys.argv[2]

    jobs_new = []
    with open(tb_file, 'r') as tab:
        for job in tab:
            tmp = job.strip().split(' ')
            interval = string.joinfields(tmp[:5], ' ')
            cmd = string.joinfields(tmp[5:], ' ')
            jobs_new.append(api.Job(interval, cmd, uid, datetime.now()))

    api.set_jobs(jobs_new, uid)

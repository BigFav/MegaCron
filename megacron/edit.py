import sys
import string
import subprocess
import os
import tempfile
from datetime import datetime

from megacron import api


def main():
    uid = os.getuid()

    if len(sys.argv) < 3:
        jobs_old = api.get_jobs_for_user(uid)
        with tempfile.NamedTemporaryFile('w', delete=False) as temp:
            for job in jobs_old:
                temp.write("%s %s\n" % (job.interval, job.command))

            tb_file = temp.name

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

    if len(sys.argv) < 3:
        os.unlink(tb_file)

    api.set_jobs(jobs_new, uid)

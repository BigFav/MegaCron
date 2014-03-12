import os
import sys
import string
import subprocess
import tempfile
from datetime import datetime

from croniter import croniter
from megacron import api


def get_crontab(uid, valid_crontab):
    remote_file = len(sys.argv) < 3
    if remote_file or (valid_crontab is False):
        jobs_old = api.get_jobs_for_user(uid)
        if (valid_crontab is None) or remote_file:
            with tempfile.NamedTemporaryFile('w', delete=False) as temp:
                for job in jobs_old:
                    temp.write("%s %s\n" % (job.interval, job.command))

                tb_file = temp.name
        else:
            tb_file = sys.argv[2]

        visual = os.getenv('VISUAL')
        editor = os.getenv('EDITOR')
        if visual:
            os.system("%s %s" % (visual, tb_file))
        elif editor:
            os.system("%s %s" % (editor, tb_file))
        else:
            try:
                subprocess.check_call(["vi", str(tb_file)])
            except OSError:
                if len(sys.argv) < 3:
                    os.unlink(tb_file)
                sys.exit("No text editor available. Please set your VISUAL" +
                         " or EDITOR environment variable.")

    elif sys.argv[1] == '-u':
        tb_file = sys.argv[2]

    return tb_file


def process_edits(uid, tb_file):
    jobs_new = []
    with open(tb_file, 'r') as tab:
        for line in tab:
            tmp = line.strip().split(' ')
            interval = string.joinfields(tmp[:5], ' ')
            cmd = string.joinfields(tmp[5:], ' ')
            try:
                valid_interval = croniter(interval) 
            except KeyError:
                while True:
                    # Different syntax in Python 3 'input()'
                    cont = raw_input("The crontab you entered has invalid " +
                                     "entries, would you like to edit it " +
                                     "again? (y/n)\n")
                    if cont == 'n':
                        if len(sys.argv) < 3:
                            os.unlink(tb_file)
                        sys.exit(1)
                    elif cont == 'y':
                        return False
            jobs_new.append(api.Job(interval, cmd, uid, datetime.now()))

    if len(sys.argv) < 3:
        os.unlink(tb_file)

    api.set_jobs(jobs_new, uid)
    return True


def main():
    uid = os.getuid()
    valid_crontab = None
    while not valid_crontab:
        tb_file = get_crontab(uid, valid_crontab)
        valid_crontab = process_edits(uid, tb_file)


if __name__ == '__main__':
    main()

import argparse
import os
import pwd
import sys
import subprocess
import tempfile
from datetime import datetime

from croniter import croniter
from megacron import api


_input = raw_input if sys.version_info < (3,) else input


def _print_usage(self, file=None):
    if file is None:
        file = sys.stdout
    # Only inserted line to adjust printed usage to fit implicit rule
    usage_str = self.format_usage().replace("[-e | -r | -l | file]",
                                            "{-e | -r | -l | file}", 1)
    self._print_message(usage_str, file)
argparse.ArgumentParser.print_usage = _print_usage


def _print_help(self, file=None):
    if file is None:
        file = sys.stdout
    # Only inserted line to adjust printed usage to fit implicit rule
    help_str = self.format_help().replace("[-e | -r | -l | file]",
                                          "{-e | -r | -l | file}", 1)
    self._print_message(help_str, file)
argparse.ArgumentParser.print_help = _print_help


def parse_args():
    parser = argparse.ArgumentParser(description="Gets options for crontab "
                                                 "editor.")
    parser.add_argument('-u', action="store", dest="usr",
                        help="User of whose crontab to use. Will use current "
                             "user's crontab, if no user is specified.")
    parser.add_argument('-i', action="store_true", dest="rm_prompt",
                        help="Modifies the -r option to prompt the user for a "
                             "'y/n' response before removing the crontab.")

    # Cannot have multiple commands at once
    commands = parser.add_mutually_exclusive_group()
    commands.add_argument('-e', action="store_true", dest="edit",
                          help="Edit the current crontab using the editor "
                               "specified by the VISUAL or EDITOR "
                               "variables. Upon exit of the editor, the "
                               "changes will be saved.")
    commands.add_argument('-r', action="store_true", dest="rm",
                          help="Remove the current crontab.")
    commands.add_argument('-l', action="store_true", dest="lst",
                          help="List - display the current crontab entries on "
                               "standard output.")
    commands.add_argument('file', nargs='?', default=False,
                          help="File to overwrite current crontab.")

    opts = parser.parse_args()
    # Ensure at least one command was selected, extra implicit rule
    if not (opts.file or opts.edit or opts.lst or opts.rm):
        parser.error("No command requested, add -e, -r, -l, or a file name.")

    return opts


def get_crontab(opts, valid_crontab, tb_file):
    old_cron = api.get_crontab(opts.usr[0])
    if (opts.file is False) or (valid_crontab is False):
        old_cron = api.get_crontab(opts.usr[0])

        # Perform list operation
        if opts.lst:
            lst = old_cron if old_cron else "No crontab for %s." % opts.usr[1]
            print(lst)
            sys.exit(0)

        # Perform an edit in text editor
        if (opts.file is False) and (valid_crontab is None):
            # Write remote crontab to tempfile if it hasn't been written
            with tempfile.NamedTemporaryFile('w', delete=False) as temp:
                if old_cron:
                    temp.write(old_cron)
                tb_file = temp.name

        # Open the crontab in editor
        visual = os.getenv('VISUAL')
        editor = os.getenv('EDITOR')
        if visual:
            subprocess.call([visual, str(tb_file)])
        elif editor:
            subprocess.call([editor, str(tb_file)])
        else:
            try:
                subprocess.check_call(["/usr/bin/editor", str(tb_file)])
            except OSError:
                if opts.file is False:
                    os.unlink(tb_file)
                sys.exit("No text editor available. Please set your VISUAL "
                         "or EDITOR environment variable.")

    # Overwriting current crontab with local file
    elif opts.file:
        tb_file = opts.file

    old_tab = set(old_cron.split('\n')) if old_cron else set()
    return (tb_file, old_tab)


def process_edits(uid, tb_file, using_local_file, old_tab):
    e_str = ""
    jobs = []
    crontab = []
    old_jobs = api.get_jobs_for_user(uid)
    with open(tb_file, 'r') as tab:
        for i, line in enumerate(tab):
            line = line.strip()
            crontab.append(line)
            # Ignore newlines and full line comments
            if line and (line[0] != '#'):
                split = line.split()
                interval = ' '.join(split[:5])
                cmd = ' '.join(split[5:])
                try:
                    # Ensure the crontab line is valid
                    croniter(interval)
                    if not cmd:
                        raise ValueError("Missing command.")
                except (KeyError, ValueError) as e:
                    if isinstance(e, KeyError):
                        e = "Bad time interval syntax, %s " % e
                    # Replace croniter's typo-riddled error msg
                    elif str(e) != "Missing command.":
                        e = ("Less than 5 fields separated by white space "
                             "(requires 6).")
                    e_str += "Error in line %i: %s\n" % (i + 1, e)
                    continue

                if not e_str:
                    # Check if job was in the old crontab
                    job = None
                    if line in old_tab:
                        for old_job in old_jobs:
                            if (old_job.interval == interval and
                                    old_job.command == cmd):
                                job = old_job
                                old_jobs.remove(old_job)
                                break
                    if not job:
                        old_tab.discard(line)
                        job = api.Job(interval, cmd, uid, datetime.now())
                    jobs.append(job)

    if e_str:
        # Prompt user to edit crontab on error
        e_str += ("The crontab you entered has invalid entries, "
                  "would you like to edit it again? (y/n) ")
        while True:
            cnt = _input(e_str)
            if (cnt == 'n') or (cnt == 'N'):
                if using_local_file is False:
                    os.unlink(tb_file)
                sys.exit(1)
            elif (cnt == 'y') or (cnt == 'Y'):
                return False
            e_str = "Please enter y or n: "

    if using_local_file is False:
        os.unlink(tb_file)

    api.set_crontab('\n'.join(crontab), uid)
    api.set_jobs(jobs, uid)
    return True


def main():
    tb_file = None
    valid_crontab = None
    usr_euid = os.geteuid()
    opts = parse_args()

    # Convert given username into (uid, username)
    if opts.usr:
        try:
            opts.usr = (pwd.getpwnam(opts.usr).pw_uid, opts.usr)
        except KeyError:
            sys.exit("User '%s' does not exist." % opts.usr)

        # Verify permissions for selected crontab
        if (usr_euid != 0) and (opts.usr[0] != usr_euid):
            sys.exit("Access denied. You do not have permission to edit %s's "
                     "crontab." % opts.usr[1])
    # If no user is specified, set to current user (euid or uid?)
    else:
        opts.usr = (usr_euid, pwd.getpwuid(usr_euid).pw_name)

    # Perform rm operation
    if opts.rm:
        if opts.rm_prompt:
            rm = None
            e_str = ("You are about to delete %s's crontab, continue? "
                     "(y/n) " % opts.usr[1])
            while (rm != 'Y') and (rm != 'y'):
                rm = _input(e_str)
                if (rm == 'N') or (rm == 'n'):
                    sys.exit(0)
                e_str = "Please enter y or n: "

        api.set_jobs([], opts.usr[0])
        api.set_crontab(False, opts.usr[0])
        sys.exit(0)

    while not valid_crontab:
        tb_file, old_tab = get_crontab(opts, valid_crontab, tb_file)
        valid_crontab = process_edits(opts.usr[0], tb_file, opts.file, old_tab)

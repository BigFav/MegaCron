import argparse
import os
import re
import sys
import string
import subprocess
import tempfile
from datetime import datetime
from pwd import getpwnam

from croniter import croniter
from megacron import api


_input_ver_map = {True: raw_input, False: input}


def _print_usage(self, file=None):
    if file is None:
        file = sys.stdout
    usage_str = re.sub("\[-e \| -r \| -l \| file\]",
                       "{-e | -r | -l | file}",
                       self.format_usage())
    self._print_message(usage_str, file)
argparse.ArgumentParser.print_usage = _print_usage


def _print_help(self, file=None):
    if file is None:
        file = sys.stdout
    help_str = re.sub("\[-e \| -r \| -l \| file\]",
                      "{-e | -r | -l | file}",
                      self.format_help())
    self._print_message(help_str, file)
argparse.ArgumentParser.print_help = _print_help


def parse_args():
    parser = argparse.ArgumentParser(description="Gets options for crontab "
                                                 "editor.")
    parser.add_argument('-u', action="store", dest="usr", nargs='?',
                        help="User of whose crontab to use. Will use current "
                             "user's crontab, if no user is specified.")
    parser.add_argument('-i', action="store_true", dest="rm_prompt",
                        help="The -i option modifies the -r option to prompt "
                             "the user for a 'Y/y' response before removing "
                             "the crontab.")

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
    # Ensure at least one command was selected
    if not (opts.file or opts.edit or opts.lst or opts.rm):
        parser.error("No command requested, add -e, -r, -l, or a file name.")

    return opts


def get_crontab(opts, valid_crontab, tb_file):
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
            os.system("%s %s" % (visual, tb_file))
        elif editor:
            os.system("%s %s" % (editor, tb_file))
        else:
            try:
                subprocess.check_call(["vi", str(tb_file)])
            except OSError:
                if opts.file is False:
                    os.unlink(tb_file)
                sys.exit("No text editor available. Please set your VISUAL "
                         "or EDITOR environment variable.")

    # Overwriting current crontab with local file
    elif opts.file:
        tb_file = opts.file

    return tb_file


def process_edits(uid, tb_file, using_local_file):
    crontab = []
    jobs = []
    with open(tb_file, 'r') as tab:
        for line in tab:
            line = line.strip()
            crontab.append(line)
            # Ignore newlines and full line comments
            if line and (line[0] != '#'):
                # Isolate interval and command from end-of-line comment
                tmp = line.partition("  #")[0].split(' ')
                interval = string.joinfields(tmp[:5], ' ')
                cmd = string.joinfields(tmp[5:], ' ')
                try:
                    # Ensure the crontab line is valid
                    croniter(interval)
                except (KeyError, ValueError):
                    # Otherwise prompt user to edit crontab
                    while True:
                        # Different syntax in Python 3 'input()'
                        e_str = ("The crontab you entered has invalid "
                                 "entries, would you like to edit it "
                                 "again? (y/n) ")
                        cnt = _input_ver_map[sys.version_info < (3, 0)](e_str)
                        if (cnt == 'n') or (cnt == 'N'):
                            if using_local_file is False:
                                os.unlink(tb_file)
                            sys.exit(1)
                        elif (cnt == 'y') or (cnt == 'Y'):
                            return False
                jobs.append(api.Job(interval, cmd, uid, datetime.now()))

    if using_local_file is False:
        os.unlink(tb_file)

    api.set_crontab(string.joinfields(crontab, '\n'), uid)
    api.set_jobs(jobs, uid)
    return True


def main():
    tb_file = None
    valid_crontab = None
    usr_euid = os.geteuid()
    opts = parse_args()

    # Convert given username into (uid, username)
    if opts.usr:
        opts.usr = (getpwnam(opts.usr).pw_uid, opts.usr)

        # Verify permissions for selected crontab
        if (usr_euid != 0) and (opts.usr[0] != usr_euid):
            sys.exit("Access denied. You do not have permission to edit %s's "
                     "crontab." % opts.usr[1])
    # If no user is specified, set to current user
    else:
        opts.usr = (usr_euid, 'root')

    # Perform rm operation
    if opts.rm:
        if opts.rm_prompt:
            e_str = ("You are about to delete %s's crontab, continue? "
                     "(Y/y) " % opts.usr[1])
            rm = _input_ver_map[sys.version_info < (3, 0)](e_str)
            if (rm != 'Y') and (rm != 'y'):
                sys.exit(0)

        api.set_jobs([], opts.usr[0])
        api.set_crontab('', opts.usr[0])
        sys.exit(0)

    while not valid_crontab:
        tb_file = get_crontab(opts, valid_crontab, tb_file)
        valid_crontab = process_edits(opts.usr[0], tb_file, opts.file)

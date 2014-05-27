import argparse
import os
import pwd
import sys
import subprocess
import tempfile
from datetime import datetime
from re import compile

from croniter import croniter
from megacron import api
from megacron import config

#ALLOW_FILE = config.get_option("Database", "shared_filesystem_")
#DENY_FILE = config.get_option("Database", "shared_filesystem_")
#DEFAULT_ALLOWANCE = config.get_option("Database", "shared_filesystem_")


_input = raw_input if sys.version_info < (3,) else input
_unescaped_pct = compile(r"((?<!\\))%")
_escaped_pct = compile(r"\\%(?=([^'\"\\]*(\\.|[\"']([^\"'\\]*\\.)*[^'\"\\]*"
                       "[\"']))*[^\"']*$)")
_special_intervals = {"@yearly": "0 0 1 1 *", "@annually": "0 0 1 1 *",
                      "@monthly": "0 0 1 * *", "@weekly": "0 0 * * 0",
                      "@daily": "0 0 * * *", "@midnight": "0 0 * * *",
                      "@hourly": "0 * * * *"}


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


def check_permissions(opts_usr, usr_euid):
    # Check if user is allowed to use megacrontab
    if os.path.isfile("/etc/cron.allow"):
        with open("/etc/cron.allow", 'r') as allowed:
            if not opts_usr[1] in map(str.strip, allowed):
                sys.exit("Access denied. The user %s is not in "
                         "/etc/cron.allow, thus is not authorized to use "
                         "megacrontab.\nSee megacrontab(1) for more "
                         "information." % opts_usr[1])
    # Otherwise check if user is not allowed to use megacrontab
    elif os.path.isfile("/etc/cron.deny"):
        with open("/etc/cron.deny", 'r') as not_allowed:
            if opts_usr[1] in map(str.strip, not_allowed):
                sys.exit("Access denied. The user %s is in /etc/cron.deny, "
                         "thus is not authorized to use megacrontab.\nSee "
                         "megacrontab(1) for more information." % opts_usr[1])
    ''' Finally check the default, all or just root?
    elif not DEFAULT_ALLOWANCE and usr_euid:
        sys.exit("Access denied. Only root is authorized to use megacrontab.\n"
                 "See megacrontab(1) for more information.")
    '''
    # Check if current user has access to the current crontab
    if usr_euid and (opts_usr[0] != usr_euid):
        sys.exit("Access denied. You do not have permission to edit %s's "
                 "crontab." % opts_usr[1])


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
                    temp.write(old_cron + '\n')
                tb_file = temp.name

        # Open the crontab in editor
        editor_exist = False
        editors = [os.getenv('VISUAL'), os.getenv('EDITOR'), "/usr/bin/editor"]
        for editor in filter(bool, editors):
            try:
                subprocess.check_call([editor, str(tb_file)])
            except OSError:
                print(editor + " not found!")
            except subprocess.CalledProcessError as e:
                sys.exit(str(e))
            else:
                editor_exist = True
                break
        if not editor_exist:
            if opts.file is False:
                os.unlink(tb_file)
            sys.exit("No text editor available. Please set your VISUAL or "
                     "EDITOR environment variable properly.")

    # Overwriting current crontab with local file
    elif opts.file:
        tb_file = opts.file

    old_tab = set(old_cron.split('\n')) if old_cron else set()
    return (tb_file, old_tab)


def process_edits(uid, tb_file, using_local_file, old_tab):
    e_str = ""
    jobs = []
    crontab = []
    environs = api.get_environs(uid)
    old_jobs = api.get_jobs_for_user(uid)
    with open(tb_file, 'r') as tab:
        for i, line in enumerate(tab):
            line = line.strip()
            crontab.append(line)
            # Ignore newlines and comments
            if line and (line[0] != '#'):
                split = line.split()
                # Check for special interval syntax
                if split[0][0] == '@':
                    try:
                        interval = _special_intervals[split[0]]
                    except KeyError:
                        e_str += ("Error in line %i: Bad special interval "
                                  "syntax, %s\n" % (i + 1, split[0]))
                        continue
                    cmd = ' '.join(split[1:])

                # Check if setting variable
                elif '=' in ''.join(split[:5]):
                    name, _, value = line.partition('=')

                    # Check if var name is zero or multiple words
                    name = name.strip()
                    num_names = len(name.split())
                    if num_names != 1:
                        if num_names:
                            e_str += ("Error in line %i: Bad variable "
                                      "assignment syntax; multiple variable "
                                      "names given\n" % (i + 1))
                        else:
                            e_str += ("Error in line %i: Bad variable "
                                      "assignment syntax; no variable name "
                                      "given\n" % (i + 1))
                    else:
                        value = value.strip()
                        if (((value[0] == "'") or (value[0] == '"')) and
                           (value[-1] == value[0])):
                            # if properly wrapped in quotes, check if escaped
                            for i, char in enumerate(reversed(value[:-1])):
                                if char != '\\':
                                    i += 1
                                    break
                            if i % 2 != 0:
                                value = value[1:-1]

                        os.environ[name] = value
                    continue

                else:
                    # Check if five or six time/date fields
                    if (len(split) > 5 and
                            not any(c.isalpha() for c in split[5]) and
                            ('*' in split[5] or
                             any(c.isdigit() for c in split[5])) and
                            split[5][0] != '/'):
                        # Could print warning that using 6 time fields
                        interval = ' '.join(split[:6])
                        cmd = ' '.join(split[6:])
                    else:
                        interval = ' '.join(split[:5])
                        cmd = ' '.join(split[5:])

                # Check for un-escaped %s in command
                job_input = None
                index = cmd.find('%')
                while (index != -1) and (cmd[index-1] == '\\'):
                    index = cmd.find('%', index + 1)
                if index != -1:
                    job_input = _escaped_pct.sub('%', _unescaped_pct.sub(
                                                 r"\1\n", cmd[index+1:]))
                    cmd = cmd[:index]
                cmd = _escaped_pct.sub('%', cmd)

                # Ensure the crontab line is valid
                try:
                    croniter(interval)
                    if not cmd:
                        raise ValueError("Missing command")
                except (KeyError, ValueError) as e:
                    if isinstance(e, KeyError):
                        e = "Bad time interval syntax, %s " % e
                    # Replace croniter's typo-riddled error msg
                    elif str(e) == ("Exactly 5 or 6 columns has to be "
                                    "specified for iteratorexpression."):
                        e = ("Less than 5 fields separated by whitespace in "
                             "the time interval (requires 5 or 6)")
                    e_str += "Error in line %i: %s\n" % (i + 1, e)
                else:
                    if not e_str:
                        job = None
                        # Check if job was in the old crontab
                        if line in old_tab:
                            for old_job in old_jobs:
                                if (old_job.interval == interval and
                                        old_job.command == cmd and
                                        old_job.job_input == job_input and
                                        old_job.environment == os.environ):
                                    job = old_job
                                    old_jobs.remove(old_job)
                                    break
                        if not job:
                            old_tab.discard(line)
                            try:
                                index = environs.index(os.environ)
                            except ValueError:
                                index = len(environs)
                                environs.append(os.environ.copy())
                            job = api.Job(interval, cmd, uid, index,
                                          job_input, datetime.now())
                        jobs.append(job)
    # Prompt user to edit crontab on error
    if e_str:
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
    api.set_environs(environs, uid)
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
            sys.exit("User `%s' does not exist." % opts.usr)
    # If no user is specified, set to current user (euid or uid?)
    else:
        opts.usr = (usr_euid, pwd.getpwuid(usr_euid).pw_name)

    check_permissions(opts.usr, usr_euid)

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

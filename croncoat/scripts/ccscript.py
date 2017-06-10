#!/usr/bin/env python

"""
croncoat
~~~~~~~~~~~~~~
A cron job wrapper that wraps jobs and enables better error reporting and command timeouts.
croncoat added: python mail handling, better subject lines, timeout kills ongoing tasks,
object-oriented design

    :copyright (cronwrap): 2010 by Plurk
    :copyright: 2015 by Matthias Kauer
    :license: BSD
"""
import argparse
import sys
import os
from croncoat.cc.cronwrapper import CronWrapper
from croncoat import __version__, __scriptname__

class MyParser(argparse.ArgumentParser):
    """custom parser class so I can output help whenever wrong / bad / no arguments are supplied"""
#  http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    def error(self, message):
        sys.stderr.write('error: %s\n\n' % message)
        self.print_help()
        sys.exit(2)


desc_str =  (
"""Wrap cron jobs for better error email error reporting with command timeouts.
Version {}
You must create a config file (~/.{}.ini by default) to store smtp server data.
Ideally this would be readable only by you.
To output a config skeleton, use {} --print-ini

Usage examples:
===============
Send test email:
{} -e test@domain.org

Send email after killing a script that takes longer than 5s
{} -t 5s -c 'sleep 10s' -e test@domain.org

Print to stdout after catching error in script;
Note: this won't work with exit(1) b/c no real shell here
{} -c 'python -c import sys; sys.exit(1)'

Print no output for successful command
{} -c 'ls -la'
Print output of successful command
{} -v -c 'ls -la'""").format(__version__, *([__scriptname__] * 7))

#  if __name__ == '__main__':
def main(input_args=None):
    parser = MyParser(prog=__scriptname__, description=desc_str, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-c', '--cmd',
                        help='Run a command. Could be `%s -c "ls -la"`. No command => test email is sent.' % __scriptname__
                        )

    parser.add_argument('-e', '--emails',
                        help='Send email to the following addresses if the command crashes or exceeds timeout. '
                        "Uses Python's email library to send emails (therefore no user names"
                        "unlike original cronwrap). "
                        "If this is not set, only output to stdout."
                        )

    parser.add_argument('-t', '--time',
                        help='Set the maximum running time. '
                        'If this time is reached, the script will be killed and an alert email will be sent. '
                        "If the script is killed stdout/stderr cannot be captured at this time! "
                        "The default is 1 hour `-t 1h`. Possible values include: `-t 2h`,`-t 5m`, `-t 30s`."
                        )

    parser.add_argument('--print-ini', '--print-config', nargs='?', default=False,
                        help='Print the configuration file format. '
                            'This can be redirected to a file name to have a config skeleton.'
                        )

    parser.add_argument('--config', '--ini', '-i', default=False,
                        help='use an .ini file with custom name and path  '
                        "(not the default .croncoat.ini in users' home directory"
                        )

    parser.add_argument('-v', '--verbose',
                        nargs='?', default=False,
                        help='Will send an email / print to stdout even on successful run.')

    sys_args = parser.parse_args(input_args)
    if(sys_args.print_ini is not False):
        CronWrapper.print_ini(__scriptname__)
    elif(sys_args.cmd is None and sys_args.emails is None):
        sys.stderr.write('error: neither command nor email was supplied;'
             'email alone => test email, command alone => console output\n\n')
        parser.print_help()
        sys.exit(1)
    else:
        if sys_args.config is not False:
            configpath = os.path.realpath(sys_args.config)
        else: # default
            configpath = os.path.expanduser("~/.%s.ini" % __scriptname__)
        if os.path.exists(configpath) and os.path.isfile(configpath):
            #  print(configpath)
            cwrap = CronWrapper(sys_args, __scriptname__, configpath)
            cwrap.run()
        else:
            sys.exit("no config file detected at %s" %configpath)



#!/usr/bin/env python

"""
    cronwrap
    ~~~~~~~~~~~~~~

    A cron job wrapper that wraps jobs and enables better error reporting and command timeouts.

    Example of usage::

        #Will print out help
        $ cronwrap -h

        #Will send out a timeout alert to cron@my_domain.com:
        $ cronwrap -c "sleep 2" -t "1s" -e cron@my_domain.com

        #Will send out an error alert to cron@my_domain.com:
        $ cronwrap -c "blah" -t "1s" -e cron@my_domain.com

        #Will not send any reports:
        $ cronwrap -c "ls" -e cron@my_domain.com

        #Will send a successful report to cron@my_domain.com:
        $ cronwrap -c "ls" -e cron@my_domain.com -v

    :copyright: 2010 by Plurk
    :license: BSD
"""
__VERSION__ = '2.0'
__scriptname__ = 'cwrap2'

#  import re
import argparse
from cronwrap.cw.cronwrapper import CronWrapper
#  import cronwrap.cw.cronwrapper
#  import tempfile

#--- Handlers ----------------------------------------------


#  if __name__ == '__main__':
def main(input_args=None):
    desc_str = "A cron job wrapper that wraps jobs and enables better error reporting and command timeouts. Version %s" % __VERSION__
    desc_str += "\nYou must create a config file ~/.%s.ini to store smtp server data (preferably readable only by you)" %__scriptname__
    desc_str += "\nTo output the format, use %s --ini" % __scriptname__
    desc_str += "\nUsage examples:" 
    desc_str += """
    %s -t 5s -c 'sleep 10s' -e test@domain.org
    %s -c 'python -c "import sys; sys.exit(1)"'
    %s -v -c 'ls -la'
    %s -c 'ls -la'
""" % ((__scriptname__,) * 4)
    parser = argparse.ArgumentParser(prog=__scriptname__, description=desc_str, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-c', '--cmd', 
                        help='Run a command. Could be `%s -c "ls -la"`. No command => test email is sent.' % __scriptname__
                        )
#     parser.add_argument('-f', '--fromaddr', help='Specify sender address for your emails. Must match your local smtp setup.')

    parser.add_argument('-e', '--emails',
                        help='Send email to the following addresses if the command crashes or exceeds timeout. '
                        "Uses Python's email library to send emails (therefore no user names unlike original cronwrap). "
                        "If this is not set, only output to stdout." 
                        )

    parser.add_argument('-t', '--time',
                        help='Set the maximum running time. '
                        'If this time is reached, the script will be killed and an alert email will be sent. '
                        "If the script is killed stdout/stderr cannot be captured at this time! "
                        "The default is 1 hour `-t 1h`. Possible values include: `-t 2h`,`-t 5m`, `-t 30s`."
                        )
    
    parser.add_argument('--ini', nargs='?', default=False,
                        help='Print the configuration file format. '  
                        )

    parser.add_argument('-v', '--verbose',
                        nargs='?', default=False,
                        help='Will send an email / print to stdout even on successful run.')

#     parser.add_argument('-k', '--kill', nargs='?', default=False, help='Terminate process after timeout (as set by -t) is exceeded.')

    #  handle_args(parser.parse_args())
    sys_args = parser.parse_args(input_args)
    if(sys_args.ini is not False):
        CronWrapper.print_ini(__scriptname__)
    else:
        cwrap = CronWrapper(sys_args, __scriptname__)
        cwrap.run()


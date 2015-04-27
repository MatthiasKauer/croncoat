#!/usr/bin/env python

"""
    croncoat
    ~~~~~~~~~~~~~~

    A cron job wrapper that wraps jobs and enables better error reporting and command timeouts.

    Example of usage::

        #Will print out help
        $ croncoat -h

        #Will send out a timeout alert to cron@my_domain.com:
        $ croncoat -c "sleep 2" -t "1s" -e cron@my_domain.com

        #Will send out an error alert to cron@my_domain.com:
        $ croncoat -c "blah" -t "1s" -e cron@my_domain.com

        #Will not send any reports:
        $ croncoat -c "ls" -e cron@my_domain.com

        #Will send a successful report to cron@my_domain.com:
        $ croncoat -c "ls" -e cron@my_domain.com -v

    :copyright: 2010 by Plurk
    :license: BSD
"""
__VERSION__ = '2.0'
__scriptname__ = 'croncoat'

#  import re
import argparse
from cronwrap.cw.cronwrapper import CronWrapper

#--- Handlers ----------------------------------------------


#  if __name__ == '__main__':
def main(input_args=None):
    desc_str = "A cron job wrapper that wraps jobs and enables better error reporting and command timeouts. Version %s" % __VERSION__
    desc_str += "\nYou must create a config file ~/.%s.ini to store smtp server data (preferably readable only by you)" %__scriptname__
    desc_str += "\nTo output the format, use %s --ini" % __scriptname__
    desc_str += "\nUsage examples:" 
    desc_str += """
    Send test email: 
        %s -e test@domain.org
    Send email after killing a script that takes longer than 5s
        %s -t 5s -c 'sleep 10s' -e test@domain.org
    Print to stdout after catching error in script; 
    Note: this won't work with exit(1) b/c no real shell here 
        %s -c 'python -c "import sys; sys.exit(1)"'
    Print no output for successful command
        %s -c 'ls -la'
    Print output of successful command
        %s -v -c 'ls -la'
""" % ((__scriptname__,) * 5)
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


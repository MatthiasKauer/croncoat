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

#  import re
import argparse
from cronwrap.cw.cronwrapper import CronWrapper
#  import tempfile

#--- Handlers ----------------------------------------------


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A cron job wrapper that wraps jobs and enables better error reporting and command timeouts. Version %s" % __VERSION__)

    parser.add_argument('-c', '--cmd', help='Run a command. Could be `cronwrap -c "ls -la"`.')
    parser.add_argument('-f', '--fromaddr', help='Specify sender address for your emails. Must match your local smtp setup.')

    parser.add_argument('-e', '--emails',
                        help='Email following users if the command crashes or exceeds timeout. '
                        'Could be `cronwrap -e "johndoe@mail.com, marcy@mail.com"`. '
                        "Uses system's `mail` to send emails. If no command (cmd) is set a test email is sent.")

    parser.add_argument('-t', '--time',
                        help='Set the maximum running time.'
                        'If this time is passed an alert email will be sent.'
                        "The command will keep running even if maximum running time is exceeded."
                        "The default is 1 hour `-t 1h`. "
                        "Possible values include: `-t 2h`,`-t 2m`, `-t 30s`."
                        )

    parser.add_argument('-v', '--verbose',
                        nargs='?', default=False,
                        help='Will send an email / print to stdout on successful run.')

    parser.add_argument('-k', '--kill', nargs='?', default=False, help='Terminate process after timeout (as set by -t) is exceeded.')

    #  handle_args(parser.parse_args())
    cw = CronWrapper(parser.parse_args())
    cw.run()


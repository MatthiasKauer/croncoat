"""
Helper
~~~~~~~~~~~~~~
contains helper functionality: trimming messages, parsing time

    :copyright (cronwrap): 2010 by Plurk
    :license: BSD
"""

import re
from datetime import datetime, timedelta

class Helper(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
#         self.sname = scriptname
        pass
    
    @staticmethod
    def parse_time_to_secs(arg_time):
        #Parse sys_args.time
        max_time = arg_time
        sp = re.match("(\d+)([hms])", max_time).groups()
        t_val, t_unit = int(sp[0]), sp[1]

        #Convert time to seconds
        if t_unit == 'h':
            t_val = t_val * 60 * 60
        elif t_unit == 'm':
            t_val = t_val * 60

        return t_val
    
    @staticmethod
    def trim_if_needed(txt, max_length=10000):
        if len(txt) > max_length:
            return '... START TRUNCATED...\n%s' % txt[-max_length:]
        else:
            return txt
        
    @staticmethod
    def render_email_template(title, sys_args, cmd):
        result_str = []

        result_str.append(title)
        result_str.append('%s\n' % sys_args.cmd)

        result_str.append('COMMAND STARTED:')
        result_str.append('%s UTC\n' % (datetime.utcnow() -
                                        timedelta(seconds=int(cmd.run_time))))

        result_str.append('COMMAND FINISHED:')
        result_str.append('%s UTC\n' % datetime.utcnow())

        result_str.append('COMMAND RAN FOR:')
        hours = cmd.run_time / 60 / 60
        if cmd.run_time < 60:
            hours = 0
        result_str.append('%d seconds (%.2f hours)\n' % (cmd.run_time, hours))

        result_str.append("COMMAND'S TIMEOUT IS SET AT:")
        result_str.append('%s\n' % sys_args.time)

        result_str.append('RETURN CODE WAS:')
        result_str.append('%s\n' % cmd.returncode)

        result_str.append('ERROR OUTPUT:')
        result_str.append('%s\n' % Helper.trim_if_needed(cmd.stderr))

        result_str.append('STANDARD OUTPUT:')
        result_str.append('%s' % Helper.trim_if_needed(cmd.stdout))

        return '\n'.join(result_str)
    
    @staticmethod
    def is_time_exceeded(sys_args, cmd):
        """Returns `True` if the command's run time has exceeded the maximum
        run time specified in command arguments. Else `False  is returned."""
        cmd_time = int(cmd.run_time)

        t_val = Helper.parse_time_to_secs(sys_args.time)
        return cmd_time > t_val

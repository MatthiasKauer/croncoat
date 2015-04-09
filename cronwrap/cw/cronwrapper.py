import platform
import time
import os
import sys
import re
from datetime import datetime, timedelta
from cronwrap.cw.expiringcommand import ExpiringCommand
from cronwrap.cw.mailbackend import MailBackend

class CronWrapper(object):
    def __init__(self, sys_args):
        """Handles comamnds that are parsed via argparse."""
        if not sys_args.time:
            sys_args.time = '1h'

        if sys_args.verbose is not False:
            sys_args.verbose = True

        if sys_args.kill is not False:
            sys_args.kill = True

        self.sys_args = sys_args

        self.mailer = MailBackend()

    def run(self):
        sys_args = self.sys_args
        if sys_args.cmd:
            self.cmd = ExpiringCommand( sys_args.cmd, sys_args.time)
            self.cmd.Run()
            if self.cmd.returncode != 0:
                self.handle_error()
            elif self.is_time_exceeded():
                self.handle_timeout()
            else:
                handle_success()
        elif sys_args.emails:
            handle_test_email()


    def handle_success(self):
        sys_args = self.sysargs; cmd = self.cmd
        """Called if a command did finish successfuly."""
        out_str = render_email_template(
            'CRONWRAP RAN COMMAND SUCCESSFULLY:',
            sys_args,
            cmd
        )

        if sys_args.verbose:
            if sys_args.emails:
                send_email(sys_args,
                           sys_args.emails,
                           'Host %s: cronwrap ran command successfully!'
                           % platform.node().capitalize(),
                           out_str)
            else:
                print out_str


    def handle_timeout(self):
        """Called if a command exceeds its running time."""

        sys_args = self.sysargs; cmd = self.cmd
        err_str = render_email_template(
            "CRONWRAP DETECTED A TIMEOUT ON FOLLOWING COMMAND:",
            sys_args,
            cmd
        )

        if sys_args.emails:
            send_email(sys_args,
                       sys_args.emails,
                       'Host %s: cronwrap detected a timeout!'
                       % platform.node().capitalize(),
                       err_str)
        else:
            print err_str


    def handle_error(self):
        """Called when a command did not finish successfully."""
        sys_args = self.sysargs; cmd = self.cmd

        err_str = render_email_template(
            "CRONWRAP DETECTED FAILURE OR ERROR OUTPUT FOR THE COMMAND:",
            sys_args,
            cmd
        )

        if sys_args.emails:
            send_email(sys_args,
                       sys_args.emails,
                       'Host %s: cronwrap detected a failure!'
                       % platform.node().capitalize(),
                       err_str)
        else:
            print err_str

        sys.exit(-1)

    def handle_test_email(self):
        subject = 'Host %s: cronwrap test mail'% platform.node().capitalize()
        content = 'just a test mail, yo! :)'

        self.send_email(subject, content)


    def send_email(subject, content):
        """Sends an email via `mail`."""
        emails = self.sys_args.emails
        emails = emails.split(',')

        for toaddr in emails:
            emailMsg = email.MIMEMultipart.MIMEMultipart('mixed')
            emailMsg['To'] = toaddr
            emailMsg['From'] = sys_args.fromaddr
            emailMsg['Subject'] = subject.replace('"', "'")
            emailMsg.attach(email.mime.Text.MIMEText(message, _charset='utf-8'))
            self.mailer.sendmail(emailMsg)
            #  smtp.sendmail(emailMsg['From'], emailMsg['To'], emailMsg.as_string())
                    
    #      else:
    #          fp_err_report = open(err_report, "w")
    #          fp_err_report.write(message)
    #          fp_err_report.close()
#  
    #          try:
    #              for email in emails:
    #                  if sys_args.fromaddr:
    #                      cmd = Command('mail -s "%s" -a "From: %s" %s < %s' %
    #                                (subject.replace('"', "'"),
    #                                  sys_args.fromaddr,
    #                                 email,
    #                                 err_report)
    #                                )
    #                  else:
    #                      cmd = Command('mail -s "%s" %s < %s' %
    #                                (subject.replace('"', "'"),
    #                                 email,
    #                                 err_report)
    #                                )
#  
    #                  if sys_args.verbose:
    #                      if cmd.returncode == 0:
    #                          print 'Sent an email to %s' % email
    #                      else:
    #                          print 'Could not send an email to %s' % email
    #                          print trim_if_needed(cmd.stderr)
    #          finally:
    #              os.remove(err_report)
#  
    @staticmethod
    def is_time_exceeded(sys_args, cmd):
        """Returns `True` if the command's run time has exceeded the maximum
        run time specified in command arguments. Else `False  is returned."""
        cmd_time = int(cmd.run_time)

        t_val = parse_time_to_secs(sys_args.time)
        return cmd_time > t_val

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


    def render_email_template(self, title, sys_args, cmd):
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
        result_str.append('%s\n' % self.trim_if_needed(cmd.stderr))

        result_str.append('STANDARD OUTPUT:')
        result_str.append('%s' % self.trim_if_needed(cmd.stdout))

        return '\n'.join(result_str)




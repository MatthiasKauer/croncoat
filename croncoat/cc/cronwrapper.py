"""
CronWrapper
~~~~~~~~~~~~~~
Main module linking together mail backend, helper scripts for, e.g., output trimming;
handles command lines as parsed by ccscript

    :copyright (cronwrap): 2010 by Plurk
    :copyright: 2015 by Matthias Kauer
    :license: BSD
"""

import platform
import sys
import email
from croncoat.cc.expiringcommand import ExpiringCommand
from croncoat.cc.mailbackend import MailBackend
from croncoat.cc.helper import Helper

class CronWrapper(object):
    def __init__(self, sys_args, scriptname, configpath):
        self.scriptname = scriptname
        self.subjectname = "cc"

        if not sys_args.time:
            sys_args.time = '1h'

        if sys_args.verbose is not False:
            sys_args.verbose = True

        self.sys_args = sys_args
        self.mailer = MailBackend(configpath)

    def run(self):
        sys_args = self.sys_args
        if sys_args.cmd:
            self.cmd = ExpiringCommand( sys_args.cmd, sys_args.time)
            self.cmd.Run()
            if self.cmd.returncode != 0:
                self.handle_error()
            elif Helper.is_time_exceeded(self.sys_args, self.cmd):
                self.handle_timeout()
            else:
                self.handle_success()
        elif sys_args.emails:
            self.handle_test_email()

    @staticmethod
    def _ini_string(scriptname):
        return (
"""#example format for ~/.{}.ini (don't use quotes!)
[Mail]
smtpserver=
smtpport=
user=
pass=
fromaddr=
security=ssl    ;ssl, starttls or none
""".format(scriptname))

    @staticmethod
    def print_ini(scriptname):
        print CronWrapper._ini_string(scriptname)

    def handle_success(self):
        sys_args = self.sys_args; cmd = self.cmd
        """Called if a command did finish successfuly."""
        content_elem = 'RAN COMMAND SUCCESSFULLY'
        subj_elem='success'

        if sys_args.verbose:
            self.handle_general(subj_elem=subj_elem, content_elem=content_elem);

    def handle_general(self, subj_elem, content_elem):
        sys_args = self.sys_args; cmd = self.cmd
        out_str = Helper.render_email_template('%s %s: ' % \
                (self.scriptname, content_elem), sys_args, cmd)
        subj_str='%s (%s): %s [%s]' % \
                (sys_args.cmd[:20],
                            platform.node().capitalize(), subj_elem, self.scriptname)

        if sys_args.emails:
            self.send_email(subject=subj_str, content=out_str)
            #  self.handle_general(subj_str=subj_str, content_str=out_str);
        else:
            print out_str

    def handle_timeout(self):
        """Called if a command exceeds its running time."""

        sys_args = self.sysargs; cmd = self.cmd
        content_elem = 'DETECTED A TIMEOUT ON FOLLOWING COMMAND'
        subj_elem= 'timeout'

        self.handle_general(subj_elem=subj_elem, content_elem=content_elem);

    def handle_error(self):
        """Called when a command did not finish successfully."""
        sys_args = self.sys_args; cmd = self.cmd

        content_elem = 'DETECTED FAILURE OR ERROR OUTPUT FOR THE COMMAND'
        subj_elem= 'failure'

        self.handle_general(subj_elem=subj_elem, content_elem=content_elem);
        sys.exit(-1)

    def handle_test_email(self):
        subject='%s (%s): Testing' % \
                (self.subjectname, platform.node().capitalize())
        content = 'just a test mail, yo! :)'
        self.send_email(subject, content)


    def send_email(self, subject, content):
        """Sends an email via MailBackend (python email lib there)."""
        emails = self.sys_args.emails
        emails = emails.split(',')

        for toaddr in emails:
            emailMsg = email.MIMEMultipart.MIMEMultipart('mixed')
            emailMsg['To'] = toaddr
            #             emailMsg['From'] = sys_args.fromaddr
            emailMsg['Subject'] = subject.replace('"', "'")
            emailMsg.attach(email.mime.Text.MIMEText(content, _charset='utf-8'))
            self.mailer.sendmail(emailMsg)


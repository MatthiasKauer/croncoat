import platform
import sys
import email
from cronwrap.cw.expiringcommand import ExpiringCommand
from cronwrap.cw.mailbackend import MailBackend
from cronwrap.cw.helper import Helper


class CronWrapper(object):
    def __init__(self, sys_args, scriptname):
        """Handles comamnds that are parsed via argparse."""
        self.scriptname = scriptname
        
        if not sys_args.time:
            sys_args.time = '1h'

        if sys_args.verbose is not False:
            sys_args.verbose = True
            
#         if sys_args.ini is not False:
#             self.sys_args = True
#         if sys_args.kill is not False:
#             sys_args.kill = True

        self.sys_args = sys_args

        self.mailer = MailBackend(scriptname)

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
    def print_ini(scriptname):
        example_ini = "#example format for ~/.%s.ini (don't use quotes!)" % scriptname
        example_ini +="""
[Mail]
smtpserver=
smtpport=
user=
pass=
fromaddr=
"""
        print(example_ini)

    def handle_success(self):
        sys_args = self.sys_args; cmd = self.cmd
        """Called if a command did finish successfuly."""
        out_str = Helper.render_email_template(
            '%s RAN COMMAND SUCCESSFULLY:' % self.scriptname,
            sys_args,
            cmd
        )

        if sys_args.verbose:
            if sys_args.emails:
                self.send_email(subject='%s (%s - %s): successful execution!' %
                       (self.scriptname, platform.node().capitalize(), Helper.trim_if_needed(cmd, max_length=20)),
                           content=out_str)
            else:
                print out_str


    def handle_timeout(self):
        """Called if a command exceeds its running time."""

        sys_args = self.sysargs; cmd = self.cmd
        err_str = Helper.render_email_template(
            "%s DETECTED A TIMEOUT ON FOLLOWING COMMAND:" % self.scriptname,
            sys_args,
            cmd
        )

        if sys_args.emails:
            self.send_email(subject='%s (%s - %s): timeout detected!' %
                       (self.scriptname, platform.node().capitalize(), Helper.trim_if_needed(cmd, max_length=20)),
                       content=err_str)
        else:
            print err_str


    def handle_error(self):
        """Called when a command did not finish successfully."""
        sys_args = self.sys_args; cmd = self.cmd

        err_str = Helper.render_email_template(
            "%s DETECTED FAILURE OR ERROR OUTPUT FOR THE COMMAND:" % self.scriptname,
            sys_args,
            cmd
        )

        if sys_args.emails:
            self.send_email(subject='%s (%s - %s): failure detected!' %
                       (self.scriptname, platform.node().capitalize(), Helper.trim_if_needed(cmd, max_length=20)),
                       content=err_str)
        else:
            print err_str

        sys.exit(-1)

    def handle_test_email(self):
        subject='%s (%s - %s): Testing' % \
                   (self.scriptname, platform.node().capitalize(), Helper.trim_if_needed("test email", max_length=20)),
        # subject = 'Host %s: %s test mail'% (platform.node().capitalize(), self.scriptname)
        content = 'just a test mail, yo! :)'

        self.send_email(subject, content)


    def send_email(self, subject, content):
        """Sends an email via `mail`."""
        emails = self.sys_args.emails
        emails = emails.split(',')
        
        for toaddr in emails:
            emailMsg = email.MIMEMultipart.MIMEMultipart('mixed')
            emailMsg['To'] = toaddr
#             emailMsg['From'] = sys_args.fromaddr
            emailMsg['Subject'] = subject.replace('"', "'")
            emailMsg.attach(email.mime.Text.MIMEText(content, _charset='utf-8'))
            self.mailer.sendmail(emailMsg)
            #  smtp.sendmail(emailMsg['From'], emailMsg['To'], emailMsg.as_string())
                    







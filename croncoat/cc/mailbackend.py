"""
MailBackend
~~~~~~~~~~~~~~
reads smtp config from ini file and sends out emails as directed by main

    :copyright: 2015 by Matthias Kauer
    :license: BSD
"""

from smtplib import SMTP_SSL
import os
import ConfigParser

class MailBackend(object):

    def __init__(self, scriptpath):
        self.smtp = SMTP_SSL()
        default_configvalues = {'use_sendmailfallback': False,
                                'sendmail_path': '/usr/sbin/sendmail'}
        self.cfg = ConfigParser.SafeConfigParser(defaults=default_configvalues)
        fname = os.path.realpath(scriptpath)
        try:
            self.cfg.read(fname)
            self.server = self.cfg.get('Mail', 'smtpserver')
            self.port = self.cfg.get('Mail', 'smtpport')
            self.mailuser = self.cfg.get('Mail','user')
            self.mailpass = self.cfg.get('Mail','pass')
            self.fromaddr = self.cfg.get('Mail', 'fromaddr')
            self.loggedin = False
        except Exception, e:
            import sys
            sys.exit( "%s appears not to be an .ini file with the appropriate sections.\n \
Call 'croncoat --ini' for an example layout of the .ini file" %scriptpath )


    def sendmail(self, emailMsg):
        try:
            if(not self.loggedin):
                emailMsg['From']=self.fromaddr
                self.smtp.connect(self.server, self.port)
                self.smtp.login(self.mailuser, self.mailpass)
                self.loggedin = True
            self.smtp.sendmail(emailMsg['From'], emailMsg['To'], emailMsg.as_string())
        except Exception, e:
            print "sendmail exception: %s" %str(e)
            if self.cfg.get('Mail', 'use_sendmailfallback', False):
                from subprocess import Popen, PIPE
                sendmailpath = self.cfg.get('Mail', 'sendmail_path')
                sm_proc = Popen([sendmailpath, "-t", "-oi"], stdin=PIPE)
                sm_proc.communicate(emailMsg.as_string())
                print "(sendmail fallback used)"

    def __exit__(self):
        print("exiting MailBackend")
        self.smtp.quit()




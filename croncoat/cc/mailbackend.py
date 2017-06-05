"""
MailBackend
~~~~~~~~~~~~~~
reads smtp config from ini file and sends out emails as directed by main

    :copyright: 2015 by Matthias Kauer
    :license: BSD
"""

from smtplib import SMTP_SSL
import os
import logging

class MailBackend(object):

    def __init__(self, cfg):
        self.smtp = SMTP_SSL()
        self.logger = logging.getLogger('croncoat')
        try:
            self.cfg = cfg
            self.server = self.cfg.get('Mail', 'smtpserver')
            self.port = self.cfg.get('Mail', 'smtpport')
            self.mailuser = self.cfg.get('Mail','user')
            self.mailpass = self.cfg.get('Mail','pass')
            self.fromaddr = self.cfg.get('Mail', 'fromaddr')
            self.loggedin = False
        except Exception, e:
            msg = "%s appears not to be an .ini file with the appropriate sections.\n \
Call 'croncoat --ini' for an example layout of the .ini file" %scriptpath
            self.logger.error(msg)
            import sys
            sys.exit(msg)


    def sendmail(self, emailMsg):
        try:
            if(not self.loggedin):
                emailMsg['From']=self.fromaddr
                self.smtp.connect(self.server, self.port)
                self.smtp.login(self.mailuser, self.mailpass)
                self.loggedin = True
            self.smtp.sendmail(emailMsg['From'], emailMsg['To'], emailMsg.as_string())
        except Exception, e:
            self.logger.error("sendmail exception: %s" %str(e))
            if self.cfg.getboolean('Mail', 'use_sendmailfallback'):
                self.use_sendmailfallback(emailMsg)
            else:
                self.logger.info('sendmail fallback not used')

    def use_sendmailfallback(self, emailMsg):
        try:
            from subprocess import Popen, PIPE                
            sendmailpath = self.cfg.get('Mail', 'sendmail_path')
            sm_proc = Popen([sendmailpath, "-t", "-oi"], stdin=PIPE)
            sm_proc.communicate(emailMsg.as_string())
            self.logger.info("sendmail fallback used")
        except Exception, e:
            msg = "use_sendmailfallback exception: Executable path: %s -  Error: %s" %(sendmailpath, str(e))
            self.logger.error(msg)           
            
    def __exit__(self):
        self.logger.debug("exiting MailBackend")
        self.smtp.quit()




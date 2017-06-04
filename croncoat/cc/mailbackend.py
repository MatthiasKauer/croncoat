"""
MailBackend
~~~~~~~~~~~~~
reads smtp config from ini file and sends out emails as directed by main

    :copyright: 2015 by Matthias Kauer
    :license: BSD
"""

from smtplib import SMTP_SSL, SMTP
import os
import ConfigParser

class MailBackend(object):
    def __init__(self, scriptpath):
        self.cfg = ConfigParser.SafeConfigParser()
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
        try:
            self.starttls = self.cfg.get('Mail', 'starttls')
        except Exception, e:
            self.starttls = 'No'


    def sendmail(self, emailMsg):
        if(not self.loggedin):
            emailMsg['From']=self.fromaddr

            if self.starttls in [True,1,"1","True","TRUE","true","yes","Yes","YES"]:
                self.smtp = SMTP(self.server, int(self.port))
                self.smtp.starttls()
            else:
                self.smtp = SMTP_SSL(self.server, self.port)
            self.smtp.login(self.mailuser, self.mailpass)

            self.loggedin = True

        self.smtp.sendmail(emailMsg['From'], emailMsg['To'], emailMsg.as_string())

    def __exit__(self):
        print("exiting MailBackend")
        self.smtp.quit()
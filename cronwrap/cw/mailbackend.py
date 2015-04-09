from smtplib import SMTP_SSL
import os
import ConfigParser

class MailBackend(object):
    def __init__(self):
        self.smtp = SMTP_SSL()
        self.cfg = ConfigParser.SafeConfigParser()
        fname = os.path.expanduser('~/.cronwrap.ini')
        self.cfg.read(fname)

        print(self.cfg.sections())
        #  print(self.cfg.options('Mail'))
        server = self.cfg.get('Mail', 'smtpserver')
        port = self.cfg.get('Mail', 'smtpport')
        mailuser = self.cfg.get('Mail','user')
        mailpass = self.cfg.get('Mail','pass')
        self.fromaddr = self.cfg.get('Mail', 'fromaddr')
        #  if False: #appears to be python 3 only
        #  server = self.cfg['Mail']['smtpserver']
        #  port = self.cfg['Mail']['smtpport']
        #  mailuser = self.cfg['Mail']['user']
        #  mailpass = self.cfg['Mail']['pass']
        #  self.fromaddr = self.cfg['Mail']['fromaddr']
        print(server, port, mailuser, mailpass, self.fromaddr)

        self.loggedin = False
        

    def sendmail(self, emailMsg):
        if(not self.loggedin):
            self.smtp.connect(server, port)
            self.smtp.login(mailuser, mailpass)
            self.loggedin = True

        self.smtp.sendmail(emailMsg['From'], emailMsg['To'], emailMsg.as_string())


    def __exit__(self):
        print("exiting MailBackend")
        self.smtp.quit()




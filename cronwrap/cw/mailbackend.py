from smtplib import SMTP_SSL
import os
import ConfigParser

class MailBackend(object):
    def __init__(self, scriptname):
        self.smtp = SMTP_SSL()
        self.cfg = ConfigParser.SafeConfigParser()
        fname = os.path.expanduser('~/.%s.ini' % scriptname)
        self.cfg.read(fname)

#         print(self.cfg.sections())
        #  print(self.cfg.options('Mail'))
        self.server = self.cfg.get('Mail', 'smtpserver')
        self.port = self.cfg.get('Mail', 'smtpport')
        self.mailuser = self.cfg.get('Mail','user')
        self.mailpass = self.cfg.get('Mail','pass')
        self.fromaddr = self.cfg.get('Mail', 'fromaddr')
        #  if False: #appears to be python 3 only
        #  server = self.cfg['Mail']['smtpserver']
        #  port = self.cfg['Mail']['smtpport']
        #  mailuser = self.cfg['Mail']['user']
        #  mailpass = self.cfg['Mail']['pass']
        #  self.fromaddr = self.cfg['Mail']['fromaddr']
        

        self.loggedin = False
        

    def sendmail(self, emailMsg):
        if(not self.loggedin):
#             print("Logging in to ", self.server, self.port, self.mailuser,
#                   self.mailpass, self.fromaddr)
            emailMsg['From']=self.fromaddr
            
            self.smtp.connect(self.server, self.port)
            self.smtp.login(self.mailuser, self.mailpass)
            self.loggedin = True

        self.smtp.sendmail(emailMsg['From'], emailMsg['To'], emailMsg.as_string())


    def __exit__(self):
        print("exiting MailBackend")
        self.smtp.quit()




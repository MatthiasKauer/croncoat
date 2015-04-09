from smtplib import SMTP_SSL
import ConfigParser

class MailBackend(object):
    def __init__(self):
        self.smtp = SMTP_SSL()
        self.cfg = ConfigParser.ConfigParser()
        self.cfg.read([~/.cronwrap.cfg])

        server = self.cfg['Mail']['smtpserver']
        port = self.cfg['Mail']['smtpport']
        mailuser = self.cfg['Mail']['user']
        mailpass = self.cfg['Mail']['pass']
        self.fromaddr = self.cfg['Mail']['fromaddr']
        
        self.smtp.connect(server, port)
        self.smtp.login(mailuser, mailpass)

    def sendmail(self, emailMsg):
        self.smtp.sendmail(emailMsg['From'], emailMsg['To'], emailMsg.as_string())


    def __exit__(self):
        print("exiting MailBackend")
        self.smtp.quit()




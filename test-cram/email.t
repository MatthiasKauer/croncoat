Setup

  $ export CCINI="$TESTDIR/cc.ini"
  $ alias croncoat="$TESTDIR/../bin/ccrun.py -i $CCINI"
  $ export CC_SMTP_PORT

  $ cat << EOF > $CCINI
  > [Mail]
  > smtpserver=localhost
  > smtpport=8025
  > user=bcoe
  > pass=foobar
  > fromaddr=cram@test.com
  > security=ssl
  > EOF

Start fake email server
  $ $TESTDIR/fakesmtp.py $TESTDIR/ssl_cert &
  $ CC_SMTP_PID=$!
  $ sleep 1


Send test email

  $ croncoat -e "admin@matthiaskauer.github.io"
  _accept_subprocess(): * (glob)
  _accept_subprocess(): * (glob)
  FakeCredentialValidator: you should replace this with an actual implementation of a credential validator.
  Content-Type: multipart/mixed; boundary="===============.*==" (re)
  MIME-Version: 1.0
  To: admin@matthiaskauer.github.io
  Subject: cc (.*): Testing (re)
  From: cram@test.com
  
  --==========.* (re)
  Content-Type: text/plain; charset="utf-8"
  MIME-Version: 1.0
  Content-Transfer-Encoding: base64
  
  anVzdCBhIHRlc3QgbWFpbCwgeW8hIDop
  
  --==========.* (re)
  _accept_subprocess(): asyncore loop exited.
.*To: admin@matthiaskauer.github.io.* (re)

Remove config file and end smtp server
  $ rm $CCINI
  $ kill $CC_SMTP_PID
  Got signal 15, shutting down.

Setup

  $ export CCINI="$TESTDIR/cc.ini"
  $ alias croncoat="$TESTDIR/../bin/ccrun.py -i $CCINI"
  $ export CC_SMTP_PORT

Start fake email server

python -m smtpd -n -c DebuggingServer localhost:8025 &

  $ $TESTDIR/fakesmtp.py $TESTDIR/ssl_cert &
  $ CC_SMTP_PID=$!

  $ cat << EOF > $CCINI
  > [Mail]
  > smtpserver=localhost
  > smtpport=8025
  > user=bcoe
  > pass=foobar
  > fromaddr=cram@test.com
  > starttls=0
  > EOF


Send test email

  $ croncoat -e "admin@matthiaskauer.github.io"
  _accept_subprocess(): * (glob)
  _accept_subprocess(): * (glob)
  FakeCredentialValidator: you should replace this with an actual implementation of a credential validator.
  Content-Type: multipart/mixed; boundary="===============.*==" (re)
  MIME-Version: 1.0
  To: admin@matthiaskauer.github.io
  Subject: cc (Xubfiend): Testing
  From: cram@test.com
  
  --==========.* (re)
  Content-Type: text/plain; charset="utf-8"
  MIME-Version: 1.0
  Content-Transfer-Encoding: base64
  
  anVzdCBhIHRlc3QgbWFpbCwgeW8hIDop
  
  --==========.* (re)
  _accept_subprocess(): asyncore loop exited.
.*To: admin@matthiaskauer.github.io.* (re)

End smtp server

  $ kill $CC_SMTP_PID
  Got signal 15, shutting down.

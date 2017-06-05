#!/usr/bin/env python
from __future__ import print_function
from secure_smtpd import SMTPServer, FakeCredentialValidator
import sys

class FakeSMTP(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, message_data):
        print(message_data)
        sys.stdout.flush()

if len(sys.argv) < 2:
    sys.stderr.write('Usage: sys.argv[0] [CERT_DIR]')
    sys.exit(1)
cert_dir = sys.argv[1]

s = FakeSMTP(
    ('localhost', 8025),
    None,
    require_authentication=True,
    ssl=True,
    certfile=cert_dir+'/server.crt',
    keyfile=cert_dir+'/server.key',
    credential_validator=FakeCredentialValidator(),
    #  maximum_execution_time = 1.0
)

s.run()

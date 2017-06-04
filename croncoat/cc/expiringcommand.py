"""
ExpiringCommand
===============
Runs a command but terminates it when the timeout expires.

This is a minimal wrapper around Popen with timeout from subprocess32
(backport of Py3 functionality).

    :copyright: 2017 Matthias Kauer
    :license: BSD
"""

import time
import subprocess32 as sp
import shlex
from croncoat.cc.helper import Helper


class ExpiringCommand(object):
    def __init__(self, command, timeout):
        self.cmd = shlex.split(command)
        self.timeout = Helper.parse_time_to_secs(timeout)
        self.start_time = time.time()

        self.stdout = "No stdout captured (yet?)"
        self.stderr = "No stderr captured (yet?)"

    def Run(self):
        self.p = sp.Popen(self.cmd,stderr=sp.PIPE, stdout=sp.PIPE, shell=False,
                universal_newlines=True)

        try:
            self.stdout, self.stderr = self.p.communicate(timeout=self.timeout)
            self.returncode = self.p.returncode
        except sp.TimeoutExpired:
            self.p.terminate()
            self.stdout, self.stderr = self.p.communicate()
            self.returncode = 1
        finally:
            self.run_time = time.time() - self.start_time


"""
ExpiringCommand
~~~~~~~~~~~~~~
Signal based implementation that starts a command and kills it once a timeout
is reached.
Caveat: Currently does not save stdout when command is killed

    :copyright: 2015 by Matthias Kauer
    :license: BSD
"""

import time
import signal
import subprocess
import shlex
from croncoat.cc.helper import Helper

class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

class ExpiringCommand(object):
    #http://stackoverflow.com/questions/1191374/subprocess-with-timeout

    def savereturn(self):
        self.run_time = time.time() - self.start_time
        self.returncode = self.p.returncode;

    def __init__(self, command, timeout):
        self.cmd = shlex.split(command)
        self.timeout = Helper.parse_time_to_secs(timeout)
        self.start_time = time.time()

        self.stdout = "No stdout captured yet"
        self.stderr = "No stderr captured yet"

    def Run(self):
        #  self.p = subprocess.Popen(self.cmd,stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False,
        #          universal_newlines=True)

        #  self.p = subprocess.Popen(self.cmd,stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False,
        #          universal_newlines=True)

        self.p = subprocess.check_output(self.cmd)

        # TODO: There is now a timeout parameter for check_output; weeh
        # https://stackoverflow.com/questions/1191374/using-module-subprocess-with-timeout


        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(self.timeout)

        #  self.stderr = "Can't capture output if terminated early (sorry, but I just spent 4h trying to get this)\n"
        #  self.stderr += "Best option at this points seems to be the queue implementation here: \n"
        #  self.stderr += "http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python\n"
        #  self.stdout = self.stderr

        try:
            self.p.wait()
            self.returncode = self.p.returncode
            self.stderr = self.p.stderr.read()
            self.stdout = self.p.stdout.read()
        except Alarm:
            self.p.terminate()

            so, se = self.p.communicate()
            print "so:", so, se
            #  so.seek(0)
            print "so", so
            #this didn't work
            #  self.stdout = []
            #  self.stderr = []
            #  for line in self.p.stdout:
            #      self.stdout.append(line)
            #  for line in self.p.stderr:
            #      self.stderr.append(line)

            self.returncode = 1
        finally:
            #  if not self.stdout:
            #      self.stdout = self.p.stdout.read()
            #  if not self.stderr:
            #      self.stderr = self.p.stderr.read()
            self.savereturn()



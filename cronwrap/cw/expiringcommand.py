import time
import signal
import subprocess
from cronwrap.cw.helper import Helper

class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

class ExpiringCommand(object):
    #http://stackoverflow.com/questions/1191374/subprocess-with-timeout
    
    def savereturn(self):
        self.run_time = time.time() - self.start_time
        self.returncode = self.p.returncode;
        #  self.stderr = self.p.stderr.read()
        #  self.stdout = self.p.stdout.read()
        #  (self.stdout, self.stderr) = self.p.communicate()
        #  self.stdout = ""

        #  self.stderr = "asdf"
        #  self.stdout = self.p.stdout.read()
        #  with open(self.outfile) as fout:
        #  with open(self.outfile) as fout, open(self.errfile) as ferr:
        #      self.stdout = fout.read()
        #      self.stderr = ferr.read()
        #      print("ExpSignal; stdout: %s %s" % (self.stdout, self.stderr))

    def __init__(self, command, timeout):
        self.cmd = command.split()
        self.timeout = Helper.parse_time_to_secs(timeout)
        self.start_time = time.time()

        self.outfile = 'stdout.txt'
        self.errfile = 'stderr.txt'

        #  self.p = subprocess.Popen(self.cmd,stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

    def Run(self):
        #  print("cmd: ", self.cmd)
        self.p = subprocess.Popen(self.cmd,stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=False,
                universal_newlines=True)
        #  with open(self.outfile, 'w') as fout, open(self.errfile, 'w') as ferr:
            #  self.p = subprocess.Popen(self.cmd,stderr=ferr, stdout=fout, shell=False)

        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(self.timeout)

        self.stderr = "Can't capture output if terminated early (sorry, but I just spent 4h trying to get this)\n"
        self.stderr += "Best option at this points seems to be the queue implementation here: \n"
        self.stderr += "http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python\n"
        self.stdout = self.stderr

        try:
            self.p.wait()
            self.returncode = self.p.returncode
            self.stderr = self.p.stderr.read()
            self.stdout = self.p.stdout.read()
        except Alarm:
            #  print("cmd %s timed out; killing now" % (self.cmd))
            self.p.terminate()

            #this didn't work
            #  self.stdout = []
            #  self.stderr = []
            #  for line in self.p.stdout:
            #      self.stdout.append(line)
            #  for line in self.p.stderr:
            #      self.stderr.append(line)


            #  self.returncode = -1
        finally:
            #  if not self.stdout:
            #      self.stdout = self.p.stdout.read()
            #  if not self.stderr:
            #      self.stderr = self.p.stderr.read()
            self.savereturn()



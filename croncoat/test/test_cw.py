"""
croncoat tests
~~~~~~~~~~~~~~

    :copyright: 2015 by Matthias Kauer
    :license: BSD
"""
import unittest
from croncoat.scripts.ccscript import main
from croncoat.cc.cronwrapper import CronWrapper
from croncoat import __scriptname__
import os

class Test(unittest.TestCase):
    
    def setUp(self):
        f = open('temp.ini', 'w')
        f.write(CronWrapper._ini_string(__scriptname__))
        f.close
        self.base_arg = ['-i', 'temp.ini']
        
    def tearDown(self):
        if os.path.exists('temp.ini'):
            os.remove('temp.ini')
        
    def test_expiring(self):
        input_args = self.base_arg + ["-t", "1s", "-c", "sleep 2"]
        with self.assertRaises(SystemExit):
            main(input_args)

        input_args = self.base_arg + ["-t", "3s", "-c", "sleep 2"]
        main(input_args) #does not raise

    def test_errorcode(self):
        input_args = self.base_arg + ['-c', 'python -c "import sys; sys.exit(1)"']
        with self.assertRaises(SystemExit):
            main(input_args)

    def test_success(self):
        input_args = self.base_arg + ['-c', 'ls -la']
        main(input_args)

        input_args = self.base_arg +  ['-v', '-c', 'ls -la']
        main(input_args)

if __name__ == "__main__":
    unittest.main()


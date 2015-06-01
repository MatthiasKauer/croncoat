"""
croncoat tests
~~~~~~~~~~~~~~

    :copyright: 2015 by Matthias Kauer
    :license: BSD
"""
import unittest
from croncoat.scripts.ccscript import main

class Test(unittest.TestCase):

    def test_expiring(self):
        input_args = ["-t", "1s", "-c", "sleep 2"]
        with self.assertRaises(SystemExit):
            main(input_args)
            
        input_args = ["-t", "3s", "-c", "sleep 2"]
        main(input_args) #does not raise
    
    def test_errorcode(self):
        input_args = ['-c', 'python -c "import sys; sys.exit(1)"']
        with self.assertRaises(SystemExit):
            main(input_args)

    def test_success(self):
        input_args = ['-c', 'ls -la']
        main(input_args)
        
        input_args = ['-v', '-c', 'ls -la']
        main(input_args)

if __name__ == "__main__":
    unittest.main()
    

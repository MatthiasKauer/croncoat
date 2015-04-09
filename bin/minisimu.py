'''
Created on 30 Jan, 2015

@author: matthias
'''
import sys

try:
    import _preamble
except ImportError:
    sys.exit(-1)

from fastsimu.scripts.minisimu import run
run()
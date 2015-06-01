'''
Created on 08 Apr, 2015

@author: matthias
'''
import sys

try:
    import _preamble
except ImportError:
    sys.exit(-1)

from croncoat.scripts.ccscript import main
main()

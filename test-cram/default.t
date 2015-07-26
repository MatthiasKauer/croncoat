Setup

  $ export CCINI="$TESTDIR/cc.ini"
  $ alias croncoat="$TESTDIR/../bin/ccrun.py -i $CCINI"

Running without config produces error

  $ croncoat -c 'ls -la'

Setting up config makes echo command succeed

  $ croncoat --print-ini > $CCINI
  $ croncoat -c "echo 'hello world'" -v
  croncoat RAN COMMAND SUCCESSFULLY: 
  echo 'hello world'
  
  COMMAND STARTED:
  .* (re)
  
  COMMAND FINISHED:
  .* (re)
  
  COMMAND RAN FOR:
  0 seconds (0.00 hours)
  
  COMMAND'S TIMEOUT IS SET AT:
  1h
  
  RETURN CODE WAS:
  0
  
  ERROR OUTPUT:
  
  
  STANDARD OUTPUT:
  hello world
  


A failing command creates an error

  $ croncoat -c 'python -c "import sys; sys.exit(1)"'
  croncoat DETECTED FAILURE OR ERROR OUTPUT FOR THE COMMAND: 
  python -c "import sys; sys.exit(1)"
  
  COMMAND STARTED:
  .* (re)
  
  COMMAND FINISHED:
  .* (re)
  
  COMMAND RAN FOR:
  0 seconds (0.00 hours)
  
  COMMAND'S TIMEOUT IS SET AT:
  1h
  
  RETURN CODE WAS:
  1
  
  ERROR OUTPUT:
  
  
  STANDARD OUTPUT:
  
  [255]

A timed out command creates an error
  $ croncoat -t 1s -c 'sleep 2'
  croncoat DETECTED FAILURE OR ERROR OUTPUT FOR THE COMMAND: 
  sleep 2
  
  COMMAND STARTED:
  .* (re)
  
  COMMAND FINISHED:
  .* (re)
  
  COMMAND RAN FOR:
  1 seconds (0.00 hours)
  
  COMMAND'S TIMEOUT IS SET AT:
  1s
  
  RETURN CODE WAS:
  None
  
  ERROR OUTPUT:
  Can't capture output if terminated early (sorry, but I just spent 4h trying to get this)
  Best option at this points seems to be the queue implementation here: 
  http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
  
  
  STANDARD OUTPUT:
  Can't capture output if terminated early (sorry, but I just spent 4h trying to get this)
  Best option at this points seems to be the queue implementation here: 
  http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
  
  [255]










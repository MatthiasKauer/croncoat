Setup

  $ export CCINI="$TESTDIR/cc.ini"
  $ alias croncoat="$TESTDIR/../bin/ccrun.py -i $CCINI"

Running without config produces error

  $ croncoat -c 'ls -la'
  no config file detected at .* (re)
  [1]

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
  $ croncoat -t 3s -c "$TESTDIR/sleep_and_echo.sh"
  croncoat DETECTED FAILURE OR ERROR OUTPUT FOR THE COMMAND: 
  */test-cram/sleep_and_echo.sh (glob)
  
  COMMAND STARTED:
  .* (re)
  
  COMMAND FINISHED:
  .* (re)
  
  COMMAND RAN FOR:
  4 seconds (0.00 hours)
  
  COMMAND'S TIMEOUT IS SET AT:
  3s
  
  RETURN CODE WAS:
  1
  
  ERROR OUTPUT:
  
  
  STANDARD OUTPUT:
  slept 1 times in total
  
  [255]


Removing config file at the end
  $ rm $CCINI








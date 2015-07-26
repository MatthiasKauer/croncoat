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
  












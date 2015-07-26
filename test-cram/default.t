Setup

  $ export CCINI="$TESTDIR/cc.ini"
  $ alias croncoat="$TESTDIR/../bin/ccrun.py -i $CCINI"

Running without config produces error

  $ croncoat -c 'ls -la'
  no config file detected at .* (re)
  [1]

Setting up config makes echo command succeed

$croncoat --print-ini > $INI_FILE
$croncoat -c "echo 'hello world'"



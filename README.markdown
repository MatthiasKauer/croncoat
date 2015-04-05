cronwrap
===========================================

A cron job wrapper that wraps jobs and enables better error reporting and command timeouts.


Installing
===========

To install cronwrap simply do::

    $ sudo easy_install cronwrap
    $ cronwrap -h


Example
===========

Basic example of usage::

    ##Will print out help
    $ cronwrap -h

        usage: cronwrap [-h] [-c CMD] [-e EMAILS] [-t TIME] [-v [VERBOSE]]

        A cron job wrapper that wraps jobs and enables better error reporting and command timeouts.

        optional arguments:
          -h, --help            show this help message and exit
          -c CMD, --cmd CMD     Run a command. Could be `cronwrap -c "ls -la"`.
          -e EMAILS, --emails EMAILS
                                Email following users if the command crashes or
                                exceeds timeout. Could be `cronwrap -e
                                "johndoe@mail.com, marcy@mail.com"`. Uses system's
                                `mail` to send emails. If no command (cmd) is set a
                                test email is sent.
          -t TIME, --time TIME  Set the maxium running time. If this time is passed an
                                alert email will be sent once the command ends.
                                The command will keep running even if maximum running time
                                is exceeded. Please note that this option doesn't
                                prevent the job from stalling and does nothing to
                                prevent running multiple cron jobs at the same time.
                                The default is 1 hour `-t 1h`. Possible values include:
                                `-t 2h`,`-t 2m`, `-t 30s`.
          -v [VERBOSE], --verbose [VERBOSE]
                                Will send an email / print to stdout on successful run.

          -f [EMAILADDRESS], --fromaddr [EMAILADDRESS] 
                                (experimental) Change the email address that cronwrap sends from.
                                This may be necessary on your system if your smtp server doesn't allow sending 
                                from the address that is the default.
          -k, --kill            (experimental) By default, cronwrap only monitors how much time a command
                                requires till completion. With this, commands are killed once the timeout is
                                reached. Unfortunately, we can currently not capture stdout/stderr for 
                                processes that were killed.


    ##Will send out a timeout alert to cron@my_domain.com:
    $ cronwrap -c "sleep 2" -t "1s" -e cron@my_domain.com

    ##Will send out an error alert to cron@my_domain.com:
    $ cronwrap -c "blah" -e cron@my_domain.com

    #Will not send any reports:
    $ cronwrap -c "ls" -e cron@my_domain.com

    #Will send a successful report to cron@my_domain.com:
    $ cronwrap -c "ls" -e cron@my_domain.com -v

    #(experimental): Kills process if it takes longer than 2 seconds and sends email from a@b.de to f@b.de
    $ cronwrap -c "sleep 10" -t 2s -k -e f@b.de -f a@b.de

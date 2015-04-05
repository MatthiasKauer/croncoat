import time
import argparse
parser = argparse.ArgumentParser(description='Throw error or not')
parser.add_argument('--err', dest='err', action='store_const',
                   default=False, const=True, help='should I throw error')

parser.add_argument('--exitcode', dest='code', action='store_const',
                   default=False, const=True, help='should I change exit code')

parser.add_argument('--sleep', dest='sleep', action='store_const',
                   default=False, const=True, help='should I sleep for 1min')

args = parser.parse_args()
print("parsed all")
print("err " + str(args.err))

with open('log.txt', 'a') as f:
        f.write("asdf\n")

if (args.sleep):
        print "sleeping"
        for k in range(10):
            time.sleep(1)

if(args.err):
        print "raising exception"
        raise Exception("default Exception")

if(args.code):
        exit(1)

exit(0)

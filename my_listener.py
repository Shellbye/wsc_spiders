__author__ = 'shellbye'
import sys
import time


def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


def main():
    while 1:
        write_stdout('READY\n')  # transition from ACKNOWLEDGED to READY, waiting...
        # get info from supervisor through stdin
        line = sys.stdin.readline()  # read header line from stdin
        # write_stderr(line)
        headers = dict([ x.split(':') for x in line.split() ])
        data = sys.stdin.read(int(headers['len']))
        # write_stderr(data)
        write_stderr('event occurred at ' + time.strftime("%H:%M:%S") + '!!!\n')
        write_stdout('RESULT 2\nOK')  # transition from READY to ACKNOWLEDGED, waiting for READY


if __name__ == '__main__':
    main()
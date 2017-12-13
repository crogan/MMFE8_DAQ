"""
daemon.py :: a script to sample the latest MMFE8 data and see how many boards are present

> python daemon.py
"""

import argparse
import os
import subprocess
import sys
import time

try:
    import yagmail
except:
    fatal("yagmail is not installed. Try:\n pip install yagmail --user")

def main():

    ops = options()

    data = "/data/mm_2016/work/mmfe8TestQuiet.dat"
    if not os.path.isfile(data):
        fatal("The data file doesnt exist (%s)" % (data))
    first = True

    # email thresholds
    too_long = 10
    nboards  = 8

    while True:

        # patience
        if first:
            first = False
        else:
            time.sleep(float(ops.m) * 60)

        # "decode"
        now    = time.time()
        human  = time.strftime("%Y-%m-%d-%Hh%Mm%Ss")
        boards = []
        times  = []
        lines  = tail(data)
        for line in lines:
            line      = line.split()
            board     = line.pop(0)
            timestamp = line.pop(0)
            boards.append(int(board))
            times.append(float(timestamp)*1e-9)

        # protection
        if not os.path.isfile(data):
            fatal("The data file doesnt exist (%s)" % (data))

        # clean it up
        boards = sorted(list(set(boards)))
        oldest = min(times)
        newest = max(times)

        # no new data: bad
        dt = (now - newest)/60.0
        if int(dt) > too_long:
            msg = "%s :: Data was last recorded %i minutes ago" % (human, int(dt))
            print msg
            mail(msg)

        # new data, but some boards missing: bad
        dt = (now - oldest)/60.0
        msg = "%s :: %i boards recorded data in the past %i minutes" % (human, len(boards), int(dt))
        print msg
        if len(boards) < nboards:
            mail(msg)

def mail(text):
    print "Bad! Sending email."
    emails   = ["tuna@cern.ch",
                "annwang@g.harvard.edu",
                "giromini@g.harvard.edu",
                ]
    subject  = "LPPC Early Warning System"
    username = "lppcautomated@gmail.com"
    password = "42oxford"
    yag = yagmail.SMTP(username, password)
    yag.send(emails, subject, [text])
    
def tail(fi):
    cmd = "tail"
    arg = "-n 2000"
    popen = subprocess.Popen([cmd, arg, fi],
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
    lines, errors = popen.communicate()
    lines = lines.split("\n")
    lines = filter(lambda line: line, lines)
    lines = filter(lambda line: "new event" not in line, lines)
    return lines
    
def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

def options():
    parser = argparse.ArgumentParser(usage=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", default="5",  help="Sleep time between reading the data [minutes]")
    return parser.parse_args()

if __name__ == "__main__":
    main()

#
# To run me in real time, do:
#    > while true; do clear; python ascii_display.py -l; sleep 2; done
#
# Format assumed:
# 111 1488579780462268160.000000 2 0 0x688000cb K 0x44a10010 0xa67057 0xb0000783 
#
# NB: Boards 0, 3, 5, 6 are flipped!
#

import argparse
import os
import sys
import time

def main():

    ops = options()

    if not ops.b in ["512", "256", "128", "64", "32", "16", "8"]:
        fatal("Since we have 512 channels, you must choose a multiple of that, like 128 or 64. %s is not okay." % (ops.b))

    # read the file
    if not os.path.isfile(ops.i):
        fatal("Input file (%s) doesnt exist. Exiting." % (ops.i))
    if ops.l:
        lines = reversed(open(ops.i).readlines())
    else:
        lines = open(ops.i).readlines()

    bcs    = []
    boards = []
    hits   = {}

    # parse the lines
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if ops.v:
            print "Processing line: %s" % (line)

        # decode
        words = line.split()
        board     = words.pop(0)
        timestamp = words.pop(0)
        nfifo0    = words.pop(0)
        nfifo1    = words.pop(0)
        header_bc = words.pop(0)
        char      = words.pop(0)
        command   = words.pop(0)

        # delimit by BC
        bc = header_bc[-5:]
        if bc not in bcs:
            # new bc!
            if len(bcs) > 0:
                if len(bcs) <= int(ops.n):
                    # display and reset
                    display(bcs[-1], boards, hits, preamble=(len(bcs)==1))
                    boards = []
                    hits = {}
                else:
                    break
            bcs.append(bc)

        # process and decode
        boards.append(board)
        hits[board] = []
        while words:
            word  = words.pop(0)
            dummy = words.pop(0)
            vmm, ch, pdo, tdo = decode(word)
            if ops.v:
                print "Decoding: %s => VMM=%i, CH=%i, PDO=%i, TDO=%i" % (word, vmm, ch, pdo, tdo)
            hits[board].append(vmm*64 + ch)

def display(bc, boards, hits, preamble=False):

    ops = options()

    channels = 512
    marker   = color.RED+color.BOLD+"x"+color.END
    if preamble:
        print
        print "Input .dat file   : %s"     % (ops.i)
        print "Using geometry of : Run %s" % (ops.r)
        print "Strips per char   : %i"     % (channels / int(ops.b))
        print
    print "Trigger = 0x%s = %i" % (bc, int(bc, base=16))
    print
    boards = ordered_boards()
    for board in boards:
        hitmap = ["."]*int(ops.b)
        for hit in hits.get(board, []):
            hitmap[int(hit) * int(ops.b) / channels] = marker
        flipped = boards.index(board) not in [0, 3, 5, 6]
        if flipped:
            hitmap = hitmap[::-1]
        print board, "".join(hitmap), sorted(hits.get(board, [])), "(flipped)" if flipped else ""

        # delimit the quadruplets
        if boards.index(board) == 3:
            print
    print

def decode(iword0):
    # https://github.com/crogan/MMFE8_DataFormats/blob/master/src/raw2dat.C#L147
    iword0 = int(iword0, base=16)
    iword0 = iword0 >> 2
    CH     = (iword0 & 63)
    if iword0 <= 0:
        CH = 0
    iword0 = iword0 >> 6
    PDO    = iword0 & 1023
    iword0 = iword0 >> 10
    TDO    = iword0 & 255
    iword0 = iword0 >> 8
    VMM    = iword0 & 7
    return VMM, CH, PDO, TDO

class color:
    BLUE      = "\033[94m"
    GREEN     = "\033[92m"
    YELLOW    = "\033[93m"
    RED       = "\033[91m"
    END       = "\033[0m"
    BOLD      = "\033[1m"
    UNDERLINE = "\033[4m"

def ordered_boards():
    ops = options()
    if int(ops.r) >= 3518:
        return ["118", "116", "102", "119", "106", "107", "117", "105"][::-1]
    elif int(ops.r) >= 3515:
        return ["111", "116", "117", "119", "106", "107", "118", "105"][::-1]
    elif int(ops.r) >= 3513:
        return ["111", "116", "101", "109", "117", "102", "107", "105"][::-1]

def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

def options():
    testquiet = "/data/mm_2016/work/mmfe8TestQuiet.dat"
    parser = argparse.ArgumentParser(usage=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", default=testquiet,   help="Input raw text file")
    parser.add_argument("-r", default="3516",      help="Run number")
    parser.add_argument("-b", default="128",       help="Number of bins to show 512 channels")
    parser.add_argument("-n", default="1",         help="Number of events to display")
    parser.add_argument("-l", action="store_true", help="Start with the last event and loop backward in time.")
    parser.add_argument("-v", action="store_true", help="Turn on verbose mode")
    return parser.parse_args()

if __name__ == "__main__":
    main()

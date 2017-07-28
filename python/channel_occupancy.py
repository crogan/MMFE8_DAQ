"""
Script for dumping the channel occupancy of a dry run (or any run).

Run like:
> python channel_occupancy.py -i mmfe8TestQuiet.dat.root

It can handle TTrees from MM_data and TPfit_data.
"""
import argparse
import os
import sys
import ROOT

def main():

    ops = options()
    if not ops.i:
        fatal("Please provide an input file (-i)")
    if not os.path.isfile(ops.i):
        fatal("The input file provided does not exist")

    fi = ROOT.TFile(ops.i)
    tr = fi.Get("MM_data") or fi.Get("TPfit_data")
    if not tr:
        fatal("Couldnt find a TTree named MM_data or TPfit_data within %s" % (ops.i))
    hits = {}
    ents = tr.GetEntries()
    istp = "tp" in tr.GetName().lower()

    print
    print "Input  : %s" % (ops.i)
    print "Events : %i" % (ents)
    print "Tree   : %s" % (tr.GetName())
    print

    # loop
    for ent in xrange(ents):
        _ = tr.GetEntry(ent)
        nhits = len(tr.tpfit_CH) if istp else len(tr.mm_CH)
        for ch in xrange(nhits):
            mmfe, vmm, ch = (tr.tpfit_MMFE8[ch], tr.tpfit_VMM[ch], tr.tpfit_CH[ch]) if istp else\
                            (tr.mm_MMFE8[ch],    tr.mm_VMM[ch],    tr.mm_CH[ch])
            if (mmfe, vmm, ch) in hits:
                hits[mmfe, vmm, ch] += 1
            else:
                hits[mmfe, vmm, ch] = 1

    # hits -> occupancy
    for key in hits:
        hits[key] /= float(ents)

    # announce
    keys = 0
    print
    print " (FE, VMM, CH) # occupancy (hits/events)"
    print "---------------------------------------"
    for key in sorted(hits, key=hits.get, reverse=True):
        col = display_color(hits[key])
        mmfe, vmm, ch = key
        if (vmm, ch) == (0, 0):
            continue
        print "%s (%i, %i, %2i), # %6.1f%% %s" % (col, mmfe, vmm, ch, 100*hits[key], color.END)
        keys += 1
        if keys > int(ops.c):
            break
    print
                
class color:
    BLUE      = "\033[94m"
    GREEN     = "\033[92m"
    RED       = "\033[91m"
    END       = "\033[0m"
    BOLD      = "\033[1m"

def display_color(rate):
    if rate < 0.1:
        return ""
    elif rate < 1:
        return color.BOLD+color.BLUE
    else:
        return color.BOLD+color.RED

def options():
    parser = argparse.ArgumentParser(usage=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", default=None,   help="Input ROOT file")
    parser.add_argument("-c", default="30",   help="Number of channels to show")
    return parser.parse_args()

def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

if __name__ == "__main__":
    main()


class MMFEConfig: 
    pass

def strip2config(strip, board):
    if board in [0, 3, 5, 6]:
        strip = 511 - strip
    vmm = strip / 64
    ch  = strip % 64 + 1
    return vmm, ch

ips = [118, 120, 119, 111,
       106, 107, 101, 105]
mmfes = {}
configload = {}

for ip in ips:
    configload[ip] = range(8)
configload[111] = []
configload[120] = [0, 1, 2, 3, 6, 7]
configload[101] = [0, 1, 2, 4, 5, 6, 7]
for ip in ips:
    mmfes[ip]                 = MMFEConfig()
    mmfes[ip].ip              = ip
    mmfes[ip].i               = ips.index(ip)
    mmfes[ip].TestPulseDAC    = 120
    mmfes[ip].ST              = {}
    if ip is not 120 and ip is not 101:
        mmfes[ip].vmmis           = range(8)
        mmfes[ip].EnableReadout   = range(8)
    elif ip is 120:
        mmfes[ip].vmmis           = [0, 1, 2, 3, 6, 7]
        mmfes[ip].EnableReadout   = [0, 1, 2, 3, 6, 7]
    else:
        mmfes[ip].vmmis           = [0, 1, 2, 4, 5, 6, 7]
        mmfes[ip].EnableReadout   = [0, 1, 2, 4, 5, 6, 7]
        
    mmfes[ip].ConfigureLoad   = configload[ip]
    mmfes[ip].ExternalTrigger = True
    mmfes[ip].isExtPulseTrig  = True
    mmfes[ip].PeakingTime     = 0
    mmfes[ip].mon             = {}
    mmfes[ip].ThresholdDACs   = {0: 220, 1: 220, 2: 220, 3: 220,
                                 4: 220, 5: 220, 6: 220, 7: 220}

xxspread = "narrow"
uvspread = "verywide"
region   = 2
if not region in [1, 2]:
    sys.exit("Please give region 1 or 2")
if not xxspread in ["wide", "narrow"]:
    sys.exit("Please give xxspread in wide or narrow")
if not uvspread in ["verywide", "wide", "narrow"]:
    sys.exit("Please give uvspread in verywide, wide, or narrow")

if region == 1:
    if xxspread=="wide":
        if uvspread=="verywide":
            mmfes[105].ST[0] = [22]
            mmfes[101].ST[7] = [45]
            mmfes[107].ST[6] = [44]
            mmfes[106].ST[1] = [43]
            mmfes[119].ST[6] = [42]
            #mmfes[120].ST[1] = [41]
            #mmfes[111].ST[0] = [19]
            mmfes[118].ST[7] = [18]
        elif uvspread=="wide":
            mmfes[105].ST[0] = [22]
            mmfes[101].ST[7] = [45]
            mmfes[107].ST[7] = [44]
            mmfes[106].ST[0] = [43]
            mmfes[119].ST[7] = [42]
            #mmfes[120].ST[0] = [41]
            #mmfes[111].ST[0] = [19]
            mmfes[118].ST[7] = [18]
        elif uvspread=="narrow":
            mmfes[105].ST[0] = [22]
            mmfes[101].ST[7] = [45]
            mmfes[107].ST[7] = [34]
            mmfes[106].ST[0] = [33]
            mmfes[119].ST[7] = [32]
            #mmfes[120].ST[0] = [31]
            #mmfes[111].ST[0] = [19]
            mmfes[118].ST[7] = [18]
    elif xxspread=="narrow":
        if uvspread=="verywide":
            mmfes[105].ST[0] = [32]
            mmfes[101].ST[7] = [35]
            mmfes[107].ST[6] = [44]
            mmfes[106].ST[1] = [43]
            mmfes[119].ST[6] = [42]
            #mmfes[120].ST[1] = [41]
            #mmfes[111].ST[0] = [39]
            mmfes[118].ST[7] = [38]
        elif uvspread=="wide":
            mmfes[105].ST[0] = [32]
            mmfes[101].ST[7] = [35]
            mmfes[107].ST[7] = [44]
            mmfes[106].ST[0] = [43]
            mmfes[119].ST[7] = [42]
            #mmfes[120].ST[0] = [41]
            #mmfes[111].ST[0] = [39]
            mmfes[118].ST[7] = [38]
        elif uvspread=="narrow":
            mmfes[105].ST[0] = [32]
            mmfes[101].ST[7] = [35]
            mmfes[107].ST[7] = [34]
            mmfes[106].ST[0] = [33]
            mmfes[119].ST[7] = [32]
            #mmfes[120].ST[0] = [31]
            #mmfes[111].ST[0] = [39]
            mmfes[118].ST[7] = [38]
if region == 2:
    if xxspread=="wide":
        if uvspread=="verywide":
            mmfes[105].ST[7-0] = [22]
            mmfes[101].ST[7-7] = [45]
            mmfes[107].ST[7-6] = [44]
            mmfes[106].ST[7-1] = [43]
            mmfes[119].ST[7-6] = [42]
            #mmfes[120].ST[7-1] = [41]
            #mmfes[111].ST[7-0] = [19]
            mmfes[118].ST[7-7] = [18]
        elif uvspread=="wide":
            mmfes[105].ST[7-0] = [22]
            mmfes[101].ST[7-7] = [45]
            mmfes[107].ST[7-7] = [44]
            mmfes[106].ST[7-0] = [43]
            mmfes[119].ST[7-7] = [42]
            #mmfes[120].ST[7-0] = [41]
            #mmfes[111].ST[7-0] = [19]
            mmfes[118].ST[7-7] = [18]
        elif uvspread=="narrow":
            mmfes[105].ST[7-0] = [22]
            mmfes[101].ST[7-7] = [45]
            mmfes[107].ST[7-7] = [34]
            mmfes[106].ST[7-0] = [33]
            mmfes[119].ST[7-7] = [32]
            #mmfes[120].ST[7-0] = [31]
            #mmfes[111].ST[7-0] = [19]
            mmfes[118].ST[7-7] = [18]
    elif xxspread=="narrow":
        if uvspread=="verywide":
            mmfes[105].ST[7-0] = [32]
            mmfes[101].ST[7-7] = [35]
            mmfes[107].ST[7-6] = [44]
            mmfes[106].ST[7-1] = [43]
            mmfes[119].ST[7-6] = [42]
            #mmfes[120].ST[7-1] = [41]
            #mmfes[111].ST[7-0] = [39]
            mmfes[118].ST[7-7] = [38]
        elif uvspread=="wide":
            mmfes[105].ST[7-0] = [32]
            mmfes[101].ST[7-7] = [35]
            mmfes[107].ST[7-7] = [44]
            mmfes[106].ST[7-0] = [43]
            mmfes[119].ST[7-7] = [42]
            #mmfes[120].ST[7-0] = [41]
            #mmfes[111].ST[7-0] = [39]
            mmfes[118].ST[7-7] = [38]
        elif uvspread=="narrow":
            mmfes[105].ST[7-0] = [32]
            mmfes[101].ST[7-7] = [35]
            mmfes[107].ST[7-7] = [34]
            mmfes[106].ST[7-0] = [33]
            mmfes[119].ST[7-7] = [32]
            #mmfes[120].ST[7-0] = [31]
            #mmfes[111].ST[7-0] = [39]
            mmfes[118].ST[7-7] = [38]

#
# OFWGMTA
#
for ip in ips:
    mmfes[ip].SM = {}
    for vmm in range(8):
        mmfes[ip].SM[vmm] = []
        for ch in range(1,65):
            if vmm in mmfes[ip].ST and (ch not in mmfes[ip].ST[vmm]):
                mmfes[ip].SM[vmm].append(ch)
            elif vmm not in mmfes[ip].ST:
                mmfes[ip].SM[vmm].append(ch)

cfgs = []
for ip in ips:
    cfgs.append(mmfes[ip])


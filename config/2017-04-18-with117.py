class MMFEConfig: 
    pass

ips = [111, 116, 102, 119, 
       106, 107, 117, 105]
mmfes = {}

for ip in ips:
    mmfes[ip]                 = MMFEConfig()
    mmfes[ip].ip              = ip
    mmfes[ip].i               = ips.index(ip)
    mmfes[ip].TestPulseDAC    = 120
    mmfes[ip].ST              = {}
    mmfes[ip].vmmis           = range(8)
    mmfes[ip].EnableReadout   = range(8)
    mmfes[ip].ConfigureLoad   = range(8)
    mmfes[ip].ExternalTrigger = True
    mmfes[ip].isExtPulseTrig  = True
    mmfes[ip].ThresholdDACs   = {0: 220, 1: 220, 2: 220, 3: 220,
                                 4: 220, 5: 220, 6: 220, 7: 220}


spread = 3
if spread == 1:
    # satisfy 3 roads
    mmfes[105].ST[0] = [38]
    mmfes[117].ST[7] = [37]
    # mmfes[117].ST[6] = [37]
    mmfes[107].ST[7] = [36]
    mmfes[106].ST[0] = [35]
    mmfes[119].ST[7] = [34]
    mmfes[102].ST[0] = [33]
    mmfes[116].ST[0] = [32]
    mmfes[111].ST[7] = []
elif spread == 2:
    # satisfy 2 roads
    mmfes[105].ST[0] = [38]
    mmfes[117].ST[7] = [37]
    mmfes[107].ST[7] = [36]
    mmfes[106].ST[0] = [35]
    mmfes[119].ST[6] = [34]
    mmfes[102].ST[1] = [33]
    mmfes[116].ST[1] = [32]
    mmfes[111].ST[6] = []
elif spread == 3:
    # satisfy 1 roads
    mmfes[105].ST[0] = [38]
    mmfes[117].ST[7] = [37]
    mmfes[107].ST[6] = [36]
    mmfes[106].ST[1] = [35]
    mmfes[119].ST[6] = [34]
    mmfes[102].ST[1] = [33]
    mmfes[116].ST[2] = [32]
    mmfes[111].ST[5] = []
elif spread == 4:
    # satisfy 0 roads
    mmfes[105].ST[0] = [38]
    mmfes[117].ST[7] = [37]
    mmfes[107].ST[6] = [36]
    mmfes[106].ST[1] = [35]
    mmfes[119].ST[5] = [34]
    mmfes[102].ST[2] = [33]
    mmfes[116].ST[3] = [32]
    mmfes[111].ST[4] = []
else:
    import sys
    sys.exit("Im not configured to hit more than 4 VMMs! You asked for %s" % spread)

for ip in ips:
    mmfes[ip].SM = {}
    for vmm in range(8):
        mmfes[ip].SM[vmm] = []
        for ch in range(1,65):
            if vmm in mmfes[ip].ST and (ch not in mmfes[ip].ST[vmm]):
                mmfes[ip].SM[vmm].append(ch)
            elif vmm not in mmfes[ip].ST:
                mmfes[ip].SM[vmm].append(ch)

# mmfes[111].SM = {0: [],
#                  1: [],
#                  2: [21],
#                  3: [2, 5, 60, 63],
#                  4: [1, 3, 10, 23, 30, 33, 36, 53, 56],
#                  5: [],
#                  6: [29, 39],
#                  7: [8]}

# mmfes[116].SM = {0: [],
#                  1: [51],
#                  2: [1, 2, 3, 5],
#                  3: [1, 2, 5],
#                  4: [1, 2],
#                  5: [1, 2, 3],
#                  6: [],
#                  7: [2, 64]}

# mmfes[102].SM = {0: [24],
#                  1: [2],
#                  2: [3],
#                  3: [],
#                  4: [],
#                  5: [1, 3, 4],
#                  6: [1, 2, 52, 58],
#                  7: []}

# mmfes[119].SM = {0: [],
#                  1: [5],
#                  2: [],
#                  3: [],
#                  4: [],
#                  5: [2],
#                  6: [],
#                  7: []}

# mmfes[106].SM = {0: [3],
#                  1: [],
#                  2: [3],
#                  3: [],
#                  4: [],
#                  5: [],
#                  6: [1],
#                  7: [2, 19, 20]}

# mmfes[107].SM = {0: [1],
#                  1: [16, 18],
#                  2: [1],
#                  3: [1, 2, 3],
#                  4: [22, 63],
#                  5: [1, 33, 35],
#                  6: [9, 34, 36],
#                  7: []}

# mmfes[117].SM = {0: [1, 2, 56],
#                  1: [1, 5, 13, 15, 25, 27, 31, 33, 63],
#                  2: [4, 64],
#                  3: [],
#                  4: [],
#                  5: [1, 2, 5, 48, 50],
#                  6: [2, 60],
#                  7: [1, 3, 14, 16, 46, 61, 63, 64]}

# mmfes[105].SM = {0: [1],
#                  1: [1, 11, 17, 19, 24, 29, 37],
#                  2: [2],
#                  3: [],
#                  4: [1, 3, 4],
#                  5: [1],
#                  6: [2],
#                  7: []}

cfgs = []
#cfgs = [mmfes[117]]
for ip in ips:
    cfgs.append(mmfes[ip])


class MMFEConfig: 
    pass

ips = [118, 111, 120, 119, 
       106, 107, 101, 105]
mmfes = {}
configload = {}

for ip in ips:
    configload[ip] = range(8)
configload[120] = [0, 1, 2, 3, 5, 6, 7]

for ip in ips:
    mmfes[ip]                 = MMFEConfig()
    mmfes[ip].ip              = ip
    mmfes[ip].i               = ips.index(ip)
    mmfes[ip].TestPulseDAC    = 120
    mmfes[ip].ST              = {}
    mmfes[ip].vmmis           = range(8) if ip is not 120 else [0, 1, 2, 3, 5, 6, 7]
    mmfes[ip].EnableReadout   = range(8) if ip is not 120 else [0, 1, 2, 3, 5, 6, 7]
    mmfes[ip].ConfigureLoad   = configload[ip]
    mmfes[ip].ExternalTrigger = True
    mmfes[ip].isExtPulseTrig  = True
    mmfes[ip].PeakingTime     = 0
    mmfes[ip].mon             = {}
    mmfes[ip].ThresholdDACs   = {0: 220, 1: 220, 2: 220, 3: 220,
                                 4: 220, 5: 220, 6: 220, 7: 220}

# first muon
mmfes[105].ST[0] = [38]
mmfes[101].ST[7] = [37]
mmfes[107].ST[7] = [36]
mmfes[106].ST[0] = [35]
mmfes[119].ST[7] = [34]
mmfes[120].ST[0] = [33]
mmfes[111].ST[0] = [32]
mmfes[118].ST[7] = [31]
# second muon
mmfes[105].ST[7] = [38]
mmfes[101].ST[0] = [37]
mmfes[107].ST[0] = [36]
mmfes[106].ST[7] = [35]
mmfes[119].ST[0] = [34]
mmfes[120].ST[7] = [33]
mmfes[111].ST[7] = [32]
mmfes[118].ST[0] = [31]

# masking
mmfes[118].SM = {0: [1, 7, 8, 9, 11, 25, 44, 49, 50, 51],
                 1: [9, 13, 45],
                 2: [1, 6, 31, 56],
                 3: [20, 62],
                 4: [6, 15, 17, 43],
                 5: [12, 15, 21, 30],
                 6: [1, 3, 4, 9, 16, 35, 37, 56],
                 7: [29, 53, 63]}

mmfes[118].ThresholdDACs[0] = 240
mmfes[118].ThresholdDACs[1] = 240
mmfes[118].ThresholdDACs[2] = 240
mmfes[118].ThresholdDACs[4] = 260
mmfes[118].ThresholdDACs[6] = 240

mmfes[111].SM = {0: [10, 17, 40],
                 1: [19, 33],
                 2: [],
                 3: [],
                 4: [35],
                 5: [1, 4],
                 6: [51, 64],
                 7: [4, 13, 23, 24, 33, 53, 32, 50, 63]}

mmfes[120].SM = {0: [14, 16, 40, 41, 43, 49],
                 1: [15, 43, 46],
                 2: [27, 38, 40, 51],
                 3: [3, 5, 20, 31, 64],
                 4: [],
                 5: [],
                 6: [1, 7, 19, 21, 37, 38, 40, 41, 50, 56],
                 7: [1, 12, 21, 25, 26, 29, 30, 33, 34, 62, 63, 64]}

mmfes[120].ThresholdDACs[0] = 240
mmfes[120].ThresholdDACs[1] = 260
mmfes[120].ThresholdDACs[2] = 260
mmfes[120].ThresholdDACs[3] = 260
mmfes[120].ThresholdDACs[6] = 260
mmfes[120].ThresholdDACs[7] = 260

mmfes[119].SM = {0: [37, 42],
                 1: [3, 6, 17, 24, 29, 31, 36, 38, 42, 44, 46, 61],
                 2: [57],
                 3: [53, 55],
                 4: [],
                 5: [2],
                 6: [11, 35, 52, 34],
                 7: [38, 64]}
for i in range(7):
    mmfes[119].ThresholdDACs[i] = 240

mmfes[106].SM = {0: [3],
                 1: [20],
                 2: [3],
                 3: [],
                 4: [],
                 5: [],
                 6: [1],
                 7: [2, 19, 20]}

mmfes[107].SM = {0: [],
                 1: [16, 18],
                 2: [1],
                 3: [1, 2, 3],
                 4: [1, 5, 28, 38, 61],
                 5: [],
                 6: [59, 62],
                 7: [62]}
mmfes[107].ThresholdDACs[4] = 230
mmfes[107].ThresholdDACs[6] = 240

mmfes[101].SM = {0: [1, 3],
                 1: [3, 5, 60],
                 2: [12, 29, 32, 35, 47],
                 3: [1, 3, 4, 10, 49],
                 4: [],
                 5: [2, 3, 4, 9, 38, 49],
                 6: [1, 58],
                 7: [1, 64]}

mmfes[105].SM = {0: [],
                 1: [],
                 2: [2],
                 3: [1, 32],
                 4: [1, 2, 3, 4, 52],
                 5: [1, 18, 37, 40, 63],
                 6: [1, 2, 22, 49],
                 7: [1, 3]}

#
# MASK THEM ALL FUCK
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


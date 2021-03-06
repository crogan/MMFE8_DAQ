class MMFEConfig: 
    pass

ips = [118, 116, 102, 119, 
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
    mmfes[ip].isExtPulseTrig  = False
    mmfes[ip].ThresholdDACs   = {0: 220, 1: 220, 2: 220, 3: 220,
                                 4: 220, 5: 220, 6: 220, 7: 220}

for ip in ips:
    mmfes[ip].SM = {}
    for vmm in range(8):
        mmfes[ip].SM[vmm] = []
        for ch in range(1,65):
            if vmm in mmfes[ip].ST and (ch not in mmfes[ip].ST[vmm]):
                mmfes[ip].SM[vmm].append(ch)
            elif vmm not in mmfes[ip].ST:
                mmfes[ip].SM[vmm].append(ch)

mmfes[118].SM = {0: [1],
                 1: [],
                 2: [1, 23, 27, 29, 31, 33, 56],
                 3: [1, 43, 45, 58, 61],
                 4: [6, 15, 21, 23, 37, 39],
                 5: [],
                 6: [1, 3, 4],
                 7: []}

mmfes[116].SM = {0: [8],
                 1: [51],
                 2: [1, 2, 3, 5],
                 3: [1, 2, 5],
                 4: [1, 2],
                 5: [1, 2, 3],
                 6: [],
                 7: [2, 64]}

mmfes[102].SM = {0: [24],
                 1: [2],
                 2: [3],
                 3: [],
                 4: [],
                 5: [1, 3, 4],
                 6: [1, 2, 22, 52, 58],
                 7: []}

mmfes[119].SM = {0: [],
                 1: [5],
                 2: [],
                 3: [],
                 4: [],
                 5: [2],
                 6: [],
                 7: []}

mmfes[106].SM = {0: [3],
                 1: [],
                 2: [3],
                 3: [],
                 4: [],
                 5: [],
                 6: [1],
                 7: [2, 19, 20]}

mmfes[107].SM = {0: [1],
                 1: [16, 18],
                 2: [1],
                 3: [1, 2, 3, 19, 25, 27],
                 4: [22, 63],
                 5: [1, 21, 33, 35],
                 6: [9, 34, 36, 49],
                 7: []}

mmfes[117].SM = {0: [1, 2, 56, 58],
                 1: [1, 5, 13, 15, 25, 27, 31, 33, 63],
                 2: [4, 64],
                 3: [],
                 4: [],
                 5: [1, 2, 5, 48, 50],
                 6: [2, 50, 60],
                 7: [1, 3, 14, 16, 36, 46, 61, 63, 64]}

mmfes[105].SM = {0: [1],
                 1: [1, 5, 11, 12, 17, 19, 24, 29, 37],
                 2: [2],
                 3: [],
                 4: [1, 3, 4],
                 5: [1],
                 6: [2],
                 7: []}

cfgs = []
#cfgs = [mmfes[117]]
for ip in ips:
    cfgs.append(mmfes[ip])


class MMFEConfig: 
    pass

ips = [118, 116, 102, 119, 
       106, 107, 101, 105]
mmfes = {}
configload = {}

for ip in ips:
    configload[ip] = range(8)
configload[102] = [0, 1, 2, 3, 4, 6, 7]

for ip in ips:
    mmfes[ip]                 = MMFEConfig()
    mmfes[ip].ip              = ip
    mmfes[ip].i               = ips.index(ip)
    mmfes[ip].TestPulseDAC    = 120
    mmfes[ip].ST              = {}
    mmfes[ip].vmmis           = range(8)
    mmfes[ip].EnableReadout   = range(8)
    mmfes[ip].ConfigureLoad   = configload[ip]
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

mmfes[118].SM = {0: [1, 8],
                 1: [],
                 2: [1, 6, 31, 56],
                 3: [62],
                 4: [6, 15],
                 5: [],
                 6: [1, 3, 4, 37],
                 7: [29, 63]}

mmfes[118].ThresholdDACs[0] = 240
mmfes[118].ThresholdDACs[1] = 240
mmfes[118].ThresholdDACs[2] = 240
mmfes[118].ThresholdDACs[4] = 240

mmfes[116].SM = {0: [1, 8, 26],
                 1: [51],
                 2: [1, 2, 3, 5],
                 3: [1, 2, 5],
                 4: [35],
                 5: [2, 3],
                 6: [39, 41],
                 7: [1, 49, 56, 64]}

mmfes[116].ThresholdDACs[0] = 240
mmfes[116].ThresholdDACs[1] = 240
mmfes[116].ThresholdDACs[4] = 240
mmfes[116].ThresholdDACs[7] = 240

mmfes[102].SM = {0: [8],
                 1: [2, 8],
                 2: [3],
                 3: [3, 26, 43],
                 4: [1, 2, 17],
                 5: [],
                 6: [12, 32, 42],
                 7: []}

mmfes[119].SM = {0: [37],
                 1: [3],
                 2: [],
                 3: [55],
                 4: [],
                 5: [2],
                 6: [11, 52],
                 7: [64]}
for i in range(7):
    mmfes[119].ThresholdDACs[i] = 240

mmfes[106].SM = {0: [3],
                 1: [],
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
                 4: [1, 5, 38, 61],
                 5: [],
                 6: [],
                 7: [62]}
mmfes[107].ThresholdDACs[4] = 230
mmfes[107].ThresholdDACs[6] = 240

mmfes[101].SM = {0: [3],
                 1: [3, 5, 60],
                 2: [12],
                 3: [1, 3, 4],
                 4: [],
                 5: [3, 4],
                 6: [],
                 7: []}

mmfes[105].SM = {0: [],
                 1: [],
                 2: [2],
                 3: [1, 32],
                 4: [1, 2, 3, 4],
                 5: [1, 18, 37, 40, 63],
                 6: [1, 2, 22],
                 7: [1]}

cfgs = []
#cfgs = [mmfes[107]]
for ip in ips:
    cfgs.append(mmfes[ip])


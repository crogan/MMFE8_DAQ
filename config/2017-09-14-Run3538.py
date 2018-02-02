class MMFEConfig: 
    pass

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
    mmfes[ip].isExtPulseTrig  = False
    mmfes[ip].PeakingTime     = 0
    mmfes[ip].mon             = {}
    mmfes[ip].ThresholdDACs   = {0: 220, 1: 220, 2: 220, 3: 220,
                                 4: 220, 5: 220, 6: 220, 7: 220}


# masking
mmfes[118].SM = {0: [1],
                 1: [],
                 2: [1, 6, 27, 31, 56],
                 3: [],
                 4: [1, 6, 15, 21, 23],
                 5: [],
                 6: [1, 2, 3, 4],
                 7: [1]}

mmfes[120].SM = {0: [13, 16, 40, 41],
                 1: [46],
                 2: [1, 20, 21, 27, 38, 40, 46, 50, 51, 53],
                 3: [3, 5, 20, 22, 25, 29, 31, 34, 51, 53, 64],
                 4: [],
                 5: [],
                 6: [1, 40],
                 7: [1, 10, 12, 21, 22, 28, 29, 34]}

mmfes[120].SM[7].extend(range(35,65))

mmfes[120].ThresholdDACs[1] = 240
mmfes[120].ThresholdDACs[3] = 240
mmfes[120].ThresholdDACs[6] = 240
mmfes[120].ThresholdDACs[7] = 240

mmfes[119].SM = {0: [37],
                 1: [1, 3, 6, 17, 24, 29, 31, 36, 38, 44, 46],
                 2: [],
                 3: [55],
                 4: [],
                 5: [2],
                 6: [11, 34, 48, 52],
                 7: [64]}
mmfes[119].ThresholdDACs[1] = 240

mmfes[106].SM = {0: [1, 3],
                 1: [1],
                 2: [3],
                 3: [],
                 4: [],
                 5: [],
                 6: [1, 2, 3, 27],
                 7: [1, 2, 3, 19, 20]}

mmfes[107].SM = {0: [],
                 1: [16, 18, 26, 29, 40, 42, 63],
                 2: [1],
                 3: [1, 2, 3],
                 4: [1, 5, 28, 61],
                 5: [],
                 6: [1, 59, 62],
                 7: []}

mmfes[101].SM = {0: [1, 3],
                 1: [3, 5],
                 2: [],
                 3: [],
                 4: [2, 3, 4],
                 5: [1],
                 6: [],
                 7: []}
mmfes[101].SM[2] = range(29,65)
mmfes[105].SM = {0: [],
                 1: [],
                 2: [2],
                 3: [1],
                 4: [1, 2, 3, 4, 52],
                 5: [1],
                 6: [1, 2],
                 7: []}

mmfes[111].SM = {0: [],
                 1: [],
                 2: [],
                 3: [],
                 4: [],
                 5: [],
                 6: [],
                 7: []}
cfgs = []
for ip in ips:
    cfgs.append(mmfes[ip])


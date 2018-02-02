class MMFEConfig: 
    pass

ips = [119, 124, 122, 126,
       106, 109, 125, 123]
mmfes = {}
configload = {}

for ip in ips:
    configload[ip] = range(8)
configload[122] = [0, 1, 3, 4, 5, 6, 7]

for ip in ips:
    mmfes[ip]                 = MMFEConfig()
    mmfes[ip].ip              = ip
    mmfes[ip].i               = ips.index(ip)
    mmfes[ip].TestPulseDAC    = 120
    mmfes[ip].ST              = {}
    if ip is not 122:
        mmfes[ip].vmmis           = range(8)
        mmfes[ip].EnableReadout   = range(8)
    else:
        mmfes[ip].vmmis           = [0, 1, 3, 4, 5, 6, 7]
        mmfes[ip].EnableReadout   = [0, 1, 3, 4, 5, 6, 7]
        
    mmfes[ip].ConfigureLoad   = configload[ip]
    mmfes[ip].ExternalTrigger = True
    mmfes[ip].isExtPulseTrig  = pulse
    mmfes[ip].PeakingTime     = 0
    mmfes[ip].mon             = {}
    mmfes[ip].ThresholdDACs   = {0: 220, 1: 220, 2: 220, 3: 220,
                                 4: 220, 5: 220, 6: 220, 7: 220}


# masking
mmfes[119].SM = {0: [],
                 1: [1, 2, 3],
                 2: [],
                 3: [],
                 4: [],
                 5: [],
                 6: [],
                 7: []}

mmfes[124].SM = {0: [1, 2, 3, 4],
                 1: [],
                 2: [],
                 3: [1, 2, 3, 4],
                 4: [],
                 5: [],
                 6: [],
                 7: [1, 2, 3, 4, 45, 47, 49]}

mmfes[122].SM = {0: [],
                 1: [],
                 2: [],
                 3: [1],
                 4: [],
                 5: [1],
                 6: [],
                 7: [3]}

mmfes[126].SM = {0: [],
                 1: [2],
                 2: [],
                 3: [],
                 4: [],
                 5: [],
                 6: [2, 3, 4],
                 7: []}

mmfes[106].SM = {0: [3],
                 1: [],
                 2: [3],
                 3: [],
                 4: [],
                 5: [],
                 6: [1],
                 7: [1, 2, 3, 19, 20]}

mmfes[109].SM = {0: [],
                 1: [],
                 2: [1],
                 3: [],
                 4: [3, 4],
                 5: [1, 3, 5],
                 6: [],
                 7: []}

mmfes[125].SM = {0: [],
                 1: [],
                 2: [],
                 3: [],
                 4: [1, 2],
                 5: [1, 2, 4, 6],
                 6: [],
                 7: [1]}

mmfes[123].SM = {0: [1, 2],
                 1: [],
                 2: [1, 2, 3, 4],
                 3: [1],
                 4: [1, 2, 3, 4],
                 5: [],
                 6: [],
                 7: []}

# mo
mmfes[126].mon[0] = 26
mmfes[126].mon[1] = 26
mmfes[126].mon[2] = 26
mmfes[126].mon[3] = 26
mmfes[126].mon[4] = 26
mmfes[126].mon[5] = 31
mmfes[126].mon[6] = 27
mmfes[126].mon[7] = 26


cfgs = []
for ip in ips:
    cfgs.append(mmfes[ip])


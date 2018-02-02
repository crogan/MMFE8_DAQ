class MMFEConfig: 
    pass

ips = [118, 111, 120, 119, 
       106, 107, 101, 105]
mmfes = {}
configload = {}

for ip in ips:
    configload[ip] = []
#configload[120] = [0, 1, 2, 3, 5, 6, 7]

for ip in ips:
    mmfes[ip]                 = MMFEConfig()
    mmfes[ip].ip              = ip
    mmfes[ip].i               = ips.index(ip)
    mmfes[ip].TestPulseDAC    = 120
    mmfes[ip].ST              = {}
    mmfes[ip].SM              = {}
    mmfes[ip].vmmis           = []
    mmfes[ip].EnableReadout   = []
    mmfes[ip].ConfigureLoad   = configload[ip]
    mmfes[ip].ExternalTrigger = True
    mmfes[ip].isExtPulseTrig  = False
    mmfes[ip].PeakingTime     = 0
    mmfes[ip].mon             = {}
    mmfes[ip].ThresholdDACs   = {0: 220, 1: 220, 2: 220, 3: 220,
                                 4: 220, 5: 220, 6: 220, 7: 220}


cfgs = []
for ip in ips:
    cfgs.append(mmfes[ip])


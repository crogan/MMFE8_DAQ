class MMFEConfig: 
    pass

ips = [123, 125, 109, 106,
       126, 122, 124, 119]
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
    mmfes[ip].isExtPulseTrig  = True
    mmfes[ip].PeakingTime     = 0
    mmfes[ip].mon             = {}
    mmfes[ip].ThresholdDACs   = {0: 220, 1: 220, 2: 220, 3: 220,
                                 4: 220, 5: 220, 6: 220, 7: 220}

cfgs = []
for ip in ips:
    cfgs.append(mmfes[ip])

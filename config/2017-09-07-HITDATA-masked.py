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
#mmfes[120].ST[0] = [33]
#mmfes[111].ST[0] = [32]
mmfes[118].ST[7] = [31]

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


class MMFEConfig: 
    pass

ips = [118, 111, 120, 119, 
       106, 107, 101, 105]
mmfes = {}

for ip in ips:
    mmfes[ip]                 = MMFEConfig()
    mmfes[ip].ip              = ip
    mmfes[ip].i               = ips.index(ip)
    mmfes[ip].TestPulseDAC    = 120
    mmfes[ip].ST              = {}
    mmfes[ip].vmmis           = range(8)
    mmfes[ip].EnableReadout   = range(8) if ip is not 120 else [0, 1, 2, 3, 5, 6, 7]
    mmfes[ip].ConfigureLoad   = range(8) if ip is not 120 else [0, 1, 2, 3, 5, 6, 7]
    mmfes[ip].ExternalTrigger = True
    mmfes[ip].isExtPulseTrig  = True
    mmfes[ip].ThresholdDACs   = {0: 240, 1: 240, 2: 240, 3: 240,
                                 4: 240, 5: 240, 6: 240, 7: 240}
    mmfes[ip].PeakingTime     = 0
    mmfes[ip].mon             = {}

ntriggers = 6
if ntriggers == 6:
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

mmfes[105].mon = {0:38}

cfgs = []
for ip in ips:
    cfgs.append(mmfes[ip])


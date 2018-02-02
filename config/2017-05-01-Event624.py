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
    mmfes[ip].ConfigureLoad   = range(8) if ip != 107 else range(1,8)
    mmfes[ip].ExternalTrigger = True
    mmfes[ip].isExtPulseTrig  = True
    mmfes[ip].ThresholdDACs   = {0: 220, 1: 220, 2: 220, 3: 220,
                                 4: 220, 5: 220, 6: 220, 7: 220}

#
# This is an event from Run 3518 
#   where the TP mishandles the strip on board 0.
#
# We blast them all in 1-2 BCs because this is all
#   the pulser can do.
#
mmfes[105].ST[4] = [40, 44]
mmfes[117].ST[3] = [4, 11]
mmfes[107].ST[2] = [58]
mmfes[107].ST[3] = [4, 5]
mmfes[106].ST[5] = [14]
mmfes[119].ST[2] = [20]
mmfes[102].ST[5] = [62]
mmfes[116].ST[6] = [5]
mmfes[118].ST[1] = [49, 51]

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


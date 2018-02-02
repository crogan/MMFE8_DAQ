class MMFEConfig: 
    pass

ips = [123, 125, 109, 106,
       126, 122, 124, 119]
mmfes = {}
configload = {}

#############
#############
pulse = True
#############
#############

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

region = 2
triggerable = True
if not region in [1, 2]:
    sys.exit("Please give region 1 or 2")

if region == 1:
    if triggerable:
        mmfes[123].ST[0] = [38]
        mmfes[125].ST[7] = [37]
        mmfes[109].ST[7] = [36]
        mmfes[106].ST[0] = [35]
        mmfes[126].ST[7] = [34]
        mmfes[122].ST[0] = [33]
        mmfes[124].ST[0] = [32]
        mmfes[119].ST[7] = [31]
    else:
        mmfes[123].ST[0] = [28]
        mmfes[125].ST[7] = [61]
        mmfes[109].ST[7] = [60]
        mmfes[106].ST[0] = [29]
        mmfes[126].ST[7] = [28]
        mmfes[122].ST[0] = [61]
        mmfes[124].ST[0] = [60]
        mmfes[119].ST[7] = [29]
if region == 2:
    if triggerable:
        print "sad"
        print "sad"
        print "sad"
        print "sad"
        print "sad"
        print "sad"
        print "sad"
        mmfes[123].ST[0] = [32]
        mmfes[125].ST[7] = [33]
        mmfes[109].ST[7] = [40]
        mmfes[106].ST[0] = [38]
        mmfes[126].ST[7] = [40]
        mmfes[122].ST[0] = [38]
        mmfes[124].ST[0] = [32]
        mmfes[119].ST[7] = [33]

        # overlap
        mmfes[123].ST[1] = [36]
        mmfes[125].ST[6] = [29]
        mmfes[109].ST[6] = [36]
        mmfes[106].ST[1] = [42]
        mmfes[126].ST[6] = [36]
        mmfes[122].ST[1] = [42]
        mmfes[124].ST[1] = [36]
        mmfes[119].ST[6] = [29]
    else:
        mmfes[123].ST[7] = [28]
        mmfes[125].ST[0] = [61]
        mmfes[109].ST[0] = [60]
        mmfes[106].ST[7] = [29]
        mmfes[126].ST[0] = [28]
        mmfes[122].ST[7] = [61]
        mmfes[124].ST[7] = [60]
        mmfes[119].ST[0] = [29]

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


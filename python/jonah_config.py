# This is a program which calibrates VMMS. Instead of using a GUI, commands are executed via command line.  
# Ideally, this program makes the calibration process more time efficient.
# the program can be evaluated with commands like
#
#                       python newcal.py config.py show
#
# where "8" is the number of MMFEs, "show" shows the gui window (leave empty to hide).
#

import os 
import sys
import time

nvmms     = 8 
nchannels = 64

from gui     import GUI
from vmm     import registers
from channel import index

######################################################################################################### 

def newcal(mmfei, vmmis, ThresholdDACs, TestPulseDAC,
           SM, ST, EnableReadout, ConfigureLoad, 
           ip, ExternalTrigger, isExtPulseTrig):   

    # set mmfe number
    gui.combo_mmfe_number.set_active(mmfei)
    gui.set_current_mmfe(gui.combo_mmfe_number)
    gui.entry_ip.set_text("192.168.0." + str(ip)) 
    gui.set_ip(gui.entry_ip)

    text = "Board %s :: [%s / %s]" % (str(ip), mmfei+1, sys.argv[1])
    color = colors[mmfei % len(colors)]
    mmfe  = color+palette.BOLD+text+palette.END
    announce(" %s with VMMs %s" % (mmfe, vmmis))

    # vmm loop
    for vmmi in vmmis:

        announce(" %s VMM %s" % (mmfe, vmmi))

        # set vmm number
        gui.vmm_number_combo.set_active(vmmi)
        gui.set_current_vmm(gui.vmm_number_combo)

        # set Threshold DAC
        announce(" %s VMM %s, THDAC %s" % (mmfe, vmmi, ThresholdDACs[vmmi]))
        gui.vmm_sdt_menu.set_active(ThresholdDACs[vmmi])
        gui.vmm_callback_word(gui.vmm_sdt_menu, registers.SDT, registers.bits_SDT)

        # set Test Pulse DAC
        if TestPulseDAC:
            announce(" %s VMM %s, TPDAC %s" % (mmfe, vmmi, TestPulseDAC))
            gui.vmm_sdp2_menu.set_active(TestPulseDAC)
            gui.vmm_callback_word(gui.vmm_sdp2_menu, registers.SDP2, registers.bits_SDP2)
        else:
            announce(" %s VMM %s, TPDAC ignored" % (mmfe, vmmi))

        # set test pulse channels
        if ST and vmmi in ST:
            for channel in ST[vmmi]:
                announce(" %s VMM %s, pulse CH %2s" % (mmfe, vmmi, channel))
                gui.channel_ST[channel-1].set_active(1)
                gui.channel_callback_bit(gui.channel_ST[channel-1], channel-1, index.ST)
        else:
            announce(" %s VMM %s, pulse nothing" % (mmfe, vmmi))

        # unmask everything, then set masked channels
        announce(" %s VMM %s, unmask everything" % (mmfe, vmmi))
        for channel in range(nchannels):
            gui.channel_SM[channel-1].set_active(0)
            gui.channel_callback_bit(gui.channel_SM[channel-1], channel-1, index.SM)
        for channel in SM[vmmi]:
            announce(" %s VMM %s, mask CH %2s" % (mmfe, vmmi, channel))
            gui.channel_SM[channel-1].set_active(1)
            gui.channel_callback_bit(gui.channel_SM[channel-1], channel-1, index.SM)
        if not SM[vmmi]:
            announce(" %s VMM %s, mask nothing" % (mmfe, vmmi))

    # enable readout
    for choice in EnableReadout:
        announce(" %s VMM %s, enable readout" % (mmfe, choice))
        gui.vmm_readout_buttons[choice].set_active(1)
        gui.readout_vmm_callback(gui.vmm_readout_buttons[choice], choice)
    if not EnableReadout:
        announce(" %s VMM %s, readout no VMMs" % (mmfe))

    # load it
    announce(" %s load readout" % (mmfe))
    gui.vmm_load_readout(gui.vmm_readout_button)

    # configure and Load
    for choice in ConfigureLoad:
        announce(" %s VMM %s, configure and load" % (mmfe, choice))
        gui.vmm_load_buttons[choice].set_active(1)
        gui.load_vmm_callback(gui.vmm_load_buttons[choice], choice)
    if not ConfigureLoad:
        announce(" %s VMM %s, configure/load no VMMs" % (mmfe))

    # load it
    announce(" %s load config" % (mmfe))
    gui.vmm_load_configs(gui.vmm_load_button)

    # set internal trigger/external trigger/external trigger with pulse
    if ExternalTrigger:
        announce(" %s enable external trigger" % (mmfe))
        gui.button_external_trigger.clicked()
        if isExtPulseTrig:
            announce(" %s enable external trigger w/pulse" % (mmfe))
            gui.button_external_trigger_pulse.clicked()


    if not quiet:
        print

def announce(message):
    if not quiet:
        print message

class palette:
    BLUE      = "\033[94m"
    GREEN     = "\033[92m"
    RED       = "\033[91m"
    END       = "\033[0m"
    BOLD      = "\033[1m"

#########################################################################################################

# load the config. beware USER ERROR.
if len(sys.argv) < 3:
    sys.exit("Fatal: please follow this format: python jonah_config.py NBOARDS CONFIG")
if not os.path.isfile(sys.argv[2]):
    sys.exit("Fatal: %s is not a file. Exiting." % (sys.argv[2]))
execfile(sys.argv[2])
if not len(cfgs)==int(sys.argv[1]):
    sys.exit("""Fatal: the number of configs in %s (%s) 
       doesnt match the number of configs on the command line (%s)"""
             % (sys.argv[2], len(cfgs), sys.argv[1]))

gui    = GUI()
show   = "show"  in sys.argv
quiet  = "quiet" in sys.argv
colors = ["", palette.BLUE, palette.GREEN, palette.RED]
start  = time.time()

if not show:
    gui.window.hide()

# loop over board configs
for cfg in cfgs:
    newcal(cfg.i, cfg.vmmis, cfg.ThresholdDACs, cfg.TestPulseDAC, 
           cfg.SM, cfg.ST, cfg.EnableReadout, cfg.ConfigureLoad, 
           cfg.ip, cfg.ExternalTrigger, cfg.isExtPulseTrig)

end   = time.time()
delta = int(end-start)
print "Configuration time: %sm%ss" % (delta/60, delta%60)

if show:
    raw_input("Press [Enter] to close.")

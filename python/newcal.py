#This is a program which calibrates VMMS. Instead of using a GUI, commands are executed via command line.  
#Ideally, this program makes the calibration process more time efficient.
#the program can be evaluated with commands like
#
#			python newcal.py 8 config_txt.txt show
#
#where "8" is the number of MMFEs, "show" shows the gui window (leave empty to hide), and config_txt has lines like:
#
#mmfei = 0; vmmis = [0]; ThresholdDACs = {0:120}; TestPulseDAC=120,SM={0:[0]}; ST={0:[0,8]}; EnableReadout=range(8); ConfigureLoad=[0];
#
#Note that lines in the .txt file with first character '#' will not be read by the program

import sys
import fileinput
import pygtk 
pygtk.require('2.0') 
import gtk 
import numpy as np  

######################################################################################################### 

nmmfes = int(sys.argv[1])
nvmms     = 8 
nchannels = 64
 
#########################################################################################################

from gui     import GUI 
from mmfe    import MMFE 
from vmm     import VMM, registers 
from udp     import udp_stuff 
from channel import index 
from helpers import convert_to_int, convert_to_32bit 
 
######################################################################################################### 

def newcal(mmfei, vmmis, ThresholdDACs, TestPulseDAC,SM, ST, EnableReadout, ConfigureLoad, ip):   

	#set mmfe number
	gui.combo_mmfe_number.set_active(mmfei)
	gui.set_current_mmfe(gui.combo_mmfe_number)
	gui.entry_ip.set_text("192.168.0." + str(ip)) 
	gui.set_ip(gui.entry_ip)
	#set internal trigger/external trigger/external trigger with pulse
	print "For trigger options, press enter without typing anything if you don't like the option. If you do want the trigger, press any character, then press enter.\n"
	isIntTrig = bool(raw_input("IntTrig? "))
	if isIntTrig:
		pulses = raw_input("Pulses (999=continuous): ")
		gui.entry_pulses.set_text(pulses)
		gui.set_pulses(gui.entry_pulses)
		gui.button_internal_trigger.set_active(1)
		gui.internal_trigger(gui.button_internal_trigger)
	else:
		isExtTrig = True
		isExtPulseTrig = bool(raw_input("So you want ExtTrig. Would you like a pulse with your trigger?"))
		gui.button_external_trigger.set_active(1)
		gui.external_trigger(gui.button_external_trigger)
		if isExtPulseTrig:
			gui.button_external_trigger_w_pulse.set_active(1)
			gui.external_trigger_w_pulse(gui.button_external_trigger_w_pulse)
	for vmmi in vmmis:
		#set vmm number
		gui.vmm_number_combo.set_active(vmmi)
		gui.set_current_vmm(gui.vmm_number_combo)
		#set Threshold DAC
		gui.vmm_sdt_menu.set_active(ThresholdDACs[vmmi])
		gui.vmm_callback_word(gui.vmm_sdt_menu, registers.SDT, registers.bits_SDT)
		#set Test Pulse DAC
		gui.vmm_sdp2_menu.set_active(TestPulseDAC)
		gui.vmm_callback_word(gui.vmm_sdp2_menu, registers.SDP2, registers.bits_SDP2)
		#set test pulse channels
		for channel in ST[vmmi]:
			gui.channel_ST[channel].set_active(1)
			gui.channel_callback_bit(gui.channel_ST[channel], channel, index.ST)
		#set masked channels
		for channel in range(nchannels):
			gui.channel_SM[channel].set_active(0)
			gui.channel_callback_bit(gui.channel_SM[channel], channel, index.SM)
		for channel in SM[vmmi]:
			gui.channel_SM[channel].set_active(1)
			gui.channel_callback_bit(gui.channel_SM[channel], channel, index.SM)
	#enable readout
	for choice in EnableReadout:
		gui.vmm_readout_buttons[choice].set_active(1)
		gui.readout_vmm_callback(gui.vmm_readout_buttons[choice], choice)
	gui.vmm_load_readout(gui.vmm_readout_button)
	#Configure and Load
	for choice in ConfigureLoad:
		gui.vmm_load_buttons[choice].set_active(1)
		gui.load_vmm_callback(gui.vmm_load_buttons[choice], choice)
	gui.vmm_load_configs(gui.vmm_load_button)

#########################################################################################################

gui = GUI()
if len(sys.argv) < 4:
	gui.window.hide()

print """
newcal successfully compiled!
"""
i =0
for line in fileinput.input(sys.argv[2]):
    if line[0] != '#':
		i += 1
		exec(line)
		newcal(mmfei, vmmis, ThresholdDACs, TestPulseDAC,SM, ST, EnableReadout, ConfigureLoad, ip)
if i ==1:
	raw_input(str(i) +" task was completed! Press enter to close the program...")
else:
	raw_input(str(i) +" tasks were completed! Press enter to close the program...")


 
 

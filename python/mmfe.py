import os
import time
import binstr
import numpy as np

from vmm     import VMM
from udp     import udp_stuff
from helpers import convert_to_32bit

nvmms = 8

class MMFE:

    def __init__(self):

        print "Creating instance of MMFE"

        self.VMMs = []
        for _ in range(nvmms):
            self.VMMs.append(VMM())

        self.udp         = udp_stuff()
        self.UDP_PORT    = 50001
        self.UDP_IP      = "192.168.0.000"
        self.udp_message = "r 0x44A1xxxx 0x1"

        self.vmm_load             = np.zeros((32), dtype=int)
        self.vmm_cfg_sel          = np.zeros((32), dtype=int)
        self.readout_runlength    = np.zeros((32), dtype=int)
        self.acq_count_runlength  = np.zeros((32), dtype=int)
        self.acq_hold_runlength   = np.zeros((32), dtype=int)
        self.xadc                 = np.zeros((32), dtype=int)
        self.admux                = np.zeros((32), dtype=int)
        self.control              = np.zeros((32), dtype=int)
        self.ds2411_low           = np.zeros((32), dtype=int)
        self.ds2411_high          = np.zeros((32), dtype=int)
        self.counts_to_acq_reset  = np.zeros((32), dtype=int)
        self.counts_to_acq_hold   = np.zeros((32), dtype=int)
        self.chnlReg              = np.zeros((51), dtype=int)
        self.byteint              = np.zeros((51), dtype=np.uint32)
        self.byteword             = np.zeros((32), dtype=int)

        self.pulses          = 0
        self.acq_reset_count = 0
        self.acq_reset_hold  = 0
        self.ext_trig_on     = 0

        self.mmfeID = 0
        self.ipAddr = ["127.0.0.1",
                       "192.168.0.130",
                       "192.168.0.101",
                       "192.168.0.102",
                       "192.168.0.103",
                       "192.168.0.104",
                       "192.168.0.105",
                       "192.168.0.106",
                       "192.168.0.107",
                       "192.168.0.108",
                       "192.168.0.109",
                       "192.168.0.110",
                       "192.168.0.111",
                       "192.168.0.112",
                       "192.168.0.167",
                       ]

        #0x44A100EC  #vmm_global_reset          #reset & vmm_gbl_rst_i & vmm_cfg_en_vec( 7 downto 0)
        #0x44A100EC  #vmm_cfg_sel               #vmm_2display_i(16 downto 12) & mmfeID(11 downto 8) & vmm_readout_i(7 downto 0)
        #0x44A100F0  #cktp_period_dutycycle     #clk_tp_period_cnt(15 downto 0) & clk_tp_dutycycle_cnt(15 downto 0)
        #0x44A100F4  #ReadOut_RunLength         #ext_trigger_in_sel(26)&axi_data_to_use(25)&int_trig(24)&vmm_readout_i(23 downto 16)&pulses(15 downto 0)
        #0x44A10120  #counts_to_acq_reset       #counts_to_acq_reset( 31 downto 0)
        #0x44A10120  #counts_to_acq_hold        #counts_to_hold_acq_reset( 31 downto 0)
        #0x44A100F8  #xadc                      #read
        #0x44A100F8  #admux                     #write
        #0x44A100FC  #was vmm_global_reset      #reset & vmm_gbl_rst_i & vmm_cfg_en_vec( 7 downto 0)
        #0x44A10100  #axi_reg_60( 0)            #original reset
        #0x44A10104,08,0C,00,14                 #user_reg_1 #user_reg_2 #user_reg_3 #user_reg_4         
        #0x44A10104,08,0C,00,14                 #user_reg_1 #user_reg_2 #user_reg_3 #user_reg_4 #user_reg_5
        #0x44A10118  #DS411_low                 #Low
        #0x44A1011C  #DS411_high                #High
        #0x44A10120  #counts_to_acq_reset       #0 to FFFF_FFFF #0=Not Used
        #0x44A10120  #counts_to_hold_acq_reset  #0 to FFFF_FFFF #0=Not Used

    def ping(self):
        print
        print "Pinging MMFE: %s" % (self.UDP_IP)
        os.system("ping %s -c 2" % (self.UDP_IP))
        print

    def write_vmm_config_all(self, widget):
        
        vmm_config_addresses = ["0x44A10204",
                                "0x44A102D0",
                                "0x44A1039C",
                                "0x44A10468",
                                "0x44A10534",
                                "0x44A10600",
                                "0x44A106CC",
                                "0x44A10798",
                                ]

        for vmm, address in zip(self.VMMs, vmm_config_addresses):
            self.write_vmm_config(None, vmm, address, False)

        self.load_IDs()

    def write_vmm_config(self, widget, vmm, address="0x44A10020", load=True):
        """ 
        Create full config list.
        Command strings must be <= 100 chars due to bram limitations on artix7.
        """
        reg           = vmm.get_channel_val()
        reglist       = list(vmm.reg.flatten())
        globalreglist = list(vmm.globalreg.flatten())
        fullreg       = reglist[::-1] + globalreglist[::-1] 

        n_words = len(fullreg) / 32
        if len(fullreg) % 32 != 0:
            fatal("Number of bits to write is not divisible by 32! Bad!")

        chunk_size         = 6
        words_to_write     = []
        vmm_config_address = address

        for iter in xrange(n_words):

            bits    = fullreg[iter*32:(iter+1)*32]
            bitword = convert_to_32bit(bits)
            words_to_write.append("0x{0:X}".format(bitword))

            if (iter+1) % chunk_size == 0 or iter == n_words-1:

                message = "w %s %s" % (vmm_config_address, " ".join(words_to_write))
                self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)
                time.sleep(0.1)

                words_to_write = []
                vmm_config_address = "0x{0:X}".format(int(vmm_config_address, base=16) + 4*chunk_size)

        if load:
            self.load_IDs()

    def print_vmm_config(self, widget, vmm):
        reg           = vmm.get_channel_val()
        reglist       = list(vmm.reg.flatten())
        globalreglist = list(vmm.globalreg.flatten())
        fullreg       = reglist[::-1] + globalreglist[::-1]

        n_words = len(fullreg) / 32

        for iter in xrange(n_words):
            bits    = fullreg[iter*32:(iter+1)*32]
            bitword = convert_to_32bit(bits)
            print "0x{0:08x}  register {1:2d}".format(bitword, iter)
        print

    def check_for_data(self):
        counter = 0
        print "hi", self.ext_trig_on
        while self.ext_trig_on==1:
            counter = counter + 1
            start = time.time()
            check_reading = self.udp.udp_client("r 0x44A10144 1", self.UDP_IP, self.UDP_PORT)
            if not check_reading:
                print "UDP communication failed in check_for_data, exiting on counter %i" % (counter)
                return
            print "time chkpt: ",time.time()-start
            check_reading_str = check_reading.split()
            if counter == 200:
                print "done reading, maybe no data?"
                break
            if int(check_reading_str[2], 16) is 1:
                bcidreg = "r 0x44A1014C 1" # read bcid_captured and external_trigger number in FPGA       
                check_bcidreg = self.udp.udp_client(bcidreg,self.UDP_IP,self.UDP_PORT)
                check_bcidreg_str = check_bcidreg.split()
                self.bcid_reg = check_bcidreg_str[2]
#                print "read_data register is up!"
#                sleep(.002)
                end = time.time()
                delta = end-start
                print "timing for check for data before start: ", delta
                self.start()
#                self.daq_readOut()
                break
        return

    def daq_readOut(self):
        data       = None
        fifo_count = 0
        attempts   = 10
        while fifo_count == 0 and attempts > 0:
            print "trying"
            attempts -= 1
            message = "r 0x44A10014 1" # word count of data fifo
            data = self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)
            print data
            if data != None:
                data_list  = data.split(" ")
                fifo_count = int(data_list[2], 16)
            #time.sleep(1)
        print "FIFOCNT ", fifo_count
        if data == None or fifo_count == 0:
            print "Warning: Did not receive data. Stop readout."
            return
        if fifo_count == 0:
            print "Warning: found 0 FIFO counts. Stop readout."
            return
        if fifo_count % 2 != 0:
            print "Warning: Lost one count in fifo reading."
            fifo_count -= 1

        bcidreg = "r 0x44A1014C 1" # read bcid_captured and external_trigger number in FPGA       
        check_bcidreg = self.udp.udp_client(bcidreg,self.UDP_IP,self.UDP_PORT)
        check_bcidreg_str = check_bcidreg.split()
        print check_bcidreg_str
#        word2 = int(check_bcidreg_str[2],   16)
        self.bcid_reg = check_bcidreg_str[2]

        peeks_per_cycle = 10
        cycles    = fifo_count / peeks_per_cycle
        remainder = fifo_count % peeks_per_cycle

        myfile = open('mmfe8TestQuiet.dat', 'a')

        for cycle in reversed(xrange(1+cycles)):
            
            peeks     = peeks_per_cycle if cycle > 0 else remainder
            message   = "k 0x44A10010 %s" % (peeks)
            data      = self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)

            if data != '!Err!':
                myfile.write(self.bcid_reg + '\t' + data +'\n')

    def read_xadc(self, widget):
        message = "x"
        for i in range(100):
            data      = self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)
            data_list = data.split()
            pd = [int(data_list[n], 16)/4096.0 for n in xrange(1, 9)]
            print 'XADC = {0:.4f} {1:.4f} {2:.4f} {3:.4f} {4:.4f} {5:.4f} {6:.4f} {7:.4f}'.format(pd[0],pd[1],pd[2],pd[3],pd[4],pd[5],pd[6],pd[7]) 
            s = '{0:.4f}\t{1:.4f}\t{2:.4f}\t{3:.4f}\t{4:.4f}\t{5:.4f}\t{6:.4f}\t{7:.4f}\n'.format(pd[0],pd[1],pd[2],pd[3],pd[4],pd[5],pd[6],pd[7])
            with open('mmfe8-xadc.dat', 'a') as myfile:
                myfile.write(s)  

    def send_external_trig(self, widget):
#        print "Sending Ext Trig"
        start = time.time()
        message = "w 0x44A10148 0"
        self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)
        message = "w 0x44A10148 1"
        self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)
#            time.sleep(trig)
        print "Send Ext Trig Pulse Completed"
        print "timing", time.time()-start
        self.check_for_data()
        message = "w 0x44A10148 0"
        self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)

    def leaky_readout(self, widget):
        self.readout_runlength[25] = 1 if widget.get_active() else 0
        self.write_readout_runlength()

    def internal_trigger(self, widget):
        self.readout_runlength[24] = 1 if widget.get_active() else 0
        self.write_readout_runlength()

    def external_trigger_w_pulse(self, widget):
        if widget.get_active():
            message = "w 0x44A1013C 1"
            self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)
            print "Ext Trig Signals are accompanied by a pulse"
        else:
            message = "w 0x44A1013C 0"
            self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)

    def external_trigger(self, widget):
        self.readout_runlength[26] = 1 if widget.get_active() else 0
        self.ext_trig_on = self.readout_runlength[26]
        print "self_ext_trig_on", self.ext_trig_on
        self.write_readout_runlength()

    def set_pulses(self, widget, entry=None):
        self.pulses = int(widget.get_text())
        word = '{0:010b}'.format(self.pulses)
        for bit in xrange(len(word)):
            self.readout_runlength[9 - bit] = int(word[bit])
        
        self.write_readout_runlength()

    def set_acq_reset_count(self, widget, entry=None):
        value   = int(widget.get_text(), base=16)
        message = "w 0x44A10120 %s" % (value)
        print "Writing %s counts to acq. reset" % (value)
        self.acq_reset_count = value
        self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)

    def set_acq_reset_hold(self, widget, entry=None):
        value   = int(widget.get_text(), base=16)
        message = "w 0x44A10124 %s" % (value)
        print "Writing %s counts to acq. hold" % (value)
        self.acq_reset_hold = value
        self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)

    def start(self):
        self.control[2] = 1
        self.write_control()

        self.daq_readOut()                   
        #time.sleep(1)

        self.control[2] = 0
        self.write_control()

    def vmm_load_configs(self, widget):
        for ivmm, vmm in enumerate(self.VMMs):
            if self.vmm_load[ivmm]:
                self.vmm_cfg_sel[ivmm] = 1
                self.write_vmm_config(None, vmm)
                self.system_init(None)
                self.system_load(None)
                time.sleep(1)
                self.vmm_cfg_sel[ivmm] = 0

    def vmm_load_readout(self, widget):
        self.load_IDs()

    def vmm_global_reset(self, widget):

        for ivmm in xrange(len(self.VMMs)):
            self.vmm_cfg_sel[ivmm] = 1
        self.load_IDs()

        self.control[0] = 1
        self.write_control()
        
        time.sleep(0.1)
        
        self.control[0] = 0
        self.write_control()
        
        for ivmm in xrange(len(self.VMMs)):
            self.vmm_cfg_sel[ivmm] = 0
        self.load_IDs()

    def reset_global(self, widget):
        self.control[0] = 1
        self.write_control()

        time.sleep(1)

        self.control[0] = 0
        self.write_control()

    def system_init(self, widget):
        self.control[1] = 1
        self.write_control()

        time.sleep(1)

        self.control[1] = 0
        self.write_control()

    def system_load(self, widget):
        self.control[3] = 1
        self.write_control()

        time.sleep(1)

        self.control[3] = 0
        self.write_control()

    def write_control(self):
        message = "w 0x44A100FC 0x{0:X}".format(convert_to_32bit(self.control))
        self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)
                        
    def write_readout_runlength(self):
        message = "w 0x44A100F4 0x{0:X}".format(convert_to_32bit(self.readout_runlength))
        self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)
        
    def write_vmm_cfg_sel(self):
        message = "w 0x44A100EC 0x{0:X}".format(convert_to_32bit(self.vmm_cfg_sel))
        self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)
                        
    def set_IDs(self, widget):
        self.load_IDs()

    def load_IDs(self):
        self.write_vmm_cfg_sel()
        self.write_readout_runlength()

    def set_ip(self, widget):
        self.UDP_IP = widget.get_text()

        try:
            self.mmfeID = self.ipAddr.index(self.UDP_IP)
        except:
            print "Warning: Did not find %s in list of valid IP addresses. Set mmfeID=0." % (self.UDP_IP)
            self.mmfeID = 0

        word = '{0:04b}'.format(self.mmfeID)
        for bit in xrange(len(word)):
            self.vmm_cfg_sel[11 - bit] = int(word[bit])
        print
        print "Set MMFE8 IP address = %s" % (self.UDP_IP)
        print "Set MMFE8 ID         = %s" % (self.mmfeID)
        print "Does MMFE8 ID mean anything?"
        print

        last_three_digits = self.UDP_IP.split(".")[-1]
        last_digit        = last_three_digits[-1]
        last_digit_hex    = hex(int(last_digit))
        message = "w 0x44A10150 %s" % (last_digit_hex)
        print "Writing last digit of IP address: %s" % (last_digit_hex)
        self.udp.udp_client(message, self.UDP_IP, self.UDP_PORT)

    def set_display(self, widget):
        word = '{0:05b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.vmm_cfg_sel[16 - bit] = int(word[bit])
        self.write_vmm_cfg_sel()

    def set_display_no_enet(self, widget):
        word = '{0:05b}'.format(widget.get_active())
        for bit in xrange(len(word)):
            self.vmm_cfg_sel[16 - bit] = int(word[bit])
        # self.write_vmm_cfg_sel()

    def readout_vmm_callback(self, widget, ivmm):
        self.readout_runlength[16+ivmm] = 1 if widget.get_active() else 0
        # self.load_IDs()

    def reset_vmm_callback(self, widget, ivmm):
        self.vmm_cfg_sel[ivmm] = 1 if widget.get_active() else 0
        # self.load_IDs()

    def load_vmm_callback(self, widget, ivmm):
        self.vmm_load[ivmm] = 1 if widget.get_active() else 0



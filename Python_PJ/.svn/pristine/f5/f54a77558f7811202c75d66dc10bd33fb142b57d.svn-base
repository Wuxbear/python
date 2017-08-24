# -*- coding: utf-8 -*-
import telnetlib
from time import sleep
import socket
from tkinter import END
from tkinter.messagebox import askyesno, showerror
from ORZ_exception import *
from JDEBUG import __JDEBUG__
import os

TP_KEY_WORDS_MAP = {}

def tp_engine_fp_init(x):
    TP_KEY_WORDS_MAP = x

def FGT_80C_engine(stop_event, sn, dn, tp_cmds):
##def tp_engine(gui, dev_setup, stop_event, tp_cmds):
    ### parser support device
    ### get the relative commands
    ### process the commands
    ### process the tp_cmds, replace the SN, DN
    tp_len = len(tp_cmds)
    line = 0
    tn = None
    
    while line != tp_len:
        if (stop_event.is_set()):
            break
        elif tp_key in TP_KEY_WORDS_MAP.keys():
            if tp_key.startswith("telnet"):
                data = tp_cmds[line].split(' ',1)[1]
                if tp_key.startswith("telnet_connect"):
                    tn = TP_KEY_WORDS_MAP[tp_key](data)
                else:
                    TP_KEY_WORDS_MAP[tp_key](tn, data)
            elif tp_key.startswith("console"):
                if tp_key.startswith("console_open"):
                    tn = TP_KEY_WORDS_MAP[tp_key](dev_setup["COM"])
                elif tp_key.startswith("console_close"):
                    TP_KEY_WORDS_MAP[tp_key](tn)
                elif tp_key.startswith("console_read"):
                    data = tp_cmds[line].split(' ',1)[1]
                else:
                    data = tp_cmds[line].split(' ',1)[1]
                    TP_KEY_WORDS_MAP[tp_key](tn, data)            
            else:
                TP_KEY_WORDS_MAP[tp_key](data)
        else:
            print("Not support keyword : %s\n" % tp_key)
            break
        
        line += 1

def manager(manager_q, devices_q_list):
    '''
    Handle the devices request
    '''
    while True:
        sleep(5)
        while not manager_q.empty():
            request = manager_q.get()
            dn, req = request.split(' ', 1)
##            print("dn:%s, req:%s" % (dn,req))
            if req.startswith("system_write"):
                scmd = req.split(' ',1)[1]
##                print(scmd)
                x = os.popen(scmd)
                result = x.readlines()
                x.close()
##                print(result)
                devices_q_list[int(dn)].put(result)
            elif req.startswith("service"):
                x, fgt, cmd, sn = req.split(' ',3)
##                print(x,'\n', fgt, '\n', cmd,'\n', sn)
                ### use the plugin method?
                if cmd.startswith("register"):
                    ### command process
                    sleep(3)
                    fx = "IP: 192.168.1.xxx"
                    devices_q_list[int(dn)].put(fx)
                    ### return IP
                elif cmd.startswith("remove"):
                    sleep(3)
                    devices_q_list[int(dn)].put("remove")

    print("mthread_close!")


def tp_engine(gui, dev_setup, stop_event, tp_cmds):
    tp_len = len(tp_cmds)
    line = 0
    sr = None
    tn = None
    
    log = open(dev_setup['SN']+".txt",mode='ab')
    
    while line != tp_len:
        # check stop event to break out!!!
        if (stop_event.is_set()):
            break
        
        print(tp_cmds[line])
        tp_key = tp_cmds[line].split()[0]
        try:
            if tp_key.startswith("sleep"):
                sleep(int(tp_cmds[line].split()[1]))
            elif tp_key.startswith("check_box"):
                if askyesno("check", tp_cmds[line].split(' ',1)[1]) == True:
                    pass
                else:
                    break
            elif tp_key.startswith("gui_item_pass"):
                gui.chk_button[gui.testing_item].config(text = gui.item_list[gui.testing_item] + " : PASS", bg = "green")
                gui.testing_item += 1
            elif tp_key.startswith("gui_end"):
                gui.go.config(text = "restart", bg = "blue", command = gui.FRAME_TEST_PACKAGE_restart)
            elif tp_key.startswith("power"):
                # for engine test
                if tp_key.startswith("power1"):
                    dev_power_port = dev_setup["PCS1"]
                elif tp_key.startswith("power2"):
                    dev_power_port = dev_setup["PCS2"]
                else:
                    print("cmd error!!!")

                if tp_key.endswith("on"):
                    TP_KEY_WORDS_MAP["power_on"](dev_power_port)
                elif tp_key.endswith("off"):
                    TP_KEY_WORDS_MAP["power_off"](dev_power_port)

                #push the power on/off request to manager thread?
            elif tp_key.startswith("system"):
                if tp_key.startswith("system_write"):
##                print("put to queue: " + str(dev_setup["dev_number"]) + ' ' + tp_cmds[line])
                    dev_setup["manager_q"].put(str(dev_setup["dev_number"]) + ' ' + tp_cmds[line])
                elif tp_key.startswith("system_read"):
                    d = tp_cmds[line].split(' ',1)[1]
                    sr = dev_setup["device_q"].get()
                    print(sr)
                    if any(d in s for s in sr):
                        pass
                    else:
                        print("miss!")
##                        raise ORZ_SystemFail
                else:
                    print("ooxx")
##                    raise ORZ_SystemFail

            elif tp_key.startswith("service"):
                ### couple-pair program, write/read
                dev_setup["manager_q"].put(str(dev_setup["dev_number"]) + ' ' + tp_cmds[line])
                x = dev_setup["device_q"].get()
                print("dev service response: ", x)
            
            elif tp_key in TP_KEY_WORDS_MAP.keys():
                if tp_key.startswith("telnet"):
                    data = tp_cmds[line].split(' ',1)[1]
                    if tp_key.startswith("telnet_connect"):
                        tn = TP_KEY_WORDS_MAP[tp_key](data)
                    else:
                        TP_KEY_WORDS_MAP[tp_key](tn, data)
                elif tp_key.startswith("console"):
                    if tp_key.startswith("console_open"):
                        tn = TP_KEY_WORDS_MAP[tp_key](dev_setup["COM"])
                    elif tp_key.startswith("console_close"):
                        TP_KEY_WORDS_MAP[tp_key](tn)
                    elif tp_key.startswith("console_read"):
                        data = tp_cmds[line].split(' ',1)[1]
                        if __JDEBUG__:
                            gui.text.insert(END, "[CMD]-->" + tp_cmds[line] + "\n")
                        else:
                            rx_data = TP_KEY_WORDS_MAP[tp_key](tn, data)
                            gui.text.insert(END, rx_data)
                            gui.text.yview(END)
                            #log.write(rx_data)
                    else:
                        data = tp_cmds[line].split(' ',1)[1]
                        TP_KEY_WORDS_MAP[tp_key](tn, data)            
                else:
                    TP_KEY_WORDS_MAP[tp_key](data)
            else:
                print("Not support keyword : %s\n" % tp_key)
                break
        except:
                print("fail in line %d!: \t" % line, tp_cmds[line],'\n')
                showerror("TestPackage cmd fail!", "line %d: \t" % line, tp_cmds[line],'\n')
                gui.go.config(text = "restart", bg = "blue", command = gui.FRAME_TEST_PACKAGE_restart)
                break
        line += 1
        
    log.close()


def test():
    tp_cmds = [
        "power1_on",
        "sleep 120",
        "telnet_connect 192.168.1.2",
        "telnet_read 10 login:",
        "telnet_write admin",
        #"sleep 5",
        "telnet_read 10 #",
        "telnet_write fap-get-status",
        "telnet_read 10 Version: FortiAP-14C v5.2,build0234,150324 (GA)",
        "telnet_read 10 Serial-Number: FAP14C3X13002870",
        "telnet_read 10 BIOS version: 04000002",
        "telnet_read 10 Branch point: 234",
        "telnet_read 10 #",
        "telnet_write ifconfig eth0",
        "telnet_read 10 #",
        "telnet_write restore FAP_14C-v5-build0234-fortinet.out 192.168.1.168",
        "telnet_read 30 Do you want to continue? (y/n)",
        "telnet_write y",
        "telnet_read 60 Please wait system to restart.",
        "sleep 180",
        #"telnet_disconnect",
        "telnet_connect 192.168.1.2",
        "telnet_read 10 login:",
        "telnet_write admin",
        "telnet_read 10 #",
        "telnet_write cfg -x",
        "telnet_read 30 #",
        "telnet_disconnect",
        "sleep 5",
        "power1_off",
        ]
    #tp_engine(tp_cmds)
    #tp_engine(console_test_cmds)
    
if __name__ == "__main__":
    test()

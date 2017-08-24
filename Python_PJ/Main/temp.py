import threading
import queue
import time import sleep
from ORZ_engine import *

event = threading.Event()
manager_queue = queue.Queue()
device1_queue = queue.Queue()
device2_queue = queue.Queue()

device_queue_list = [device1_queue, device2_queue]

### manager service
### service_name: cmd_list

test_manager_cmds = ["preconfig ooxxxx",
                     "wait_queue",
                     "loop"]

power_test_cmds = [
        "telnet_connect 192.168.1.100",
        "telnet_read 10 Synaccess Inc. Telnet Session V6.",
        "telnet_write pset 1 1",
        "sleep 5",
        "telnet_read 10 >",
        "telnet_write pset 1 0",
        "telnet_read 10 >",
        "telnet_disconnect"]

test_device_cmds = ["power up",
                    "sleep 60",
                    "console_write fap-get-status",
                     "console_read 10 Version:",
                     "sleep 10",
                    "system ifconfig",
                    "sleep 5",
                    "console_write reboot",
                    "power down",
                    "sleep 5",
                    "power up"]

TP_MANGER_DATA = {  "event":event,
                    "manager_queue":manager_queue,
                    "device_queue_list":device_queue_list,
                    "test_cmds":test_manager_cmds
                }

TP_DEV1_DATA = {"DEV_number":0,
                "DEV_SN":"FPPPPP_00001"
               "event":event,
               "manager_queue":manager_queue,
               "device_queue":device1_queue,
               "test_cmds":test_device_cmds}

TP_DEV2_DATA = {"DEV_number":1,
                "DEV_SN":"FPPPPP_00099"
               "event":event,
               "manager_queue":manager_queue,
               "device_queue":device2_queue,
               "test_cmds":power_test_cmds}

def manager_thread(manager_data):
    """
    handle the system, power service, 80C service?
    the servies method will be one shut( open ... action ... close)
    """
    while not manager_data["event"].isSet():
        sleep(5)
        while not manager_data["manager_queue"].empty():
            x= manager_data["manager_queue"].get()
            print(x)
            if x.split(' ',1)[0] == "dev":
                o, dev_n, syscmd = x.split(' ',2)
                print("get!", o, dev_n, syscmd)
                response = syscmd + " ack"
                print("response! ", response)
                manager_data["device_queue_list"][int(dev_n)].put(response)
                sleep(3)

    print("mthread_close!")
        
def device_thread(device_data):
    print("Thread for Device: ", device_data["DEV_number"])
    lp_len = len(device_data["test_cmds"])
    line = 0
    log = open('device' + str(device_data["DEV_number"]) + '.txt', mode='w+')
    while not device_data["event"].isSet():
        print(device_data["test_cmds"][line])
        log.write(device_data["test_cmds"][line])
        if device_data["test_cmds"][line].split(' ',1)[0] == "system":
            device_data["manager_queue"].put("dev "+str(device_data["DEV_number"])+" ifconfig")
            print(device_data["device_queue"].get())
        line += 1
        sleep(1)
        if line == lp_len:
            print("Test done!, create report log!")
            break

    # test package down, create report
    print(str(device_data["DEV_number"]),"_close!")
    log.close()


def manager_engine(manager_data):
    """
    handle the system, power service, 80C service?
    the servies method will be one shut( open ... action ... close)
    """
    while not manager_data["event"].isSet():
        sleep(5)
        while not manager_data["manager_queue"].empty():
            x= manager_data["manager_queue"].get()
            if x.split(' ',1)[0] == "dev":
                o, dev_n, syscmd = x.split(' ',2)
                print("get!", o, dev_n, syscmd)
                response = syscmd + " ack"
                print("response! ", response)
                manager_data["device_queue_list"][int(dev_n)].put(response)
                sleep(3)

    print("mthread_close!")

def device_engine(device_data):
    print("Thread for Device: ", device_data["DEV_number"])
    tp_cmds = device_data["test_cmds"]
    device_number = device_data["DEV_number"]
    lp_len = len(tp_cmds)
    line = 0
    tn = None
    counter = None
    looper = None
    #open log
    log = open(device_data["DEV_SN"]+'.txt', mode='a+')
    # write the whole test script?
    log.write("--------Test Start--------"+)
    while not device_data["event"].isSet():
        tp_key = tp_cmds[line].split()[0]
        if tp_key in TP_KEY_WORDS_MAP.keys():
            try:               
                if tp_key.startswith("telnet"):
                    if tp_key.startswith("telnet_connect"):
                        tn = TP_KEY_WORDS_MAP[tp_key](tp_cmds[line], log)
                    else:
                        TP_KEY_WORDS_MAP[tp_key](tn, tp_cmds[line], log)
                elif tp_key.startswith("system"):
                    log.write(tp_cmds[line]+'\n')
                    TP_KEY_WORDS_MAP[tp_key](str(device_number), manager_queue, device_queue, tp_cmds[line])
                elif tp_key.startswith("power"):
                    log.write(tp_cmds[line]+'\n')
                    TP_KEY_WORDS_MAP[tp_key](device_number, tp_cmds[line])
                elif tp_key.startswith("message"):
                    log.write(tp_cmds[line].split(' ',1)[1]+'\n')
                else:
                    TP_KEY_WORDS_MAP[tp_key](tp_cmds[line])
            except:
                # check retry_flag, loop test, back the label mark line
                print("fail in line %d!\n" % line, tp_cmds[line])
                break
        else:
            print("Not support keyword : %s\n" % tp_key, tp_cmds[line])
            break
        
        line += 1
        sleep(1)
        if line == lp_len:
            print("Test done!, create report!")
            break
    #close log
    log.write("--------Test End--------")
    log.close()


def test():
    #man = threading.Thread(target=manager_thread, args=(TP_MANGER_DATA,))
    dx = threading.Thread(target=device_engine, args=(TP_DEV2_DATA,))
    #do = threading.Thread(target=device_thread, args=(TP_DEV2_DATA,))

    #man.start()
    dx.start()
    #do.start()

    #sleep(20)
    #print("close all thread")
    #event.set()

    #man.join()
    dx.join()
    #do.join()
    print("all down!")  

def main():
    device_list = []

    # the manager thread is independent
    mh = threading.Thread(target=manager_engine, args=(TP_MANGER_DATA,))
    mh.start()
    
    # init the list
    for x in range(2):
        w = None
        device_list.append(w)
    
    while True:
        try:
            x = int(input("input which thread to run:"))
            if x == 99:
                break
            if device_list[x] == None:
                print(x)
                device_list[x] = threading.Thread(target=device_engine, args=(TP_DEV2_DATA,))
                device_list[x].start()
            elif device_list[x].isAlive():
                print("thread is running!", device_list[x])
            else:
                print(x)
                device_list[x] = threading.Thread(target=device_engine, args=(TP_DEV2_DATA,))
                device_list[x].start()
        except:
            pass

if __name__ == '__main__':
    #main()
    test()

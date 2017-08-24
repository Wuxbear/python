import threading
import queue
from time import sleep

event = threading.Event()
manager_queue = queue.Queue()
device1_queue = queue.Queue()
device2_queue = queue.Queue()

device_queue_list = [device1_queue, device2_queue]

test_manager_cmds = ["preconfig ooxxxx",
                     "wait_queue",
                     "loop"]

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
               "event":event,
               "manager_queue":manager_queue,
               "device_queue":device1_queue,
               "test_cmds":test_device_cmds}

TP_DEV2_DATA = {"DEV_number":1,
               "event":event,
               "manager_queue":manager_queue,
               "device_queue":device2_queue,
               "test_cmds":test_device_cmds}

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
                response = syscmd + " ack" + "\n\n\noooxoxoxoxoxo\n\n\niadfkjasf\n"
                print("response! ", response)
                manager_data["device_queue_list"][int(dev_n)].put(response)
                sleep(3)

    print("mthread_close!")
        
def device_thread(device_data):
    print("Thread for Device: ", device_data["DEV_number"])
    lp_len = len(device_data["test_cmds"])
    line = 0
    while not device_data["event"].isSet():
        print(device_data["test_cmds"][line])
        if device_data["test_cmds"][line].split(' ',1)[0] == "system":
            device_data["manager_queue"].put("dev "+str(device_data["DEV_number"])+" ifconfig")
            print(device_data["device_queue"].get())
        line += 1
        sleep(1)
        if line == lp_len:
            print("Test done!, create report log!")
            break

    print(str(device_data["DEV_number"]),"_close!")    

man = threading.Thread(target=manager_thread, args=(TP_MANGER_DATA,))
dx = threading.Thread(target=device_thread, args=(TP_DEV1_DATA,))
do = threading.Thread(target=device_thread, args=(TP_DEV2_DATA,))


man.start()
dx.start()
do.start()

sleep(20)
print("close all thread")
event.set()

man.join()
dx.join()
do.join()
print("all down!")


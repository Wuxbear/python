from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror,showinfo
from tkinter.scrolledtext import ScrolledText
from time import sleep
from threading import *
import queue

### private lib
from ORZ_engine import *
from ORZ_equipment import *
from ORZ_parser import config_dev_setting
from test_fake_data import *
from JDEBUG import __JDEBUG__

class ORZ_GUI:
    fake_test_items = ["SN check", "OS update", "Wifi", "Factory reset"]
    Software_info = {"SW_version":"0000", "Author":"JohnnyWu"}
    Window_Setup = {"Max_devices":4}
    DEV1_Setup = {"COM":1,"PCS1":1,"PCS2":2}
    DEV2_Setup = {"COM":2,"PCS1":3,"PCS2":4}
    DEV3_Setup = {"COM":3,"PCS1":5,"PCS2":6}
    DEV4_Setup = {"COM":4,"PCS1":7,"PCS2":8}
    DEV5_Setup = {"COM":5,"PCS1":9,"PCS2":10}
    DEV6_Setup = {"COM":6,"PCS1":11,"PCS2":12}
    DEV_SETUP = {"window1":DEV1_Setup, "window2":DEV2_Setup, "window3":DEV3_Setup,
                 "window4":DEV4_Setup, "window5":DEV5_Setup, "window6":DEV6_Setup}
    Equipment_Resource = {"ATE_ip":"192.168.1.168","ConsoleEquipment":{},"PowerEquipment":{}}
    TP_KEY_WORDS_MAP = {
        "telnet_connect":telnet_connect,
        "telnet_disconnect":telnet_disconnect,
        "telnet_read":telnet_read,
        "telnet_write":telnet_write,
        "console_open":None,
        "console_close":None,
        "console_read":None,
        "console_write":None,
        "power_on":None,
        "power_off":None,
        }
    MANAGER_QUEUE = None
    DEVICES_QUEUE_LIST = []
    DEVICES_QUEUE_LIST.append(None)
            
    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close_handler)
        self.menubar = Menu(self.master)

        self.setup_menu = Menu(self.menubar, tearoff = 0)
        self.setup_menu.add_command(label="Window Setup", command = self.Window_setup)
        self.setup_menu.add_separator()
        self.setup_menu.add_command(label="Equipments Setting", command = self.Equipment_setup)
        self.menubar.add_cascade(label="Setup", menu = self.setup_menu)

        self.setup_menu = Menu(self.menubar, tearoff = 0)
        self.setup_menu.add_command(label="Sync", command = self.sync)
        self.menubar.add_cascade(label="DataBase", menu = self.setup_menu)

        self.help_menu = Menu(self.menubar, tearoff = 0)
        self.help_menu.add_command(label="Info", command = self.help)
        self.menubar.add_cascade(label="Help", menu = self.help_menu)
        self.master.config(menu = self.menubar)

        self.load_equipment_cfg()
        tp_engine_fp_init(TP_KEY_WORDS_MAP)
        
        ORZ_GUI.MANAGER_QUEUE = queue.Queue()
        
        try:            
             equipments_open()
        except Exception as ex:
##            template = "An exception of type {0} occured. Arguments:\n{1!r}"
##            message = template.format(type(ex).__name__, ex.args)
##            showerror("Equipment Error", ex.args[1] + "\n\nPlease check equipment setup!")
##            self.master.destroy()
            showerror("Equipment Error", "\n\nPlease check equipment setup!")
            self.master.destroy()
        else:
            self.create_dev_window()

        m = Thread(target = manager, args = ( ORZ_GUI.MANAGER_QUEUE, ORZ_GUI.DEVICES_QUEUE_LIST))
        m.start()
        
    def close_handler(self):
        print("release resource before program close!!")
        equipments_close()
        self.master.destroy()
    
    def sync(self):
        print("sync data to FLDB2.")

    def help(self):
        showinfo("Version",
                 """Hahahahahahaha!!!~~~~\n""" + "SW Version : " + self.Software_info["SW_version"])
        
    def create_dev_window(self):
        self.devWindow = []
        mx = ORZ_GUI.Window_Setup["Max_devices"]
        s_w_max = self.master.winfo_screenwidth()/(mx/2) - 20
        s_h_max = self.master.winfo_screenheight()/2 - 20
        
##        for number in range(mx):
        for number in range(1,mx+1):
            locate = number - 1
            devWindow = Toplevel(self.master)
            devWindow.focus()

            if (locate % 2) == 0:
                px = 0 + (s_w_max * (locate/2))
                py = 0
            else:
                px = 0 + (s_w_max * ((locate-1)/2))
                py = s_h_max
            devWindow.geometry(("%dx%d+%d+%d")%(s_w_max,s_h_max,px,py))
            # pass the device setup to sub window
            #DEV_WINDOW(devWindow, ORZ_GUI.DEV_SETUP['window'+str(number+1)])
            #DEV_WINDOW(devWindow, ORZ_GUI.Test_Package)
            self.devWindow.append(devWindow)

            dq = queue.Queue()
            ORZ_GUI.DEVICES_QUEUE_LIST.append(dq)
            ORZ_GUI.DEV_SETUP['window'+str(number)]['device_q'] = dq
            ORZ_GUI.DEV_SETUP['window'+str(number)]['manager_q'] = ORZ_GUI.MANAGER_QUEUE
            ORZ_GUI.DEV_SETUP['window'+str(number)]['dev_number'] = number
            DEV_WINDOW(devWindow, ORZ_GUI.DEV_SETUP['window'+str(number)])

    def load_equipment_cfg(cls):
        # load equipmnet cfg and init
        if __JDEBUG__:
            equipment_init(FAKE_Power_cfg, cls.Equipment_Resource["PowerEquipment"], TP_KEY_WORDS_MAP)
            equipment_init(FAKE_Console_cfg, cls.Equipment_Resource["ConsoleEquipment"], TP_KEY_WORDS_MAP)
        else:
            power_cfg = config_dev_setting("power_equipment.txt", "PowerEquipment")
            equipment_init(power_cfg, cls.Equipment_Resource["PowerEquipment"], TP_KEY_WORDS_MAP)
            print(cls.Equipment_Resource["PowerEquipment"])
            console_cfg = config_dev_setting("console_equipment.txt", "ConsoleEquipment")
            equipment_init(console_cfg, cls.Equipment_Resource["ConsoleEquipment"], TP_KEY_WORDS_MAP)
            print(cls.Equipment_Resource["ConsoleEquipment"])
            
##        equipment_init(power_cfg, cls.Equipment_Resource, TP_KEY_WORDS_MAP)
##        equipment_init(console_cfg, cls.Equipment_Resource, TP_KEY_WORDS_MAP)
##        equipment_init(FAKE_Power_cfg, cls.Equipment_Resource, TP_KEY_WORDS_MAP)
##        equipment_init(FAKE_Console_cfg, cls.Equipment_Resource, TP_KEY_WORDS_MAP)       
        
    def Equipment_setup(cls):
        print(cls.Equipment_Resource)
            
    def Window_setup(cls):
        print(cls.DEV_SETUP)

class Test_Thread(Thread):
    def __init__(self, gui, dev, stop_event, tp_cmds):
        self.gui = gui
        self.dev = dev
        self.stop_event = stop_event
        self.tp_cmds = tp_cmds
        Thread.__init__(self)

    def run(self):
        tp_engine(self.gui, self.dev, self.stop_event, self.tp_cmds)
            
class DEV_WINDOW:
    number = 0
    def __init__(self, parent, dev_setup):
        self.parent = parent
        self.dev_setup = dev_setup
##        DEV_WINDOW.number += 1
##        parent.title("DUT Window"+str(DEV_WINDOW.number))
        self.parent.title("DUT Window" + str(self.dev_setup["dev_number"]))
        self.parent.protocol("WM_DELETE_WINDOW", self.close_handler)       
        
##        self.dev_setup["dev_number"] = DEV_WINDOW.number
        print(dev_setup['device_q'], " ", dev_setup['manager_q'])
        self.menubar = Menu(self.parent)
        self.file_menu = Menu(self.parent, tearoff = 0)
        self.file_menu.add_command(label="Open", command = self.load_test_package)
        self.menubar.add_cascade(label="Test Package", menu=self.file_menu)
        self.parent.config(menu = self.menubar)
        self.frame = Frame(self.parent)
        self.dev_sn = Label(self.parent, text = "device serial number", relief=RIDGE)
        self.dev_sn.grid(sticky = W, padx=10)

     
    def close_handler(self):
        print("hahaha, you can't close me")

    def load_test_package(self):
        if self.frame != None:
            self.frame.destroy()
        
        fname = askopenfilename(filetypes=(("python files", "*.py"),
                                           ("All files", "*.*") ))
        print("open and parser test package",fname)
        
        # parser test package data
        # load test package
        self.test_package = fake_test_package
        self.FRAME_DATA_CHECK()
        
    def FRAME_DATA_CHECK(self):
        self.frame = Frame(self.parent)
        self.dev_data = StringVar()
        # get the check info from test package?
        self.d_info = {"SN":"", "HW":"", "SW":""}
        
        self.l1 = Label(self.frame, text = " SN: ", relief=RIDGE)
        self.l1.grid(sticky = W, padx=10)
        self.l2 = Label(self.frame, text = " HW: ", relief=GROOVE)
        self.l2.grid(sticky= W, padx=10)
        self.l3 = Label(self.frame, text = " SW: ", relief=SUNKEN)
        self.l3.grid(sticky= W, padx=10)
        self.entry = Entry(self.frame, textvariable = self.dev_data)
        self.entry.focus()
        self.entry.bind("<Return>", self.FRAME_DATA_CHECK_run)
        self.entry.grid()
        self.frame.grid()

    def FRAME_DATA_CHECK_run(self, event):
        if self.dev_data.get() == self.test_package["Device_info"]["SN"]:
            self.l1.config(text = " SN : " + self.dev_data.get())
            self.d_info["SN"] = self.dev_data.get()
            self.dev_setup["SN"] = self.dev_data.get()
        elif self.dev_data.get() == self.test_package["Device_info"]["HW"]:
            self.l2.config(text = " HW : " + self.dev_data.get())
            self.d_info["HW"] = self.dev_data.get()
        elif self.dev_data.get() == self.test_package["Device_info"]["SW"]:
            self.l3.config(text = " SW : " + self.dev_data.get())
            self.d_info["SW"] = self.dev_data.get()
        else:
            print("not match")
            
        self.entry.delete(0,'end')
        ## check all device_info and quit if all data match!
        self.dc = 0
        for i in self.d_info.values():
            if i == '':
                break
            self.dc += 1
            
        if self.dc == len(self.d_info):
            self.frame.destroy()
            self.FRAME_TEST_PACKAGE()

    def FRAME_TEST_PACKAGE(self):
        self.frame = Frame(self.parent)
        self.testing_item = 0
        self.item_list = self.test_package["Test_Items"]
        self.chk_var = []
        self.chk_button = []

        for n in range(len(self.item_list)):
            var = IntVar()
            var.set(1)
            chk = Checkbutton(self.frame, text = self.item_list[n], variable = var)
            chk.grid(sticky = W)
            self.chk_button.append(chk)
            self.chk_var.append(var)
            
        self.go = Button(self.frame, text = "Go", command = self.FRAME_TEST_PACKAGE_go, bg="green")
        self.go.grid()

        self.text = ScrolledText(self.frame)
        self.text.grid()
        self.frame.grid()
        
    def FRAME_TEST_PACKAGE_go(self):
        print("start test")
        self.cl = [None] * len(self.item_list)
        for n in range(len(self.item_list)):
            self.cl[n] = self.chk_var[n].get()

        # self.cl : check result?
        print(self.cl)

        for x in self.chk_button:
            x.config(state="disabled")
            
        self.go.config(text = "Stop", command = self.FRAME_TEST_PACKAGE_stop, bg = "red")
        self.stop_event = Event()
        t = Test_Thread(self, self.dev_setup, self.stop_event, self.test_package["Tp_cmds"])
        t.start()
        
    def FRAME_TEST_PACKAGE_stop(self):
        print("stop test")
        self.stop_event.set()
        self.go.config(text = "restart", bg = "blue", command = self.FRAME_TEST_PACKAGE_restart)
        # stop/restart the process

    def FRAME_TEST_PACKAGE_restart(self):
        print("restart test")
        self.frame.destroy()
        self.FRAME_DATA_CHECK()
        

def main():
    root = Tk()
    root.title("ORZ_QS_TOOL")
    screen_width_max = root.winfo_screenwidth()
    screen_height_max = root.winfo_screenheight()
    root.geometry(("%dx%d")%(screen_width_max,screen_height_max))
    orz = ORZ_GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()


# -*- coding: utf-8 -*-

import telnetlib
from time import sleep

# Equipments that manager by ATE
Equipment_open_list = []
Equipment_close_list = []

def telnet_connect(ip):
    tn = telnetlib.Telnet(ip,23,5)
    return tn

def telnet_disconnect(tn):
    #empty the buffer ?
    #tn.read_very_eager()
    tn.close()
    
def telnet_read(tn, x):
    print(x)
    timeout, msg = x.split(' ',2)
    return tn.read_until(msg.encode('ascii'), int(timeout))
    
def telnet_write(tn, x):
    print(x)
    tn.write(bytes(x.encode('ascii')))

def equipment_init(cfg, resource_data, tp_func_map):
    #load the config file and setup the relate function
    #regist the resoucre to manager
    if cfg["name"] == "netBooter":
        import Equip.netBooter as netBooter
        netBooter._setup_ip(cfg["ip"])
        resource_data["name"] = cfg["name"]
        resource_data[cfg["name"]+'_ip'] = cfg["ip"]
        resource_data["power_ports"] = cfg["ports"]
        Equipment_open_list.append(netBooter._open)
        Equipment_close_list.append(netBooter._close)
        tp_func_map["power_on"] = netBooter._power_on
        tp_func_map["power_off"] = netBooter._power_off
        return True
    elif cfg["name"] == "fake_power":
        import Equip.fake_power as fake_power
        resource_data["name"] = cfg["name"]
        resource_data["power_ports"] = cfg["ports"]
        Equipment_open_list.append(fake_power._open)
        Equipment_close_list.append(fake_power._close)
        tp_func_map["power_on"] = fake_power._power_on
        tp_func_map["power_off"] = fake_power._power_off
        return True
    elif cfg["name"] == "C2600":
        import Equip.C2600 as C2600
        C2600._setup_ip(cfg["ip"])
        resource_data["name"] = cfg["name"]
        resource_data[cfg["name"]+'_ip'] = cfg["ip"]
        resource_data["console_ports"] = cfg["ports"]
        tp_func_map["console_open"] = C2600._open
        tp_func_map["console_read"] = C2600._read
        tp_func_map["console_write"] = C2600._write
        tp_func_map["console_close"] = C2600._close
        return True
    elif cfg["name"] == "fake_console":
        import Equip.fake_console as fake_console
        fake_console._setup_ip(cfg["ip"])
        resource_data[cfg["name"]+'_ip'] = cfg["ip"]
        resource_data["console_ports"] = cfg["ports"]
        tp_func_map["console_open"] = fake_console._open
        tp_func_map["console_read"] = fake_console._read
        tp_func_map["console_write"] = fake_console._write
        tp_func_map["console_close"] = fake_console._close
        return True
    else:
        print(cfg["name"] + " not support!")
        return False

def equipments_open():
    #open all equipment before program start
    for open_func in Equipment_open_list:
        open_func()

def equipments_close():
    #close all equipment before program terminate
    for close_func in Equipment_close_list:
        close_func()

def test():
    Equipment_Resource = {
        "power_ports":None,
        "console_ports":None,
        }

    FAKE_netBooter_cfg = {
        "name":"netBooter",
        "ports":8,
        "ip":"192.168.1.100",
    }

    FAKE_C2600_cfg = {
        "name":"C2600",
        "ports":8,
        "ip":"192.168.1.99",
    }
    
    FAKE_Console_cfg = {
        "name":"fake_console",
        "ports":8,
        "ip":"192.168.1.99",
    }

    TP_K = {
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
    
    equipment_init(FAKE_netBooter_cfg, Equipment_Resource, TP_K)
    equipment_init(FAKE_C2600_cfg, Equipment_Resource, TP_K)
    #equipment_init(FAKE_Console_cfg, Equipment_Resource, TP_K)

    print(Equipment_Resource)
    equipments_open()

    TP_K["power_on"](1)

    cn = TP_K["console_open"](0)
    print(TP_K["console_read"](cn, "90 PS313C3U15000001 login:"))
##    .decode('ascii'), end = '')
    TP_K["console_write"](cn, "admin\n")
    print(TP_K["console_read"](cn, "10 PS313C3U15000001>"))
    TP_K["console_write"](cn, "fap-get-status\n")
    print(TP_K["console_read"](cn, "10 Version: FortiAP-S313C v5.4,build6004,150724 (Interim)"))
    print(TP_K["console_read"](cn, "10 PS313C3U15000001>"))
    TP_K["console_write"](cn, "exit\n")
    print(TP_K["console_read"](cn, "10 PS313C3U15000001 login:"))
    TP_K["console_close"](cn)

    
    TP_K["power_off"](1)

    equipments_close()
if __name__ == "__main__":
    test()

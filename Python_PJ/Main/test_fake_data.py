# -*- coding: utf-8 -*-

FAKE_netBooter_cfg = {
    "name":"netBooter",
    "ports":8,
    "ip":"192.168.1.100",
}

FAKE_Power_cfg = {
    "name":"fake_power",
    "ports":8,
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



power_test_cmds = [
        "telnet_connect 192.168.1.100",
        "telnet_read 10 Synaccess Inc. Telnet Session V6.",
        "telnet_write pset 1 1",
        "sleep 5",
        "telnet_read 10 >",
        "telnet_write pset 1 0",
        "telnet_read 10 >",
        "telnet_close",
        ]

console_test_cmds = [
        "power1_on",
        "console_open",
        "console_read 120 Please press Enter to activate this console.",
        "console_write \n",
        "console_read 20 PS321C3U15000014 #",
        "sleep 5",
        "gui_item_pass",
        "console_write fap-get-status",
        "console_read 30 Version: FortiAP-S321C v5.4,build0101,150423 (Interim)",
        "console_read 10 Release Version Information: Interim",
        "console_read 20 PS321C3U15000014 #",
        "sleep 3",
        "gui_item_pass",
        "sleep 5",
        "console_read 30 wifi fake\n",
        "check_box box confirm message",
        "console_read 20 wifi setup\n",
        "gui_item_pass",
        "console_read 30 factory reset\n",
        "console_read 20 done\n",
        "sleep 5",
        "console_read 20 shutdown\n",
        "console_read 20 shutdown\n",
        "console_read 20 shutdown\n",
        "console_read 20 shutdown\n",
        "console_read 20 shutdown\n",
        "console_read 20 shutdown\n",
        "console_read 20 shutdown\n",
        "console_read 20 shutdown\n",
        "console_read 20 shutdown\n",
        "console_read 20 shutdown\n",
        "console_read 20 shutdown\n",
        "console_read 20 shutdown\n",
        "gui_item_pass",
        "gui_end",
        "console_close",
        "power1_off",
        ]

demo_cmds = [
        "power1_on",
        "console_open",
        "system_write dir",
        "system_read ooo",
        "service FGT-80C register PS313C3U15000001",
        "service FGT-80C remove PS313C3U15000001",
        "console_read 90 PS313C3U15000001 login:",
        "console_write admin\n",
        "console_read 10 PS313C3U15000001>",
        "sleep 5",
        "console_write fap-get-status\n",
        "console_read 10 Version: FortiAP-S313C v5.4,build6004,150724 (Interim)",
        "console_read 10 PS313C3U15000001>",
        "gui_item_pass",
        "sleep 3",
        "power1_off",
        "sleep 3",
        "power1_on",
        "console_read 30 Hit any key to stop autoboot:",
        "sleep 3",
        "console_write g",
        "console_read 30 Enter G,Q,or H:",
        "sleep 3",
        "console_write g",
        "console_read 30 Enter TFTP server address [192.168.1.10]: ",
        "sleep 3",
        "console_write 192.168.1.168\n",
        "console_read 30 Enter local address [192.168.1.1]: ",
        "sleep 3",
        "console_write \n",
        "console_read 30 Enter firmware image file name [image.out]: ",
        "sleep 3",
        "console_write FAP_S313C-v5-build6004-fortinet.out\n",
        "console_read 60 Save as Default firmware[D]?",
        "sleep 3",
        "console_write d",
        "console_read 180 Starting kernel ...",
        "console_read 300 PS313C3U15000001 login:",
        "gui_item_pass",
        "sleep 3",
        "check_box operator check message!!",
        "sleep 3",
        "gui_item_pass",
        "sleep 5",
        "console_write admin\n",
        "console_read 10 PS313C3U15000001>",
        "console_write factoryreset\n",
        "console_read 60 Do you want to continue? (y/n)",
        "console_write y",
        "console_read 300 PS313C3U15000001 login:",
        "gui_item_pass",
        "gui_end",
        "console_close",
        "power1_off",
        ]

fake_test_package ={
    "Device_info":{"SN":"ORZ","HW":"hw0000","SW":"sw0001"},
    "Test_Items":["SN verify", "OS update", "Box check", "Factory reset"],
    "Tp_cmds":demo_cmds,
}
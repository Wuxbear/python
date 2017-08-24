import telnetlib
from time import sleep

netBooter_node = None
netBooter_ip = None

def _setup_ip(ip):
    global netBooter_ip
    netBooter_ip = ip
	
def _open():
        global netBooter_node
        netBooter_node = telnetlib.Telnet(netBooter_ip,23,5)
        netBooter_node.read_until(b'Synaccess Inc. Telnet Session V6.1.')
        cmd = "ps 0\r\n"
        netBooter_node.write(bytes(cmd.encode('ascii')))
        # need time to close all power port
        # sleep(5)
    
def _close():
        netBooter_node.close()
        
def _power_on(port):
        netBooter_node.read_very_eager()
        cmd = "pset %d 1 \r\n" % port
        netBooter_node.write(bytes(cmd.encode('ascii')))

def _power_off(port):
        netBooter_node.read_very_eager()
        cmd = "pset %d 0 \r\n" % port
        netBooter_node.write(bytes(cmd.encode('ascii')))


if __name__ == '__main__':
    _setup_ip("192.168.1.100")
    _open()
    _power_on(1)
    sleep(3)
    _power_off(1)
    _close()

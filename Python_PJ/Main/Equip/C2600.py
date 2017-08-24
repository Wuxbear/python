import telnetlib
from time import sleep

C2600_ip = None
C2600_base_port = 2033

def _setup_ip(ip):
    global C2600_ip
    C2600_ip = ip

def _open(port):
    console_port = C2600_base_port + port - 1
    cn = telnetlib.Telnet(C2600_ip, console_port, 5)
    return cn
	
def _close(cn):
    cn.close()

def _read(cn, x):
    timeout, msg = x.split(' ',1)
    return cn.read_until(msg.encode('ascii'), int(timeout))
##    o = cn.read_until(msg.encode('ascii'), int(timeout))
##    if o == None:
##        raise error
##    else:
##        return o

def _write(cn, x):
    #cn.read_eager()
    cn.write(bytes(x.encode('ascii')))

if __name__ == '__main__':
    _setup_ip("192.168.1.99")
    cn = _open(0)
##    print(_read(cn, "10 FortiAP-S313C"), end = '')
##    print(_read(cn, "30 Serial number: PS313C3U15000001"), end = '')
##    print(_read(cn, "30 Starting kernel ..."), end = '')
    print(_read(cn, "90 PS313C3U15000001 login:"), end = '')    
    _write(cn, "admin\n")
    print(_read(cn, "10 PS313C3U15000001>"), end = '')
    _write(cn, "fap-get-status\n")
    print(_read(cn, "10 Version: FortiAP-S313C v5.4,build6004,150724 (Interim)"), end = '')
    print(_read(cn, "10 PS313C3U15000001>"), end = '')
    _write(cn, "exit\n")
    print(_read(cn, "10 PS313C3U15000001 login:"), end = '')
    _close(cn)

    ## There is issue that get data, start with 0xFC byte, course by C2600 or ?
    ## Need to debug

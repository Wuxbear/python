import socket
import sys

def ReceivePkt(UDP_SERVER_IP,UDP_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_SERVER_IP, UDP_PORT))
    
    count = 0
    while True:
        data, addr = sock.recvfrom(8192) # buffer size is 1024 bytes    
#         strReceiveData = data.decode("utf-8")
        UDP_CLIENT_IP = addr[0]
        rcv_port = addr[1]
        iDataLen = sys.getsizeof(data)
        if rcv_port != UDP_PORT:
            print ("Error port number {0}".format(rcv_port))
            return
        if iDataLen<22:
            print ("Error length ({0})".format(iDataLen))
            return
            
        sock.sendto(bytes(data), (UDP_CLIENT_IP, UDP_PORT))
        count = count+1
		
if __name__ == "__main__":
    argc = len(sys.argv)
    if(argc<3):
	    print ("Please enter Server_IP Port.")
    else:
        strServerIP = sys.argv[1]
        iPort = int(sys.argv[2])
        ReceivePkt(strServerIP,iPort)
	


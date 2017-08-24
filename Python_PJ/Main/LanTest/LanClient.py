import socket
import sys
import time
import LanTestData


def TransPkt(UDP_SERVER_IP, UDP_PORT, iIndex, iDataLen, UDP_CLIENT_IP):	
  print ("UDP server IP:", UDP_SERVER_IP)
  print ("UDP target port:", UDP_PORT)
  print ("client IP:", UDP_CLIENT_IP) 
  
  if iDataLen<64:
    print("Error Length!")
    return

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
  sock.bind((UDP_CLIENT_IP, UDP_PORT))

  count = 0

  t_start = time.time()

  for x in range(iIndex):  
      MESSAGE = LanTestData.Create_Data(str(x),iDataLen)
      sock.sendto(bytes(MESSAGE,encoding = "utf8"), (UDP_SERVER_IP, UDP_PORT))
#      print ("send message:", MESSAGE)
  
      data,addr = sock.recvfrom(8192)
      strReceiveData = data.decode("utf-8")
#      print (strReceiveData," count=",count)
      bRet = check_receive_from_server(MESSAGE,strReceiveData,iIndex,count, t_start)
      if not bRet:
        break
      count=count+1
      

def check_receive_from_server(OrgData, RcvData, iIndex, count, t_start):
  if OrgData != RcvData:
      print("Data Fail! count=",count)
      return False
        
  iReceive = LanTestData.find_index(RcvData)
  if iReceive!= count:
      print ("Fail count=",count)
      return False
  elif iReceive == iIndex-1:
      t_end=time.time()
      print ("\n| Packets length | Send pkt check | Receive Pkt check | Drop/Error/crc")
      print ("      {0}              {1}                {2}             0".format(64,iIndex,iReceive+1))
      print("\nLan Test takes {0} seconds".format(round(t_end-t_start,3)))
      print("WinLanTest Result: Pass\n")
  elif (iReceive%50) == 0:  
      print(".", end="") 
  return True


  
if __name__ == "__main__":

  argc = len(sys.argv)
  if(argc<4):
    print ("Please enter server_ip port client_ip")
  else:
    strServerIP = sys.argv[1]
    iPort = int(sys.argv[2])
    iDataNum = int(sys.argv[3])
    iDataLen = int(sys.argv[4])
    strClientIP = sys.argv[5]

    TransPkt(strServerIP, iPort, iDataNum, iDataLen, strClientIP)  
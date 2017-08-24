####### connect to console port ###########
#
# Can read message from com port and send command to com port.
# Example:	connect_COM_port.py /dev/ttyS0 w 9600 "admin"
#			connect_COM_port.py /dev/ttyS0 r 9600
#
#
# Please install the following tool first: 
#	sudo apt-get install python3-pip
#	sudo pip3 install pyserial
#
###################################

import serial
import sys
import time

def write_port(fd, strWcmd):
  fd.write(strWcmd.encode())

def read_port_and_search_string(fd,strSearch,iTimeout):
  Ret = False
  tStart_t=time.time()
  while Ret==False:
   strRead = read_port(fd)
   Ret = search_string(strSearch,strRead)
   if (time.time()-tStart_t)>iTimeout:
#    print ("timeout~~~~")
    break
  return Ret

def read_port(fd):
  strRead = ""
  iReady2ReadNum = fd.inWaiting()
  if iReady2ReadNum:
    strRead = fd.read(iReady2ReadNum)
    strRead = strRead.decode()    
    print (strRead)
  return strRead

def search_string(strSearch,strRead):
  iFindPos = strRead.find(strSearch,0,len(strRead))
  if iFindPos>-1 and strSearch != "":
#   print ("#@![",strSearch,"]"," Get")
   return True
  return False


def open_port(strDev, iBoundRate):	
  fd= serial.Serial(strDev,iBoundRate,timeout = 0.5)
  return fd  
  
if __name__ == "__main__":

  strDev = sys.argv[1]
  strRW = sys.argv[2]
  iBoundRate = int(sys.argv[3])
  
  fd = open_port(strDev,iBoundRate)

  if strRW == "w":
   strWcmd = sys.argv[4] + "\n"
   write_port(fd,strWcmd)
  else:
   read_port(fd)  fd.close()
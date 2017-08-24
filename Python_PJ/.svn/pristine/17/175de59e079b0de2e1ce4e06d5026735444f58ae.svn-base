##### create data ####
import sys

def Create_Data(sIndex,iExpectDataLen):
    iRemaindNum = 0
    iCreateDataLen = 0
    strCreateData = "1"
    
    iIndexLen = sys.getsizeof(sIndex)
#    print ("iIndexLen:",iIndexLen)
    for x in range(100):
        iIndexLen = sys.getsizeof(sIndex)
        if(iIndexLen < 56):
            sIndex += "@"
        else:    
            break
            
#    print (sIndex," ",iIndexLen)
    strCreateData = sIndex    
    for x in range(99999): 
        iCreateDataLen = sys.getsizeof(strCreateData)
        if(iCreateDataLen < iExpectDataLen):
            strCreateData += "{0}".format(x)
        else:
            iRemain = iCreateDataLen - iExpectDataLen
            break;

    iCreateDataLen = len(strCreateData)
    strTransData = strCreateData[:iCreateDataLen-iRemain]		
    #print (strTransData, sys.getsizeof(strTransData))
    return strTransData

def find_index(strData):
    iLen = len(strData)
    strIndex = ""
    for i in range(iLen):
        if strData[i] =="@":
            break		
        strIndex += strData[i]
#        print (strData[i])
    return (int(strIndex))	
	
if __name__ == "__main__":    
    sIndex = sys.argv[1]
    iLen = int(sys.argv[2])
    strData = Create_Data(sIndex, iLen)
    print (strData)
#    print(find_index(strData))

#    haha = bytes("111",encoding="utf-8")
#    haha2 = str(haha.decode())
#    print (haha2)    
'''
Created on 24.11.2014

@author: Josef Kohnle
'''


class Packet(object):
    '''
    classdocs
    '''
    
    def __init__(self, ComC0=b"\x00", comC1=b"\x00", deviceId=b"\x00\x00"):
        if comC1!=None:
            self.__commandCode0 = ComC0
            self.__commandCode1 = comC1
            self.__deviceId = deviceId

    def getCommandCode0(self):
        return self.__commandCode0
    
    def getCommandCode1(self):
        return self.__commandCode1
    
    def getDeviceId(self):
        return self.__deviceId
    
    def getCheckSum(self, byteCode):
        bArray=bytearray(byteCode)
        length = len(bArray)
        i = 0
        cSum = 0
        for i in range(0,length):
            cSum += bArray[i]
            i += 1

        b1 = cSum & 255
        b0 = (cSum & 65280)>>8
     
        erg = bytearray()
        erg.append(b1)
        erg.append(b0)
        #print ("erg:",bytes(erg))
        
        return bytes(erg)
    
    def getByteCode(self):
        bArray = self.__commandCode0
        bArray += self.__commandCode1
        bArray += self.__deviceId
        bArray += Packet.getCheckSum(bArray)
        return bArray


'''
Created on 22.10.2014

@author: Josef Kohnle
'''

from Packet import Packet
from SensorException import SensorException
from Define import *


class DataPacket(Packet):
    '''
    classdocs
    '''


    def __init__(self, byteCodeId=None, data=None):
        if data != None:
            Packet.__init__(self, b"\x5A", b"\xA5", byteCodeId)
            self.__data = data
        else:
            length = len(byteCodeId)
            if length >= 8:
                if byteCodeId[0]== b"\x5A" and byteCodeId[1]== b"\xA5":
                    Packet.__init__(self, byteCodeId[0], byteCodeId[1], byteCodeId[2:4])
                    self.__data = byteCodeId[4:length-2]
                
                    #print("com1:", self.__commandCode0)
                    #print("com2:", self.__commandCode1)
                    #print("Id:", self.__deviceId)
                    #print("rawData:", self.__data)
                    
                    #checkRec = bytearray(byteCode)[length-2] + bytearray(byteCode)[length-1]
                    #print("checkRec:", checkRec)
                    #print("checkRec:", receivedByteArray[length-2:length])
                    
                    #checkCalc = bytearray(super.getCheckSum())[0]+ bytearray(super.getCheckSum())[1]
                    #print("checkCalc:", checkCalc)
                    #print("checkCalc:", self.getCheckSum())
                    
                    #if self.getCheckSum() != receivedByteArray[length-1:length]:
                    #if checkRec != checkCalc:
                    if self.getCheckSum(byteCodeId[0:length-2]) != byteCodeId[length-2:length]:
                        raise SensorException(CHECKSUM_ERROR, DATA_PACK_ERROR)
                else:
                    raise SensorException(PACKET_HEADER_ERROR,DATA_PACK_ERROR)
            else:
                raise SensorException(LENGTH_ERROR, DATA_PACK_ERROR)
    
    def getData(self):
        return self.__data
    
    def getByteCode(self):
        bArray = self.getCommandCode0()
        bArray += self.getCommandCode1()
        bArray += self.getDeviceId()
        bArray += self.__data
        bArray += self.getCheckSum(bArray)
        return bArray
    
'''
Created on 22.10.2014

@author: Josef Kohnle
'''

from Packet import Packet
from SensorException import SensorException
from Define import COMMAND_PACK_ERROR,CHECKSUM_ERROR,LENGTH_ERROR,PACKET_HEADER_ERROR


class CommandPacket(Packet):
    '''
    classdocs
    '''


    def __init__(self, byteCodeId=None, comResp=None, parameter=None):
        
        if comResp != None:
            #super().__init__(b"\x55", b"\xAA", byteCodeId)
            Packet.__init__(self, b"\x55", b"\xAA", byteCodeId)
            self.__parameter = parameter
            self.__comResp = comResp
        else:

            length = len(byteCodeId)
            if length == 12:
                if byteCodeId[0]== b"\x55" and byteCodeId[1]== b"\xAA":
                    Packet.__init__(self, byteCodeId[0], byteCodeId[1], byteCodeId[2:4])
                    self.__parameter = byteCodeId[4:8]
                    self.__comResp = byteCodeId[8:10]
                    
                    #print("com1:", self.__commandCode0)
                    #print("com2:", self.__commandCode1)
                    #print("deviceId:", self.__deviceId)
                    #print("parameter:", self.__parameter)
                    #print("comResp:", self.__comResp)
                    #print("check:", receivedByteArray[10:12])
                    #print("checkCalc:",self.getCheckSum())

                    if self.getCheckSum(byteCodeId[0:length-2]) != byteCodeId[length-2:length]:
                        raise SensorException(CHECKSUM_ERROR, COMMAND_PACK_ERROR)
                else:
                    raise SensorException(PACKET_HEADER_ERROR, COMMAND_PACK_ERROR)
            else:
                raise SensorException(LENGTH_ERROR, COMMAND_PACK_ERROR) 
    
    def getParameter(self):
        return self.__parameter
    
    def getComResp(self):
        return self.__comResp  
    
    def getByteCode(self):
        bArray = self.getCommandCode0()
        bArray += self.getCommandCode1()
        bArray += self.getDeviceId()
        bArray += self.__parameter
        bArray += self.__comResp
        bArray += self.getCheckSum(bArray)
        return bArray
 
        
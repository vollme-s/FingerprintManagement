'''
Created on 24.11.2014

@author: jk
'''

import serial
from CommandPacket import CommandPacket
from DataPacket import DataPacket
from SensorException import SensorException
from Define import *


class SensorCom(object):
    '''
    classdocs
    '''


    def __init__(self, serialPort, baud, idNr=b"\x01\x00"):
        self.__portName = serialPort
        self.__baudrate = baud
        self.__port = serial.Serial()
        self.__openPort()
        self.__deviceId = idNr
        
            
        
    def __openPort(self):
        if self.__port.isOpen():
            self.__port.close()
        self.__port.port = self.__portName
        self.__port.baudrate = self.__baudrate
        self.__port.timeout = 3.0
        self.__port.open()
        
    def open(self, info):
        if info == True: 
            self.__sendCommand(b"\x01\x00", b"\x01\x00\x00\x00")
            self.__receiveCommandPack()
            received = self.__receiveDataPack(24+6)
        else:
            self.__sendCommand(b"\x01\x00", b"\x00\x00\x00\x00")
            received = self.__receiveCommandPack()
        return received
        
    def close(self):
        self.__sendCommand(b"\x02\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def usbInternalCheck(self):
        self.__sendCommand(b"\x03\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def changeBaudrate(self,baud):
        param = self.__intToParamArray(baud)
        self.__sendCommand(b"\x04\x00", param)
        received = self.__receiveCommandPack()
        return received
        
    def setApiMode(self):
        self.__sendCommand(b"\x40\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def cmosLed(self, state):
        if state ==  True:
            self.__sendCommand(b"\x12\x00", b"\x01\x00\x00\x00")
        else:
            self.__sendCommand(b"\x12\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def getEnrollCount(self):
        self.__sendCommand(b"\x20\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def checkEnroll(self, idNr):
        retval = True
        param = self.__intToParamArray(idNr)
        try:
            self.__sendCommand(b"\x21\x00", param)
            self.__receiveCommandPack()
        except SensorException as e:
            if e.getParam() == NACK_IS_NOT_USED:
                retval = False
            else:
                raise e
        return retval
    
    def __intToParamArray(self, integer):
        param = bytearray(4)
        param[0] = integer & 255
        param[1] = (integer >> 8) & 255
        param[2] = (integer >> 16) & 255
        param[3] = (integer >> 24) & 255
        return param
        
    def enrollStart(self, idNr):
        param = self.__intToParamArray(idNr)
        #print("idNr:", param)
        self.__sendCommand(b"\x22\x00", param)
        received = self.__receiveCommandPack()
        return received
        
    def enroll0(self):
        self.__sendCommand(b"\x23\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def enroll1(self):
        self.__sendCommand(b"\x24\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def enroll2(self, idNr):
        self.__sendCommand(b"\x25\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        if idNr==-1:
            received = self.__receiveDataPack(498+6)
        return received
    
    def isPressFinger(self):
        retval = True
        try:
            self.__sendCommand(b"\x26\x00", b"\x00\x00\x00\x00")
            self.__receiveCommandPack()
        except SensorException as e:
            if e.getParam()==NACK_FINGER_IS_NOT_PRESSED:
                retval = False
            else:
                raise e
        return retval
        
    def deleteId(self, idNr):
        param = self.__intToParamArray(idNr)
        self.__sendCommand(b"\x40\x00", param)
        received = self.__receiveCommandPack()
        return received
        
    def deleteAll(self):
        self.__sendCommand(b"\x41\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def verify(self,idNr):
        param = self.__intToParamArray(idNr)
        self.__sendCommand(b"\x50\x00", param)
        received = self.__receiveCommandPack()
        return received
        
    def identify(self):
        self.__sendCommand(b"\x51\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()   
        return received
        
    def verifyTemplate(self, idNr, data):
        param = self.__intToParamArray(idNr)
        self.__sendCommand(b"\x52\x00", param)
        self.__receiveCommandPack()
        self.__sendData(data)
        received = self.__receiveCommandPack()
        return received
        
    def identifyTemplate(self, data):
        self.__sendCommand(b"\x53\x00", b"\x00\x00\x00\x00")
        self.__receiveCommandPack()
        self.__sendData(data)
        received = self.__receiveCommandPack()
        return received
        
    def captureFinger(self, mode):
        if mode == True:
            self.__sendCommand(b"\x60\x00", b"\x01\x00\x00\x00")
        else:
            self.__sendCommand(b"\x60\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def makeTemplate(self):
        self.__sendCommand(b"\x61\x00", b"\x00\x00\x00\x00")
        self.__receiveCommandPack()
        received = self.__receiveDataPack(TEMPLATE+HEADER)
        return received
        
    def getImage(self):
        self.__sendCommand(b"\x62\x00", b"\x00\x00\x00\x00")
        self.__receiveCommandPack()
        received = self.__receiveDataPack(IMAGE+HEADER)
        return received 
           
    def getRawImage(self):
        self.__sendCommand(b"\x63\x00", b"\x00\x00\x00\x00")
        self.__receiveCommandPack()
        received = self.__receiveDataPack(QVGA_IMAGE+HEADER)
        return received
        
    def getTemplate(self, idNr):
        param = self.__intToParamArray(idNr)
        self.__sendCommand(b"\x70\x00", param)
        self.__receiveCommandPack()
        received = self.__receiveDataPack(TEMPLATE+HEADER)
        return received
        
    def setTemplate(self, idNr, data):
        param = self.__intToParamArray(idNr)
        self.__sendCommand(b"\x71\x00", param)
        self.__receiveCommandPack()
        self.__sendData(data)
        received = self.__receiveCommandPack()
        return received
        
    def getDatabaseStart(self):
        self.__sendCommand(b"\x72\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def getDatabaseEnd(self):
        self.__sendCommand(b"\x73\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def upgradeFirmware(self):
        self.__sendCommand(b"\x80\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def upgradeIsocdImage(self):
        self.__sendCommand(b"\x81\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def ack(self):
        self.__sendCommand(b"\x30\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def nack(self):
        self.__sendCommand(b"\x31\x00", b"\x00\x00\x00\x00")
        received = self.__receiveCommandPack()
        return received
        
    def __sendCommand(self, command, parameter):
        retval = 0
        packet = CommandPacket(self.__deviceId, command, parameter)
        if self.__port.isOpen():
            retval = self.__port.write(packet.getByteCode())
            #print("send:", packet.getByteCode())
        else:
            raise SensorException(SERIAL_PORT_ERROR,0)
        return retval
    
    def __sendData(self, data):
        retval = 0
        packet = DataPacket(self.__deviceId, data)
        if self.__port.isOpen():
            retval = self.__port.write(packet.getByteCode())
            #print("sendData:", packet.getByteCode())
        else:
            raise SensorException(SERIAL_PORT_ERROR,0)
        return retval
    
    def receive(self, length):
        if self.__port.isOpen():    
            received = self.__port.read(length)
            if len(received) == 0:
                raise SensorException(SERIAL_PORT_TIMEOUT,0)
        else:
            raise SensorException(SERIAL_PORT_ERROR,0)
        
        return received
     
    def __receiveCommandPack(self):
        if self.__port.isOpen():    
            received = self.__port.read(12)
            #received = b"\x55\xaa\x00\x01\x00\x00\x00\x00\x00\x30\x01\x30"
            #print("received:",received)
            if len(received) == 0:
                raise SensorException(SERIAL_PORT_TIMEOUT,COMMAND_PACK_ERROR)
            resPack = CommandPacket(received)
            if resPack.getDeviceId() != self.__deviceId:
                raise SensorException(ID_ERROR,COMMAND_PACK_ERROR)
            if self.paramCodeToInt(resPack.getParameter()) < 0:
                raise SensorException(self.commandCodeToInt(resPack.getComResp()), self.paramCodeToInt(resPack.getParameter()))
            if resPack.getComResp() == b"\x31\x00" and self.paramCodeToInt(resPack.getParameter()) >= 0:
                raise SensorException(DUPLICATED_ID_ERROR, self.paramCodeToInt(resPack.getParameter()))
        else:
            raise SensorException(SERIAL_PORT_ERROR,0)
            
        return self.paramCodeToInt(resPack.getParameter())
   
    def __receiveDataPack(self, length):
        if self.__port.isOpen():
            received = self.__port.read(length)
            #print("dataRec:", received)
            if len(received) == 0:
                raise SensorException(SERIAL_PORT_TIMEOUT,DATA_PACK_ERROR)
            if length == len(received):
                dataPack = DataPacket(received)
                if dataPack.getDeviceId() != self.__deviceId:
                    raise SensorException(ID_ERROR,DATA_PACK_ERROR)   
            else:
                raise SensorException(LENGTH_ERROR,DATA_PACK_ERROR)
        else:
            raise SensorException(SERIAL_PORT_ERROR,0)       
                
        return dataPack.getData()

    def commandCodeToInt(self,code):
        if code == b"\x30\x00":
            retval = ACK
            #print("ACK")
        elif code == b"\x31\x00":
            retval = NACK
            #print("NACK")
        else:
            retval = bytearray(code)[0] + bytearray(code)[1]*16**2;
        
        return retval
    
    def commandCodeToStr(self, error):
        retval = 0
        if error == ACK:
            retval = "ACK"
        elif error == NACK:
            retval = "NACK"
        elif error == ID_ERROR:
            retval = "ID_ERROR"
        elif error == LENGTH_ERROR:
            retval = "LENGTH_ERROR"
        elif error == PACKET_HEADER_ERROR:
            retval = "PACKET_HEADER_ERROR"
        elif error == CHECKSUM_ERROR:
            retval = "CHECKSUM_ERROR"
        elif error == SERIAL_PORT_ERROR:
            retval = "SERIAL_PORT_ERROR"
        elif error == DUPLICATED_ID_ERROR:
            retval = "DUPLICATED_ID_ERROR"
        elif error == SERIAL_PORT_TIMEOUT:
            retval = "SERIAL_PORT_TIMEOUT"
        else:
            retval = str(error)         
        
        return retval

    def paramCodeToInt(self,code):
        error = code[0:2]
        #print("code:",code)
        retval = 0
        if error[1] == b"\x10":
            if error == b"\x01\x10":
                retval = NACK_TIMEOUT
                #print("NACK_TIMEOUT")
            elif error == b"\x02\x10":
                retval = NACK_INVALID_BAUDRATE
                #print("NACK_INVALID_BAUDRATE")
            elif error == b"\x03\x10":
                retval = NACK_INVALIDE_POS
                #print("NACK_INVALIDE_POS")
            elif error == b"\x04\x10":
                retval = NACK_IS_NOT_USED
                #print("NACK_IS_NOT_USED")
            elif error == b"\x05\x10":
                retval = NACK_IS_ALREDY_USED
                #print("NACK_IS_ALREDY_USED")
            elif error == b"\x06\d10":
                retval = NACK_COMM_ERR
                #print("NACK_COMM_ERR")
            elif error == b"\x07\x10":
                retval = NACK_VERIVY_FAILED
                #print("NACK_VERIVY_FAILED")
            elif error == b"\x08\x10":
                retval = NACK_IDENTIFY_FAILD
                #print("NACK_IDENTIFY_FAILD")
            elif error == b"\x09\x10":
                retval = NACK_DB_IS_FULL
                #print("NACK_DB_IS_FULL")
            elif error == b"\x0A\x10":
                retval = NACK_DB_IS_EMPTY
                #print("NACK_DB_IS_EMPTY")
            elif error == b"\x0B\x10":
                retval = NACK_TURN_ERR
                #print("NACK_TURN_ERR")
            elif error == b"\x0C\x10":
                retval = NACK_BAD_FINGER
                #print("NACK_BAD_FINGER")
            elif error == b"\x0D\x10":
                retval = NACK_ENROLL_FAILED
                #print("NACK_ENROLL_FAILED")
            elif error == b"\x0E\x10":
                retval = NACK_IS_NOT_SUPPORTED
                #print("NACK_IS_NOT_SUPPORTED")
            elif error == b"\x0F\x10":
                retval = NACK_DEV_ERR
                #print("NACK_DEV_ERR")
            elif error == b"\x10\x10":
                retval = NACK_CAPTURE_CANCELED
                #print("NACK_CAPTURE_CANCELED")
            elif error == b"\x11\x10":
                retval = -NACK_INVALID_PARAM 
                #print("NACK_INVALID_PARAM")
            elif error == b"\x12\x10":
                retval = NACK_FINGER_IS_NOT_PRESSED
                #print("NACK_FINGER_IS_NOT_PRESSED")
        else:
            retval = bytearray(error)[0] + bytearray(error)[1]*16**2;
        
        return retval
    
    
    def paramIntToStr(self,error):
        retval = 0
        if error == NACK_TIMEOUT:
            retval = "NACK_TIMEOUT"
        elif error == NACK_INVALID_BAUDRATE:
            retval = "NACK_INVALID_BAUDRATE"
        elif error == NACK_INVALIDE_POS:
            retval = "NACK_INVALIDE_POS"
        elif error == NACK_IS_NOT_USED:
            retval = "NACK_IS_NOT_USED"
        elif error == NACK_IS_ALREDY_USED:
            retval = "NACK_IS_ALREDY_USED"
        elif error == NACK_COMM_ERR:
            retval = "NACK_COMM_ERR"
        elif error == NACK_VERIVY_FAILED:
            retval = "NACK_VERIVY_FAILED"
        elif error == NACK_IDENTIFY_FAILD:
            retval = "NACK_IDENTIFY_FAILD"
        elif error == NACK_DB_IS_FULL:
            retval = "NACK_DB_IS_FULL"
        elif error == NACK_DB_IS_EMPTY:
            retval = "NACK_DB_IS_EMPTY"
        elif error == NACK_TURN_ERR:
            retval = "NACK_TURN_ERR"
        elif error == NACK_BAD_FINGER:
            retval = "NACK_BAD_FINGER"
        elif error == NACK_ENROLL_FAILED:
            retval = "NACK_ENROLL_FAILED"
        elif error == NACK_IS_NOT_SUPPORTED:
            retval = "NACK_IS_NOT_SUPPORTED"
        elif error == NACK_DEV_ERR:
            retval = "NACK_DEV_ERR"
        elif error == NACK_CAPTURE_CANCELED:
            retval = "NACK_CAPTURE_CANCELED"
        elif error == NACK_INVALID_PARAM:
            retval = "NACK_INVALID_PARAM"
        elif error == NACK_FINGER_IS_NOT_PRESSED:
            retval = "NACK_FINGER_IS_NOT_PRESSED"
        elif error == COMMAND_PACK_ERROR:
            retval = "COMMAND_PACK_ERROR"
        elif error == DATA_PACK_ERROR:
            retval = "DATA_PACK_ERROR"
        else:
            retval = str(error)
        
        return retval
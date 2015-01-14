'''
Created on 24.11.2014

@author: jk
'''


class SensorException(Exception):
    
    def __init__(self, ack, param):
        self.__ack = ack
        self.__param = param
    
    def getMessage(self):
        return "SensorException: ("+str(self.__ack)+","+str(self.__param)+")"
    
    def getAck(self):
        return self.__ack
    
    def getParam(self):
        return self.__param

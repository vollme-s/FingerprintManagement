'''
Created on 15.01.2015

@author: Stefan
'''

from django.apps import AppConfig
from sensor.HardwareMain import initHardware
 
 
class MyAppConfig(AppConfig):
 
    name = 'fingerprint'
    verbose_name = 'fingerprint scanner'
 
    def ready(self):
       initHardware()
        
        
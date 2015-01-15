'''
Created on 29.11.2014

@author: jk
'''

from SensorException import SensorException
from time import sleep
from SensorCom import SensorCom
from Define import *
from DisplayMessages import *
import RPIO
import display

sensor = None

def gpioCapSensor_callback(gpio_id, val):
    print("\n>interrupt_start")
    idNr = identification()
    print(idNr)
    if idNr != False:
        activateRelay()
    print(">interrupt_end")
    

#input: template
#output: idNr/false
def setTemplate(template):
    RPIO.stop_waiting_for_interrupts()
    retval = True
    usedId = True
    idNr = 0
    try:
        #finde freie idNr
        while idNr < ID_MAX and usedId == True:
            idNr = idNr+1   #checkEnroll beginnt bei Index 1; enroll und setTemplate bei 0
            usedId = sensor.checkEnroll(idNr)
        if usedId == False:
            retval = idNr - 1
        else:
            retval = False
        sensor.setTemplate(idNr, template)
    except SensorException as e:
        print(sensor.commandCodeToStr(e.getAck())+" : "+sensor.paramIntToStr(e.getParam()))
        retval = False
        
    RPIO.wait_for_interrupts(threaded = True)
    return retval

#input: idNr
#output: template/false
def getTemplate(idNr):
    RPIO.stop_waiting_for_interrupts()
    try:
        retval = sensor.getTemplate(idNr+1)
    except SensorException as e:
        print(sensor.commandCodeToStr(e.getAck())+" : "+sensor.paramIntToStr(e.getParam()))
        retval = False
    
    RPIO.wait_for_interrupts(threaded = True)
    return retval

#input: template
#output: idNr/false
def identifyTemplate(template):
    RPIO.stop_waiting_for_interrupts()
    retval = True
    try:
        retval = sensor.identifyTemplate(template)-1
    except SensorException as e:
        print(sensor.commandCodeToStr(e.getAck())+" : "+sensor.paramIntToStr(e.getParam()))
        retval = False
        
    RPIO.wait_for_interrupts(threaded = True)
    return retval
    
    
#input:
#output: true/false    
def deleteAll():
    RPIO.stop_waiting_for_interrupts()
    retval = True
    try:
        sensor.deleteAll()
    except SensorException as e:
        print(sensor.commandCodeToStr(e.getAck())+" : "+sensor.paramIntToStr(e.getParam()))
        retval = False
    
    RPIO.wait_for_interrupts(threaded = True)
    return retval
 
#input: idNr
#output: true/false    
def deleteId(idNr):
    RPIO.stop_waiting_for_interrupts()
    retval = True
    try:
        sensor.deleteId(idNr+1)
    except SensorException as e:
        print(sensor.commandCodeToStr(e.getAck())+" : "+sensor.paramIntToStr(e.getParam()))
        retval = False
    
    RPIO.wait_for_interrupts(threaded = True)
    return retval

#input: template
#output: idNr/false
def deleteTemplate(template):
    RPIO.stop_waiting_for_interrupts()
    retval = True
    try:
        idNr = sensor.identifyTemplate(template)
        sensor.deleteId(idNr)
        retval = idNr-1
    except SensorException as e:
        print(sensor.commandCodeToStr(e.getAck())+" : "+sensor.paramIntToStr(e.getParam()))
        retval = False
        
    RPIO.wait_for_interrupts(threaded = True)
    return retval
    
def activateRelay():
    RPIO.stop_waiting_for_interrupts()
    # set gpio to high
    RPIO.output(23, True)
    sleep(DOOR_OPEN_TIME)
    RPIO.output(23, False)
    RPIO.wait_for_interrupts(threaded = True)

#input: idNr
#output: true/false
def verification(idNr):
    RPIO.stop_waiting_for_interrupts()
    state = "LED_ON"
    timeout = WAIT_FOR_USER_INTERACTION
    retval = True
    try:
        while state != "EXIT":
            if state == "LED_ON":
                print("LED_ON")
                sensor.cmosLed(True)
                state = "WAIT_FOR_FINGER"
            if state == "WAIT_FOR_FINGER":
                print("WAIT_FOR_FINGER")
                if waitForFinger(timeout)==True:
                    state = "VERIFY"
                else:
                    sensor.cmosLed(False)
                    print("WAIT_FOR_FINGER : TIMEOUT")
                    retval = False
                    state = "EXIT"
            if state == "VERIFY":
                print("VERIFY")
                sensor.verify(idNr)
                state = "LED_OFF"
            if state == "LED_OFF":
                print("LED_OFF")
                sensor.cmosLed(False)
                state = "EXIT"
    except SensorException as e:
        if e.getParam() == NACK_VERIVY_FAILED or e.getParam() == NACK_IS_NOT_USED or e.getParam() == NACK_INVALIDE_POS:
            sensor.cmosLed(False)
        print(sensor.commandCodeToStr(e.getAck())+" : "+sensor.paramIntToStr(e.getParam()))
        retval = False
        
    RPIO.wait_for_interrupts(threaded = True)
    return retval

#input:
#output: idNr/false    
def identification():
    RPIO.stop_waiting_for_interrupts()
    state = "LED_ON"
    timeout = WAIT_FOR_USER_INTERACTION
    retval = True
    try:
        while state != "EXIT":
            if state == "LED_ON":
                print("LED_ON")
                sensor.cmosLed(True)
                state = "WAIT_FOR_FINGER"
            if state == "WAIT_FOR_FINGER":
                print("WAIT_FOR_FINGER")
                display.printscan(WAIT_FOR_FINGER)
                if waitForFinger(timeout)==True:
                    state = "IDENTIFY"
                else:
                    sensor.cmosLed(False)
                    print("WAIT_FOR_FINGER : TIMEOUT")
                    display.printclock(WAIT_FOR_FINGER_TIMEOUT)
                    sleep(1)
                    retval = False
                    state = "EXIT"
            if state == "IDENTIFY":
                print("IDENTIFY")
                display.printscan(IDENTIFY)
                sensor.captureFinger(False)
                retval = sensor.identify()-1
                state = "LED_OFF"
            if state == "LED_OFF":
                print("LED_OFF")
                sensor.cmosLed(False)
                state = "EXIT"
    except SensorException as e:
        if e.getParam() == NACK_IDENTIFY_FAILD or e.getParam() == NACK_DB_IS_EMPTY:
            sensor.cmosLed(False) 
        print(sensor.commandCodeToStr(e.getAck())+" : "+sensor.paramIntToStr(e.getParam()))
        retval = False
        
    if retval != False:    
        display.printok(IDENTIFICATION_OK)
    else:
        display.printunaut(IDENTIFICATION_FAILED)
    sleep(2)
    display.printok(READY_FOR_ACTION)
           
    RPIO.wait_for_interrupts(threaded = True)
    return retval

#input: idNr
#output: false/template
def enrollment():
    idNr = -1
    RPIO.stop_waiting_for_interrupts()
    state = "ENROLL_START"
    enrollCount = 0
    timeout = WAIT_FOR_USER_INTERACTION
    retval = True
    try:
        while state != "EXIT":
            if state == "ENROLL_START":
                print("ENROLL_START")
                sensor.enrollStart(idNr)
                state = "LED_ON"
            if state == "LED_ON":
                print("LED_ON")
                sensor.cmosLed(True)
                state = "WAIT_FOR_FINGER"
            if state == "WAIT_FOR_FINGER":
                print("WAIT_FOR_FINGER")
                display.printscan(WAIT_FOR_FINGER)
                if waitForFinger(timeout)==True:
                    state = "CAPTURE_FINGER"
                else:
                    sensor.cmosLed(False)
                    print("WAIT_FOR_FINGER : TIMEOUT")
                    display.printclock(WAIT_FOR_FINGER_TIMEOUT)
                    sleep(1)
                    retval = False
                    state = "EXIT"
            if state == "CAPTURE_FINGER":
                print("CAPTURE_FINGER")
                display.printscan(ENROLL)
                sensor.captureFinger(True)
                state = "ENROLL"
            if state == "ENROLL":
                print("ENROLL")
                if enrollCount == 0:
                    sensor.enroll0()
                elif enrollCount == 1:
                    sensor.enroll1()
                elif enrollCount == 2:
                    if idNr == -1:
                        retval = sensor.enroll2(idNr)
                    else:
                        sensor.enroll2(idNr)
                enrollCount += 1
                state = "LED_OFF"
            if state == "LED_OFF":
                print("LED_OFF")
                sensor.cmosLed(False)
                if enrollCount <= 2:
                    state = "WAIT_FOR_NO_FINGER"
                else:
                    state = "EXIT"
            if state == "WAIT_FOR_NO_FINGER":
                print("WAIT_FOR_NO_FINGER")
                display.printscan(WAIT_FOR_NO_FINGER)
                if waitForNoFinger(timeout)==True:
                    state = "LED_ON"
                else:
                    print("WAIT_FOR_NO_FINGER : TIMEOUT")
                    display.printclock(WAIT_FOR_NO_FINGER_TIMEOUT)
                    sleep(1)
                    retval = False
                    state = "EXIT"
                
    except SensorException as e:
        print(sensor.commandCodeToStr(e.getAck())+" : "+sensor.paramIntToStr(e.getParam()))
        retval = False
        
    if retval != False:
        display.printok(ENROLL_OK)
    else:
        display.printerr(ENROLL_FAILED)
    sleep(2)
    display.printok(READY_FOR_ACTION)
        
    RPIO.wait_for_interrupts(threaded = True)            
    return retval


def waitForNoFinger(timeout):
    time = 0
    ans = True
    while ans == True and time < timeout:
        ans = sensor.isPressFinger()
        time+=1
        sleep(1)
    return not ans  
    
def waitForFinger(timeout):
    time = 0
    ans = False
    while ans == False and time < timeout:
        ans = sensor.isPressFinger()
        time+=1
        sleep(1)
    return ans
 
def initHardware():
    global sensor
    sensor = SensorCom("/dev/ttyAMA0", 9600)
    display.init_tft()
    display.printok(READY_FOR_ACTION)
    
    # set up GPIO output channel
    RPIO.setup(23, RPIO.OUT, initial=RPIO.LOW)
    
    RPIO.add_interrupt_callback(24, gpioCapSensor_callback, edge='falling', debounce_timeout_ms=200)
    RPIO.wait_for_interrupts(threaded = True)
     
    
def freeResources():
    RPIO.cleanup()
    display.close_tft() 
    

def testMain(testTemplate):
    ans = 0
    try:
        initHardware()
    
        print("Start")
        mode=raw_input("->")
        while mode!="q":
            if mode == "enrollment":
                print("enrollment")
                param = int(raw_input("->>"))
                ans = enrollment()
                if param != -1 and ans != False:
                    ans = setTemplate(ans)
            elif mode == "identification":
                print("identification")
                ans = identification()
            elif mode == "verification":
                print("verification")
                param = int(raw_input("->>"))
                ans = verification(param)
            elif mode == "deleteTemplate":
                print("deleteTemplate")
                ans = deleteTemplate(testTemplate)
            elif mode == "deleteId":
                print("deleteId")
                param = int(raw_input("->>"))
                ans = deleteId(param)
            elif mode == "deleteAll":
                print("deleteAll")
                ans = deleteAll()
            elif mode == "identifyTemplate":
                print("identifyTemplate")
                ans = identifyTemplate(testTemplate)
            elif mode == "getTemplate":
                print("getTemplate")
                param = int(raw_input("->>"))
                ans = getTemplate(param)
            elif mode == "setTemplate":
                print("setTemplate")
                ans = setTemplate(testTemplate)
            elif mode == "activateRelay":
                print("activateRelay")
                ans = activateRelay()
            elif mode == "tftScan":
                print("tftScan")
                ans = display.printscan("Test-Scan")
            elif mode == "tftOK":
                print("tftOK")
                ans = display.printok("Test-OK")
            elif mode == "tftNOK":
                print("tftNOK")
                ans = display.printunaut("Test-NOK")
            elif mode == "tftError":
                print("tftError")
                ans = display.printerr("Test-Error")
            elif mode == "tftClock":
                print("tftClock")
                ans = display.printclock("Test-Clock")
            else:
                print("This function is not available!")
                    
            print(ans)
            ans = 0
            mode=raw_input("->")

        freeResources()
    except Exception as e:
        print(e)
        freeResources()
            

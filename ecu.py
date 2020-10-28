import configparser
import channel8Relay
import time
import math
global relay

config = configparser.ConfigParser()
config.read('settings.ini')

vendorID = int(config['setting']['vendor_id'],16)
productID = int(config['setting']['product_id'],16)
nrSetups = int(config['setting']['nrOfSetups'])

class ECU_SETUP(object):

    def __init__(self,number):
        if number == 1 :
            self.relay = channel8Relay.Relay(vendorID,productID)
            self.number =1
            self.powerOnFlag = False
            self.debugOnFlag = False
            self.ignitionFlag = False
            self.powerOn = int(config['ECU_setup_1']['powerOn'][-1])
            self.debugOn = int(config['ECU_setup_1']['debugOn'][-1])
            self.ignitionOff = int(config['ECU_setup_1']['ignitionOff'][-1])
        elif number == 2:
            self.relay = channel8Relay.Relay(vendorID,productID)
            self.number = 2
            self.powerOnFlag = False
            self.debugOnFlag = False
            self.ignitionFlag = False
            self.powerOn = int(config['ECU_setup_2']['powerOn'][-1])
            self.debugOn = int(config['ECU_setup_2']['debugOn'][-1])
            self.ignitionOff = int(config['ECU_setup_2']['ignitionOff'][-1])
        elif number == 3:
            self.relay = channel8Relay.Relay(vendorID,productID)
            self.number = 3
            self.powerOnFlag = False
            self.debugOnFlag = False
            self.ignitionFlag = False
            self.powerOn = int(config['ECU_setup_3']['powerOn'][-1])
            self.debugOn = int(config['ECU_setup_3']['debugOn'][-1])
            self.ignitionOff = int(config['ECU_setup_3']['ignitionOff'][-1])
        elif number == 4:
            self.relay = channel8Relay.Relay(vendorID,productID)
            self.number = 4
            self.powerOnFlag = False
            self.debugOnFlag = False
            self.ignitionFlag = False
            self.powerOn = int(config['ECU_setup_4']['powerOn'][-1])
            self.debugOn = int(config['ECU_setup_4']['debugOn'][-1])
            self.ignitionOff = int(config['ECU_setup_4']['ignitionOff'][-1])


    def getNumber(self):
        return self.number

    def getPowerRelay(self):
        return self.powerOn

    def getDebugRelay(self):
        return self.debugOn

    def getIgnitionRelay(self):
        return self.ignitionOff

    def turnPowerOn(self):
        self.relay.state(self.powerOn,on=True)
        self.powerOnFlag = True

    def turnPowerOff(self):
        self.relay.state(self.powerOn,on=False)
        self.powerOnFlag = False

    def turnDebugOn(self):
        if self.powerOnFlag == False:
          self.relay.state(self.debugOn,on=True)
          self.debugOnFlag = True

    def turnDebugOff(self):
        if self.powerOnFlag == False:
          self.relay.state(self.debugOn,on=False)
          self.debugOnFlag = False

    def turnIgnitionOn(self):
        if self.powerOnFlag == True:
            self.relay.state(self.ignitionOff,on=True)
            self.ignitionFlag = True

    def turnIgnitionOff(self):
        self.relay.state(self.ignitionOff,on=False)
        self.ignitionFlag = False

    def printStats(self):
        print(self.powerOn,self.debugOn,self.ignitionOff)

    def isPowered(self):
        return self.powerOnFlag

    def isDebugging(self):
        return self.debugOnFlag

    def wipeSetup(self):
        if self.powerOnFlag == True:
            self.turnPowerOff()
            self.powerOnFlag = False
            self.debugOnFlag = False
            self.ignitionFlag = False
        if self.debugOnFlag == True:
            self.turnDebugOff()
            self.debugOnFlag = False
        if self.ignitionFlag == True:
            self.turnIgnitionOff()
            self.ignitionFlag = False
    """Turns off power,debug and ignition for given setup"""

if __name__ == "__main__":
    set1 = ECU_SETUP(1)
    set1.turnPowerOn()
    set1.wipeSetup()
    set1.turnPowerOn()
    set1.turnDebugOn()
    set1.wipeSetup()
from collections import namedtuple
import string
import hid
#from helpers import getErrorString
import  skyrcUSB.helpers


class NoChargerException(Exception):
    pass

class badResponse(Exception):
    pass

class chargeException(Exception):
    pass


# TODO what is send FE - stop charge?

class Charger:

    def __init__(self, vid: hex = 0x0000, pid: hex = 0x0001):
        self._h = hid.device()
        try:
            self._h.open(vid, pid)
        except OSError:
            raise NoChargerException(
                f"No Charger detected at {vid:04x}:{pid:04x}. Check that the device is connected, and has the correct HID driver."
            ) from None

        self._h.set_nonblocking(1)
        self.getMachineID()
        return

    def _sendpacket(self, packet: bytearray):
        self._h.write(packet)  # no padding needed huh

    def sendcommand(self, CMD: hex, side: int = 0):
        packet = bytearray([0x00, 0x0F, 0x00, CMD, 0x00, side])
        # Add more optional packets here.
        num = 6
        packet[2] = num - 2
        packet.append(sum(packet[3:num]))
        packet.append(0xFF)
        packet.append(0xFF)
        self._sendpacket(packet)
        while True:
            try:
                d = self._h.read(64)
            except OSError:
                raise NoChargerException
            if d:
                return d

    def getMachineID(self) -> None:
        pkt = self.sendcommand(0x57)
        if (pkt[0] != 0x0F or pkt[2] != 0x57): raise badResponse

        self.core_type = ''.join(map(chr, pkt[5:11]))
        self.model_name = skyrcUSB.helpers.getModel(self.core_type)
        self.upgrade_type = pkt[11]
        self.encrypted = bool(pkt[12])
        self.customer_id = pkt[13] + 256 * pkt[14]
        self.language_id = pkt[15]
        self.software_version = pkt[16] + 0.01 * pkt[17]
        self.hardware_version = pkt[18]
        self.reserved = pkt[19]

    def getCellInfo(self, side: int) -> list[int]:
        pkt = self.sendcommand(0x5F, side)
        if pkt[0] != 0x5F: raise badResponse
        cells = []
        for i in range(6):
            if pkt[2 * i + 3]:
                cells.append(pkt[2*i+3]*256 + pkt[2*i+4])
        i = 15
        return cells

    def getSettings(self) -> None:
        pkt = self.sendcommand(0x5A)
        if pkt[0] != 0x5A: raise badResponse

        self.sysKeyBeep = pkt[2] # look into the sys ones more!
        self.sysBuzzer = pkt[3]
        self.sysMaxCapacity = pkt[4]
        self.sysMaxTime = pkt[5]
        self.temp = pkt[6]
        self.maxCapacity = pkt[7]*256+pkt[8]
        self.maxTime = pkt[9]*256+pkt[10]
        self.maxTemp = pkt[11]
        self.restTime = pkt[12]
        self.dcMin = pkt[13]
        self.nimhSense = pkt[14]
        self.nicdSense = pkt[15]
        self.nimhSense = pkt[16]
        self.acPower = pkt[17]
        self.sysMaxTemp = pkt[18]
        

    def getChargeData(self, side: int, raiseErrors:bool = False):
        pkt = self.sendcommand(0x55, side)  #dec 85
        if pkt[0] != 0x55: raise badResponse
        if pkt[1] != side: raise badResponse
        
        if pkt[2] == 0: print("does this mean not chargin??")

        status = pkt[4]
                        
        if (status >= 128):
            errorcode = status - 127
        else:
            errorcode = 0
        status = 0 
            
        #n5 = pkt[3] - 0 always        
        
        chargeDuration = pkt[5]*256 + pkt[6] # minus one if greater than 0.
        
        voltage = pkt[7]*256 + pkt[8] #! THIS MAY BE INCORRECT WHEN DONE!!
        current =  pkt[9]*256 + pkt[10]
        capacity =  pkt[11]*256 + pkt[12]
        temp =  pkt[15]*10
        
        if errorcode > 0 and raiseErrors == True:
            raise chargeException(skyrcUSB.helpers.getErrorString(errorcode))
            
        cellVoltages = []
        if self.core_type != 100123:
            for i in range(6):
                v = pkt[2*i+17]*256 + pkt[2*i+18]
                if v > 100:
                    cellVoltages.append(v)

        return chargeState(voltage,current,capacity, chargeDuration, temp, cellVoltages, status, errorcode)


class chargeState(object):
    def __init__(self, voltage, current, capacity, chargeDuration, temp , cellVoltages, status, errorcode):
        self.voltage = voltage
        self.current = current
        self.capacity = capacity
        self.chargeDuration = chargeDuration
        self.temp = temp
        self.cellVoltages = cellVoltages
        self.status = status
        self.errorcode = errorcode
        
    def getStatusString(self) -> str:
        if self.status == 0:
            return "Not Charging" 
        if self.status == 1:
            return "Charging"
        if self.status == 4:
            return "Done Charging"

    def getErrorString(self):
        return skyrcUSB.helpers.getErrorString(self.errorcode)
    
    def getChargeType(self) -> str:
        if self.cellvoltages:  # pretty garbage function tbh - avoid me!
            return "balancing"
        else:
            return "charging"
        
    def isError(self) -> bool:
        return True if self.errorcode > 0  else False

    def isIdle(self) -> bool:
        return True if self.status == 0 else False

    def isCharging(self) -> bool:
        return True if self.status == 1 else False
    
    def isDone(self) -> bool:
        return True if self.status == 4 else False
    
    def hasTempSensor(self) -> bool:
        return False if self.temp == 0 else True
    

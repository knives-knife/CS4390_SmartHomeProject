from utils import *

from enum import IntEnum

class DeviceEnum(IntEnum):
    NONE = 0
    LIGHT_SWITCH = 1 << 1
    THERMOSTAT = 1 << 2

def maxDeviceFlag():
    maxFlag = 0
    for dev in DeviceEnum:
        maxFlag += dev.value
    return maxFlag

def parseDevices(names: list, activeDevices: list) -> int:
    deviceFlag = 0
    maxFlag = maxDeviceFlag()
    for device in activeDevices:
        if device.DeviceType.value & deviceFlag == 0 and device.Name in names:
            deviceFlag += device.DeviceType.value
        if deviceFlag == maxFlag:
            return maxFlag
    return deviceFlag

def findDeviceNames(string: str, activeDevices: list) -> list:
    names = string.upper().split(" ")
    activeDeviceNames = []
    for device in activeDevices:
        activeDeviceNames.append(device.Name)
    found = [value for value in names if value in activeDeviceNames]
    notFound = [value for value in names if value not in activeDeviceNames]
    if (len(notFound) > 0):
        printError("Name(s) not found: " + ", ".join(notFound))
    return found

def getDevicesFromList(devicesDict: list) -> list:
    devicesList = []
    for dictObj in devicesDict:
        devicesList.append(Device(dictObj['Name'], dictObj['Description'], DeviceEnum(dictObj['DeviceType'])))
    return devicesList


class Device():
    def __init__(self, name: str, desc: str, devType: DeviceEnum) -> None:
        self.Name = name
        self.DeviceType = devType
        self.Description = desc

    def toJSON(self) -> object:
        return {'Name': self.Name, 'DeviceType': self.DeviceType, 'Description': self.Description}
    
    def __str__(self) -> str:
        return f"{{Name: {self.Name}, DeviceType: {self.DeviceType.name}, Description: {self.Description}}}"

class LightSwitch(Device):    
    def __init__(self, name: str, desc: str, switchState: bool) -> None:
        Device.__init__(self, name, desc, DeviceEnum.LIGHT_SWITCH)
        self.IsSwitchOn = switchState

    def getState(self):
        return self.IsSwitchOn

    def setState(self, isOn: bool):
        self.IsSwitchOn = isOn
    
    def toDevice(self) -> Device:
        return Device(self.Name, self.Description, DeviceEnum.LIGHT_SWITCH)

class Thermostat(Device):    
    def __init__(self, name: str, desc: str, temperatue: float, unit: chr) -> None:
        Device.__init__(self, name, desc, DeviceEnum.THERMOSTAT)
        self.Temperature = temperatue
        self.Unit = unit
    
    def getTemperature(self):
        return self.Temperature
    
    def getUnit(self):
        return self.Unit
    
    def setTemperature(self, temperature: float):
        self.Temperature = temperature
    
    def setUnit(self, unit: chr):
        self.Unit = unit
    
    def toDevice(self) -> Device:
        return Device(self.Name, self.Description, DeviceEnum.THERMOSTAT)

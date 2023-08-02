import socket
import json
import re
import time
from utils import *
from devices import *

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

lightSwitches = [LightSwitch("FR", "Family Room", False), LightSwitch("K", "Kitchen", False)]
thermostats = [Thermostat("T", "House", 80, "F")]

#region TCP Functions

def startServer() -> socket:
    serverSock.listen()
    print("Server listening...")

def listenForClients():
    while True:
        global clientConnection
        clientConnection, addr = serverSock.accept()
        print(f"Client {addr[0]} found and connected\n\n\n")
        return addr
    
def receiveMessages():
    while True:
        rawMessage = clientConnection.recv(1024)
        message: Message
        try:
            message = MessageFromString(rawMessage.decode())
        except:
            if len(rawMessage) == 0:
                clientConnection.close()
                return
            print("Could not convert string to Message :(")
            continue
        print("\n")
        handleMessage(message)

def sendMessage(message: Message):
    print("Sent Message")
    clientConnection.sendall(str(message).encode())

def closeServer():
    serverSock.shutdown(socket.SHUT_RDWR)
    serverSock.close()

#endregion TCP Functions

def sendDeviceInfoMessage():
    deviceInfo = []
    deviceInfoJSON = []
    for ls in lightSwitches:
        deviceInfo.append(ls.toDevice())
    for th in thermostats:
        deviceInfo.append(th.toDevice())
    print("Sending Device Info...")
    for device in deviceInfo:
        deviceInfoJSON.append(device.toJSON())
    sendMessage(Message(MessageTypeEnum.REPLY, 0, [], json.dumps(deviceInfoJSON)))
    

#region Handling Message Functions

def handleMessage(message: Message):
    if message.MessageType == MessageTypeEnum.PULL:
        print("Received PULL Message")
        handlePULLMessage(message)
    elif message.MessageType == MessageTypeEnum.PUSH:
        print("Received PUSH Message")
        handlePUSHMessage(message)
    elif message.MessageType == MessageTypeEnum.EXIT:
        print("Received EXIT Message")
        handleEXITMessage()

#region PULL Message Functions

def handlePULLMessage(message: Message):
    if message.DeviceFlag == DeviceEnum.NONE.value:
        sendDeviceInfoMessage()
        return
    
    if message.DeviceFlag & DeviceEnum.LIGHT_SWITCH == DeviceEnum.LIGHT_SWITCH:
        handlePULLLightSwitch(message)
    time.sleep(0.1)
    if message.DeviceFlag & DeviceEnum.THERMOSTAT == DeviceEnum.THERMOSTAT:
        handlePULLThermostat(message)

def handlePULLLightSwitch(message: Message):
    print("PULLing Light Switches")
    for lightSwitch in lightSwitches:
        if lightSwitch.Name in message.DeviceNames:
            sendMessage(Message(MessageTypeEnum.REPLY, DeviceEnum.LIGHT_SWITCH, [lightSwitch.Name], f"The {lightSwitch.Name} light switch ({lightSwitch.Description}) is set to {'ON' if lightSwitch.IsSwitchOn else 'OFF'}"))
            time.sleep(0.1)


def handlePULLThermostat(message: Message):
    print("PULLing Thermostats")
    for thermostat in thermostats:
        if thermostat.Name in message.DeviceNames:
            sendMessage(Message(MessageTypeEnum.REPLY, DeviceEnum.THERMOSTAT, [thermostat.Name], f"The {thermostat.Name} thermostat ({thermostat.Description}) is set to {thermostat.Temperature}° {thermostat.Unit}"))
            time.sleep(0.1)
#endregion PULL Message Functions


#region PUSH Message Functions

def handlePUSHMessage(message: Message):
    if message.DeviceFlag & DeviceEnum.LIGHT_SWITCH == DeviceEnum.LIGHT_SWITCH:
        handlePUSHLightSwitch(message)
    time.sleep(0.1)
    if message.DeviceFlag & DeviceEnum.THERMOSTAT == DeviceEnum.THERMOSTAT:
        handlePUSHThermostat(message)

def handlePUSHLightSwitch(message: Message):
    print("PUSHing Light Switches")
    for lightSwitch in lightSwitches:
        if lightSwitch.Name in message.DeviceNames:
            time.sleep(0.1)
            if re.search("(ON)|(OFF)", message.Value.upper()) is None:
                value = f"Could not set the {lightSwitch.Name} light switch ({lightSwitch.Description}) to '{message.Value}'"
                printError(value)
                sendMessage(Message(MessageTypeEnum.ERROR, DeviceEnum.LIGHT_SWITCH, [lightSwitch.Name], value))
                continue
            lightSwitch.IsSwitchOn = True if message.Value == "ON" else False
            value = f"Set the {lightSwitch.Name} light switch ({lightSwitch.Description}) to {'ON' if lightSwitch.IsSwitchOn else 'OFF'}"
            printBlue(value)
            sendMessage(Message(MessageTypeEnum.REPLY, DeviceEnum.LIGHT_SWITCH, [lightSwitch.Name], value))

def handlePUSHThermostat(message: Message):
    print("PUSHing Thermostats")
    for thermostat in thermostats:
        if thermostat.Name in message.DeviceNames:
            time.sleep(0.1)
            if re.search("([0-9]+)|([0-9]*\\.[0-9]+)", message.Value) is None:
                value = f"Could not set the {thermostat.Name} thermostat ({thermostat.Description}) to '{message.Value}'"
                printError(f"Could not set thermostat to '{message.Value}'")
                sendMessage(Message(MessageTypeEnum.ERROR, DeviceEnum.THERMOSTAT, [thermostat.Name], value))
                continue
            thermostat.Temperature = float(message.Value)
            value = f"Set the {thermostat.Name} thermostat ({thermostat.Description}) to {thermostat.getTemperature()}"
            printBlue(value)
            sendMessage(Message(MessageTypeEnum.REPLY, DeviceEnum.THERMOSTAT, [thermostat.Name], value))

#endregion PUSH Message Functions

def handleEXITMessage():
    clientConnection.shutdown(socket.SHUT_RDWR)
    clientConnection.close()
    closeServer()
    exit("Shutting down...")

#endregion Handling Message Functions



def main():
    serverSock.bind(('', PortEnum.SERVER.value))
    while True:
        startServer()
        addr = listenForClients()
        receiveMessages()




    

if __name__ == "__main__":
    main()
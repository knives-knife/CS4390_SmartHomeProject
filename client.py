import socket
import time
import json
import re
from utils import *
from devices import *


clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.settimeout(10)

def establishTCPConnection():
    try:
        clientSock.connect((AddressEnum.SERVER.value, PortEnum.SERVER.value))
        print("Connected")
    except:
        exit("Could not connect to server\nExiting...")

def sendMessage(message: Message):
    clientSock.sendall(str(message).encode())

def getActiveDevices():
    sendMessage(Message(MessageTypeEnum.PULL, 0, [], "list"))
    rawMessage = clientSock.recv(1024)
    message: Message
    try:
        message = MessageFromString(rawMessage.decode())
    except:
        print("Could not convert string to Message :(")

    global activeDevices
    activeDevices = getDevicesFromList(json.loads(message.Value))



def takeInput():
    initialInstructions = """What would you like to do?\n
PULL - get the current status of a device
PUSH - set the current status of a device
EXIT - terminate the program (and server)\n
->"""
    
    deviceInfo = ""
    for device in activeDevices:
        deviceInfo += f"{device.Name} - {device.Description} - {device.DeviceType.name}\n"

    deviceInstructions = """\n\n
Which device(s) would you like to {0}?
If you would like more than one device, please put a space between each device name.
Name - Description - Device Type\n
{1}
->"""

    valueInstructions = """\n\nWhat would you like to set the value to?
ON or OFF accepted for light switches
Integers and decimals accepted for thermostats\n
->"""

    while True:
        initialInput = input(initialInstructions)
        messageType: MessageTypeEnum
        try:
            messageType = MessageTypeEnum[initialInput.upper()]
        except:
            printError(f"{initialInput.upper()} is not a valid operation")
            time.sleep(2)
            continue

        if messageType == MessageTypeEnum.EXIT:
            shutdown()
            return
        
        deviceInput = input(deviceInstructions.format(messageType.name, deviceInfo))
        deviceNames = findDeviceNames(deviceInput.strip(), activeDevices)
        if (len(deviceNames) < 1):
            printError("No names found that match the active devices")
            time.sleep(2)
            continue

        deviceFlag = parseDevices(deviceNames, activeDevices)

        value = ""
        if (messageType == MessageTypeEnum.PUSH):
            valueInput = input(valueInstructions)
            if re.search("(^[0-9]+$)|(^[0-9]*\\.[0-9]+$)|(^ON$)|(^OFF$)|^$", valueInput.upper()) is None:
                printError(f"'{valueInput}' is not a valid value\n\n")
                time.sleep(2)
                continue
            value = valueInput
        
        sendMessage(Message(messageType, deviceFlag, deviceNames, value))
        print("Sent message\nWaiting for reply")
        awaitReply(len(deviceNames))

def awaitReply(expectedReplies: int):
    print()
    try:
        replies = 0
        while (replies < expectedReplies):
            rawMessage = clientSock.recv(1024)
            message: Message
            try:
                message = MessageFromString(rawMessage.decode())
            except:
                print("Could not convert string to Message :(")
                continue
            if message.MessageType == MessageTypeEnum.REPLY:
                replies += 1
                printBlue(message.Value)
            elif message.MessageType == MessageTypeEnum.ERROR:
                replies += 1
                printError(message.Value)
    except socket.timeout as te:
        print("Waiting for reply timed out")
    print("\n")

def shutdown():
    sendMessage(Message(MessageTypeEnum.EXIT, 0, [], ""))
    clientSock.shutdown(socket.SHUT_RDWR)
    clientSock.close()
    exit("Closed socket\nExiting...")

def main():
    establishTCPConnection()
    time.sleep(1)
    getActiveDevices()
    takeInput()



if __name__ == "__main__":
    main()
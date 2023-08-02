from enum import Enum

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class AddressEnum(Enum):
    SERVER = "10.0.0.1"
    CLIENT = "10.0.0.2"

class PortEnum(Enum):
    SERVER = 58426
    CLIENT = 49047

class MessageTypeEnum(Enum):
    EXIT = -1
    PULL = 0
    PUSH = 1
    REPLY = 2
    ERROR = 3


class Message():
    def __init__(self, messageType: MessageTypeEnum, deviceFlag: int, deviceNames: list, value: str):
        self.MessageType = messageType
        self.DeviceFlag = deviceFlag
        self.DeviceNames = deviceNames
        self.Value = value
    
    def __str__(self):
        return f"{MessageTypeEnum(self.MessageType).name}~~~{self.DeviceFlag}~~~{'^^^'.join(self.DeviceNames)}~~~{self.Value}"
    

def MessageFromString(string: str) -> Message:
    fields = string.split("~~~")
    return Message(MessageTypeEnum[fields[0]], int(fields[1]), fields[2].split("^^^"), fields[3])

def printError(message: str):
    print(f"{bcolors.FAIL}{message}{bcolors.ENDC}")

def printBlue(message: str):
    print(f"{bcolors.OKBLUE}{message}{bcolors.ENDC}")
    

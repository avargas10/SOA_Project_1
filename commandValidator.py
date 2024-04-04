from enum import Enum
from configuration import Addressing

class Arguments(Enum):
    SENDER = 1
    RECEIVER = 2
    MAILBOX = 3
    CONTENT = 4
    PROCESS_ID = 5
    PRIORITY = 6

class CommandValidator:
    def __init__(self):
        """Inicializa la interfaz de línea de comandos con la simulación proporcionada."""
        pass

    def getSenderArgs(self, args, addressing):
        isValid = False
        extractedArgs = {}
        if addressing == Addressing.DIRECT_EXPLICIT and len(args) >= 3:
            extractedArgs[Arguments.SENDER] = args[0]
            extractedArgs[Arguments.RECEIVER] = args[1]
            extractedArgs[Arguments.PRIORITY] = args[2]
            extractedArgs[Arguments.CONTENT] = ' '.join(args[3:])
            isValid = True
        elif addressing == Addressing.DIRECT_IMPLICIT and len(args) >= 3:
            extractedArgs[Arguments.SENDER] = args[0]
            extractedArgs[Arguments.RECEIVER] = args[1]
            extractedArgs[Arguments.PRIORITY] = args[2]
            extractedArgs[Arguments.CONTENT] = ' '.join(args[3:])
            isValid = True
        elif addressing == Addressing.INDIRECT_DYNAMIC and len(args) >= 3:
            extractedArgs[Arguments.SENDER] = args[0]
            extractedArgs[Arguments.MAILBOX] = args[1]
            extractedArgs[Arguments.PRIORITY] = args[2]
            extractedArgs[Arguments.CONTENT] = ' '.join(args[3:])
            isValid = True
        elif addressing == Addressing.INDIRECT_STATIC and len(args) >= 3:
            extractedArgs[Arguments.SENDER] = args[0]
            extractedArgs[Arguments.MAILBOX] = args[1]
            extractedArgs[Arguments.PRIORITY] = args[2]
            extractedArgs[Arguments.CONTENT] = ' '.join(args[3:])
            isValid = True
        return isValid, extractedArgs
        
    def getReceiverArgs(self, args, addressing):
        isValid = False
        extractedArgs = {}
        if addressing == Addressing.DIRECT_EXPLICIT and len(args) >= 2:
            extractedArgs[Arguments.RECEIVER] = args[0]
            extractedArgs[Arguments.SENDER] = args[1]
            isValid = True
        elif addressing == Addressing.DIRECT_IMPLICIT and len(args) >= 1:
            extractedArgs[Arguments.RECEIVER] = args[0]
            isValid = True
        elif addressing == Addressing.INDIRECT_DYNAMIC and len(args) >= 1:
            extractedArgs[Arguments.RECEIVER] = args[0]
            isValid = True
        elif addressing == Addressing.INDIRECT_STATIC and len(args) >= 1:
            extractedArgs[Arguments.RECEIVER] = args[0]
            isValid = True
        return isValid, extractedArgs
    
    def getCreateProcessArgs(self, args, addressing):
        isValid = False
        extractedArgs = {}
        if addressing == Addressing.DIRECT_EXPLICIT and len(args) >= 1:
            extractedArgs[Arguments.PROCESS_ID] = args[0]
            isValid = True
        elif addressing == Addressing.DIRECT_IMPLICIT and len(args) >= 1:
            extractedArgs[Arguments.PROCESS_ID] = args[0]
            isValid = True
        elif addressing == Addressing.INDIRECT_DYNAMIC and len(args) >= 2:
            extractedArgs[Arguments.PROCESS_ID] = args[0]
            extractedArgs[Arguments.MAILBOX] = args[1]
            isValid = True
        elif addressing == Addressing.INDIRECT_STATIC and len(args) >= 2:
            extractedArgs[Arguments.PROCESS_ID] = args[0]
            extractedArgs[Arguments.MAILBOX] = args[1]
            isValid = True
        return isValid, extractedArgs
        
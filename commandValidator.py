from enum import Enum
from configuration import Addressing

# Enumeración que define los argumentos posibles y sus números de índice asociados
class Arguments(Enum):
    SENDER = 1
    RECEIVER = 2
    MAILBOX = 3
    CONTENT = 4
    PROCESS_ID = 5
    PRIORITY = 6

# Clase para validar comandos
class CommandValidator:
    def __init__(self):
        """Inicializa la interfaz de línea de comandos con la simulación proporcionada."""
        pass

    def getSenderArgs(self, args, addressing):
        """
        Obtiene los argumentos del remitente.

        Parámetros:
        - args (list): Lista de argumentos.
        - addressing (Addressing): Tipo de direccionamiento.

        Salida:
        - isValid (bool): Indica si los argumentos son válidos.
        - extractedArgs (dict): Argumentos extraídos.
        """
        isValid = False
        extractedArgs = {}
        if addressing in [Addressing.DIRECT_EXPLICIT, Addressing.DIRECT_IMPLICIT] and len(args) >= 3:
            extractedArgs[Arguments.SENDER] = args[0]
            extractedArgs[Arguments.RECEIVER] = args[1]
            extractedArgs[Arguments.PRIORITY] = args[2]
            extractedArgs[Arguments.CONTENT] = ' '.join(args[3:])
            isValid = True
        elif addressing in [Addressing.INDIRECT_DYNAMIC, Addressing.INDIRECT_STATIC] and len(args) >= 3:
            extractedArgs[Arguments.SENDER] = args[0]
            extractedArgs[Arguments.MAILBOX] = args[1]
            extractedArgs[Arguments.PRIORITY] = args[2]
            extractedArgs[Arguments.CONTENT] = ' '.join(args[3:])
            isValid = True
        return isValid, extractedArgs
        
    def getReceiverArgs(self, args, addressing):
        """
        Obtiene los argumentos del receptor.

        Parámetros:
        - args (list): Lista de argumentos.
        - addressing (Addressing): Tipo de direccionamiento.

        Salida:
        - isValid (bool): Indica si los argumentos son válidos.
        - extractedArgs (dict): Argumentos extraídos.
        """
        isValid = False
        extractedArgs = {}
        if addressing in [Addressing.DIRECT_EXPLICIT, Addressing.DIRECT_IMPLICIT] and len(args) >= 2:
            extractedArgs[Arguments.RECEIVER] = args[0]
            extractedArgs[Arguments.SENDER] = args[1]
            isValid = True
        elif addressing in [Addressing.INDIRECT_DYNAMIC, Addressing.INDIRECT_STATIC] and len(args) >= 1:
            extractedArgs[Arguments.RECEIVER] = args[0]
            isValid = True
        return isValid, extractedArgs
    
    def getCreateProcessArgs(self, args, addressing):
        """
        Obtiene los argumentos de creación de proceso.

        Parámetros:
        - args (list): Lista de argumentos.
        - addressing (Addressing): Tipo de direccionamiento.

        Salida:
        - isValid (bool): Indica si los argumentos son válidos.
        - extractedArgs (dict): Argumentos extraídos.
        """
        isValid = False
        extractedArgs = {}
        if addressing in [Addressing.DIRECT_EXPLICIT, Addressing.DIRECT_IMPLICIT] and len(args) >= 1:
            extractedArgs[Arguments.PROCESS_ID] = args[0]
            isValid = True
        elif addressing in [Addressing.INDIRECT_DYNAMIC, Addressing.INDIRECT_STATIC] and len(args) >= 2:
            extractedArgs[Arguments.PROCESS_ID] = args[0]
            extractedArgs[Arguments.MAILBOX] = args[1]
            isValid = True
        return isValid, extractedArgs

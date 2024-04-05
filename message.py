import time

from constants import DEFAULT_PRIORITY

class Message:
    """
    Clase para representar un mensaje.

    Attributes:
    - source (str): Origen del mensaje.
    - destination (str): Destino del mensaje.
    - content (str): Contenido del mensaje.
    - priority (int): Prioridad del mensaje (por defecto DEFAULT_PRIORITY).
    - timestamp (float): Marca de tiempo del mensaje.
    """
    def __init__(self, source, destination, content, priority=DEFAULT_PRIORITY):
        """
        Inicializa un objeto de mensaje.

        Parámetros:
        - source (str): Origen del mensaje.
        - destination (str): Destino del mensaje.
        - content (str): Contenido del mensaje.
        - priority (int): Prioridad del mensaje (por defecto DEFAULT_PRIORITY).
        """
        self.source = source
        self.destination = destination
        self.content = content
        self.messageLenghtLimit = len(self.content)
        self.timestamp = time.time()
        self.priority = priority

    def validateLenght(self, lenght):
        """
        Valida la longitud del contenido del mensaje.

        Parámetros:
        - lenght (int): Longitud a validar.

        Returns:
        - bool: True si la longitud del contenido coincide con la proporcionada, False en caso contrario.
        """
        return len(self.content) == lenght

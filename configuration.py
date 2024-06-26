import pandas as pd

from enum import Enum
from tabulate import tabulate

class Synchronization(Enum):
    """
    Enumeración para los tipos de sincronización.
    """
    BLOCKING = 1
    NONBLOCKING = 2
    TEST_FOR_ARRIVAL = 3

class Addressing(Enum):
    """
    Enumeración para los tipos de direccionamiento.
    """
    DIRECT_EXPLICIT = 1
    DIRECT_IMPLICIT = 2
    INDIRECT_STATIC = 3
    INDIRECT_DYNAMIC = 4

class Format(Enum):
    """
    Enumeración para los formatos de mensaje.
    """
    FIXED_LENGTH = 1
    VARIABLE_LENGTH = 2

class QueueDiscipline(Enum):
    """
    Enumeración para las disciplinas de cola.
    """
    FIFO = 1
    PRIORITY = 2

class Configuration:
    """
    Clase para cargar y acceder a la configuración.
    """
    def __init__(self, file_path):
        """
        Inicializa la configuración a partir del archivo proporcionado.

        Parámetros:
        - file_path (str): Ruta del archivo de configuración.
        """
        self.syncSender = None
        self.syncReceiver = None
        self.addr = None
        self.format = None
        self.queue_size = 1
        self.messageLenght = 0
        self.queue_discipline = None
        self.max_processes = None
        self.load_configuration(file_path)

    def load_configuration(self, file_path):
        """
        Carga la configuración desde el archivo especificado.

        Parámetros:
        - file_path (str): Ruta del archivo de configuración.
        """
        with open(file_path, 'r') as file:
            
            for line in file:
                key, value = line.strip().split('=')
                if key == 'SynchronizationSender':
                    self.syncSender = Synchronization[value.upper()]
                elif key == 'SynchronizationReceiver':
                    self.syncReceiver = Synchronization[value.upper()]
                elif key == 'Addressing':
                    self.addr = Addressing[value.upper()]
                elif key == 'Format':
                    self.format = Format[value.upper()]
                elif key == 'MessageLenght':
                    self.messageLenght = int(value)
                elif key == 'QueueDiscipline':
                    self.queue_discipline = QueueDiscipline[value.upper()]
                elif key == 'QueueSize':
                    self.queue_size = int(value)
                elif key == 'MaxProcesses':
                    self.max_processes = int(value)

    def get_sync_sender_configuration(self):
        """
        Obtiene la configuración de sincronización del emisor.
        """
        return self.syncSender

    def get_sync_receiver_configuration(self):
        """
        Obtiene la configuración de sincronización del receptor.
        """
        return self.syncReceiver

    def get_addressing_configuration(self):
        """
        Obtiene la configuración de direccionamiento.
        """
        return self.addr

    def get_format_configuration(self):
        """
        Obtiene la configuración del formato de mensaje.
        """
        return self.format, self.messageLenght

    def get_queue_discipline_configuration(self):
        """
        Obtiene la configuración de la disciplina de cola.
        """
        return self.queue_discipline
    
    def get_queue_size_configuration(self):
        """
        Obtiene la configuración del tamaño de la cola.
        """
        return self.queue_size
      
    def get_max_processes_configuration(self):
        return self.max_processes
    
    def to_dataframe(self):
        """
        Genera un DataFrame con el contenido actual de los parámetros.
        """
        data = {
            'Sender Sync': [self.syncSender],
            'Receiver Sync': [self.syncReceiver],
            'Adressing': [self.addr],
            'Format': [self.format],
            'Mailbox Size': [self.queue_size],
            'Message Lenght': [self.messageLenght],
            'Queue Discipline': [self.queue_discipline],
            'Max Process Limit': [self.max_processes]
        }
        df = pd.DataFrame(data)
        # Transponer el DataFrame
        df_transposed = df.transpose()
        # Restablecer los índices
        df_transposed.reset_index(inplace=True)
        # Renombrar las columnas
        df_transposed.columns = ['Parámetro', 'Valor']
        return df_transposed

    def print_configuration(self):
        """
        Imprime el contenido actual de los parámetros en formato tabular.
        """
        df = self.to_dataframe()
        print(tabulate(df, headers='keys', tablefmt='pretty'))


# Ejemplo de uso
if __name__ == "__main__":
    conf_file_path = "tests/test1.conf"  # Ruta del archivo .conf
    config = Configuration(conf_file_path)

    print("Synchronization Sender:", config.get_sync_sender_configuration())
    print("Synchronization Receiver:", config.get_sync_receiver_configuration())
    print("Addressing:", config.get_addressing_configuration())
    print("Format:", config.get_format_configuration())
    print("Queue Discipline:", config.get_queue_discipline_configuration())
    print("Queue Size:", config.get_queue_size_configuration())

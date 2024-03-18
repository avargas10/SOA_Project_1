from enum import Enum

class Synchronization(Enum):
    BLOCKING = 1
    NONBLOCKING = 2
    TEST_FOR_ARRIVAL = 3

class Addressing(Enum):
    DIRECT_SEND_RECEIVE = 1
    EXPLICIT_RECEIVE = 2
    IMPLICIT = 3
    DYNAMIC = 4
    INDIRECT = 5

class Format(Enum):
    FIXED_LENGTH = 1
    VARIABLE_LENGTH = 2

class QueueDiscipline(Enum):
    FIFO = 1
    PRIORITY = 2

class Configuration:
    def __init__(self, file_path):
        self.syncSender = None
        self.syncReceiver = None
        self.addr = None
        self.format = None
        self.messageLenght = 0
        self.queue_discipline = None
        self.load_configuration(file_path)

    def load_configuration(self, file_path):
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

    def get_sync_sender_configuration(self):
        return self.syncSender

    def get_sync_receiver_configuration(self):
        return self.syncReceiver

    def get_addressing_configuration(self):
        return self.addr

    def get_format_configuration(self):
        return self.format, self.messageLenght

    def get_queue_discipline_configuration(self):
        return self.queue_discipline

# Ejemplo de uso
if __name__ == "__main__":
    conf_file_path = "tests/test1.conf"  # Ruta del archivo .conf
    config = Configuration(conf_file_path)

    print("Synchronization Sender:", config.get_sync_sender_configuration())
    print("Synchronization Receiver:", config.get_sync_receiver_configuration())
    print("Addressing:", config.get_addressing_configuration())
    print("Format:", config.get_format_configuration())
    print("Queue Discipline:", config.get_queue_discipline_configuration())

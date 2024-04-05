import pandas as pd
from logger import Logger
from constants import MAILBOX_LOGGER
from configuration import QueueDiscipline
from enum import Enum
from operator import attrgetter

class MailboxTypes(Enum):
    SINGLE_PORT = 1
    QUEUE = 2

class CustomMailbox:
    def __init__(self, id, size = 1, type=MailboxTypes.SINGLE_PORT, queueDiscipline=QueueDiscipline.FIFO):
        self.id = id
        self.type = type
        self.size = size
        self.queueDiscipline = queueDiscipline
        self.messages = []
        self.logger = Logger(MAILBOX_LOGGER + "-" + id) 
        self.logger.info(f"Mailbox {id}, created with discipline {queueDiscipline.name} and size {size}")

    def clean(self):
        if self.type == MailboxTypes.SINGLE_PORT:
            self.messages = []
            self.logger.info(f"Mailbox {self.id} was cleaned")

    def send(self, message):
        self.messages.append(message)
        self.sort_queue()
        if len(self.messages) > self.size:
            self.remove_element()
        self.logger.info(f"Mailbox {self.id} new message inserted")

    def remove_element(self):
        if self.queueDiscipline == QueueDiscipline.PRIORITY:
            self.messages.pop(len(self.messages) - 1)
        elif self.queueDiscipline == QueueDiscipline.FIFO:
            self.messages.pop(0)
        self.logger.info(f"Mailbox {self.id} Oldest message deleted")

    def receive(self):
        if self.messages:
            self.logger.info(f"Mailbox {self.id} message pulled")
            return self.messages.pop(0)
        else:
            return None
        
    def sort_queue(self):
        if self.type == MailboxTypes.QUEUE and self.queueDiscipline == QueueDiscipline.PRIORITY:
            self.messages.sort(key=lambda x: x.priority, reverse=False)
            self.logger.info(f"Mailbox {self.id} Sorted by Priority")
        else:
            self.logger.info("Not sorted")
        
    def display_state(self):
        # Crear DataFrame para mostrar el estado de la cola
        data = {
            'Mailbox': self.id,
            'Message': [msg.content for msg in self.messages],
            'Sender': [msg.source for msg in self.messages],
            'Index': [idx for idx, msg in enumerate(self.messages, start=1)],
            'Priority': [msg.priority for msg in self.messages],
            'Timestamp': [msg.timestamp for msg in self.messages]
        }
        df_data = pd.DataFrame(data)

        # Agregar información adicional
        df_info = pd.DataFrame({
            'Mailbox': self.id,
            'Max Size': [self.size],
            'Actual Size': [len(self.messages)],
            'Type': [self.type.name],
            'Discipline': [self.queueDiscipline.name]
        }, index=['Config Information'])

        return df_info, df_data
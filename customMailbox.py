from logger import Logger
from constants import MAILBOX_LOGGER
class CustomMailbox:
    def __init__(self, id):
        self.id = id
        self.messages = []
        self.logger = Logger(MAILBOX_LOGGER + "-" + id) 

    def send(self, message):
        self.messages.append(message)

    def receive(self):
        if self.messages:
            return self.messages.pop(0)
        else:
            return None
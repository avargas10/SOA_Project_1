import time

from constants import DEFAULT_PRIORITY

class Message:
    def __init__(self, source, destination, content, priority=DEFAULT_PRIORITY):
        self.source = source
        self.destination = destination
        self.content = content
        self.messageLenghtLimit = len(self.content)
        self.timestamp = time.time()
        self.priority = priority

    def validateLenght(self, lenght):
        return len(self.content) == lenght
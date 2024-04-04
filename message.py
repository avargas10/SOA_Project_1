import time

class Message:
    def __init__(self, source, destination, content, priority=0):
        self.source = source
        self.destination = destination
        self.content = content
        self.priority = priority
        self.messageLenghtLimit = len(self.content)
        self.timestamp = time.time()

    def validateLenght(self, lenght):
        return len(self.content) == lenght
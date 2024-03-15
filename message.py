import time

class Message:
    def __init__(self, source, destination, content):
        self.source = source
        self.destination = destination
        self.content = content
        self.timestamp = time.time()
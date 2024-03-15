class CustomMailbox:
    def __init__(self):
        self.messages = []

    def send(self, message):
        self.messages.append(message)

    def receive(self):
        if self.messages:
            return self.messages.pop(0)
        else:
            return None
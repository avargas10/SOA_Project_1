from message import Message

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.mailbox = None

    def assign_mailbox(self, mailbox):
        self.mailbox = mailbox

    def send_message(self, destination_pid, content):
        if self.mailbox:
            message = Message(self.pid, destination_pid, content)
            self.mailbox.send(message)
            print(f"Message sent from process {self.pid} to {destination_pid}")
        else:
            print("Process has no mailbox assigned.")

    def receive_message(self):
        if self.mailbox:
            message = self.mailbox.receive()
            if message:
                print(f"Process {self.pid} received message from {message.source}: {message.content}")
            else:
                print("No messages available for process", self.pid)
        else:
            print("Process has no mailbox assigned.")
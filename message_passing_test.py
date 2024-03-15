import time

class Message:
    def __init__(self, source, destination, content):
        self.source = source
        self.destination = destination
        self.content = content
        self.timestamp = time.time()

class Mailbox:
    def __init__(self):
        self.messages = []

    def send(self, message):
        self.messages.append(message)

    def receive(self):
        if self.messages:
            return self.messages.pop(0)
        else:
            return None

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

class Simulation:
    def __init__(self):
        self.processes = {}
        self.mailboxes = {}

    def create_process(self, pid):
        self.processes[pid] = Process(pid)

    def create_mailbox(self, mailbox_id):
        self.mailboxes[mailbox_id] = Mailbox()

    def assign_mailbox_to_process(self, pid, mailbox_id):
        if pid in self.processes and mailbox_id in self.mailboxes:
            self.processes[pid].assign_mailbox(self.mailboxes[mailbox_id])
        else:
            print("Invalid process or mailbox ID.")

    def execute_command(self, command):
        # Aquí implementa la lógica para ejecutar los comandos
        pass

    def display_state(self):
        # Aquí implementa la lógica para mostrar el estado del sistema
        pass

# Ejemplo de uso
simulation = Simulation()
simulation.create_process(1)
simulation.create_process(2)
simulation.create_mailbox('A')
simulation.create_mailbox('B')
simulation.assign_mailbox_to_process(1, 'A')
simulation.assign_mailbox_to_process(2, 'B')
simulation.processes[1].send_message(2, "Hello")
simulation.processes[2].receive_message()

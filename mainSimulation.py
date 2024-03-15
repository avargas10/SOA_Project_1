from customMailbox import CustomMailbox
from process import Process

class Simulation:
    def __init__(self):
        self.processes = {}
        self.mailboxes = {}

    def create_process(self, pid):
        self.processes[pid] = Process(pid)

    def create_mailbox(self, mailbox_id):
        self.mailboxes[mailbox_id] = CustomMailbox()

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

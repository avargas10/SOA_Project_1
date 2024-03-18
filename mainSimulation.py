from customMailbox import CustomMailbox
from process import Process
from logger import Logger
class Simulation:
    def __init__(self, conf):
        self.processes = {}
        self.mailboxes = {}
        self.conf = conf
        self.logger = Logger("MainSimulation")

    def create_process(self, pid):
        syncSender = self.conf.get_sync_sender_configuration()
        syncReceiver = self.conf.get_sync_receiver_configuration()
        format, messageLenght = self.conf.get_format_configuration()
        self.processes[pid] = Process(pid, syncReceiver, syncSender, format, messageLenght)

    def create_mailbox(self, mailbox_id):
        self.mailboxes[mailbox_id] = CustomMailbox(mailbox_id)

    def assign_mailbox_to_process(self, pid, mailbox_id):
        if pid in self.processes and mailbox_id in self.mailboxes:
            self.processes[pid].assign_mailbox(self.mailboxes[mailbox_id])
        else:
            self.logger.error("Invalid process or mailbox ID.")

    def execute_command(self, command):
        # Aquí implementa la lógica para ejecutar los comandos
        pass

    def display_state(self):
        # Aquí implementa la lógica para mostrar el estado del sistema
        pass

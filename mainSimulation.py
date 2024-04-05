import pandas as pd

from customMailbox import CustomMailbox, MailboxTypes
from process import Process
from logger import Logger
from commandValidator import CommandValidator, Arguments
from configuration import Addressing
from tabulate import tabulate

class Simulation:
    def __init__(self, conf):
        self.processes = {}
        self.mailboxes = {}
        self.conf = conf
        self.logger = Logger("MainSimulation", True, True)
        self.commandValidator = CommandValidator()

    def get_conf(self):
        return self.conf

    def create_process(self, args):
        syncSender = self.conf.get_sync_sender_configuration()
        syncReceiver = self.conf.get_sync_receiver_configuration()
        format, messageLenght = self.conf.get_format_configuration()
        addressing = self.conf.get_addressing_configuration()
        self.validate_create_process(args, addressing, syncReceiver, syncSender,format,messageLenght)

    def create_mailbox(self, mailbox_id):
        mailboxSize = self.conf.get_queue_size_configuration()
        mailboxDispline = self.conf.get_queue_discipline_configuration()
        new_mailbox = CustomMailbox(mailbox_id, mailboxSize, MailboxTypes.QUEUE, mailboxDispline)
        self.mailboxes[mailbox_id] = new_mailbox
        return new_mailbox

    def process_send(self, args):
        addressing = self.conf.get_addressing_configuration()
        isValid, jsonArgs = self.commandValidator.getSenderArgs(args, addressing)
        if not isValid:
            self.logger.error(f"Send not valid!!\nNot meeting requirements for addressing {addressing}")
            return
        if (addressing == Addressing.DIRECT_EXPLICIT or addressing == Addressing.DIRECT_IMPLICIT) and \
                self.process_exist(jsonArgs[Arguments.SENDER], jsonArgs[Arguments.RECEIVER], True):
            mailbox = self.processes[jsonArgs[Arguments.RECEIVER]].get_mailbox()
            self.processes[jsonArgs[Arguments.SENDER]].send_message(jsonArgs[Arguments.RECEIVER], 
                                                                               jsonArgs[Arguments.CONTENT], 
                                                                               mailbox,
                                                                               jsonArgs[Arguments.PRIORITY])
        
        elif (addressing == Addressing.INDIRECT_STATIC or addressing == Addressing.INDIRECT_DYNAMIC) and \
                self.process_exist(jsonArgs[Arguments.SENDER]):
            mailbox = self.mailboxes[jsonArgs[Arguments.MAILBOX]]
            self.processes[jsonArgs[Arguments.SENDER]].send_message(jsonArgs[Arguments.MAILBOX], 
                                                                    jsonArgs[Arguments.CONTENT], 
                                                                    mailbox,
                                                                    jsonArgs[Arguments.PRIORITY])
        
        else:
            self.logger.error(f"Adressing configuration error {addressing}")
        return isValid
    
    def process_exist(self, sender, receiver=None, validateReceiver=False):
        exist = True
        sender_process = self.processes.get(sender)
        receiver_process = self.processes.get(receiver)
        if sender_process is None:
            exist = False
            self.logger.error(f"Sender Process {sender} not found")
        if receiver_process is None and validateReceiver:
            exist = False
            self.logger.error(f"Receiver Process {sender} not found")
        return exist
    
    def get_mailbox(self, mailbox):
        found_mailbox = self.mailboxes.get(mailbox)
        if found_mailbox is None:
            self.logger.error(f"Mailbox {mailbox} not found")
        return found_mailbox
    
    def get_process(self, process):
        found_process = self.processes.get(process)
        if found_process is None:
            self.logger.error(f"Process {process} not found")
        return found_process

    def validate_create_process(self, args, addressing, syncReceiver, syncSender, format, messageLenght):
        isValid, jsonArgs = self.commandValidator.getCreateProcessArgs(args, addressing)
        if not isValid:
            self.logger.error(f"Receive not valid!!\n, not meeting requirements for addressing {addressing}")
            return
        if addressing == Addressing.DIRECT_EXPLICIT or addressing == Addressing.DIRECT_IMPLICIT:
                pid = jsonArgs[Arguments.PROCESS_ID]
                mailbox = self.create_mailbox("process_" + str(pid))
                self.processes[pid] = Process(pid, syncReceiver, syncSender, mailbox, format, messageLenght)
        
        elif addressing == Addressing.INDIRECT_STATIC \
            or addressing == Addressing.INDIRECT_DYNAMIC:
            pid = jsonArgs[Arguments.PROCESS_ID]
            mailbox = self.get_mailbox(jsonArgs[Arguments.MAILBOX])
            if mailbox:
                self.processes[pid] = Process(pid, syncReceiver, syncSender, mailbox, format, messageLenght)
            else:
                self.logger.error(f"Error creating process, missing mailbox")

        else:
            self.logger.error(f"Adressing configuration not supported {addressing}")
        return isValid
    

    def process_receive(self, args):
        addressing = self.conf.get_addressing_configuration()
        isValid, jsonArgs = self.commandValidator.getReceiverArgs(args, addressing)
        if not isValid:
            self.logger.error(f"Receive not valid!!\n, not meeting requirements for addressing {addressing}")
            return
        if addressing == Addressing.DIRECT_EXPLICIT and self.process_exist(jsonArgs[Arguments.SENDER], jsonArgs[Arguments.RECEIVER], True):
            self.processes[jsonArgs[Arguments.RECEIVER]].receive_message(jsonArgs[Arguments.SENDER])
        
        elif (addressing == Addressing.DIRECT_IMPLICIT \
            or addressing == Addressing.INDIRECT_STATIC \
            or addressing == Addressing.INDIRECT_DYNAMIC) and \
            self.process_exist(jsonArgs[Arguments.RECEIVER]):
            self.processes[jsonArgs[Arguments.RECEIVER]].receive_message()   
        else:
            self.logger.error(f"Adressing configuration error {addressing}")
        return isValid

    def assign_mailbox_to_process(self, pid, mailbox_id):
        addressing = self.conf.get_addressing_configuration()
        if pid in self.processes and mailbox_id in self.mailboxes and addressing != Addressing.INDIRECT_STATIC:
            self.processes[pid].assign_mailbox(self.mailboxes[mailbox_id])
        else:
            self.logger.error(f"Invalid process, invalide mailbox ID or Adressing set to {addressing}.")

    def display_state(self): 
        self.display_processes_state()
        self.display_mailboxes_state()

    def display_processes_state(self):
        processes_status = []
        self.logger.info(f"\n**************** Process Status ****************")
        for process in self.processes:
            processes_status.append(self.processes[process].display_state())
        if len(processes_status) > 0:
            concatenated_df = pd.concat(processes_status, ignore_index=True)
            table = tabulate(concatenated_df, headers='keys', tablefmt='fancy_grid', showindex=False)
            self.logger.info(f"\n{table}")
        else:
            self.logger.error("There are no processes created")

    def display_mailboxes_state(self):
        for mailbox in self.mailboxes:
            self.logger.info(f"\n**************** Mailbox {mailbox} ****************")
            info, data = self.mailboxes[mailbox].display_state()
            info_table = tabulate(info, headers='keys', tablefmt='fancy_grid', showindex=False)
            data_table = tabulate(data, headers='keys', tablefmt='fancy_grid', showindex=False)
            self.logger.info(f"\nMailbox Information\n{info_table}\nMailbox Data\n{data_table}")

    def exit(self):
        for process in self.processes:
            self.processes[process].kill_thread()
        self.logger.info("Simulation Ended")
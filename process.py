
import time
import pandas as pd

from threading import Thread
from message import Message
from enum import Enum
from configuration import Synchronization, Format
from logger import Logger
from constants import PROCESS_LOGGER, DEFAULT_SENDER

class Operation(Enum):
    SEND = 1
    RECEIVE = 2
    INITIAL = 3

class Status(Enum):
    RUNNING = 1
    BLOCKED = 2

class Process():
    def __init__(self, pid, receiverSync, senderSync, mailbox, format, messageLenght=0):
        super().__init__()
        self.pid = pid
        self.mailbox = mailbox
        self.queue = None
        self.receiverSync = receiverSync
        self.senderSync = senderSync
        self.senderWaiting = False
        self.status = Status.RUNNING
        self.format = format
        self.waitingThread = None
        self.running = False
        self.messageLenght = messageLenght
        self.logger = Logger(PROCESS_LOGGER + "-" + pid) 

    def wait_for_message(self, sender=DEFAULT_SENDER):
        success = False
        self.running = True
        self.logger.info(f"Process {self.pid} started waiting for messages")
        while self.running:
            success = self.receive_onetime_message(sender)
            if success:
                self.logger.info("Wait for message in process " + self.pid + " is over")
                self.running = False
        self.manage_sync(Operation.RECEIVE, success)
        self.kill_thread()
        return success
    
    def manage_sync(self, operation, success=False):
        if self.senderSync == Synchronization.BLOCKING and operation == Operation.SEND:
            self.status = Status.BLOCKED
        elif self.senderSync == Synchronization.NONBLOCKING and operation == Operation.SEND:
            self.status = Status.RUNNING
        elif self.receiverSync == Synchronization.TEST_FOR_ARRIVAL and operation == Operation.RECEIVE:
            self.status = Status.RUNNING
        elif operation == Operation.RECEIVE and self.receiverSync == Synchronization.BLOCKING:
            if success:
                self.status = Status.RUNNING
                self.senderWaiting = False
            else:
                self.status = Status.BLOCKED
        elif operation == Operation.RECEIVE and self.receiverSync == Synchronization.NONBLOCKING:
            if not success and self.senderSync == Synchronization.BLOCKING and self.senderWaiting:
                self.status = Status.BLOCKED
            else:
                self.status = Status.RUNNING
                self.senderWaiting = False

        self.logger.info("Process " + self.pid + " current status " + str(self.status) + " after " + str(operation))

    def get_mailbox(self):
        if self.mailbox == None:
            self.logger.warning("Process " + self.pid + "don't have mailbox")
        return self.mailbox

    def assign_mailbox(self, mailbox):
        self.mailbox = mailbox

    def send_message(self, destination_pid, content, mailbox, priority):
        if self.status == Status.RUNNING:
            if self.mailbox: 
                message = Message(self.pid, destination_pid, content, priority)
                mailbox.send(message)
                self.logger.info(f"Message sent from process {self.pid} to {destination_pid}")
                self.manage_sync(Operation.SEND)
                if self.status == Status.BLOCKED:
                    self.senderWaiting = True
                    self.create_thread_for_receive(self.wait_for_message, destination_pid)
            else:
                self.logger.error("Process has no mailbox assigned.")
        else:
            self.logger.warning("Process ID " + self.pid + " is blocked and cannot process operation send")    

    def receive_onetime_message(self, sender=DEFAULT_SENDER):
        success = False
        if self.mailbox:
            message = self.mailbox.receive()
            if message and self.validateFormat(message, sender):
                success = True
                self.logger.info(f"Process {self.pid} received message from {message.source}: {message.content}")
        else:
            self.logger.error("Process has no mailbox assigned.")
        return success
    
    def validateFormat(self, message, sender=DEFAULT_SENDER):
        isValid = False
        if self.format == Format.FIXED_LENGTH:
            isValid = message.validateLenght(self.messageLenght)
        elif self.format == Format.VARIABLE_LENGTH:
            isValid = message.validateLenght(message.messageLenghtLimit)
        if not isValid:
            self.logger.info("Message with invalid format " + self.pid)
        if sender != DEFAULT_SENDER and (sender != message.source):
            isValid = False
            self.logger.info(f"Receiving in {self.pid}.\n Message no match between expected sender {sender} and message sender {message.source}.\n Ignoring message")
        return isValid

    def create_thread_for_receive(self,function, parameter):
        # create a new thread
        if self.waitingThread == None:
            self.waitingThread = Thread(target=function, args=(parameter,))
            self.waitingThread.start()
        else:
            self.logger.info(f"Process {self.pid} is already waiting for a message.")
    
    def kill_thread(self):
        self.waitingThread = None
        self.running = False
        self.logger.info(f"Thread for process {self.pid} killed")


    def receive_message(self, sender=DEFAULT_SENDER):
        if self.status == Status.RUNNING:
            success = False
            self.manage_sync(Operation.RECEIVE, success)
            if self.receiverSync == Synchronization.TEST_FOR_ARRIVAL or self.receiverSync == Synchronization.BLOCKING:
                self.create_thread_for_receive(self.wait_for_message, sender)
            else:
                success = self.receive_onetime_message(sender)
                self.manage_sync(Operation.RECEIVE, success)
        else:
            self.logger.warning("Process ID " + self.pid + " is blocked and cannot process operation receive")

    def display_state(self):
            data = {
                'PID': [self.pid],
                'Mailbox': [self.mailbox.id],
                'Status': [self.status.name],  # Convertir el enum a string
                'Format': [self.format.name],  # Convertir el enum a string
                'Lenght': [self.messageLenght],  # Convertir el enum a string
                'SenderWaiting': [self.senderWaiting]
            }
            df = pd.DataFrame(data)
            return df

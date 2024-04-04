
import time

from threading import Thread
from message import Message
from enum import Enum
from configuration import Synchronization, Format
from logger import Logger
from constants import PROCESS_LOGGER

class Operation(Enum):
    SEND = 1
    RECEIVE = 2
    INITIAL = 3

class Status(Enum):
    RUNNING = 1
    BLOCKED = 2

class Process():
    def __init__(self, pid, receiverSync, senderSync, format, messageLenght=0):
        super().__init__()
        self.pid = pid
        self.mailbox = None
        self.queue = None
        self.receiverSync = receiverSync
        self.senderSync = senderSync
        self.status = Status.RUNNING
        self.format = format
        self.waitingThread = None
        self.messageLenght = messageLenght
        self.logger = Logger(PROCESS_LOGGER + "-" + pid) 

    def wait_for_message(self):
        success = False
        running = True
        self.logger.info(f"Process {self.pid} started waiting for messages")
        while running:
            success = self.receive_onetime_message()
            if success:
                self.logger.info("Wait for message in process " + self.pid + " is over")
                running = False
        self.manage_sync(Operation.RECEIVE, success)
        self.kill_thread(self.wait_for_message)
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
            else:
                self.status = Status.BLOCKED
        elif operation == Operation.RECEIVE and self.receiverSync == Synchronization.NONBLOCKING:
            self.status = Status.RUNNING

        self.logger.info("Process " + self.pid + " current status " + str(self.status) + " after " + str(operation))

    def get_mailbox(self):
        if self.mailbox == None:
            self.logger.warning("Process " + self.pid + "don't have mailbox")
        return self.mailbox

    def assign_mailbox(self, mailbox):
        self.mailbox = mailbox

    def send_message(self, destination_pid, content, mailbox, priority=0):
        if self.status == Status.RUNNING:
            if self.mailbox: 
                # Agrega prioridad
                message = Message(self.pid, destination_pid, content, priority)
                mailbox.send(message)
                self.logger.info(f"Message sent from process {self.pid} to {destination_pid}")
                self.manage_sync(Operation.SEND)
                if self.status == Status.BLOCKED:
                    self.create_thread_for_receive(self.wait_for_message)
            else:
                self.logger.error("Process has no mailbox assigned.")
        else:
            self.logger.warning("Process ID " + self.pid + " is blocked and cannot process operation send")    

    def receive_onetime_message(self):
        success = False
        if self.mailbox:
            message = self.mailbox.receive()
            if message and self.validateFormat(message):
                success = True
                self.logger.info(f"Process {self.pid} received message from {message.source}: {message.content}")
        else:
            self.logger.error("Process has no mailbox assigned.")
        return success
    
    def validateFormat(self, message):
        isValid = False
        if self.format == Format.FIXED_LENGTH:
            isValid = message.validateLenght(self.messageLenght)
        elif self.format == Format.VARIABLE_LENGTH:
            isValid = message.validateLenght(message.messageLenghtLimit)
        if not isValid:
            self.logger.info("Message with invalid format " + self.pid)
        return isValid

    def create_thread_for_receive(self,function):
        # create a new thread
        if self.waitingThread == None:
            self.logger.info("Creating thread for function " + str(function))
            self.waitingThread = Thread(target=function)
            self.waitingThread.start()
    
    def kill_thread(self, function):
        self.waitingThread = None
        self.logger.info("Thread for function " + str(function) + " killed")


    def receive_message(self):
        if self.status == Status.RUNNING:
            success = False
            self.manage_sync(Operation.RECEIVE, success)
            if self.receiverSync == Synchronization.TEST_FOR_ARRIVAL:
                self.create_thread_for_receive(self.wait_for_message)
            else:
                success = self.receive_onetime_message()
                self.manage_sync(Operation.RECEIVE, success)
        else:
            self.logger.warning("Process ID " + self.pid + " is blocked and cannot process operation receive")
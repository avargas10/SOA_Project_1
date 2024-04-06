import time
import pandas as pd
import sys

from threading import Thread
from message import Message
from enum import Enum
from configuration import Synchronization, Format
from logger import Logger
from logViewer import LogViewer
from constants import PROCESS_LOGGER, DEFAULT_SENDER

class Operation(Enum):
    """
    Enumeración para representar operaciones de procesamiento.
    """
    SEND = 1
    RECEIVE = 2
    INITIAL = 3

class Status(Enum):
    """
    Enumeración para representar estados de un proceso.
    """
    RUNNING = 1
    BLOCKED = 2

class Process():
    """
    Clase para representar un proceso.

    Attributes:
    - pid (str): Identificador del proceso.
    - receiverSync (Synchronization): Sincronización del receptor.
    - senderSync (Synchronization): Sincronización del emisor.
    - mailbox (CustomMailbox): Buzón asociado al proceso.
    - format (Format): Formato de los mensajes.
    - messageLenght (int): Longitud del mensaje (por defecto 0).
    """
    def __init__(self, pid, receiverSync, senderSync, mailbox, format, messageLenght=0):
        """
        Inicializa un objeto de proceso.

        Parámetros:
        - pid (str): Identificador del proceso.
        - receiverSync (Synchronization): Sincronización del receptor.
        - senderSync (Synchronization): Sincronización del emisor.
        - mailbox (CustomMailbox): Buzón asociado al proceso.
        - format (Format): Formato de los mensajes.
        - messageLenght (int): Longitud del mensaje (por defecto 0).
        """
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
        self.logPath = PROCESS_LOGGER + "-" + pid
        self.logViewer = None
        self.logger = Logger(self.logPath) 

    def wait_for_message(self, sender=DEFAULT_SENDER):
        """
        Espera un mensaje en el buzón asociado al proceso.

        Parámetros:
        - sender (str): Identificador del remitente (por defecto DEFAULT_SENDER).

        Returns:
        - bool: True si se recibió el mensaje correctamente, False si no.
        """
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
        """
        Gestiona la sincronización del proceso.

        Parámetros:
        - operation (Operation): Operación realizada por el proceso.
        - success (bool): Éxito de la operación (por defecto False).
        """
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
        """
        Obtiene el buzón asociado al proceso.

        Returns:
        - CustomMailbox: Buzón asociado al proceso.
        """
        if self.mailbox == None:
            self.logger.warning("Process " + self.pid + "don't have mailbox")
        return self.mailbox

    def assign_mailbox(self, mailbox):
        """
        Asigna un buzón al proceso.

        Parámetros:
        - mailbox (CustomMailbox): Buzón a asignar al proceso.
        """
        self.mailbox = mailbox

    def send_message(self, destination_pid, content, mailbox, priority):
        """
        Envía un mensaje al buzón asociado al proceso.

        Parámetros:
        - destination_pid (str): Identificador del proceso destino.
        - content (str): Contenido del mensaje.
        - mailbox (CustomMailbox): Buzón asociado al proceso.
        - priority (int): Prioridad del mensaje.
        """
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
        """
        Recibe un mensaje del buzón asociado al proceso.

        Parámetros:
        - sender (str): Identificador del remitente (por defecto DEFAULT_SENDER).

        Returns:
        - bool: True si se recibió el mensaje correctamente, False si no.
        """
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
        """
        Valida el formato del mensaje recibido.

        Parámetros:
        - message (Message): Mensaje a validar.
        - sender (str): Identificador del remitente (por defecto DEFAULT_SENDER).

        Returns:
        - bool: True si el mensaje es válido, False si no.
        """
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
        """
        Crea un hilo para esperar un mensaje.

        Parámetros:
        - function (function): Función a ejecutar en el hilo.
        - parameter: Parámetro de la función.
        """
        if self.waitingThread == None:
            self.waitingThread = Thread(target=function, args=(parameter,))
            self.waitingThread.start()
        else:
            self.logger.info(f"Process {self.pid} is already waiting for a message.")
    
    def kill_thread(self):
        """Detiene el hilo de espera."""
        self.waitingThread = None
        self.running = False
        self.logger.info(f"Thread for process {self.pid} killed")


    def receive_message(self, sender=DEFAULT_SENDER):
        """
        Recibe un mensaje del buzón asociado al proceso.

        Parámetros:
        - sender (str): Identificador del remitente (por defecto DEFAULT_SENDER).
        """
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
        """
        Muestra el estado del proceso.

        Returns:
        - DataFrame: DataFrame con el estado del proceso.
        """
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

    def display_live(self):
        self.logViewer = LogViewer(self.logPath,f"Process-{self.pid}")
        self.logViewer.run()
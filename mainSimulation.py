import pandas as pd


from customMailbox import CustomMailbox, MailboxTypes
from process import Process
from logger import Logger
from configuration import Configuration
from commandValidator import CommandValidator, Arguments
from configuration import Addressing
from tabulate import tabulate

class Simulation:
    def __init__(self, configFile):
        """
        Inicializa la simulación con la configuración proporcionada.

        Parámetros:
        - conf: Configuración de la simulación.
        """
        self.processes = {}
        self.mailboxes = {}
        self.conf = Configuration(configFile)
        self.logger = Logger("MainSimulation", True, True)
        self.commandValidator = CommandValidator()
        config_table = self.conf.to_dataframe()
        config_table = tabulate(config_table, headers='keys', tablefmt='fancy_grid', showindex=False)
        self.logger.info(f"Simulation Actual Configuration\n{config_table}")

    def get_conf(self):
        """ 
        Obtiene la configuración de la simulación.
        
        Salida:
        - conf: Configuración de la simulación.
        """
        return self.conf

    def create_process(self, args):        
        """
        Crea un proceso en la simulación.

        Parámetros:
        - args: Argumentos para la creación del proceso.
        """
        if len(self.processes) >= self.conf.get_max_processes_configuration():
            # Log a message saying the max number of processes is reached
            self.logger.error("Maximum number of processes reached. Cannot create more processes.")
            return
        syncSender = self.conf.get_sync_sender_configuration()
        syncReceiver = self.conf.get_sync_receiver_configuration()
        format, messageLength = self.conf.get_format_configuration()
        addressing = self.conf.get_addressing_configuration()
        self.validate_create_process(args, addressing, syncReceiver, syncSender, format, messageLength)

    def create_mailbox(self, mailbox_id):
        """
        Crea un buzón en la simulación.

        Parámetros:
        - mailbox_id: Identificador del buzón.
        
        Salida:
        - new_mailbox: Buzón creado.
        """
        mailboxSize = self.conf.get_queue_size_configuration()
        mailboxDispline = self.conf.get_queue_discipline_configuration()
        new_mailbox = CustomMailbox(mailbox_id, mailboxSize, MailboxTypes.QUEUE, mailboxDispline)
        self.mailboxes[mailbox_id] = new_mailbox
        return new_mailbox

    def process_send(self, args):
        """
        Envía un mensaje desde un proceso.

        Parámetros:
        - args: Argumentos para el envío del mensaje.
        
        Salida:
        - isValid: Indica si los argumentos son válidos.
        """
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
        """
        Comprueba si un proceso existe en la simulación.

        Parámetros:
        - sender: ID del proceso.
        - receiver: ID del proceso receptor.
        - validateReceiver: Booleano que indica si se debe validar el receptor.

        Salida:
        - exist: Indica si el proceso existe.
        """
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
        """
        Obtiene un buzón de la simulación.

        Parámetros:
        - mailbox: ID del buzón.

        Salida:
        - found_mailbox: Buzón encontrado.
        """
        found_mailbox = self.mailboxes.get(mailbox)
        if found_mailbox is None:
            self.logger.error(f"Mailbox {mailbox} not found")
        return found_mailbox
    
    def get_process(self, process):
        """
        Obtiene un proceso de la simulación.

        Parámetros:
        - process: ID del proceso.

        Salida:
        - found_process: Proceso encontrado.
        """
        found_process = self.processes.get(process)
        if found_process is None:
            self.logger.error(f"Process {process} not found")
        return found_process

    def validate_create_process(self, args, addressing, syncReceiver, syncSender, format, messageLength):
        """
        Valida y crea un proceso en la simulación.

        Parámetros:
        - args: Argumentos para la creación del proceso.
        - addressing: Tipo de direccionamiento.
        - syncReceiver: Configuración de sincronización del receptor.
        - syncSender: Configuración de sincronización del emisor.
        - format: Formato del mensaje.
        - messageLength: Longitud del mensaje.
        """
        isValid, jsonArgs = self.commandValidator.getCreateProcessArgs(args, addressing)
        if not isValid:
            self.logger.error(f"Receive not valid!!\n, not meeting requirements for addressing {addressing}")
            return
        if addressing == Addressing.DIRECT_EXPLICIT or addressing == Addressing.DIRECT_IMPLICIT:
                pid = jsonArgs[Arguments.PROCESS_ID]
                mailbox = self.create_mailbox("process_" + str(pid))
                self.processes[pid] = Process(pid, syncReceiver, syncSender, mailbox, format, messageLength)
        
        elif addressing == Addressing.INDIRECT_STATIC \
            or addressing == Addressing.INDIRECT_DYNAMIC:
            pid = jsonArgs[Arguments.PROCESS_ID]
            mailbox = self.get_mailbox(jsonArgs[Arguments.MAILBOX])
            if mailbox:
                self.processes[pid] = Process(pid, syncReceiver, syncSender, mailbox, format, messageLength)
            else:
                self.logger.error(f"Error creating process, missing mailbox")

        else:
            self.logger.error(f"Adressing configuration not supported {addressing}")
        return isValid
    

    def process_receive(self, args):
        """
        Recibe un mensaje en un proceso.

        Parámetros:
        - args: Argumentos para la recepción del mensaje.

        Salida:
        - isValid: Indica si los argumentos son válidos.
        """
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
        """
        Asigna un buzón a un proceso.

        Parámetros:
        - pid: ID del proceso.
        - mailbox_id: ID del buzón.
        """
        addressing = self.conf.get_addressing_configuration()
        if pid in self.processes and mailbox_id in self.mailboxes and addressing != Addressing.INDIRECT_STATIC:
            self.processes[pid].assign_mailbox(self.mailboxes[mailbox_id])
        else:
            self.logger.error(f"Invalid process, invalide mailbox ID or Adressing set to {addressing}.")

    def display_live(self):
        for process in self.processes:
            self.processes[process].display_live()
        for mailbox in self.mailboxes:
            self.mailboxes[mailbox].display_live()
    
    def display_state(self): 
        """
        Muestra el estado actual de la simulación.
        """
        self.display_processes_state()
        self.display_mailboxes_state()

    def display_processes_state(self):
        """
        Muestra el estado actual de los procesos en la simulación.
        """
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
        """
        Muestra el estado actual de los buzones en la simulación.
        """
        for mailbox in self.mailboxes:
            
            info, data = self.mailboxes[mailbox].display_state()
            info_table = tabulate(info, headers='keys', tablefmt='fancy_grid', showindex=False)
            data_table = tabulate(data, headers='keys', tablefmt='fancy_grid', showindex=False)
            self.logger.info(f"\n**************** Mailbox {mailbox} ****************" +
                             f"\nMailbox Information\n{info_table}\nMailbox Data\n{data_table}")

    def exit(self):
        """
        Termina la simulación.
        """
        for process in self.processes:
            self.processes[process].kill_thread()
        self.logger.info("Simulation Ended")
    
    def reset(self, configFile):
        self.exit()
        self.processes = {}
        self.mailboxes = {}
        self.conf = Configuration(configFile)
        self.commandValidator = CommandValidator()
        # self.logger = Logger("MainSimulation", True, True)
        config_table = self.conf.to_dataframe()
        config_table = tabulate(config_table, headers='keys', tablefmt='fancy_grid', showindex=False)
        self.logger.info(f"Simulation New Configuration\n{config_table}")
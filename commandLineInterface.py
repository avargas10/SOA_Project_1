class CommandLineInterface:
    def __init__(self, simulation):
        """Inicializa la interfaz de línea de comandos con la simulación proporcionada."""
        self.simulation = simulation

    def start(self):
        """Comienza la interfaz de línea de comandos."""
        print("Welcome to the Command Line Interface.")
        print("Type 'help' for a list of available commands.")

        while True:
            command = input("> ")
            self.execute_command(command)

    def run_tests(self, tests_file):
        with open(tests_file, 'r') as file:
            for line in file:
                self.execute_command(line.strip())

    def execute_command(self, command):
        """Ejecuta el comando proporcionado por el usuario."""
        parts = command.split()
        if not parts:
            return

        command_name = parts[0]
        args = parts[1:]

        if command_name == 'create_process':
            pid = args[0]
            self.simulation.create_process(pid)
        elif command_name == 'create_mailbox':
            mailbox_id = args[0]
            self.simulation.create_mailbox(mailbox_id)
        elif command_name == 'assign_mailbox':
            pid = args[0]
            mailbox_id = args[1]
            self.simulation.assign_mailbox_to_process(pid, mailbox_id)
        elif command_name == 'send_message':
            sender_pid = args[0]
            receiver_pid = args[1]
            priority = 0  # 0 por default
            
            # Revisamos si pasaron prioridad o no
            if args[-1].isdigit():
                priority = int(args.pop())  # sacamos el argumento
                
            content = ' '.join(args[2:])
            mailbox = self.simulation.processes[receiver_pid].get_mailbox()
            
            # enviamos con prioridad
            self.simulation.processes[sender_pid].send_message(receiver_pid, content, mailbox, priority)
        elif command_name == 'receive_message':
            pid = args[0]
            self.simulation.processes[pid].receive_message()
        elif command_name == 'display_state':
            self.simulation.display_state()
        elif command_name == 'run_test':
            test_file_path = args[0]
            self.run_tests(test_file_path)
        elif command_name == 'help':
            self.display_help()
        elif command_name == 'exit':
            print("Exiting...")
            exit()
        else:
            print("Invalid command. Type 'help' for a list of available commands.")

    def display_help(self):
        """Muestra la lista de comandos disponibles."""
        print("Available commands:")
        print("create_process <pid>")
        print("create_mailbox <mailbox_id>")
        print("assign_mailbox <pid> <mailbox_id>")
        print("send_message <sender_pid> <receiver_pid> <content>")
        print("receive_message <pid>")
        print("display_state")
        print("help")
        print("exit")


# SOA_Project_1
Simulation of inter-process communication using message passing. CLI allows process creation, message exchange, and system state visualization. Educational tool for understanding OS fundamentals.

# Inter-Process Communication Simulation

This project simulates inter-process communication using a CommandLineInterface. It allows users to create processes, message exchange, and visualize system state.

##Configuration

Before starting, the system must be configured by editing the config.txt file. This file allows adjusting various parameters:

`SynchronizationSender`=BLOCKING|NONBLOCKING|TEST_FOR_ARRIVAL
`SynchronizationReceiver`=BLOCKING|NONBLOCKING|TEST_FOR_ARRIVAL
`Addressing`=DIRECT_EXPLICIT|DIRECT_IMPLICIT|INDIRECT_STATIC|INDIRECT_DYNAMIC
`Format`=FIXED_LENGTH|VARIABLE_LENGTH
`MessageLength`=<number>
`QueueDiscipline`=FIFO|PRIORITY
`MaxProcesses`=<number>

## Usage

To run the simulation, execute `main.py`. This will launch the CommandLineInterface, where you can interact with the simulated system via commands.

## CommandLineInterface Commands

- `create_process <pid>`: Create a new process with the specified ID.
- `create_mailbox <mailbox_id>`: Create a new mailbox with the specified ID.
- `assign_mailbox <pid> <mailbox_id>`: Assign a mailbox to a process.
- `send_message <sender_pid> <receiver_pid> <content>`: Send a message from one process to another.
- `receive_message <pid>`: Receive a message for the specified process.
- `display_state`: Display the current state of the system.
- `help`: Display available commands.
- `exit`: Exit the simulation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

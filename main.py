from mainSimulation import Simulation
from commandLineInterface import CommandLineInterface
from configuration import Configuration

if __name__ == "__main__":
    conf_file_path = "tests/test1.conf"  # Ruta del archivo .conf
    simulation = Simulation(conf_file_path)
    cli = CommandLineInterface(simulation)
    cli.start()
    # cli.run_tests("tests/test1.txt")
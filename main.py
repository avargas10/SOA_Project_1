from mainSimulation import Simulation
from commandLineInterface import CommandLineInterface


if __name__ == "__main__":
    simulation = Simulation()
    cli = CommandLineInterface(simulation)
    cli.run_tests("tests/test1.txt")
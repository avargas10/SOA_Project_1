import logging
import sys
import os
#run_test tests/test1.txt

from constants import LOGS_PATH
from datetime import datetime
import shutil

class Logger:
    def __init__(self, loggerName, printConsole=False, clean=False):
        if clean:
            self.clean_logs()
        self.loggerName = loggerName
        self.filename = LOGS_PATH + self.loggerName + ".log"
        self.logger = logging.getLogger(self.filename)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Configurar el manejador de archivos para escribir en el archivo de registro
        file_handler = logging.FileHandler(self.filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

        # Configurar el manejador de consola para imprimir en la consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.ERROR)
        if printConsole:
            console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def info(self, message):
        self.logger.info(message)
    
    def clean_logs(self):
        shutil.rmtree(LOGS_PATH)
        os.mkdir(LOGS_PATH)

    def close(self):
        # Limpiar los manejadores de registro
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

# Ejemplo de uso:
if __name__ == "__main__":
    # Crear un objeto Logger para un archivo específico
    logger = Logger("process-1")

    # Ejemplo de registro de mensajes con diferentes niveles de urgencia
    logger.error("Esto es un mensaje de error")
    logger.warning("Esto es un mensaje de advertencia")
    logger.info("Esto es un mensaje informativo")

    # Cerrar el Logger al finalizar
    logger.close()

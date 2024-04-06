import tkinter as tk
from tkinter import scrolledtext
from constants import LOGS_PATH
import threading
import time

class LogViewer:
    def __init__(self, file_path, name):
        self.file_path = LOGS_PATH + file_path + ".log"
        self.running = False
        self.root = tk.Tk()
        self.root.title(f"Log Viewer {name}")
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Captura el evento de cierre de la ventana

    def start(self):
        self.running = True
        self.read_thread = threading.Thread(target=self._read_log, daemon=True)
        self.read_thread.start()
        self.root.mainloop()  # Ejecuta el bucle principal de Tkinter en el hilo principal

    def stop(self):
        self.running = False

    def on_close(self):
        self.stop()  # Detiene la lectura del archivo de registro
        self.root.destroy()  # Cierra la ventana

    def _update_text(self):
        while self.running:
            time.sleep(0.01)
            self.text_area.update()

    def _read_log(self):
        with open(self.file_path, 'r') as file:
            while self.running:
                line = file.readline()
                if line:
                    self.text_area.insert(tk.END, line)
                    self.text_area.yview(tk.END)  # Auto-scroll to the bottom
                else:
                    time.sleep(0.1)

    def run(self):
        self.start()  # Este método ahora inicia el bucle principal de Tkinter en el hilo principal
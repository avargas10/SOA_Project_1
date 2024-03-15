class MessageQueue:
    def __init__(self):
        self.queue = []

    def add_message(self, message):
        """Agrega un mensaje a la cola."""
        self.queue.append(message)

    def get_message(self):
        """Obtiene y elimina el mensaje más antiguo de la cola (FIFO)."""
        if self.queue:
            return self.queue.pop(0)
        else:
            return None

    def is_empty(self):
        """Devuelve True si la cola está vacía, False de lo contrario."""
        return len(self.queue) == 0
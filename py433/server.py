import logging
from socket import (
    AF_INET,
    SOCK_STREAM,
    socket
)

from . import defaults


class server:

    def __init__(self, host='localhost', port=defaults.port, handler=lambda x: print(x)):
        self.host = host
        self.port = port
        self.handler = handler

    def run(self):
        logging.debug("Server listening on '" + str(self.port) + "'")
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.running = True

        while self.running:
            connection = None
            try:
                connection, client_address = self.sock.accept()
            except OSError as e:
                if self.running:
                    raise e

            try:
                data = b''
                while self.running:
                    buffer = connection.recv(256)
                    if buffer:
                        data += buffer
                    else:
                        break
                content = data.decode("utf-8", "strict")
                logging.debug("Received '" + content + "'")
                self.handler(content)
            finally:
                if connection:
                    connection.close()

    def stop(self):
        self.running = False
        self.sock.shutdown(2)
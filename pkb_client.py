import socket
import pickle

ip = "192.168.1.241"

class PiClient:
    def __init__(self, ip, port):
        self.HEADER = 64
        self.PORT = port
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SHUTDOWN_MESSAGE = "!SHUTDOWN"
        self.SERVER = ip
        self.ADDR = (self.SERVER, self.PORT)

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

    def send(self, msg):
        message = pickle.dumps(msg)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def disconnect(self):
        self.send(self.DISCONNECT_MESSAGE)

    def shutdown(self):
        self.send(self.SHUTDOWN_MESSAGE)
    
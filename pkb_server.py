import socket
import threading
import pickle

class PiServer:
    def __init__(self):
        self.HEADER = 64
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SHUTDOWN_MESSAGE = "!SHUTDOWN"

        self.run_server = True

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.ADDR)

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = pickle.loads(conn.recv(msg_length))
                if msg == self.DISCONNECT_MESSAGE:
                    connected = False
                if msg == self.SHUTDOWN_MESSAGE:
                    self.run_server = False
                    connected = False
                
                print(f"[{addr}] {msg}")
            
        conn.close()

    def shutDown(self):
        print("[SHUTTING DOWN] server is shutting down...")
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        print("[SHUTTING DOWN] shut down complete.")

    def start(self):
        print("[STARTING] server is starting...")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while self.run_server:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        self.shutDown()



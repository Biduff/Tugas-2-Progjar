from socket import *
import socket
import threading
import logging
from datetime import datetime
import pytz

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            data = self.connection.recv(32).decode('utf-8')
            if not data:
                break
                
            logging.info(f"Recv {self.address}: {data.strip()}")
            
            if data == "TIME\r\n":
                wib = pytz.timezone('Asia/Jakarta')
                current_time = datetime.now(wib).strftime("%H:%M:%S")
                self.connection.sendall(f"JAM {current_time}\r\n".encode())
                logging.info(f"Sent {self.address}: JAM {current_time}")
            
            elif data == "SCRIPT TEST\r\n":
                self.connection.sendall(b"SCRIPT OK\r\n")
                logging.info(f"Sent {self.address}: SCRIPT OK")
            
            elif data == "QUIT\r\n":
                self.connection.close()
                logging.info(f"Closed {self.address}")
                break
            
            else:
                self.connection.sendall(b"INVALID\r\n")

        self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.clients = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.sock.bind(('172.16.16.101', 45000))
        self.sock.listen(5)
        logging.info("Server ready on 172.16.16.101:45000")
        while True:
            conn, addr = self.sock.accept()
            logging.info(f"New connection: {addr}")
            client = ProcessTheClient(conn, addr)
            client.start()
            self.clients.append(client)

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        handlers=[logging.StreamHandler()]
    )
    Server().start()

if __name__ == "__main__":
    main()
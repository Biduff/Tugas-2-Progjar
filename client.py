import socket
import time
from datetime import datetime, timedelta
import pytz
import threading

def format_time():
    return datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")

def script_test(sock):
    start = datetime.now()
    end = start + timedelta(minutes=3)
    
    now = datetime.now()
    next_15 = (now + timedelta(seconds=15)).replace(second=0, microsecond=0)
    while next_15.second % 15 != 0:
        next_15 += timedelta(seconds=15)
    
    delay = (next_15 - now).total_seconds()
    print(f"\nFirst msg in {delay:.0f}s")
    
    while datetime.now() < end:
        now = datetime.now()
        if now.second % 15 == 0:
            sock.sendall(b"SCRIPT TEST\r\n")
            resp = sock.recv(32).decode().strip()
            print(f"[{format_time()}] SCRIPT: {resp}")
            time.sleep(1)  
        time.sleep(0.1)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('172.16.16.101', 45000))
        print("Connected to server")
        
        while True:
            print("\n1. TIME\n2. SCRIPT TEST\n3. QUIT")
            cmd = input("Choose: ")
            
            if cmd == '1':
                sock.sendall(b"TIME\r\n")
                print(f"[{format_time()}] TIME: {sock.recv(32).decode().strip()}")
            
            elif cmd == '2':
                thread = threading.Thread(target=script_test, args=(sock,))
                thread.daemon = True
                thread.start()
                thread.join(timeout=180)
            
            elif cmd == '3':
                sock.sendall(b"QUIT\r\n")
                print("Disconnected")
                break
                
    finally:
        sock.close()

if __name__ == "__main__":
    main()
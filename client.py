from socket import *
import time
import psutil
import sys
from cryptography.fernet import Fernet

KEY = b'gZuGeUfiriA6avdQMY1zq_8BxBD5Gb0WBdWQszsWJcg='
f = Fernet(KEY)

server = ("192.168.137.1", 1000)

clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.settimeout(5)
clientSocket.connect(server)

client_id = sys.argv[1]

try:
    while(True):
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        netio = psutil.net_io_counters().bytes_sent
        loadAvg = psutil.getloadavg()[0]
        
        message = f"{client_id}||{cpu:.2f}||{memory:.2f}||{disk:.2f}||{netio}||{loadAvg:.2f}"

        encrypted_message = f.encrypt(message.encode())
        clientSocket.sendto(encrypted_message, server)

        try:
            encrypted_response, _ = clientSocket.recvfrom(2048)
            try:
                decrypted_response = f.decrypt(encrypted_response)
                print(decrypted_response.decode())
            except Exception:
                print("Decryption failed (tampered data)")
        except timeout:
            print("No alert from the server")

        time.sleep(5)

except KeyboardInterrupt:
    print("Client closing the connection")

clientSocket.close()

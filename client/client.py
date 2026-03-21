from socket import *
import time
import psutil
import sys
from dtls import do_patch
do_patch()
import ssl

serverName = "192.168.137.1"
serverPort = 1000

clientSocket = socket(AF_INET, SOCK_DGRAM)
context = ssl.SSLContext(ssl.PROTOCOL_DTLSv1)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = False
context.load_verify_locations("server-cert.pem")
secureSocket = context.wrap_socket(clientSocket)

secureSocket.settimeout(5)
secureSocket.connect((serverName, serverPort))

client_id = sys.argv[1]

try:
    while(True):
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        netio = psutil.net_io_counters().bytes_sent
        loadAvg = psutil.getloadavg()[0]
        
        message = f"{client_id}||{cpu:.2f}||{memory:.2f}||{disk:.2f}||{netio}||{loadAvg:.2f}"

        secureSocket.sendto(message.encode())

        try:
            modifiedMessage = secureSocket.recvfrom(2048)
            print(modifiedMessage.decode())
        except timeout:
            print("No alert from the server")

        time.sleep(5)

except KeyboardInterrupt:
    print("Client closing the connection")

clientSocket.close()

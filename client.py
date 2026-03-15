from socket import *
import time
import psutil
import sys

serverName = "localhost"
serverPort = 1000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(3) # incase the reply is not sent back within 3 seconds, it is timed out
client_id = sys.argv[1]

try: 
    while(True):
        cpu = psutil.cpu_percent(interval=1) # interval means : measures CPU usage over 1 second
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        message = f"{client_id}||{cpu:.2f}||{memory:.2f}||{disk:.2f}"
        clientSocket.sendto(message.encode(),(serverName, serverPort))

        try:
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            print(modifiedMessage.decode())
        except timeout:
            print("No alert from the server")

        time.sleep(5)

except KeyboardInterrupt:
    print("Client closing the connection")

clientSocket.close()
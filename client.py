from socket import *
import time
import psutil
import sys

serverName = "localhost"
serverPort = 1000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(3)

client_id = sys.argv[1]

try:
    while(True):
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        netio = psutil.net_io_counters().bytes_sent
        loadAvg = psutil.getloadavg()[0]

        temps = psutil.sensors_temperatures()
        temp = 0
        if temps:
            first = list(temps.values())[0]
            temp = first[0].current

        message = f"{client_id}||{cpu:.2f}||{memory:.2f}||{disk:.2f}||{netio}||{loadAvg:.2f}||{temp:.2f}"

        clientSocket.sendto(message.encode(), (serverName, serverPort))

        try:
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            print(modifiedMessage.decode())
        except timeout:
            print("No alert from the server")

        time.sleep(5)

except KeyboardInterrupt:
    print("Client closing the connection")

clientSocket.close()

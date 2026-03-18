from socket import *
import time
import psutil
import sys

serverName = "192.168.137.1"
serverPort = 5000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(3)

client_id = sys.argv[1]

try:
    while True:
        # Collect system metrics
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        # Network usage (per interval)
        net1 = psutil.net_io_counters().bytes_sent
        time.sleep(1)
        net2 = psutil.net_io_counters().bytes_sent
        netio = net2 - net1

        # Load average (safe for Windows)
        try:
            loadAvg = psutil.getloadavg()[0]
        except:
            loadAvg = 0.0

        message = f"{client_id}||{cpu:.2f}||{memory:.2f}||{disk:.2f}||{netio}||{loadAvg:.2f}"

        # 🔥 LATENCY MEASUREMENT START
        start_time = time.time()

        clientSocket.sendto(message.encode(), (serverName, serverPort))

        try:
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

            end_time = time.time()
            latency = (end_time - start_time) * 1000  # ms

            print(f"{modifiedMessage.decode()} | Latency: {latency:.2f} ms")

        except timeout:
            print("No response from server (packet loss)")

        time.sleep(.5)

except KeyboardInterrupt:
    print("Client closing the connection")

clientSocket.close()
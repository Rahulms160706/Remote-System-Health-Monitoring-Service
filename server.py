from socket import *

serverPort = 1000
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(("", serverPort))
print("The server is ready to receive")

cpu_threshold = 80
memory_threshold = 85
disk_threshold = 90
load_threshold = 2.0
temp_threshold = 80

try:
    while(True):
        message, clientAddress = serverSocket.recvfrom(2048)

        node, cpu, memory, disk, netio, loadavg, temp = message.decode().split("||")

        cpu = float(cpu)
        memory = float(memory)
        disk = float(disk)
        netio = float(netio)
        loadavg = float(loadavg)
        temp = float(temp)

        print(f"{node} | CPU:{cpu}% MEM:{memory}% DISK:{disk}% LOAD:{loadavg} TEMP:{temp}")

        if cpu > cpu_threshold:
            modifiedMessage = f"ALERT : CPU for {node} crossed threshold"
        
        elif memory > memory_threshold:
            modifiedMessage = f"ALERT : Memory for {node} crossed threshold"
        
        elif disk > disk_threshold:
            modifiedMessage = f"ALERT : Disk for {node} crossed threshold"
        
        elif loadavg > load_threshold:
            modifiedMessage = f"ALERT : Load average high for {node}"
        
        elif temp > temp_threshold:
            modifiedMessage = f"ALERT : Temperature high for {node}"
        
        else:
            modifiedMessage = f"{node} is running normally"

        serverSocket.sendto(modifiedMessage.encode(), clientAddress)

except KeyboardInterrupt:
    print("\nServer is shutting down")

finally:
    serverSocket.close()

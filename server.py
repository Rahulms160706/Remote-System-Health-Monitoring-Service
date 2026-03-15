from socket import *

serverPort = 1000
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(("", serverPort))
print("The server is ready to receive")

cpu_threshold = 80
memory_threshold = 85
disk_threshold = 90

try:
    while(True):
        message, clientAddress = serverSocket.recvfrom(2048) # 2048 means the maximum data in bytes from incoming packet
        node, cpu, memory, disk = message.decode().split("||")
        cpu = float(cpu)
        memory = float(memory)
        disk = float(disk)
        print(f"Received from {node} : CPU = {cpu}, Memory = {memory}, Disk = {disk}")

        if(cpu > cpu_threshold):
            modifiedMessage = f"ALERT : CPU for {node} has crossed the threshold"
        elif(memory > memory_threshold):
            modifiedMessage = f"ALERT : Memory for {node} has crossed the threshold"
        elif(disk > disk_threshold):
            modifiedMessage = f"ALERT : Disk for {node} has crossed the threshold"
        else:
            modifiedMessage = f"{node} is running normally"
        
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)

except KeyboardInterrupt:
    print("\nServer is shutting down")

finally: # makes sure no matter whether keyboard interrupt is there or an exception, it will exit
    serverSocket.close()
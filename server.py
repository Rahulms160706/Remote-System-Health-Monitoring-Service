from time import *
from socket import *
import psutil
from dtls import do_patch
do_patch()
import ssl

serverPort = 1000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

context = ssl.SSLContext(ssl.PROTOCOL_DTLSv1)
context.load_cert_chain(certfile = "server-cert.pem", keyfile = "server-key.pem")

secureSocket = context.wrap_socket(serverSocket, server_side=True)

total_request = 0
start_time = time()
latencies = []

print("DTLS server is ready to receive")

cpu_threshold = 80
memory_threshold = 85
disk_threshold = 90
load_threshold = 2.0

try:
    while(True):
        request_start = time()
        message, clientAddress = secureSocket.recvfrom(2048)

        total_request += 1

        node, cpu, memory, disk, netio, loadavg = message.decode().split("||")

        cpu = float(cpu)
        memory = float(memory)
        disk = float(disk)
        netio = float(netio)
        loadavg = float(loadavg)

        print(f"{node} | CPU:{cpu}% MEM:{memory}% DISK:{disk}% LOAD:{loadavg}")

        if cpu > cpu_threshold:
            modifiedMessage = f"ALERT : CPU for {node} crossed threshold"
        
        elif memory > memory_threshold:
            modifiedMessage = f"ALERT : Memory for {node} crossed threshold"
        
        elif disk > disk_threshold:
            modifiedMessage = f"ALERT : Disk for {node} crossed threshold"
        
        elif loadavg > load_threshold:
            modifiedMessage = f"ALERT : Load average high for {node}"
        
        else:
            modifiedMessage = f"{node} is running normally"

        secureSocket.sendto(modifiedMessage.encode(), clientAddress)

        request_end = time()
        latencies.append(request_end - request_start)

        if total_request % 10 == 0:
            elapsed = time() - start_time
            throughput = total_request / elapsed
            avg_latency = sum(latencies) / len(latencies)
            server_cpu = psutil.cpu_percent()
            server_mem = psutil.virtual_memory().percent

            print("\n--- SERVER PERFORMANCE ---")
            print(f"Requests handled: {total_request}")
            print(f"Throughput: {throughput:.2f} req/sec")
            print(f"Avg Latency: {avg_latency:.4f} sec")
            print(f"Server CPU: {server_cpu}%")
            print(f"Server Memory: {server_mem}%")
            print("--------------------------\n")

except KeyboardInterrupt:
    print("\nServer is shutting down")

finally:
    serverSocket.close()

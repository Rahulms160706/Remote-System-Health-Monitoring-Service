from socket import *
import time
import psutil
import sys
from cryptography.fernet import Fernet

KEY = b'gZuGeUfiriA6avdQMY1zq_8BxBD5Gb0WBdWQszsWJcg='
f = Fernet(KEY)

server = ("100.125.20.105", 5000)

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(5)

client_id = sys.argv[1]


def count_primes_range(start, end):
    count = 0
    for num in range(start, end + 1):  
        if num < 2:
            continue
        prime = True
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                prime = False
                break
        if prime:
            count += 1
    return count


try:
    while True:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        netio = psutil.net_io_counters().bytes_sent

        try:
            loadAvg = psutil.getloadavg()[0]
        except:
            loadAvg = 0.0

        message = f"METRIC||{client_id}||{cpu:.2f}||{memory:.2f}||{disk:.2f}||{netio}||{loadAvg:.2f}"
        encrypted_message = f.encrypt(message.encode())

        start_time = time.time()
        clientSocket.sendto(encrypted_message, server)

        try:
            encrypted_response, _ = clientSocket.recvfrom(4096)
            decrypted_response = f.decrypt(encrypted_response)

            latency = (time.time() - start_time) * 1000

            parts = decrypted_response.decode().split("||")
            msg_type = parts[0]

            if msg_type == "TASK":
                _, task_type, ranges_data = parts

                ranges = ranges_data.split(";")

                total_result = 0

                for r in ranges:
                    start_val, end_val = map(int, r.split(","))
                    result = count_primes_range(start_val, end_val)
                    total_result += result

                    print(f"{client_id} computed {start_val}-{end_val}")

                result_msg = f"RESULT||{client_id}||{task_type}||{total_result}"
                clientSocket.sendto(f.encrypt(result_msg.encode()), server)

                print(f"Total computed result: {total_result} | Latency: {latency:.2f} ms")

                try:
                    ack, _ = clientSocket.recvfrom(2048)
                    ack = f.decrypt(ack)
                    print(ack.decode())
                except timeout:
                    print("ACK not received")

            elif msg_type == "NO_TASK":
                print("All work completed. Exiting.")
                break

        except timeout:
            print("No response from server")
            
        time.sleep(1)

except KeyboardInterrupt:
    print("Client shutting down")

finally:
    clientSocket.close()

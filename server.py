from socket import *
from time import *
import threading
from cryptography.fernet import Fernet

KEY = b'gZuGeUfiriA6avdQMY1zq_8BxBD5Gb0WBdWQszsWJcg='
f = Fernet(KEY)

serverPort = 5000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("0.0.0.0", serverPort))

print("Server running on port 5000...\n")

clients = {}        
task_queue = []     
in_progress = {}    
results = {}        

lock = threading.Lock()

TASK_TIMEOUT = 10

def generate_tasks(n, chunk_size=2000):
    tasks = []
    for start in range(2, n, chunk_size):
        end = min(start + chunk_size - 1, n)
        tasks.append((start, end))
    return tasks


task_queue = generate_tasks(200000)

def get_task_batch(node):
    with lock:
        if node not in clients:
            return []

        cpu = clients[node]["cpu"]
        memory = clients[node]["memory"]
        
        capacity = (100 - cpu) * 0.6 + (100 - memory) * 0.4\
        
        if capacity > 120:
            batch_size = 4
        elif capacity > 80:
            batch_size = 3
        elif capacity > 50:
            batch_size = 2
        else:
            batch_size = 1

        batch = []

        for _ in range(min(batch_size, len(task_queue))):
            task = task_queue.pop(0)
            in_progress[task] = {
                "node": node,
                "time": time()
            }
            batch.append(task)

        return batch

def requeue_stale_tasks():
    while True:
        sleep(2)
        now = time()

        with lock:
            stale = [
                task for task, info in in_progress.items()
                if now - info["time"] > TASK_TIMEOUT
            ]

            for task in stale:
                print(f"⚠️ Reassigning task {task}")
                task_queue.append(task)
                del in_progress[task]

def handle_message(enc_msg, addr):
    try:
        msg = f.decrypt(enc_msg).decode()
    except:
        print("❌ Decryption failed")
        return

    parts = msg.split("||")
    msg_type = parts[0]
    
    if msg_type == "METRIC":
        node = parts[1]

        try:
            cpu = float(parts[2])
            memory = float(parts[3])
            disk = parts[4]
            loadavg = parts[6]
        except:
            cpu, memory = 50, 50

        with lock:
            clients[node] = {
                "addr": addr,
                "cpu": cpu,
                "memory": memory,
                "last_seen": time()
            }

        print(f"[METRIC] {node} | CPU:{cpu}% MEM:{memory}% DISK:{disk} LOAD:{loadavg}")

        batch = get_task_batch(node)

        if batch:
            ranges_str = ";".join([f"{s},{e}" for s, e in batch])
            msg = f"TASK||prime_range||{ranges_str}"
            serverSocket.sendto(f.encrypt(msg.encode()), addr)

            print(f"[TASK] {node} assigned → {ranges_str}")

        else:
            msg = "NO_TASK"
            serverSocket.sendto(f.encrypt(msg.encode()), addr)

    elif msg_type == "RESULT":
        _, node, task_type, total = parts
        total = int(total)

        print(f"[RESULT] {node} → {total}")

        with lock:
            if node not in results:
                results[node] = 0
            results[node] += total

            done_tasks = [
                task for task, info in in_progress.items()
                if info["node"] == node
            ]
            for t in done_tasks:
                del in_progress[t]

        ack = "ACK||OK"
        serverSocket.sendto(f.encrypt(ack.encode()), addr)

def monitor_completion():
    while True:
        sleep(3)

        with lock:
            if not task_queue and not in_progress:
                print("\n🎯 ALL TASKS COMPLETED\n")

                total = sum(results.values())

                print("📊 FINAL RESULTS PER CLIENT:")
                for node, val in results.items():
                    print(f"{node} → {val}")

                print(f"\n🔥 TOTAL PRIME COUNT = {total}\n")
                return

threading.Thread(target=requeue_stale_tasks, daemon=True).start()
threading.Thread(target=monitor_completion, daemon=True).start()

try:
    while True:
        data, addr = serverSocket.recvfrom(4096)

        threading.Thread(
            target=handle_message,
            args=(data, addr),
            daemon=True
        ).start()

except KeyboardInterrupt:
    print("\n🛑 Server shutting down")

finally:
    serverSocket.close()


# System Health Monitoring (UDP)

Lightweight client–server monitoring system that sends CPU, memory, disk, load average and netIO usage from multiple machines to a central server using UDP sockets.

Dependencies: Python 3 
Libraries: socket, psutil

Install required library: ```pip install psutil```

**Files:**
server.py → monitoring server,
client.py → metric sender

## Download
clone the repo with ```git clone https://github.com/Rahulms160706/Remote-System-Health-Monitoring-Service/```

**Commands to run:**

python3 server.py\
python3 client.py <node_id>

## Architectural working of repo
![architecture_diagram](https://github.com/user-attachments/assets/02e75e76-c694-4b6a-a249-c59cc0944170)

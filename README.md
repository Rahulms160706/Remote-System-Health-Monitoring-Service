#System Health Monitoring (UDP)

Lightweight client–server monitoring system that sends CPU, memory, disk, load average and netio usage from multiple machines to a central server using UDP sockets.

Dependencies: Python 3

Install required library: ```pip install psutil```

**Files:**
server.py → monitoring server,
client.py → metric sender

##Download
clone the repo with ```git clone https://github.com/Rahulms160706/Remote-System-Health-Monitoring-Service/```

**Commands to run:**

python3 server.py\
python3 client.py <node_id>

**System Health Monitoring (UDP)**

Lightweight client–server monitoring system that sends CPU, memory, and disk usage from multiple machines to a central server using UDP sockets. Works across networks using Tailscale.

Dependencies: Python 3

Install required library: pip install psutil

**Files:**
server.py   → monitoring server,
client.py   → metric sender

**Commands to run:**

python3 server.py
python3 client.py <node_id>

**------------------------------**
Server listens on:
port: 1000
protocol: UDP
Clients send metrics every 5 seconds.

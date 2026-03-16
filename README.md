System Health Monitoring (UDP)

Lightweight client–server monitoring system that sends CPU, memory, and disk usage from multiple machines to a central server using UDP sockets. Works across networks using Tailscale.

Dependencies: Python 3

Install required library: pip install psutil

Files:
server.py   → monitoring server,
client.py   → metric sender

Running the Server:

Start the server first.

python3 server.py

Server listens on:

port: 1000
protocol: UDP
Running a Client

Run a client with a node identifier.

python3 client.py <node_id>

Example:

python3 client.py node1
python3 client.py laptop

Clients send metrics every 5 seconds.

Metrics Sent

Each client sends:

client_id||cpu||memory||disk

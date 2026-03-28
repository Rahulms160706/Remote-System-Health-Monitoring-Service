# Distributed Load-Aware Task Scheduling System

A distributed system where multiple clients compute tasks assigned dynamically by a central server using encrypted UDP communication.

---

## Structure

```
.
├── server.py
├── client.py
└── README.md
```

---

## Setup

### Install dependencies

```bash
pip install psutil cryptography
```

### Run server

```bash
python server.py
```

### Run clients

```bash
python client.py client1
python client.py client2
```

---

## How It Works

### Client

* Sends system metrics (CPU, memory, etc.)
* Receives task batch
* Computes prime count for assigned ranges
* Sends result back

### Server

* Tracks client load
* Assigns tasks dynamically
* Reassigns stale tasks (timeout: 10s)
* Aggregates final results

---

## Protocol

**Client → Server**

```
METRIC||client_id||cpu||memory||disk||network||loadavg
RESULT||client_id||task_type||result
```

**Server → Client**

```
TASK||prime_range||start,end;start,end
ACK||OK
NO_TASK
```

---

## Fault Handling

* Tasks are reassigned if not completed within the timeout

---

## Notes

* Uses UDP (no guaranteed delivery)


## Architectural working of repo
![architecture_diagram](https://github.com/user-attachments/assets/02e75e76-c694-4b6a-a249-c59cc0944170)

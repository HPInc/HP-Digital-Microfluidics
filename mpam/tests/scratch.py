from __future__ import annotations

import socket

host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)

print(f"Hostname: {host_name}.  IP: {ip}")
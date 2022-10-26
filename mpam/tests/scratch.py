from __future__ import annotations
from erk.network import local_ipv4_addrs, local_ipv4_addr

print(local_ipv4_addrs())
print(local_ipv4_addr())
print(local_ipv4_addrs(subnet="192.168"))
print(local_ipv4_addr(subnet="192.168"))
print(local_ipv4_addrs(subnet="192.168.86"))
print(local_ipv4_addr(subnet="192.168.86"))
print(local_ipv4_addrs(subnet="15"))
print(local_ipv4_addr(subnet="15"))
        
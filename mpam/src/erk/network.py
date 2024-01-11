from __future__ import annotations

import logging
from re import Pattern
import re
import socket
from typing import Sequence, Optional, Final, NoReturn

from .stringutils import conj_str


logger = logging.getLogger(__name__)

_dotted_num_re: Final[Pattern] = re.compile("(?:\\d+\\.)*\\d+")

def ip_addr_as_int(addr: str) -> int:
    def error() -> NoReturn:
        raise ValueError(f"'{addr}' not parsable as dotted bytes")
    if not _dotted_num_re.fullmatch(addr):
        error()
    def check_range(cpt: str) -> int:
        c = int(cpt)
        if c > 255:
            error()
        return c
    cpts = addr.split(".")
    if len(cpts) > 4:
        error()
    while len(cpts) < 4:
        cpts.append("0")
    ip = 0
    for c in cpts:
        ip <<= 8
        ip += check_range(c)
    return ip

def int_to_ip_addr(ip: int) -> str:
    cpts: list[str] = []
    for _ in range(4):
        cpts.append(str(ip & 0xff))
        ip >>= 8
    cpts.reverse()
    return ".".join(cpts)

def canonicalize_ip_addr(addr: str) -> str:
    return int_to_ip_addr(ip_addr_as_int(addr))

def local_ipv4_addrs(*, subnet: Optional[str] = None,
                     subnet_mask: Optional[str] = None) -> Sequence[str]:
    hostname = socket.gethostname()
    info = socket.getaddrinfo(hostname, None, socket.AddressFamily.AF_INET)
    addrs = [canonicalize_ip_addr(i[4][0]) for i in info]
    if subnet is not None:
        sn = ip_addr_as_int(subnet)
        if subnet_mask is None:
            subnet_mask = "255"+(".255"*(subnet.count(".")))
        mask = ip_addr_as_int(subnet_mask)
        addrs = [a for a in addrs if ip_addr_as_int(a) & mask == sn]
    return addrs


def local_ipv4_addr(*, 
                    addr: Optional[str] = None,
                    subnet: Optional[str] = None,
                    subnet_mask: Optional[str] = None
                    ) -> Optional[str]:
    
    addrs = local_ipv4_addrs()
    
    def possibilities() -> str:
        if len(addrs) == 0:
            return "There are no possibilities."
        if len(addrs) == 1:
            return f"The only possibility is {addrs[0]}."
        return f"Possibilities are {conj_str(addrs)}."
        
    if addr is not None:
        addr = canonicalize_ip_addr(addr)
        if addr not in addrs:
            logger.warn(f"Asserted IP address {addr} not a local IP address. {possibilities()}  Using anyway.")
        return addr
    
    if subnet is not None:
        matching = local_ipv4_addrs(subnet=subnet, subnet_mask=subnet_mask)
        subnet = canonicalize_ip_addr(subnet)
        if len(matching) == 0:
            msg = f"No local IP addresses on subnet {subnet}. {possibilities()}  Using "
            if len(addrs) == 1:
                msg += "it."
            else:
                msg += "the first one."
            logger.warn(msg)
            return addrs[0]
        if len(matching) > 1:
            msg = f"Multiple local IP addresses on subnet {subnet}: {conj_str(matching)}.  Using the first one."
            logger.warn(msg)
            return matching[0]
    
    if len(addrs) == 0:
        logger.warn(f"There are no known local IP addresses.")
        return None
    if len(addrs) > 1:
        logger.warn(f"Multiple local IP addresses: {conj_str(addrs)}.  Using the first one.")
    return addrs[0]
    
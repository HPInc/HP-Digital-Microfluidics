from __future__ import annotations

x = 0

bs = bytearray(3)

def set_bit(b: int, val: bool) -> int:
    global bs
    bit = 1 << b
    if val:
        bs[2] |= bit
    else:
        bs[2] &= ~bit
    return bs[2]


print(set_bit(1, True))
print(set_bit(3, False))
print(set_bit(3, True))
print(set_bit(1, False))
print(bs)
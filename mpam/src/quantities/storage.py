from __future__ import annotations

from quantities.core import BaseDim, Prefix, DerivedDim, Unit, Quantity
from quantities import prefixes, dimensions, SI
from typing import TypeVar, Final


class Storage(BaseDim): ...
class DataRate (DerivedDim):
    derived = Storage/dimensions.Time

bkilo = Prefix("K", 1024**1)
bmega = Prefix("M", 1024**2)
bgiga = Prefix("G", 1024**3)
btera = Prefix("T", 1024**4)
bpeta = Prefix("P", 1024**5)
bexa  = Prefix("E", 1024**6)
bzetta = Prefix("Z", 1024**7)
byotta = Prefix("Y", 1024**8)


kibi = Prefix("Ki", 1024**1)
mebi = Prefix("Mi", 1024**2)
gibi = Prefix("Gi", 1024**3)
tebi = Prefix("Ti", 1024**4)
pebi = Prefix("Pi", 1024**5)
exbi  = Prefix("Ei", 1024**6)
zebi  = Prefix("Zi", 1024**7)
yobi  = Prefix("Yi", 1024**8)

dec_kilo = prefixes.kilo
dec_mega = prefixes.mega
dec_giga = prefixes.giga
dec_tera = prefixes.tera
dec_peta = prefixes.peta
dec_exa = prefixes.exa
dec_zetta = prefixes.zetta
dec_yotta = prefixes.yotta

_bin_prefixes = (bkilo, bmega, bgiga, btera, bpeta, bexa, bzetta, byotta)
_bibi_prefixes = (kibi, mebi, gibi, tebi, pebi, exbi, zebi, yobi)
_dec_prefixes = (prefixes.kilo, prefixes.mega, prefixes.giga, prefixes.tera,
                 prefixes.peta, prefixes.exa, prefixes.zetta, prefixes.yotta)

_force_import: Quantity

_D = TypeVar('_D', bound='Quantity')
def _prefixed(unit: Unit[_D], n: int) -> tuple[Unit[_D], Unit[_D], Unit[_D]]:
    return (_bin_prefixes[n-1](unit),
            _bibi_prefixes[n-1](unit),
            _dec_prefixes[n-1](unit))

b = bit = bits = Storage.base_unit("bits", singular="bit")


kilobit = kilobits = Kb = bkilo(bits)
megabit = megabits = Mb = bmega(bits)
gigabit = gigabits = Gb = bgiga(bits)

kibibit = kibibits = Kib = kibi(bits)
mebibit = mebibits = Mib = mebi(bits)
gibibit = gibibits = Gib = gibi(bits)

dec_kilobit = dec_kilobits = dec_Kb = dec_kilo(bits)
dec_megabit = dec_megabits = dec_Mb = dec_mega(bits)
dec_gigabit = dec_gigabits = dec_Gb = dec_tera(bits)

# Note, "bytes" is a reserved word in Python
B = byte = n_bytes = (8*bits).as_unit("bytes", singular="byte")


kilobyte = kilobytes = KB = bkilo(n_bytes)
megabyte = megabytes = MB = bmega(n_bytes)
gigabyte = gigabytes = GB = bgiga(n_bytes)
terabyte = terabytes = TB = btera(n_bytes)
petabyte = petabytes = PB = bpeta(n_bytes)

kibibyte = kibibytes = KiB = kibi(n_bytes)
mebibyte = mebibytes = MiB = mebi(n_bytes)
gibibyte = gibibytes = GiB = gibi(n_bytes)
tebibyte = tebibytes = TiB = tebi(n_bytes)
pebibyte = pebibytes = PiB = pebi(n_bytes)

dec_kilobyte = dec_kilobytes = dec_KB = dec_kilo(n_bytes) 
dec_megabyte = dec_megabytes = dec_MB = dec_mega(n_bytes)
dec_gigabyte = dec_gigabytes = dec_GB = dec_giga(n_bytes)
dec_terabyte = dec_terabytes = dec_TB = dec_tera(n_bytes)
dec_petabyte = dec_petabytes = dec_PB = dec_peta(n_bytes)

bps = bit_per_sec = bits_per_sec = (bit/SI.second).a(DataRate ).as_unit("bps")

kilobit_per_sec = kilobits_per_sec = Kbps = bkilo(bps)
megabit_per_sec = megabits_per_sec = Mbps = bmega(bps)
gigabit_per_sec = gigabits_per_sec = Gbps = bgiga(bps)

kibibit_per_sec = kibibits_per_sec = Kibps = kibi(bps)
mebibit_per_sec = mebibits_per_sec = Mibps = mebi(bps)
gibibit_per_sec = gibibits_per_sec = Gibps = gibi(bps)

Bps = byte_per_sec = bytes_per_sec = (n_bytes/SI.second).a(DataRate ).as_unit("Bps")


kilobyte_per_sec = kilobytes_per_sec = KBps = bkilo(Bps)
megabyte_per_sec = megabytes_per_sec = MBps = bmega(Bps)
gigabyte_per_sec = gigabytes_per_sec = GBps = bgiga(Bps)

kibibyte_per_sec = kibibytes_per_sec = KiBps = kibi(Bps)
mebibyte_per_sec = mebibytes_per_sec = MiBps = mebi(Bps)
gibibyte_per_sec = gibibytes_per_sec = GiBps = gibi(Bps)

class WordSize:
    bits_per_word: Final[int]
    
    def __init__(self, bits_per_word: int) -> None:
        self.bits_per_word = bits_per_word
        self.word = self.words = (bits_per_word*bits).as_unit("words", singular="word")
        self.dword = self.dwords = (2*self.word).as_unit("dwords", singular="dword")
        self.hword = self.hwords = (0.5*self.word).as_unit("hwords", singular="hword")
        
arch_16 = WordSize(16)
arch_32 = WordSize(32)
arch_64 = WordSize(64)
arch_128 = WordSize(128)


        
    


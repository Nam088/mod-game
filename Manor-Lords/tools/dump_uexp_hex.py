import os
import struct

uexp_path = r"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\HoodedHorse\DT_Translation_BuildingNames.uexp"

with open(uexp_path, "rb") as f:
    data = f.read()

# Let's inspect from offset 0 to 500 in hex and ascii
for chunk_start in range(0, min(len(data), 1500), 64):
    chunk = data[chunk_start:chunk_start+64]
    hex_str = " ".join(f"{b:02x}" for b in chunk)
    asc_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
    print(f"{chunk_start:04x}: {hex_str:192s} | {asc_str}")

import os
import struct

uexp_path = r"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\HoodedHorse\DT_Translation_Items.uexp"

with open(uexp_path, "rb") as f:
    data = f.read()

# Search for "Wheat Grain"
pos = data.find(b"Wheat Grain")
print(f"'Wheat Grain' found at offset: {pos}")
if pos != -1:
    # Print 64 bytes before Wheat Grain
    start = max(0, pos - 48)
    chunk = data[start:pos+32]
    hex_str = " ".join(f"{b:02x}" for b in chunk)
    asc_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
    print(f"Header before Wheat Grain: {hex_str} | {asc_str}")
    
# Let's find all items in Items.uexp
# Look at the pattern before English strings

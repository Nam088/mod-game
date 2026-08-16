import os
import struct
import json

uexp_path = r"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\HoodedHorse\DT_Translation_BuildingNames.uexp"

with open(uexp_path, "rb") as f:
    data = f.read()

print(f"File size: {len(data)}")

# Let's search for FString entries: Length (int32) followed by UTF-8 or UTF-16
pos = 0
strings = []
while pos < len(data) - 4:
    length, = struct.unpack("<i", data[pos:pos+4])
    if 1 < length < 500 and pos + 4 + length <= len(data):
        # check if it's null-terminated ascii/utf8
        s_bytes = data[pos+4:pos+4+length]
        if s_bytes[-1] == 0:
            try:
                s = s_bytes[:-1].decode("utf-8")
                if all(32 <= ord(c) < 127 or ord(c) >= 160 or c in '\r\n\t' for c in s) and len(s) >= 2:
                    strings.append((pos, length, s))
            except:
                pass
    pos += 1

print(f"Found {len(strings)} possible strings in uexp:")
for p, l, s in strings[:30]:
    print(f"  [{p:5d}] {s}")

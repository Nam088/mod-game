import os
import struct

uexp_path = r"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\DT_Translation.uexp"

with open(uexp_path, "rb") as f:
    data = f.read()

print(f"DT_Translation uexp size: {len(data)}")

pos = 0
strings = []
while pos < len(data) - 4:
    length, = struct.unpack("<i", data[pos:pos+4])
    if 1 < length < 500 and pos + 4 + length <= len(data):
        s_bytes = data[pos+4:pos+4+length]
        if s_bytes[-1] == 0:
            try:
                s = s_bytes[:-1].decode("utf-8")
                if len(s) >= 2:
                    strings.append((pos, length, s))
            except:
                pass
    pos += 1

print(f"Found {len(strings)} strings:")
for p, l, s in strings[:40]:
    print(f"  [{p:5d}] {s}")

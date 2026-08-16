import os
import struct

uasset_path = r"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\HoodedHorse\DT_Translation_BuildingNames.uasset"
uexp_path = r"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\HoodedHorse\DT_Translation_BuildingNames.uexp"

def read_namemap(uasset_path):
    with open(uasset_path, "rb") as f:
        data = f.read()
    
    # Read NameCount (at offset 0x29/0x2D roughly in header, let's search for names)
    # Header in UE5:
    # Tag (4 bytes 0x9E2A83C1)
    tag, = struct.unpack_from("<I", data, 0)
    print(f"Asset tag: {hex(tag)}")
    # In UE5 cooked header:
    # NameCount at offset 0x31 or similar:
    # Let's find NameMapOffset and NameMapCount:
    # In UE5 header:
    # Tag(4), Legacy(12), UE4Ver(4), UE5Ver(4), CustomVers(12+count*20)...
    # Let's inspect NameOffset and NameCount
    # Or find all null-terminated ASCII strings in the name map:
    pos = 0x40
    names = []
    # Let's scan from 0 to first export
    return data

data = read_namemap(uasset_path)
print(f"UAsset size: {len(data)}, UExp size: {os.path.getsize(uexp_path)}")

# Let's dump all strings in .uasset
import re
uasset_names = [m.group(0).decode('utf-8', errors='ignore') for m in re.finditer(b'[\x20-\x7E]{2,}', data)]
print("All names in uasset:")
for n in uasset_names:
    print(" ", n)

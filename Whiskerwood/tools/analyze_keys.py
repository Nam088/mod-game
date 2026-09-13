import struct
import json
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open(r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uasset", "rb") as f:
    uasset = f.read()
with open(r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uexp", "rb") as f:
    uexp = f.read()

name_count, name_offset = struct.unpack_from("<ii", uasset, 85)
names = []
pos = name_offset
for i in range(name_count):
    s_len, = struct.unpack_from("<i", uasset, pos)
    pos += 4
    if s_len > 0:
        s = uasset[pos:pos+s_len-1].decode("utf-8", errors="replace")
        pos += s_len
    elif s_len < 0:
        s_len = -s_len
        s = uasset[pos:pos+s_len*2-2].decode("utf-16le", errors="replace")
        pos += s_len * 2
    else:
        s = ""
    non_case_hash, case_hash = struct.unpack_from("<HH", uasset, pos)
    pos += 4
    names.append(s)

row_count, = struct.unpack_from("<i", uexp, 10)

entries = []
pos = 14
for r in range(row_count):
    name_idx, name_inst = struct.unpack_from("<ii", uexp, pos)
    pos += 8
    key_name = names[name_idx] if 0 <= name_idx < len(names) else f"Unknown_{name_idx}"
    flags = uexp[pos:pos+2]
    pos += 2
    text_len_offset = pos
    s_len, = struct.unpack_from("<i", uexp, pos)
    pos += 4
    if s_len > 0:
        text = uexp[pos:pos+s_len-1].decode("utf-8", errors="replace")
        pos += s_len
    elif s_len < 0:
        s_len = -s_len
        text = uexp[pos:pos+s_len*2-2].decode("utf-16le", errors="replace")
        pos += s_len * 2
    else:
        text = ""
    
    prefix = key_name.split('.')[0] if '.' in key_name else "other"
    entries.append({
        "row_idx": r,
        "key": key_name,
        "prefix": prefix,
        "en": text,
        "offset": text_len_offset,
        "length": s_len
    })

prefix_counts = Counter(e['prefix'] for e in entries)
print("Key Prefix Distribution:")
for prefix, count in prefix_counts.most_common(30):
    print(f"  {prefix:<25}: {count:4d} entries")

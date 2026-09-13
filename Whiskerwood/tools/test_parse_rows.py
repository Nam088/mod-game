import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uasset", "rb") as f:
    uasset = f.read()

with open(r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uexp", "rb") as f:
    uexp = f.read()

name_count = 2762
name_offset = 265
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

pos = 10
row_count, = struct.unpack_from("<i", uexp, pos)
pos += 4
print(f"Total Rows: {row_count}")

parsed_rows = []
for r in range(row_count):
    row_start = pos
    if pos + 8 > len(uexp):
        print(f"Buffer underflow at row {r}, pos={pos}")
        break
    name_idx, name_inst = struct.unpack_from("<ii", uexp, pos)
    pos += 8
    key_name = names[name_idx] if 0 <= name_idx < len(names) else f"Unknown_{name_idx}"
    
    # 2 bytes flag (0x00, 0x03 or FText flags)
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
        
    parsed_rows.append({
        "row_idx": r,
        "key": key_name,
        "name_idx": name_idx,
        "flags": flags.hex(),
        "offset": text_len_offset,
        "text": text
    })

print(f"Successfully parsed {len(parsed_rows)} / {row_count} rows!")
print(f"Final pos: {pos}, uexp total len: {len(uexp)}, remaining bytes: {len(uexp) - pos}")

# Inspect some samples across the rows
for idx in [0, 10, 50, 100, 500, 1000, 1500, 2000, 2500, 2750]:
    if idx < len(parsed_rows):
        r = parsed_rows[idx]
        print(f"Row {r['row_idx']:4d} | Key: {r['key']:<35} | Text: {r['text'][:50]}")

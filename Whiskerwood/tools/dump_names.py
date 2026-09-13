import struct

with open(r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uasset", "rb") as f:
    data = f.read()

name_count = 2762
name_offset = 265

names = []
pos = name_offset
for i in range(name_count):
    s_len, = struct.unpack_from("<i", data, pos)
    pos += 4
    if s_len > 0:
        s = data[pos:pos+s_len-1].decode("utf-8", errors="replace")
        pos += s_len
    elif s_len < 0:
        s_len = -s_len
        s = data[pos:pos+s_len*2-2].decode("utf-16le", errors="replace")
        pos += s_len * 2
    else:
        s = ""
    # UE NameMap hash
    non_case_hash, case_hash = struct.unpack_from("<HH", data, pos)
    pos += 4
    names.append(s)

print(f"Successfully read {len(names)} names!")
print("First 20 names:", names[:20])
print("Sample names 100-120:", names[100:120])
print("End pos of names:", pos)

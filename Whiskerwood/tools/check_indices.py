import struct

with open(r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uasset", "rb") as f:
    uasset = f.read()

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

print("Name[2353]:", names[2353])
print("Name[2367]:", names[2367])
print("Name[2343]:", names[2343])
print("Name[2362]:", names[2362])
print("Name[2359]:", names[2359])

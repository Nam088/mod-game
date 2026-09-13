import struct

with open(r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uasset", "rb") as f:
    data = f.read()

# Let's inspect where the Name table is.
# Look at offset 81:
# after "/Game/Data/TextDB/Loc_En\0" (52 + 4 + 25 = 81):
# let's look at bytes from offset 80 to 200:
pos = 52 + 4 + 25 # 81
print("Pos after package name:", pos)

for i in range(pos, pos + 100, 4):
    val, = struct.unpack_from("<i", data, i)
    uval, = struct.unpack_from("<I", data, i)
    print(f"Offset {i:04x} ({i}): int={val}, uint={uval} (hex: {hex(uval)})")


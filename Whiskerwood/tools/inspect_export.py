import struct

with open(r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uasset", "rb") as f:
    uasset = f.read()

# Export count is at offset 109: 1
# Export offset is at offset 113: 83232 (0x14520)
# Let's inspect bytes from 83232:
exp_offset = 83232
print(f"Export data at {exp_offset} (length: {len(uasset) - exp_offset}):")
for i in range(exp_offset, len(uasset), 16):
    chunk = uasset[i:i+16]
    hex_str = " ".join(f"{b:02x}" for b in chunk)
    ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
    print(f"{i:04x}:  {hex_str:<48}  {ascii_str}")

# In UE4/UE5 FObjectExport:
# ClassIndex (4), SuperIndex (4), TemplateIndex (4), OuterIndex (4)
# ObjectName (FName: 8 bytes = 4 index + 4 number)
# Save (4), SerialSize (8), SerialOffset (8)
# Let's check unpack from exp_offset:
class_idx, super_idx, template_idx, outer_idx = struct.unpack_from("<iiii", uasset, exp_offset)
obj_name_idx, obj_name_num = struct.unpack_from("<ii", uasset, exp_offset + 16)
save, = struct.unpack_from("<i", uasset, exp_offset + 24)
serial_size, serial_offset = struct.unpack_from("<qq", uasset, exp_offset + 28)

print(f"Class: {class_idx}, ObjectNameIdx: {obj_name_idx}")
print(f"SerialSize (int64): {serial_size} (uexp size is 137423)")
print(f"SerialOffset (int64): {serial_offset} (uasset size is 83348)")

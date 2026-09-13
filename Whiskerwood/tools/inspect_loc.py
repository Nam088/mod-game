import struct
import os

uasset_path = r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uasset"
uexp_path = r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uexp"

with open(uasset_path, "rb") as f:
    uasset = f.read()

with open(uexp_path, "rb") as f:
    uexp = f.read()

print("uasset size:", len(uasset))
print("uexp size:", len(uexp))

tag, leg_fv, leg_ue3, fv_ue4, fv_ue5 = struct.unpack_from("<iiiii", uasset, 0)
print(f"Tag: {hex(tag & 0xFFFFFFFF)}, LegacyFV: {leg_fv}, LegacyUE3: {leg_ue3}, UE4Ver: {fv_ue4}, UE5Ver: {fv_ue5}")

pos = 20
custom_ver_count, = struct.unpack_from("<i", uasset, pos)
pos += 4 + custom_ver_count * 20
total_hdr_size, = struct.unpack_from("<i", uasset, pos)
pos += 4
fn_len, = struct.unpack_from("<i", uasset, pos)
pos += 4
if fn_len > 0:
    folder_name = uasset[pos:pos+fn_len-1].decode('utf-8', errors='replace')
    pos += fn_len
elif fn_len < 0:
    fn_len = -fn_len
    folder_name = uasset[pos:pos+fn_len*2-2].decode('utf-16le', errors='replace')
    pos += fn_len * 2
else:
    folder_name = ""

pkg_flags, = struct.unpack_from("<I", uasset, pos)
pos += 4

name_count, name_offset = struct.unpack_from("<ii", uasset, pos)
pos += 8

print(f"FolderName: '{folder_name}', PkgFlags: {hex(pkg_flags)}, NameCount: {name_count}, NameOffset: {name_offset}")

names = []
n_pos = name_offset
for i in range(name_count):
    s_len, = struct.unpack_from("<i", uasset, n_pos)
    n_pos += 4
    if s_len > 0:
        s = uasset[n_pos:n_pos+s_len-1].decode("utf-8", errors="replace")
        n_pos += s_len
    elif s_len < 0:
        s_len = -s_len
        s = uasset[n_pos:n_pos+s_len*2-2].decode("utf-16le", errors="replace")
        n_pos += s_len * 2
    else:
        s = ""
    non_case_hash, case_hash = struct.unpack_from("<HH", uasset, n_pos)
    n_pos += 4
    names.append(s)

print(f"Parsed {len(names)} names.")
print("First 30 names:", names[:30])
print("Last 30 names:", names[-30:])

# Let's inspect the exports and imports in the header
# UE4/UE5 header table locations:
# NameCount (4), NameOffset (4)
# SoftObjectPathsCount (4), SoftObjectPathsOffset (4)
# GatherableTextDataCount (4), GatherableTextDataOffset (4)
# ExportCount (4), ExportOffset (4)
# ImportCount (4), ImportOffset (4)
# DependsOffset (4)
# SoftPackageReferencesCount (4), SoftPackageReferencesOffset (4)
# SearchableNamesOffset (4)
# ThumbnailTableOffset (4)
# Guid (16)
# GenerationCount (4) ...

soft_paths_count, soft_paths_offset = struct.unpack_from("<ii", uasset, pos)
pos += 8
gatherable_text_count, gatherable_text_offset = struct.unpack_from("<ii", uasset, pos)
pos += 8
export_count, export_offset = struct.unpack_from("<ii", uasset, pos)
pos += 8
import_count, import_offset = struct.unpack_from("<ii", uasset, pos)
pos += 8

print(f"Exports: count={export_count}, offset={export_offset}")
print(f"Imports: count={import_count}, offset={import_offset}")

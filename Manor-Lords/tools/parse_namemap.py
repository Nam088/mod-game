import os
import struct
import json

def parse_uasset_names(uasset_path):
    with open(uasset_path, "rb") as f:
        data = f.read()
    
    # In UE4/UE5 Header:
    # Tag (4 bytes 0x9E2A83C1)
    # LegacyFileVersion (4), LegacyUE3Version (4), FileVersionUE4 (4), FileVersionUE5 (4)
    # TotalHeaderSize (4), FolderName (FString), PackageFlags (4)
    # NameCount (4), NameOffset (4)
    # Let's inspect where NameCount and NameOffset are located
    # Let's locate the FNames by reading the header:
    tag, leg_fv, leg_ue3, fv_ue4, fv_ue5 = struct.unpack_from("<iiiii", data, 0)
    pos = 20
    # Custom versions
    custom_ver_count, = struct.unpack_from("<i", data, pos)
    pos += 4 + custom_ver_count * 20
    
    # TotalHeaderSize (4)
    total_hdr_size, = struct.unpack_from("<i", data, pos)
    pos += 4
    
    # FolderName (FString)
    fn_len, = struct.unpack_from("<i", data, pos)
    pos += 4
    if fn_len > 0:
        pos += fn_len
    elif fn_len < 0:
        pos += (-fn_len) * 2
        
    # PackageFlags (4)
    pkg_flags, = struct.unpack_from("<I", data, pos)
    pos += 4
    
    # NameCount (4), NameOffset (4)
    name_count, name_offset = struct.unpack_from("<ii", data, pos)
    print(f"[{os.path.basename(uasset_path)}] NameCount: {name_count}, NameOffset: {name_offset}")
    
    # Parse Names
    names = []
    n_pos = name_offset
    for i in range(name_count):
        s_len, = struct.unpack_from("<i", data, n_pos)
        n_pos += 4
        if s_len > 0:
            s = data[n_pos:n_pos+s_len-1].decode("utf-8", errors="replace")
            n_pos += s_len
        elif s_len < 0:
            s_len = -s_len
            s = data[n_pos:n_pos+s_len*2-2].decode("utf-16le", errors="replace")
            n_pos += s_len * 2
        else:
            s = ""
        # Non-case preserving hash (2 bytes) + case preserving hash (2 bytes) = 4 bytes
        non_case_hash, case_hash = struct.unpack_from("<HH", data, n_pos)
        n_pos += 4
        names.append(s)
        
    return names

names_menu = parse_uasset_names(r"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\HoodedHorse\DT_Translation_Menus.uasset")
print("First 30 names in Menus:", names_menu[:30])

names_items = parse_uasset_names(r"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\HoodedHorse\DT_Translation_Items.uasset")
print("First 30 names in Items:", names_items[:30])

names_mainui = parse_uasset_names(r"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\HoodedHorse\DT_Translation_MainUI.uasset")
print("First 30 names in MainUI:", names_mainui[:30])

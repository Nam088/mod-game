import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')

def parse_uasset_header(data):
    tag, leg_fv, leg_ue3, fv_ue4, fv_ue5 = struct.unpack_from("<iiiii", data, 0)
    pos = 44
    total_hdr_size, = struct.unpack_from("<i", data, pos)
    pos = 52
    fn_len, = struct.unpack_from("<i", data, pos)
    pos += 4
    if fn_len > 0:
        folder_name = data[pos:pos+fn_len-1].decode('utf-8', errors='replace')
        pos += fn_len
    elif fn_len < 0:
        fn_len = -fn_len
        folder_name = data[pos:pos+fn_len*2-2].decode('utf-16le', errors='replace')
        pos += fn_len * 2
    else:
        folder_name = ""
        
    pkg_flags, = struct.unpack_from("<I", data, pos)
    pos += 4
    name_count, name_offset = struct.unpack_from("<ii", data, pos)
    pos += 8
    
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
        non_case_hash, case_hash = struct.unpack_from("<HH", data, n_pos)
        n_pos += 4
        names.append(s)
        
    return {
        "folder_name": folder_name,
        "pkg_flags": hex(pkg_flags),
        "total_hdr_size": total_hdr_size,
        "name_count": name_count,
        "names": names
    }

with open(r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_Root.uasset", "rb") as f:
    uasset = f.read()

hdr = parse_uasset_header(uasset)
print(f"Folder: {hdr['folder_name']}, Names ({hdr['name_count']}): {hdr['names']}")

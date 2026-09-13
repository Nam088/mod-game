import struct
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def patch_loc_en(trans_entries, orig_uasset_path, orig_uexp_path, out_uasset_path, out_uexp_path):
    with open(orig_uasset_path, "rb") as f:
        uasset_bytes = bytearray(f.read())
    with open(orig_uexp_path, "rb") as f:
        orig_uexp = f.read()

    # Create mapping from ID or Key to Target Text
    trans_map = {}
    for entry in trans_entries:
        key = entry.get("key")
        vi = entry.get("target_vi", "").strip()
        en = entry.get("source_en", "")
        # If target_vi is provided, use it; otherwise fallback to en
        chosen_text = vi if vi else en
        trans_map[key] = chosen_text

    # Parse names to match row indices
    name_count, name_offset = struct.unpack_from("<ii", uasset_bytes, 85)
    names = []
    pos = name_offset
    for i in range(name_count):
        s_len, = struct.unpack_from("<i", uasset_bytes, pos)
        pos += 4
        if s_len > 0:
            s = uasset_bytes[pos:pos+s_len-1].decode("utf-8", errors="replace")
            pos += s_len
        elif s_len < 0:
            s_len = -s_len
            s = uasset_bytes[pos:pos+s_len*2-2].decode("utf-16le", errors="replace")
            pos += s_len * 2
        else:
            s = ""
        non_case_hash, case_hash = struct.unpack_from("<HH", uasset_bytes, pos)
        pos += 4
        names.append(s)

    row_count, = struct.unpack_from("<i", orig_uexp, 10)
    
    # Build new uexp
    new_uexp = bytearray()
    new_uexp.extend(orig_uexp[:14]) # Copy header + row count
    
    read_pos = 14
    for r in range(row_count):
        name_idx, name_inst = struct.unpack_from("<ii", orig_uexp, read_pos)
        read_pos += 8
        flags = orig_uexp[read_pos:read_pos+2]
        read_pos += 2
        
        orig_s_len, = struct.unpack_from("<i", orig_uexp, read_pos)
        read_pos += 4
        if orig_s_len > 0:
            read_pos += orig_s_len
        elif orig_s_len < 0:
            read_pos += (-orig_s_len) * 2
            
        key_name = names[name_idx] if 0 <= name_idx < len(names) else f"Unknown_{name_idx}"
        target_text = trans_map.get(key_name, "")
        
        # Write row to new_uexp
        new_uexp.extend(struct.pack("<ii", name_idx, name_inst))
        new_uexp.extend(flags)
        
        if not target_text:
            # Empty string in Unreal Engine FString is 4 bytes of 0 (Length = 0)
            new_uexp.extend(struct.pack("<i", 0))
        else:
            # Check if text contains non-ASCII (Unicode / Vietnamese)
            is_unicode = any(ord(c) > 127 for c in target_text)
            if is_unicode:
                char_count = len(target_text) + 1
                new_len = -char_count
                encoded = target_text.encode("utf-16le") + b"\x00\x00"
                new_uexp.extend(struct.pack("<i", new_len))
                new_uexp.extend(encoded)
            else:
                char_count = len(target_text) + 1
                new_len = char_count
                encoded = target_text.encode("utf-8") + b"\x00"
                new_uexp.extend(struct.pack("<i", new_len))
                new_uexp.extend(encoded)
            
    # Append footer magic (0x9E2A83C1)
    new_uexp.extend(struct.pack("<I", 0x9E2A83C1))
    
    # Update SerialSize in uasset
    new_serial_size = len(new_uexp) - 4
    struct.pack_into("<q", uasset_bytes, 83260, new_serial_size)
    
    os.makedirs(os.path.dirname(out_uasset_path), exist_ok=True)
    os.makedirs(os.path.dirname(out_uexp_path), exist_ok=True)
    
    with open(out_uasset_path, "wb") as f:
        f.write(uasset_bytes)
    with open(out_uexp_path, "wb") as f:
        f.write(new_uexp)
        
    print(f"[SUCCESS] Patched Loc_En! New uexp size: {len(new_uexp)} bytes (orig: {len(orig_uexp)})")
    return len(new_uexp)

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    orig_uasset = os.path.join(project_root, "extracted", "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uasset")
    orig_uexp = os.path.join(project_root, "extracted", "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uexp")
    master_json = os.path.join(project_root, "translations", "Whiskerwood_Loc_En_Master.json")
    
    with open(master_json, "r", encoding="utf-8") as f:
        entries = json.load(f)
        
    out_uasset = os.path.join(project_root, "build", "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uasset")
    out_uexp = os.path.join(project_root, "build", "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uexp")
    
    patch_loc_en(entries, orig_uasset, orig_uexp, out_uasset, out_uexp)

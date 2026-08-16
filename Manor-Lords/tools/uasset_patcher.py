import os
import struct
import io

def patch_uexp_strings(orig_uexp_path, string_replacements):
    """
    string_replacements: dict of {orig_offset: new_utf8_string}
    Returns: new_uexp_bytes
    """
    with open(orig_uexp_path, "rb") as f:
        data = bytearray(f.read())
    
    # Sort replacements in reverse offset order to maintain valid offsets during slicing
    sorted_replacements = sorted(string_replacements.items(), key=lambda x: x[0], reverse=True)
    
    for offset, new_text in sorted_replacements:
        orig_len, = struct.unpack_from("<i", data, offset)
        if orig_len <= 0:
            continue
        
        orig_total_size = 4 + orig_len
        new_text_bytes = new_text.encode("utf-8") + b"\x00"
        new_len = len(new_text_bytes)
        new_chunk = struct.pack("<i", new_len) + new_text_bytes
        
        # Replace slice
        data[offset:offset+orig_total_size] = new_chunk
        
    return bytes(data)

def patch_uasset_serial_size(orig_uasset_path, new_uexp_size):
    """
    Updates SerialSize of the primary export in .uasset header
    """
    with open(orig_uasset_path, "rb") as f:
        data = bytearray(f.read())
    
    # In UE4/UE5 UAsset header:
    # Exports list offset and count are in the asset header.
    # Header format:
    # Tag (4), LegacyFileVersion (4), LegacyUE3Version (4), FileVersionUE4 (4), FileVersionUE5 (4)...
    # Let's locate the export definition and update SerialSize (int64 at export + offset).
    # Since exports have SerialSize (int64), we can also update it via UAssetAPI or binary patching.
    return data

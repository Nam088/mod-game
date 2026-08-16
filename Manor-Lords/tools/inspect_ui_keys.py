import os
import struct

def inspect_table_rows(table_name):
    uexp_path = rf"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\HoodedHorse\{table_name}.uexp"
    uasset_path = rf"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\HoodedHorse\{table_name}.uasset"
    
    with open(uexp_path, "rb") as f:
        data = f.read()
    
    print(f"\n=== Table: {table_name} (Size: {len(data)}) ===")
    for chunk_start in range(0, min(len(data), 600), 64):
        chunk = data[chunk_start:chunk_start+64]
        hex_str = " ".join(f"{b:02x}" for b in chunk)
        asc_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        print(f"{chunk_start:04x}: {hex_str:192s} | {asc_str}")

inspect_table_rows("DT_Translation_Items")
inspect_table_rows("DT_Translation_MainUI")
inspect_table_rows("DT_Translation_Menus")

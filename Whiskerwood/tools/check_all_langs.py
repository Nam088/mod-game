import struct
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

textdb_dir = r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB"

for file in sorted(os.listdir(textdb_dir)):
    if file.endswith(".uasset") and not file.startswith("Loc_Dev") and not file.startswith("Loc_Root"):
        base = file[:-7]
        uasset_path = os.path.join(textdb_dir, f"{base}.uasset")
        uexp_path = os.path.join(textdb_dir, f"{base}.uexp")
        
        with open(uasset_path, "rb") as f:
            uasset = f.read()
        with open(uexp_path, "rb") as f:
            uexp = f.read()
            
        # Parse names
        # Offset of NameOffset is at 89
        name_count, name_offset = struct.unpack_from("<ii", uasset, 85)
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
            
        row_count, = struct.unpack_from("<i", uexp, 10)
        
        # Test parse uexp
        pos = 14
        parsed = 0
        unicode_count = 0
        for r in range(row_count):
            if pos + 10 > len(uexp):
                break
            name_idx, name_inst = struct.unpack_from("<ii", uexp, pos)
            pos += 8
            flags = uexp[pos:pos+2]
            pos += 2
            s_len, = struct.unpack_from("<i", uexp, pos)
            pos += 4
            if s_len > 0:
                text = uexp[pos:pos+s_len-1].decode("utf-8", errors="replace")
                pos += s_len
            elif s_len < 0:
                s_len = -s_len
                text = uexp[pos:pos+s_len*2-2].decode("utf-16le", errors="replace")
                pos += s_len * 2
                unicode_count += 1
            else:
                text = ""
            parsed += 1
            
        rem = len(uexp) - pos
        print(f"[{base:<10}] Names: {len(names):4d}, Rows: {row_count:4d}, Parsed: {parsed:4d}, Unicode: {unicode_count:4d}, Remaining: {rem} bytes")
